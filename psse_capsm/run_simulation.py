"""Run PSS/E v35 quasi-static simulations from an immutable .raw benchmark.

Requires licensed PSS/E Python (psspy). No PyTorch inside PSS/E. The JSONL
trajectory can be consumed later by the PyTorch policy/training process.

Examples (from repository root):
  python -m psse_capsm.run_simulation --case C:\cases\IEEE39.raw --profiles profiles.csv --policy none --output runs/no_control
  python -m psse_capsm.run_simulation --case C:\cases\IEEE39.raw --profiles profiles.csv --policy droop --output runs/droop
  python -m psse_capsm.run_simulation --case C:\cases\IEEE39.raw --profiles profiles.csv --policy qirl_exact --output runs/qirl
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import random
import tempfile
import time
from pathlib import Path
from .case import RawCase
from .controls import ACTION_NAMES, LO, HI, EV_BUSES, EVFleet, apply_action, clamp_action
from .psse_adapter import Psse35

def read_profiles(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("timestamp"):
                raise ValueError("timestamp required")
            record = {k: row.get(k, "") for k in ("timestamp", "load_scale", "wind_mw", "solar_mw")}
            for key in ("load_scale", "wind_mw", "solar_mw"):
                record[key] = float(record[key] or (1.0 if key == "load_scale" else 0.0))
                if not math.isfinite(record[key]):
                    raise ValueError("nonfinite profile value")
            if record["load_scale"] < 0 or record["wind_mw"] < 0 or record["solar_mw"] < 0:
                raise ValueError("negative load scaling or renewable generation")
            yield record

def profile_case(base, row):
    case = base.clone()
    case.set_load_scale(row["load_scale"])
    # Measured OPSD temporal shapes are translated to synthetic IEEE test-system
    # injections. They are NOT measured nodal generation or measured PMU faults.
    for bus in (4, 14):
        case.add_load(bus, "WN", -row["wind_mw"] / 2)
    for bus in (8, 15):
        case.add_load(bus, "SO", -row["solar_mw"] / 2)
    return case

def reward(result, action, actual_ev=None, requested_ev=None, loss_ref_mw=50.0):
    """Shared candidate-dependent reward with no artificial performance targets."""
    if not result.get("converged"):
        return -1e6
    loss_ref_mw = max(float(loss_ref_mw), 1.0)
    a = clamp_action(action)
    active = [i for i in range(9) if i != 5]
    effort = sum(((a[i] / max(HI[i] - LO[i], 1e-6)) ** 2) for i in active) / len(active)
    infeasible = 0.0
    if actual_ev is not None and requested_ev is not None:
        infeasible = sum(abs(p-q) for p,q in zip(actual_ev, requested_ev)) / 150.0
    return (
        -1.0 * result["voltage_deviation_pu"]
        -10.0 * result["voltage_violation_severity"]
        -0.5 * result["losses_mw"] / loss_ref_mw
        -5.0 * result["thermal_overload_severity"]
        -2.0 * infeasible
        -0.01 * effort
    )

def candidate_actions(rng, count=32):
    """Nine-position schema, eight active positions (index 5 neutral)."""
    candidates = []
    for _ in range(count):
        cand = [rng.uniform(lo, hi) for lo, hi in zip(LO, HI)]
        cand[5] = 0.0
        candidates.append(tuple(cand))
    return candidates

def sample_born(rewards, rng, beta=5.0):
    m = max(rewards)
    scores = [math.exp(max(-700.0, beta * (r-m))) for r in rewards]
    total = sum(scores)
    z = rng.random() * total
    for i, value in enumerate(scores):
        z -= value
        if z <= 0:
            return i
    return len(rewards) - 1

def droop_action(observation):
    if not observation.get("converged"):
        return None
    mapping = dict(zip(observation["bus_numbers"], observation["vm"]))
    err = 1.0 - mapping[14]
    return clamp_action((5.0*err, 0, 0.3, 0, 0, 0, 0, 0, 0))

def _solve(case, adapter, root, ordinal):
    path = root / ("candidate_%05d.raw" % ordinal)
    case.save(path)
    return adapter.solve(path, case.bus_ids(), case.branch_records(), case.generators())

def simulate(case_path, profile_path, policy, output, max_steps=None, seed=42,
             candidates=32, beta=5.0, statcom_bus=39, trip=None, dry_run=False,
             adapter=None):
    base = RawCase.read(case_path)
    if len(base.bus_ids()) != 39:
        raise ValueError("First deployment targets IEEE 39-bus only; other cases require placement/encoder adaptation")
    for must_exist in (3, 4, 8, 14, 15, 16, 17, 26, 28, 39):
        if must_exist not in base.bus_ids():
            raise ValueError("CAPSM missing required bus %d" % must_exist)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    profiles = list(read_profiles(profile_path))
    if max_steps is not None:
        profiles = profiles[:max_steps]
    if not profiles:
        raise ValueError("No profile steps")
    fleet, rng = EVFleet(), random.Random(seed)
    adapter = None if dry_run else (adapter if adapter is not None else Psse35(max_buses=2000))
    summary = {"policy": policy, "source_case": str(case_path), "profiles": str(profile_path),
               "seed": seed, "count": len(profiles), "simulator": "PSS/E 35",
               "model_class": "AC quasi-static, FACTS steady-state equivalents",
               "evidence_status": "DRY_RUN" if dry_run else "PENDING_VALIDATION",
               "failed_solves": 0, "completed": 0}
    log = output / "trajectory.jsonl"
    with tempfile.TemporaryDirectory(prefix="capsm_psse_") as tmp:
        tempdir = Path(tmp)
        with log.open("w", encoding="utf-8") as stream:
            for step, profile in enumerate(profiles):
                state = profile_case(base, profile)
                is_outage = trip is not None and trip[2] <= step < trip[2] + trip[3]
                if is_outage:
                    state.trip_branch(trip[0], trip[1], "1")
                if dry_run:
                    record = {"step": step, "timestamp": profile["timestamp"],
                              "load_scale": profile["load_scale"], "wind_mw": profile["wind_mw"],
                              "solar_mw": profile["solar_mw"], "outage": is_outage,
                              "dry_run": True, "state_bus_count": len(state.bus_ids())}
                    stream.write(json.dumps(record)+"\n")
                    summary["completed"] += 1
                    continue
                # Observe the current operating point first. One exact solve
                # per candidate then uses the SAME frozen operating snapshot.
                obs = _solve(state, adapter, tempdir, 0)
                actions_evaluated = 0
                if policy == "none" or not obs.get("converged"):
                    chosen = None
                elif policy == "droop":
                    chosen = droop_action(obs)
                elif policy in ("qirl_exact", "greedy_exact"):
                    choices = candidate_actions(rng, candidates)
                    scores = []
                    for idx, action in enumerate(choices, 1):
                        variant = state.clone()
                        preview = apply_action(variant, action, fleet, commit=False, statcom_bus=statcom_bus)
                        predicted = _solve(variant, adapter, tempdir, idx)
                        scores.append(reward(predicted, action, preview["ev_mw"], action[6:9]))
                    chosen = choices[(sample_born(scores,rng,beta) if policy=="qirl_exact" else max(range(len(scores)), key=scores.__getitem__))]
                    actions_evaluated = len(choices)
                else:
                    raise ValueError("unknown policy: " + policy)
                if chosen is None:
                    result = obs
                    actual_action = None
                    applied = None
                else:
                    variant = state.clone()
                    applied = apply_action(variant, chosen, fleet, commit=False, statcom_bus=statcom_bus)
                    result = _solve(variant, adapter, tempdir, candidates + 1)
                    # Committing the EV energy transition exactly once AFTER a
                    # successful power flow prevents candidate evaluation from
                    # changing the live state.
                    if result.get("converged"):
                        fleet.dispatch(chosen[6:9], commit=True)
                    actual_action = list(chosen)
                record = {"step": step, "timestamp": profile["timestamp"], "profile": profile,
                          "outage": is_outage, "observation": obs, "post_action": result,
                          "action": actual_action, "soc": list(fleet.soc),
                          "candidate_evaluations": actions_evaluated,
                          "action_metadata": applied}
                stream.write(json.dumps(record, allow_nan=False) + "\n")
                summary["completed"] += 1
                summary["failed_solves"] += int(not result.get("converged"))
    summary["evidence_status"] = "UNVERIFIED_PSSE_RUN" if not dry_run else "DRY_RUN"
    (output / "manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--case", required=True)
    ap.add_argument("--profiles", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--policy", choices=["none", "droop", "qirl_exact", "greedy_exact"], default="none")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-steps", type=int)
    ap.add_argument("--candidates", type=int, default=32)
    ap.add_argument("--beta", type=float, default=5.0)
    ap.add_argument("--statcom-bus", type=int, default=39)
    ap.add_argument("--trip-line", nargs=4, type=int, metavar=("FROM","TO","START_STEP","DURATION"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    result = simulate(args.case, args.profiles, args.policy, args.output, args.max_steps,
                      args.seed, args.candidates, args.beta, args.statcom_bus,
                      tuple(args.trip_line) if args.trip_line else None, args.dry_run)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
