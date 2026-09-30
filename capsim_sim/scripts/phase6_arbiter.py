"""Phase 6 (v2) — Full CAPSM integration evaluation.

Evaluates the complete CAPSM dual-process architecture:
  System 1 (CNN-LSTM) + System 2 (QIRL) + Metacognitive Arbiter

against all baselines on the held-out January 2019 IEEE 39-bus benchmark.

Rebuilt per the master plan:
  - System 1 is trained on 2015-2017 demonstrations only (no leakage);
    this script expects a frozen Phase-4 checkpoint by default so the
    evaluated controller is exactly the deployed one.
  - System 2 uses the candidate-dependent counterfactual evaluators.
  - Outputs are versioned to ``results/phase6_v2/``.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np

from capsm.agents.arbiter import MetacognitiveArbiter
from capsm.agents.baselines import (
    NoControl, PIDVoltage, RuleBasedVoltage, run_controller,
)
from capsm.agents.system2 import QIRLController
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase6_v2")
RESULTS.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint", type=str,
                   default="results/phase4_v2/system1_cnnlstm_seed42.pt")
    p.add_argument("--test-start", type=str, default="2019-01-01")
    p.add_argument("--test-end", type=str, default="2019-01-31")
    p.add_argument("--evaluator", choices=["exact", "surrogate"], default="surrogate")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--skip-system1", action="store_true",
                   help="evaluate System 2 / arbiter-blend variants only")
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


def _load_system1(ckpt: str, profiles):
    if ckpt == "NONE":
        return None
    import torch
    from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
    env_tmp = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env_tmp)
    model = CNNLSTM(encoder.n_features, 9)
    model.load_state_dict(torch.load(ckpt, map_location="cpu", weights_only=True))
    model.eval()
    return System1Controller(model, encoder, temporal_mode="window_reset")


def main():
    args = parse_args()
    profiles = load_opsd(start=args.test_start, end=args.test_end)
    s1 = _load_system1(args.checkpoint, profiles)
    if s1 is None and not args.skip_system1:
        raise SystemExit("System 1 checkpoint required (train it with phase4_system1.py "
                         "or pass --skip-system1)")

    results = {}
    controllers = {
        "no_control": NoControl(),
        "rule_based": RuleBasedVoltage(),
        "pid": PIDVoltage(),
    }
    if s1 is not None:
        controllers["system1"] = s1

    env_s2 = QSTSEnvironment("case39", profiles)
    s2 = QIRLController(env=env_s2, n_candidates=32, seed=args.seed,
                        evaluator=args.evaluator)
    controllers["system2"] = s2

    if s1 is not None:
        env_arb = QSTSEnvironment("case39", profiles)
        s1_a = _load_system1(args.checkpoint, profiles)
        s2_a = QIRLController(env=env_arb, n_candidates=32, seed=args.seed,
                              evaluator=args.evaluator)
        controllers["capsm"] = MetacognitiveArbiter(s1_a, s2_a, threshold=0.03)

    for label, ctrl in controllers.items():
        print(f"[phase6-v2] evaluating {label} ...")
        env = QSTSEnvironment("case39", profiles)
        t0 = time.perf_counter()
        df = run_controller(env, ctrl, start=args.test_start)
        dt = time.perf_counter() - t0
        results[label] = _summarise(df)
        results[label]["wall_s"] = round(dt, 2)
        if hasattr(ctrl, "arbitration_summary"):
            results[label]["arbitration"] = ctrl.arbitration_summary()
        s = results[label]
        print(f"[phase6-v2] {label}: dev={s['mean_voltage_dev_pu']} "
              f"viol={s['voltage_violation_hours']} h "
              f"sev={s['violation_severity_pu2']} losses={s['mean_losses_mw']} MW")

    summary = {
        "checkpoint": args.checkpoint,
        "test_window": [args.test_start, args.test_end],
        "results": results,
        "note": "All values are E1 (offline measured) once produced by this script.",
    }
    with open(RESULTS / "phase6_v2_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[phase6-v2] summary written to {RESULTS / 'phase6_v2_summary.json'}")
    print("[phase6-v2] done.")


if __name__ == "__main__":
    main()
