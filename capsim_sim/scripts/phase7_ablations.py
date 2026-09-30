"""Phase 7 — QIRL and Arbiter ablation campaigns.

Implements the ablation matrices required by master plan §10 (Phase G)
and §12 (Phase I), with multi-seed stochastic repeats (§18 Phase O).

QIRL ablations (selection mechanisms over identical candidate sets):
    random          — uniform candidate choice
    greedy          — argmax of the candidate-dependent reward
    softmax         — per-step Boltzmann sampling (no persistent amplitudes)
    softmax_refresh — Boltzmann sampling + per-step candidate re-draw
    qirl_no_tunnel  — full QIRL with tunnelling disabled
    qirl            — full QIRL (amplitudes + Born rule + tunnelling)

Arbiter ablations:
    s1_only         — System 1 alone
    s2_only         — System 2 alone
    fixed_5050      — constant α = 0.5 blend
    hard_switch     — α ∈ {0,1} at the stress threshold
    sigmoid_nosafe  — deployed sigmoid blend (safe mode off) = full CAPSM
    capsm           — full CAPSM (sigmoid arbiter; alias of sigmoid_nosafe)

All rows are appended to CSV so phase8_statistics.py can compute
mean/SD/median/IQR/95% CI and paired block-bootstrap comparisons.

Usage (requires a trained System 1 checkpoint):
  python scripts/phase7_ablations.py --checkpoint results/phase4_v2/system1_cnnlstm_seed42.pt
      [--qirl-seeds 10] [--window 2019-01-01 2019-01-31]
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from capsm.agents.arbiter import MetacognitiveArbiter
from capsm.agents.baselines import run_controller
from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.system2 import QIRLController
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase7")
RESULTS.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint", type=str,
                   default="results/phase4_v2/system1_cnnlstm_seed42.pt")
    p.add_argument("--qirl-seeds", type=int, default=10)
    p.add_argument("--campaign", choices=["qirl", "arbiter", "both"], default="both")
    p.add_argument("--candidates", type=int, default=32)
    p.add_argument("--evaluator", choices=["exact", "surrogate"], default="surrogate")
    p.add_argument("--start", type=str, default="2019-01-01")
    p.add_argument("--end", type=str, default="2019-01-31")
    p.add_argument("--seed-base", type=int, default=100)
    return p.parse_args()


def summarise(df) -> dict:
    return {
        "mean_voltage_dev_pu": round(float(df["voltage_deviation_pu"].mean()), 5),
        "voltage_violation_hours": int(df["n_voltage_violations"].sum()),
        "violation_severity_pu2": round(float(df["violation_severity_pu2"].sum()), 5),
        "mean_losses_mw": round(float(df["losses_mw"].mean()), 3),
        "min_vm_min": round(float(df["vm_min"].min()), 4),
        "n_overloaded_steps": int((df["n_overloaded_lines"] > 0).sum()),
        "converged": int(df["converged"].sum()),
        "n_steps": len(df),
    }


def load_system1(ckpt: str, profiles: pd.DataFrame):
    env_tmp = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env_tmp)
    model = CNNLSTM(encoder.n_features, 9)
    model.load_state_dict(torch.load(ckpt, map_location="cpu", weights_only=True))
    model.eval()
    return System1Controller(model, encoder, temporal_mode="window_reset")


def run_variant(label: str, controller, profiles, start: str) -> dict:
    env = QSTSEnvironment("case39", profiles)
    df = run_controller(env, controller, start=start)
    row = {"variant": label, **summarise(df)}
    if hasattr(controller, "arbitration_summary"):
        row.update({f"arb_{k}": v for k, v in controller.arbitration_summary().items()})
    return row


def main():
    args = parse_args()
    profiles = load_opsd(start=args.start, end=args.end)
    s1 = load_system1(args.checkpoint, profiles)

    rows = []
    seed_ids = list(range(args.seed_base, args.seed_base + args.qirl_seeds))

    if args.campaign in ("qirl", "both"):
        variants = [
            ("random", dict(mode="random")),
            ("greedy", dict(mode="greedy")),
            ("softmax", dict(mode="softmax")),
            ("softmax_refresh", dict(mode="softmax", candidate_refresh=True)),
            ("qirl_no_tunnel", dict(mode="qirl", tunnel=False)),
            ("qirl", dict(mode="qirl")),
        ]
        print(f"[phase7] QIRL ablation campaign: {len(variants)} variants "
              f"x {len(seed_ids)} seeds")
        for label, kw in variants:
            for seed in seed_ids:
                env = QSTSEnvironment("case39", profiles)
                s2 = QIRLController(env=env, n_candidates=args.candidates,
                                    seed=seed, evaluator=args.evaluator, **kw)
                row = run_variant(f"qirl_{label}", s2, profiles, args.start)
                row["seed"] = seed
                rows.append(row)
                print(f"[phase7] {row['variant']} seed={seed}: "
                      f"dev={row['mean_voltage_dev_pu']:.4f} "
                      f"viol={row['voltage_violation_hours']}")

    if args.campaign in ("arbiter", "both"):
        print(f"[phase7] Arbiter ablation campaign x {len(seed_ids)} seeds")
        for seed in seed_ids:
            env_s2_only = QSTSEnvironment("case39", profiles)
            s2_only = QIRLController(env=env_s2_only, n_candidates=args.candidates,
                                     seed=seed, evaluator=args.evaluator)
            rows.append({**run_variant("s2_only", s2_only, profiles, args.start),
                         "seed": seed})

            env_s1_only = QSTSEnvironment("case39", profiles)
            s1_only = load_system1(args.checkpoint, profiles)
            rows.append({**run_variant("s1_only", s1_only, env_s1_only, args.start),
                         "seed": seed})

            for label, kw in [
                ("fixed_5050", dict(mode="fixed", fixed_alpha=0.5)),
                ("hard_switch", dict(mode="hard")),
                ("capsm", dict(mode="sigmoid")),
            ]:
                env_v = QSTSEnvironment("case39", profiles)
                s1_v = load_system1(args.checkpoint, profiles)
                s2_v = QIRLController(env=env_v, n_candidates=args.candidates,
                                      seed=seed, evaluator=args.evaluator)
                arb = MetacognitiveArbiter(s1_v, s2_v, threshold=0.03, **kw)
                row = run_variant(f"capsm_{label}" if label != "capsm" else "capsm",
                                  arb, profiles, args.start)
                row["seed"] = seed
                rows.append(row)
                print(f"[phase7] {row['variant']} seed={seed}: "
                      f"dev={row['mean_voltage_dev_pu']:.4f} "
                      f"viol={row['voltage_violation_hours']}")

    out = RESULTS / ("ablation_rows.csv")
    df_out = pd.DataFrame(rows)
    header = not out.exists()
    df_out.to_csv(out, mode="a", header=header, index=False)
    with open(RESULTS / "ablation_config.json", "w") as f:
        json.dump({"config": vars(args),
                   "evidence_class": "E1 once produced"}, f, indent=2)
    print(f"[phase7] {len(df_out)} rows appended to {out}")
    print("[phase7] done.")


if __name__ == "__main__":
    main()
