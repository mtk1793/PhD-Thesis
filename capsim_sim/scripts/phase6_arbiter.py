"""Phase 6 — Full CAPSM integration evaluation.

Evaluates the complete CAPSM dual-process architecture:
  System 1 (CNN-LSTM) + System 2 (QIRL) + Metacognitive Arbiter

against all baselines on the January 2019 IEEE 39-bus benchmark.
"""

import json
import time
from pathlib import Path

import numpy as np

from capsm.agents.arbiter import MetacognitiveArbiter
from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.system2 import QIRLController
from capsm.agents.baselines import NoControl, RuleBasedVoltage, PIDVoltage, run_controller
from capsm.agents.trainer import collect_demos, train_behavior_cloning
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase6")
RESULTS.mkdir(parents=True, exist_ok=True)


def main():
    print("[phase6] loading OPSD profiles ...")
    profiles = load_opsd(start="2019-01-01", end="2019-01-31")

    print("[phase6] training System 1 ...")
    env_train = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env_train)
    trajs, _ = collect_demos("case39", profiles, n_episodes=4, steps_per_episode=168)
    model = train_behavior_cloning(trajs, encoder.n_features, 9, epochs=100,
                                   batch_size=128, lr=1e-3, verbose=False)
    s1 = System1Controller(model, encoder)
    print("[phase6] System 1 trained")

    s2 = QIRLController(n_candidates=32, seed=42)
    arb = MetacognitiveArbiter(s1, s2, threshold=0.03)

    results = {}
    controllers = {
        "no_control": NoControl(),
        "rule_based": RuleBasedVoltage(),
        "pid": PIDVoltage(),
        "system1": s1,
        "system2": s2,
        "capsm": arb,
    }

    for label, ctrl in controllers.items():
        print(f"[phase6] evaluating {label} ...")
        env = QSTSEnvironment("case39", profiles)
        t0 = time.time()
        df = run_controller(env, ctrl, start="2019-01-01")
        dt = time.time() - t0
        results[label] = {
            "mean_losses_mw": round(float(df["losses_mw"].mean()), 2),
            "max_losses_mw": round(float(df["losses_mw"].max()), 2),
            "mean_voltage_dev_pu": round(float(df["voltage_deviation_pu"].mean()), 4),
            "voltage_violation_hours": int(df["n_voltage_violations"].sum()),
            "min_vm_min": round(float(df["vm_min"].min()), 4),
            "converged": int(df["converged"].sum()),
            "n_steps": len(df),
            "time_s": round(dt, 1),
            "ms_per_step": round(dt / len(df) * 1000, 1),
        }

    print("\n[phase6] === CAPSM Dual-Process Evaluation (Jan 2019, case39) ===\n")
    header = f"{'Controller':<16} {'Loss MW':>8} {'Dev p.u.':>9} {'Violations':>11} {'Conv':>6} {'ms/step':>8}"
    print(header)
    print("-" * len(header))
    for label, s in results.items():
        print(f"{label:<16} {s['mean_losses_mw']:>8.1f} {s['mean_voltage_dev_pu']:>9.4f} "
              f"{s['voltage_violation_hours']:>11} {s['converged']:>4}/{s['n_steps']:<3} {s['ms_per_step']:>7.1f}")

    capsm = results["capsm"]
    none = results["no_control"]
    rule = results["rule_based"]
    s1r = results["system1"]
    s2r = results["system2"]

    print(f"\n[phase6] CAPSM vs NoControl: dev {capsm['mean_voltage_dev_pu'] - none['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {capsm['voltage_violation_hours'] - none['voltage_violation_hours']:+d} h")
    print(f"[phase6] CAPSM vs RuleBased: dev {capsm['mean_voltage_dev_pu'] - rule['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {capsm['voltage_violation_hours'] - rule['voltage_violation_hours']:+d} h")
    print(f"[phase6] CAPSM vs System1: dev {capsm['mean_voltage_dev_pu'] - s1r['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {capsm['voltage_violation_hours'] - s1r['voltage_violation_hours']:+d} h")
    print(f"[phase6] CAPSM vs System2: dev {capsm['mean_voltage_dev_pu'] - s2r['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {capsm['voltage_violation_hours'] - s2r['voltage_violation_hours']:+d} h")

    with open(RESULTS / "phase6_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[phase6] done. Artifacts in {RESULTS}")


if __name__ == "__main__":
    main()
