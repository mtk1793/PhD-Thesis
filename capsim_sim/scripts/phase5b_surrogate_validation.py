"""Phase 5b — Surrogate (Evaluator B) validation against exact AC (Evaluator A).

Implements the validation campaign required by master plan §5.2. At every
sampled step both evaluators score the SAME candidate set; we report:

  - candidate reward correlation (Pearson r)
  - Spearman rank correlation
  - top-1 action agreement
  - top-k action overlap (k = 3)
  - voltage prediction MAE (p.u.)
  - overload prediction error (mean absolute count difference)
  - computation time per evaluator (ms per evaluate-all call)

Output: ``results/phase5b/surrogate_validation.json`` (+ per-step CSV).

Usage:
  python scripts/phase5b_surrogate_validation.py [--steps 168] [--candidates 32]
      [--refresh-every 24] [--start 2019-01-01]
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from capsm.agents.evaluators import (
    ExactPowerFlowEvaluator, SensitivitySurrogateEvaluator,
    make_evaluator, vector_to_controls,
)
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment

RESULTS = Path("results/phase5b")
RESULTS.mkdir(parents=True, exist_ok=True)

ACTION_LO = np.array([-0.5, -1.0, 0.3, -0.5, -0.5, 0.0, -50.0, -50.0, -50.0])
ACTION_HI = np.array([0.5, 1.0, 0.7, 0.5, 0.5, 0.0, 50.0, 50.0, 50.0])


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--steps", type=int, default=168, help="validation steps (1 week)")
    p.add_argument("--candidates", type=int, default=32)
    p.add_argument("--refresh-every", type=int, default=24)
    p.add_argument("--start", type=str, default="2019-01-01")
    p.add_argument("--end", type=str, default="2019-01-31")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main():
    args = parse_args()
    profiles = load_opsd(start=args.start, end=args.end)
    env = QSTSEnvironment("case39", profiles)
    rng = np.random.default_rng(args.seed)

    exact = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    surrogate = SensitivitySurrogateEvaluator(
        env, ACTION_LO, ACTION_HI, refresh_every=args.refresh_every
    )

    rows = []
    obs = env.reset(start=args.start)
    for step in range(args.steps):
        candidates = rng.uniform(ACTION_LO, ACTION_HI,
                                 size=(args.candidates, 9)).astype(np.float64)
        candidates[:, 5] = 0.0  # reserved dimension neutral

        ex = exact.evaluate_all(env, obs, candidates)
        sr = surrogate.evaluate_all(env, obs, candidates, )

        r = ex.rewards
        s = sr.rewards
        pear = float(pearsonr(r, s)[0])
        spear = float(spearmanr(r, s)[0])
        top1 = int(np.argmax(r) == np.argmax(s))
        topk_ex = set(np.argsort(r)[-3:])
        topk_sr = set(np.argsort(s)[-3:])
        topk_overlap = len(topk_ex & topk_sr) / 3.0
        v_mae = float(np.mean(np.abs(ex.vm_pred - sr.vm_pred)))
        ov_err = float(np.mean(np.abs(
            ex.overload_pred.astype(float) - sr.overload_pred.astype(float))))

        rows.append({
            "step": step,
            "timestamp": str(obs["timestamp"]),
            "pearson_r": round(pear, 4),
            "spearman_rho": round(spear, 4),
            "top1_agreement": top1,
            "topk3_overlap": round(topk_overlap, 3),
            "voltage_mae_pu": round(v_mae, 5),
            "overload_mae": round(ov_err, 3),
            "exact_ms": round(ex.elapsed_ms, 2),
            "surrogate_ms": round(sr.elapsed_ms, 2),
            "surrogate_pfs_this_step": int(sr.n_power_flows),
            "surrogate_refreshed": bool(sr.refreshed),
        })
        print(f"[phase5b] step {step+1}/{args.steps}  rho={spear:.3f}  "
              f"top1={top1}  vMAE={v_mae:.4f}  "
              f"exact={ex.elapsed_ms:.1f} ms  surr={sr.elapsed_ms:.2f} ms")

        obs = env.step(vector_to_controls(env, candidates[int(np.argmax(ex.rewards))]))

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "surrogate_validation_steps.csv", index=False)
    summary = {
        "config": vars(args),
        "n_steps": args.steps,
        "pearson_r": {"mean": float(df.pearson_r.mean()), "min": float(df.pearson_r.min())},
        "spearman_rho": {"mean": float(df.spearman_rho.mean()),
                         "min": float(df.spearman_rho.min())},
        "top1_agreement_rate": float(df.top1_agreement.mean()),
        "topk3_overlap_mean": float(df.topk3_overlap.mean()),
        "voltage_mae_pu_mean": float(df.voltage_mae_pu.mean()),
        "overload_mae_mean": float(df.overload_mae.mean()),
        "exact_ms_mean": float(df.exact_ms.mean()),
        "surrogate_ms_mean": float(df.surrogate_ms.mean()),
        "surrogate_ms_p95": float(df.surrogate_ms.quantile(0.95)),
        "speedup_mean": float(df.exact_ms.mean() / max(df.surrogate_ms.mean(), 1e-9)),
        "evidence_class": "E1 (offline measured) once produced by this script",
    }
    with open(RESULTS / "surrogate_validation.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print("[phase5b] done.")


if __name__ == "__main__":
    main()
