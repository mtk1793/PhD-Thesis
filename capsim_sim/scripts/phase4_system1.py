"""Phase 4 — System 1 training and evaluation.

Trains a CNN-LSTM reflexive controller via behavior cloning from
RuleBasedVoltage demonstrations, then evaluates it against the
baseline controllers on the January 2019 IEEE 39-bus benchmark.
"""

import json
import time
from pathlib import Path

import numpy as np

from capsm.agents.baselines import NoControl, RuleBasedVoltage, run_controller
from capsm.agents.collector import collect_trajectory
from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.trainer import collect_demos, train_behavior_cloning, save_model
from capsm.agents.reward import reward_fn
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase4")
RESULTS.mkdir(parents=True, exist_ok=True)


def main():
    print("[phase4] loading OPSD profiles ...")
    profiles = load_opsd(start="2019-01-01", end="2019-01-31")

    print("[phase4] collecting demonstrations from RuleBasedVoltage ...")
    trajectories, encoder = collect_demos(
        "case39", profiles, n_episodes=4, steps_per_episode=168
    )
    total_steps = sum(len(t["states"]) for t in trajectories)
    print(f"[phase4] collected {len(trajectories)} episodes, {total_steps} total steps")

    print("[phase4] training CNN-LSTM via behavior cloning ...")
    t0 = time.time()
    model = train_behavior_cloning(
        trajectories,
        encoder.n_features,
        9,
        epochs=100,
        batch_size=128,
        lr=1e-3,
        verbose=True,
    )
    dt = time.time() - t0
    print(f"[phase4] training complete in {dt:.1f}s")
    save_model(model, RESULTS / "system1_cnnlstm.pt")

    print("[phase4] evaluating System1 vs baselines on January 2019 ...")
    env = QSTSEnvironment("case39", profiles)
    ctrl = System1Controller(model, encoder)
    t0 = time.time()
    df_s1 = run_controller(env, ctrl, start="2019-01-01")
    dt_s1 = time.time() - t0

    env2 = QSTSEnvironment("case39", profiles)
    t0 = time.time()
    df_none = run_controller(env2, NoControl(), start="2019-01-01")
    dt_none = time.time() - t0

    env3 = QSTSEnvironment("case39", profiles)
    t0 = time.time()
    df_rule = run_controller(env3, RuleBasedVoltage(), start="2019-01-01")
    dt_rule = time.time() - t0

    summary = {}
    for label, df in [("system1", df_s1), ("no_control", df_none), ("rule_based", df_rule)]:
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

    print("[phase4] results:")
    for label, s in summary.items():
        print(f"  {label}: losses={s['mean_losses_mw']} MW  "
              f"dev={s['mean_voltage_dev_pu']}  "
              f"viol={s['voltage_violation_hours']} h  "
              f"conv={s['converged']}/{s['n_steps']}")

    with open(RESULTS / "phase4_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    s1 = summary["system1"]
    none = summary["no_control"]
    rule = summary["rule_based"]
    dev_delta = (s1["mean_voltage_dev_pu"] - none["mean_voltage_dev_pu"])
    viol_delta = s1["voltage_violation_hours"] - none["voltage_violation_hours"]
    print(f"\n[phase4] System1 vs NoControl: dev {dev_delta:+.4f} p.u.  "
          f"viol {viol_delta:+d} h")
    print(f"[phase4] System1 vs RuleBased: dev "
          f"{s1['mean_voltage_dev_pu'] - rule['mean_voltage_dev_pu']:+.4f} p.u.  "
          f"viol {s1['voltage_violation_hours'] - rule['voltage_violation_hours']:+d} h")
    print(f"[phase4] System1 inference time: {dt_s1:.1f}s for {len(df_s1)} steps "
          f"({dt_s1/len(df_s1)*1000:.1f} ms/step)")
    print("[phase4] done.")


if __name__ == "__main__":
    main()
