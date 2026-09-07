"""Phase 5 — System 2 QIRL evaluation.

Evaluates the Quantum-Inspired RL controller against baselines on
the January 2019 IEEE 39-bus benchmark.
"""

import json
import time
from pathlib import Path

from capsm.agents.system2 import QIRLController
from capsm.agents.baselines import NoControl, RuleBasedVoltage, run_controller
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase5")
RESULTS.mkdir(parents=True, exist_ok=True)


def main():
    print("[phase5] loading OPSD profiles ...")
    profiles = load_opsd(start="2019-01-01", end="2019-01-31")

    print("[phase5] evaluating QIRL vs baselines on January 2019 ...")
    env1 = QSTSEnvironment("case39", profiles)
    ctrl = QIRLController(n_candidates=32, seed=42)
    t0 = time.time()
    df_qirl = run_controller(env1, ctrl, start="2019-01-01")
    dt_qirl = time.time() - t0

    env2 = QSTSEnvironment("case39", profiles)
    t0 = time.time()
    df_none = run_controller(env2, NoControl(), start="2019-01-01")
    dt_none = time.time() - t0

    env3 = QSTSEnvironment("case39", profiles)
    t0 = time.time()
    df_rule = run_controller(env3, RuleBasedVoltage(), start="2019-01-01")
    dt_rule = time.time() - t0

    summary = {}
    for label, df in [("qirl", df_qirl), ("no_control", df_none), ("rule_based", df_rule)]:
        summary[label] = {
            "mean_losses_mw": round(float(df["losses_mw"].mean()), 2),
            "max_losses_mw": round(float(df["losses_mw"].max()), 2),
            "mean_voltage_dev_pu": round(float(df["voltage_deviation_pu"].mean()), 4),
            "voltage_violation_hours": int(df["n_voltage_violations"].sum()),
            "mean_vm_min": round(float(df["vm_min"].mean()), 4),
            "min_vm_min": round(float(df["vm_min"].min()), 4),
            "converged": int(df["converged"].sum()),
            "n_steps": len(df),
        }

    print("[phase5] results:")
    for label, s in summary.items():
        print(f"  {label}: losses={s['mean_losses_mw']} MW  "
              f"dev={s['mean_voltage_dev_pu']}  "
              f"viol={s['voltage_violation_hours']} h  "
              f"conv={s['converged']}/{s['n_steps']}")

    with open(RESULTS / "phase5_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    q = summary["qirl"]
    n = summary["no_control"]
    r = summary["rule_based"]
    print(f"\n[phase5] QIRL vs NoControl: dev {q['mean_voltage_dev_pu'] - n['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {q['voltage_violation_hours'] - n['voltage_violation_hours']:+d} h")
    print(f"[phase5] QIRL vs RuleBased: dev {q['mean_voltage_dev_pu'] - r['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {q['voltage_violation_hours'] - r['voltage_violation_hours']:+d} h")
    print(f"[phase5] QIRL time: {dt_qirl:.1f}s for {len(df_qirl)} steps "
          f"({dt_qirl/len(df_qirl)*1000:.1f} ms/step)")
    print("[phase5] done.")


if __name__ == "__main__":
    main()
