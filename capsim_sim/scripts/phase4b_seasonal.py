"""Phase 4b — Seasonal and extreme-event generalisation evaluation.

Implements master plan §16 (Phase M): evaluate frozen controllers across
the full held-out year 2019 with January retained as the detailed
benchmark month. Produces monthly summaries for each controller and
flags the extreme windows required by the plan:

  - largest positive/negative 3 h load ramp of the test year
  - highest-renewable / lowest-load hour
  - highest-load / lowest-renewable hour

Usage (frozen System 1 checkpoint required):
  python scripts/phase4b_seasonal.py --checkpoint results/phase4_v2/system1_cnnlstm_seed42.pt \
      [--controllers capsm system1 rule_based no_control] [--year 2019]
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from capsm.agents.baselines import NoControl, PIDVoltage, RuleBasedVoltage, run_controller
from capsm.agents.system1 import StateEncoder, System1Controller
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase4b")
RESULTS.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint", type=str, default="")
    p.add_argument("--controllers", type=str, nargs="+",
                   default=["rule_based", "no_control"])
    p.add_argument("--year", type=int, default=2019)
    return p.parse_args()


def summarise(df) -> dict:
    return {
        "mean_voltage_dev_pu": round(float(df["voltage_deviation_pu"].mean()), 5),
        "voltage_violation_hours": int(df["n_voltage_violations"].sum()),
        "violation_severity_pu2": round(float(df["violation_severity_pu2"].sum()), 5),
        "mean_losses_mw": round(float(df["losses_mw"].mean()), 3),
        "min_vm_min": round(float(df["vm_min"].min()), 4),
        "converged": int(df["converged"].sum()),
        "n_steps": len(df),
    }


def make_controller(name: str, profiles: pd.DataFrame, checkpoint: str):
    if name == "no_control":
        return NoControl()
    if name == "rule_based":
        return RuleBasedVoltage()
    if name == "pid":
        return PIDVoltage()
    if name == "system1":
        import torch
        env_tmp = QSTSEnvironment("case39", profiles)
        encoder = StateEncoder(env_tmp)
        model = System1_ARCH(encoder.n_features)
        model.load_state_dict(torch.load(checkpoint, map_location="cpu",
                                         weights_only=True))
        model.eval()
        return System1Controller(model, encoder, temporal_mode="window_reset")
    if name == "capsm":
        from capsm.agents.arbiter import MetacognitiveArbiter
        from capsm.agents.system2 import QIRLController
        env_tmp = QSTSEnvironment("case39", profiles)
        s1 = make_controller("system1", profiles, checkpoint)
        s2 = QIRLController(env=env_tmp, n_candidates=32, seed=42,
                            evaluator="surrogate")
        return MetacognitiveArbiter(s1, s2, threshold=0.03)
    raise ValueError(f"unknown controller: {name}")


# late import alias to avoid a hard torch dependency at module import time
def System1_ARCH(n_features: int):
    from capsm.agents.system1 import CNNLSTM
    return CNNLSTM(n_features, 9)


def extreme_windows(profiles: pd.DataFrame) -> dict:
    """Locate extreme-event windows per master plan §16."""
    load = profiles["load_actual_mw"]
    ramp3 = load.diff(3)
    return {
        "largest_positive_ramp_start": str(ramp3.idxmax()),
        "largest_negative_ramp_start": str(ramp3.idxmin()),
        "highest_load_hour": str(load.idxmax()),
        "lowest_load_hour": str(load.idxmin()),
    }


def main():
    args = parse_args()
    year = args.year
    profiles = load_opsd(start=f"{year}-01-01", end=f"{year}-12-31")
    extremes = extreme_windows(profiles)
    print(f"[phase4b] extreme windows: {json.dumps(extremes, indent=1)}")

    monthly_rows = []
    for month in range(1, 13):
        start = pd.Timestamp(f"{year}-{month:02d}-01", tz="UTC")
        end = start + pd.offsets.MonthBegin(1)
        # slice profiles to the month (views keep the original index)
        m_profiles = profiles[(profiles.index >= start) & (profiles.index < end)]
        if len(m_profiles) < 24:
            continue
        for name in args.controllers:
            ctrl = make_controller(name, m_profiles, args.checkpoint)
            env = QSTSEnvironment("case39", m_profiles)
            df = run_controller(env, ctrl, start=str(m_profiles.index[0]))
            row = {"month": f"{year}-{month:02d}", "controller": name,
                   **summarise(df)}
            monthly_rows.append(row)
            print(f"[phase4b] {row['month']} {name}: dev={row['mean_voltage_dev_pu']:.4f} "
                  f"viol={row['voltage_violation_hours']} h")

    df_out = pd.DataFrame(monthly_rows)
    df_out.to_csv(RESULTS / f"seasonal_summary_{year}.csv", index=False)

    annual = df_out.groupby("controller").agg(
        voltage_violation_hours=("voltage_violation_hours", "sum"),
        violation_severity_pu2=("violation_severity_pu2", "sum"),
        mean_voltage_dev_pu=("mean_voltage_dev_pu", "mean"),
        mean_losses_mw=("mean_losses_mw", "mean"),
    ).round(4).reset_index()
    annual.to_csv(RESULTS / f"annual_summary_{year}.csv", index=False)

    with open(RESULTS / f"extreme_windows_{year}.json", "w") as f:
        json.dump(extremes, f, indent=2)
    print(f"[phase4b] annual summary:\n{annual.to_string(index=False)}")
    print("[phase4b] done.")


if __name__ == "__main__":
    main()
