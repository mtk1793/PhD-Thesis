"""Phase 8 — Statistical analysis rebuild (master plan §18, Phase O).

Consumes the ablation CSV produced by ``phase7_ablations.py`` (and any
per-seed result tables) and produces the full statistical report:

  - mean, SD, median, IQR, 95% confidence interval per variant
  - lag-1 autocorrelation of the hourly series (time-correlation diagnostic)
  - paired MOVING-BLOCK bootstrap confidence intervals for key comparisons
  - explicit statistical vs engineering significance split

Because hourly QSTS observations are strongly time-correlated, i.i.d.
paired t-tests are NOT used as primary evidence (master plan §18).
Block bootstrap uses block length L = ceil(1.5 * n ** (1/3)) steps
(Politis & White-style heuristic) with B = 10000 resamples by default.

Usage:
  python scripts/phase8_statistics.py --ablation results/phase7/ablation_rows.csv
      [--baseline-variant qirl_qirl] [--compare capsm]
      [--series-csv results/phase6/case39_jan2019_capsm.csv ...]
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS = Path("results/phase8")
RESULTS.mkdir(parents=True, exist_ok=True)

METRICS = [
    "mean_voltage_dev_pu",
    "voltage_violation_hours",
    "violation_severity_pu2",
    "mean_losses_mw",
]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ablation", type=str,
                   default="results/phase7/ablation_rows.csv")
    p.add_argument("--series-csv", type=str, nargs="*", default=[],
                   help="optional per-step controller CSVs for autocorrelation diagnostics")
    p.add_argument("--n-bootstrap", type=int, default=10000)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def descriptive(series: np.ndarray) -> dict:
    s = np.asarray(series, dtype=float)
    s = s[~np.isnan(s)]
    if len(s) == 0:
        return {}
    lo, hi = np.percentile(s, [2.5, 97.5])
    return {
        "n": int(len(s)),
        "mean": float(np.mean(s)),
        "std": float(np.std(s, ddof=1)) if len(s) > 1 else 0.0,
        "median": float(np.median(s)),
        "iqr": float(np.percentile(s, 75) - np.percentile(s, 25)),
        "ci95_low": float(lo),
        "ci95_high": float(hi),
    }


def lag1_autocorr(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    if len(x) < 3 or np.std(x) == 0:
        return float("nan")
    x0 = x[:-1] - x[:-1].mean()
    x1 = x[1:] - x[1:].mean()
    return float(np.sum(x0 * x1) / np.sqrt(np.sum(x0**2) * np.sum(x1**2)))


def block_bootstrap_indices(n: int, block: int, rng: np.random.Generator):
    """Yield resampled index arrays of length n using moving blocks."""
    n_blocks = int(np.ceil(n / block))
    while True:
        starts = rng.integers(0, n - block + 1, size=n_blocks)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        yield idx


def paired_block_bootstrap(diff: np.ndarray, n_boot: int,
                           seed: int) -> tuple[float, float]:
    """95% CI for the mean of a paired difference series via moving blocks.

    ``diff`` must already be an aligned per-seed or per-step difference.
    """
    x = np.asarray(diff, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 8:
        return float("nan"), float("nan")
    block = max(2, int(np.ceil(1.5 * n ** (1 / 3))))
    rng = np.random.default_rng(seed)
    gen = block_bootstrap_indices(n, block, rng)
    means = np.empty(n_boot)
    for b in range(n_boot):
        idx = next(gen)
        means[b] = x[idx].mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi)


def main():
    args = parse_args()
    report = {"n_bootstrap": args.n_bootstrap, "seed": args.seed}

    # ── variant-level descriptives ───────────────────────────────────
    ab_path = Path(args.ablation)
    if ab_path.exists():
        df = pd.read_csv(ab_path)
        desc = {}
        for variant, g in df.groupby("variant"):
            desc[variant] = {m: descriptive(g[m].to_numpy()) for m in METRICS}
        report["descriptives"] = desc

        # ── paired comparisons on aligned seeds ──────────────────────
        pivot = df.pivot_table(index="seed", columns="variant",
                               values="voltage_violation_hours")
        comparisons = {}
        if "capsm" in pivot.columns:
            baseline_variants = [c for c in pivot.columns
                                 if c not in ("capsm", "s1_only", "s2_only")]
            for other in baseline_variants:
                d = pivot["capsm"] - pivot[other]
                lo, hi = paired_block_bootstrap(
                    d.to_numpy(), args.n_bootstrap, args.seed)
                comparisons[f"capsm_vs_{other}"] = {
                    "metric": "voltage_violation_hours",
                    "mean_diff": float(np.nanmean(d)),
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "statistically_significant": bool(
                        np.isfinite(lo) and np.isfinite(hi) and (hi < 0 or lo > 0)),
                    "n_seeds": int(d.notna().sum()),
                }
        report["paired_comparisons"] = comparisons

        # ── engineering significance template ────────────────────────
        report["engineering_significance_note"] = (
            "A comparison is reported as statistically significant only when "
            "the 95% paired block-bootstrap CI of the mean difference excludes "
            "zero. Engineering significance must be judged separately against "
            "the operational relevance of the metric magnitude (master plan §18)."
        )
    else:
        report["descriptives"] = {}
        report["warning"] = f"ablation file not found: {ab_path}"

    # ── autocorrelation diagnostics on per-step series ───────────────
    ac = {}
    for path in args.series_csv:
        p = Path(path)
        if not p.exists():
            continue
        s = pd.read_csv(p)
        col = "n_voltage_violations" if "n_voltage_violations" in s.columns else None
        if col is None:
            continue
        ac[p.stem] = {
            "lag1_autocorr": lag1_autocorr(s[col].to_numpy()),
            "n_steps": int(len(s)),
        }
    if ac:
        report["autocorrelation"] = ac
        report["autocorrelation_note"] = (
            "Lag-1 autocorrelation of hourly violation counts; values near 1 "
            "confirm i.i.d. t-tests are inappropriate and block bootstrap is "
            "required."
        )

    out = RESULTS / "statistical_report.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2)[:3000])
    print(f"[phase8] report written to {out}")
    print("[phase8] done.")


if __name__ == "__main__":
    main()
