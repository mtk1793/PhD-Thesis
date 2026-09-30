"""Phase 5 (v2) — System 2 QIRL evaluation with candidate-dependent evaluators.

Rebuilt per master plan §5 (Phase B) and §11 (Phase H, Option 2):

- Candidates are scored on the COUNTERFACTUAL network state (Evaluator A:
  exact AC power flow per candidate; Evaluator B: sensitivity surrogate).
- Selection is honestly single-step (no multi-step planning claims).
- Reports evaluator timing separately so the 50 ms real-time question is
  answered with measured numbers.

Outputs are versioned to ``results/phase5_v2/``.

Usage:
  python scripts/phase5_system2.py [--evaluator surrogate] [--seeds 42]
      [--candidates 32] [--test-start 2019-01-01 --test-end 2019-01-31]
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np

from capsm.agents.baselines import (
    NoControl, PIDVoltage, RuleBasedVoltage, run_controller,
)
from capsm.agents.system2 import QIRLController
from capsm.agents.trainer import TEST_YEARS
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase5_v2")
RESULTS.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evaluator", choices=["exact", "surrogate"], default="surrogate")
    p.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44, 45, 46,
                                                           47, 48, 49, 50, 51])
    p.add_argument("--candidates", type=int, default=32)
    p.add_argument("--refresh-every", type=int, default=24)
    p.add_argument("--test-start", type=str, default="2019-01-01")
    p.add_argument("--test-end", type=str, default="2019-01-31")
    p.add_argument("--beta", type=float, default=5.0)
    p.add_argument("--tunnel-rate", type=float, default=0.1)
    return p.parse_args()


def _summarise(df) -> dict:
    return {
        "mean_losses_mw": round(float(df["losses_mw"].mean()), 2),
        "mean_voltage_dev_pu": round(float(df["voltage_deviation_pu"].mean()), 4),
        "p95_voltage_dev_pu": round(float(df["p95_voltage_dev_pu"].mean()), 4),
        "voltage_violation_hours": int(df["n_voltage_violations"].sum()),
        "violation_severity_pu2": round(float(df["violation_severity_pu2"].sum()), 5),
        "min_vm_min": round(float(df["vm_min"].min()), 4),
        "converged": int(df["converged"].sum()),
        "n_steps": len(df),
    }


def main():
    args = parse_args()
    print(f"[phase5-v2] evaluator={args.evaluator} candidates={args.candidates} "
          f"seeds={args.seeds}")
    profiles = load_opsd(start=args.test_start, end=args.test_end)

    # ── baselines (deterministic; run once) ──────────────────────────
    baselines = {}
    for label, cls in [("no_control", NoControl),
                       ("rule_based", RuleBasedVoltage),
                       ("pid", PIDVoltage)]:
        env_b = QSTSEnvironment("case39", profiles)
        df_b = run_controller(env_b, cls(), start=args.test_start)
        baselines[label] = _summarise(df_b)
        print(f"[phase5-v2] baseline {label}: dev={baselines[label]['mean_voltage_dev_pu']} "
              f"viol={baselines[label]['voltage_violation_hours']} h")

    # ── QIRL per seed ────────────────────────────────────────────────
    per_seed = []
    for seed in args.seeds:
        env = QSTSEnvironment("case39", profiles)
        ctrl = QIRLController(
            env=env,
            n_candidates=args.candidates,
            beta=args.beta,
            tunnel_rate=args.tunnel_rate,
            seed=seed,
            evaluator=args.evaluator,
            refresh_every=args.refresh_every,
        )
        t0 = time.perf_counter()
        df_q = run_controller(env, ctrl, start=args.test_start)
        wall = time.perf_counter() - t0
        s = _summarise(df_q)
        s.update({
            "seed": seed,
            "evaluator_wall_ms_per_step": round(wall / max(len(df_q), 1) * 1000.0, 3),
            "evaluator_power_flows_total": ctrl.evaluator_power_flows,
        })
        per_seed.append(s)
        print(f"[phase5-v2] qirl seed={seed}: dev={s['mean_voltage_dev_pu']} "
              f"viol={s['voltage_violation_hours']} h "
              f"sev={s['violation_severity_pu2']} "
              f"wall={s['evaluator_wall_ms_per_step']} ms/step "
              f"PFs={s['evaluator_power_flows_total']}")

    def agg(key):
        vals = [s[key] for s in per_seed]
        return {"mean": float(np.mean(vals)), "std": float(np.std(vals)),
                "median": float(np.median(vals)),
                "iqr": float(np.percentile(vals, 75) - np.percentile(vals, 25)),
                "n_seeds": len(vals)}

    summary = {
        "config": vars(args),
        "test_window": [args.test_start, args.test_end],
        "scope": "single-step candidate optimisation (planning reserved for future work)",
        "per_seed": per_seed,
        "qirl_aggregates": {
            "mean_voltage_dev_pu": agg("mean_voltage_dev_pu"),
            "voltage_violation_hours": agg("voltage_violation_hours"),
            "violation_severity_pu2": agg("violation_severity_pu2"),
            "mean_losses_mw": agg("mean_losses_mw"),
            "evaluator_wall_ms_per_step": agg("evaluator_wall_ms_per_step"),
        },
        "baselines": baselines,
        "note": "All values are E1 (offline measured) once produced by this script.",
    }
    with open(RESULTS / "phase5_v2_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[phase5-v2] summary written to {RESULTS / 'phase5_v2_summary.json'}")
    print("[phase5-v2] done.")


if __name__ == "__main__":
    main()
