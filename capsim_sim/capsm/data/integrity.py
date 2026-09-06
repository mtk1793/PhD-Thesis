"""Data integrity analysis for the OPSD time-series files.

Produces a JSON report and a Markdown summary covering:
- temporal coverage and missing timestamps
- NaN census for the German national and control-area columns
- gap runs (consecutive missing values) per key column
- basic statistics of the real measured series

No values are modified, imputed, or synthesised here; this module only
measures the raw data.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
REPORT_DIR = Path(__file__).resolve().parents[2] / "data"

KEY_COLUMNS_60MIN = [
    "DE_load_actual_entsoe_transparency",
    "DE_load_forecast_entsoe_transparency",
    "DE_solar_generation_actual",
    "DE_wind_generation_actual",
    "DE_wind_onshore_generation_actual",
    "DE_wind_offshore_generation_actual",
    "DE_LU_price_day_ahead",
    "DE_50hertz_load_actual_entsoe_transparency",
    "DE_amprion_load_actual_entsoe_transparency",
    "DE_tennet_load_actual_entsoe_transparency",
    "DE_transnetbw_load_actual_entsoe_transparency",
    "DE_50hertz_solar_generation_actual",
    "DE_amprion_solar_generation_actual",
    "DE_tennet_solar_generation_actual",
    "DE_transnetbw_solar_generation_actual",
    "DE_50hertz_wind_generation_actual",
    "DE_amprion_wind_onshore_generation_actual",
    "DE_tennet_wind_generation_actual",
    "DE_transnetbw_wind_onshore_generation_actual",
]

KEY_COLUMNS_15MIN = [
    "DE_load_actual_entsoe_transparency",
    "DE_load_forecast_entsoe_transparency",
    "DE_solar_generation_actual",
    "DE_wind_generation_actual",
    "DE_wind_offshore_generation_actual",
    "DE_wind_onshore_generation_actual",
]


def gap_runs(series: pd.Series) -> list:
    """Return runs of consecutive NaN values as (start, end, length)."""
    isna = series.isna().to_numpy()
    if not isna.any():
        return []
    idx = series.index
    runs = []
    start = None
    for i, v in enumerate(isna):
        if v and start is None:
            start = i
        elif not v and start is not None:
            runs.append((str(idx[start]), str(idx[i - 1]), int(i - start)))
            start = None
    if start is not None:
        runs.append((str(idx[start]), str(idx[-1]), int(len(isna) - start)))
    return runs


def column_report(df: pd.DataFrame, col: str, freq: str) -> dict:
    s = df[col]
    n = len(s)
    nan_count = int(s.isna().sum())
    runs = gap_runs(s)
    long_runs = [r for r in runs if r[2] > 2]
    total_missing_hours = int(sum(r[2] for r in long_runs))
    return {
        "column": col,
        "n_points": n,
        "nan_count": nan_count,
        "nan_pct": round(100 * nan_count / n, 3) if n else None,
        "n_gap_runs": len(runs),
        "n_gap_runs_gt_2_steps": len(long_runs),
        "steps_in_long_gaps": total_missing_hours,
        "longest_gap_steps": max((r[2] for r in runs), default=0),
        "gap_runs_over_2": long_runs[:20],
        "min": None if nan_count == n else float(np.nanmin(s)),
        "max": None if nan_count == n else float(np.nanmax(s)),
        "mean": None if nan_count == n else float(np.nanmean(s)),
    }


def coverage_report(df: pd.DataFrame, freq: str) -> dict:
    ts = pd.to_datetime(df["utc_timestamp"], utc=True)
    full = pd.date_range(ts.min(), ts.max(), freq=freq)
    missing = full.difference(ts)
    return {
        "start_utc": str(ts.min()),
        "end_utc": str(ts.max()),
        "expected_points": int(len(full)),
        "actual_points": int(ts.nunique()),
        "missing_timestamps": int(len(missing)),
        "missing_timestamp_list": [str(m) for m in missing[:20]],
        "duplicate_timestamps": int(len(ts) - ts.nunique()),
    }


def analyse_file(path: Path, freq: str, key_cols: list) -> dict:
    print(f"[integrity] loading {path.name} ...")
    df = pd.read_csv(path, usecols=["utc_timestamp"] + key_cols)
    df = df.sort_values("utc_timestamp").reset_index(drop=True)
    print(f"[integrity] {path.name}: {len(df):,} rows x {len(df.columns)} cols")
    report = {
        "file": path.name,
        "frequency": freq,
        "coverage": coverage_report(df, freq),
        "columns": {},
    }
    for col in key_cols:
        if col not in df.columns:
            report["columns"][col] = {"present": False}
            continue
        report["columns"][col] = {"present": True, **column_report(df, col, freq)}
        cr = report["columns"][col]
        print(
            f"[integrity]   {col}: NaN {cr['nan_count']:,} ({cr['nan_pct']}%), "
            f"gaps>2: {cr['n_gap_runs_gt_2_steps']}, mean {cr['mean']:.1f}"
            if cr["mean"] is not None
            else f"[integrity]   {col}: all NaN"
        )
    return report


def to_markdown(report: dict) -> str:
    lines = [
        "# OPSD Data Integrity Report",
        "",
        f"Generated from verified raw files (see `data/raw/provenance_manifest.json`).",
        "",
        f"Dataset: {report['dataset']} v{report['version']}",
        f"DOI: {report['doi']}",
        "",
    ]
    for fkey, frep in report["files"].items():
        cov = frep["coverage"]
        lines += [
            f"## {fkey} ({frep['frequency']})",
            "",
            f"- Coverage: {cov['start_utc']} to {cov['end_utc']}",
            f"- Expected points: {cov['expected_points']:,}; actual unique: {cov['actual_points']:,}; "
            f"missing timestamps: {cov['missing_timestamps']:,}; duplicates: {cov['duplicate_timestamps']:,}",
            "",
            "| Column | Present | NaN | NaN % | Gaps >2 steps | Longest gap | Min | Mean | Max |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for col, cr in frep["columns"].items():
            if not cr.get("present"):
                lines.append(f"| {col} | NO | - | - | - | - | - | - | - |")
                continue
            fmt = lambda v: "-" if v is None else f"{v:,.1f}"
            lines.append(
                f"| {col} | yes | {cr['nan_count']:,} | {cr['nan_pct']} | "
                f"{cr['n_gap_runs_gt_2_steps']} | {cr['longest_gap_steps']} | "
                f"{fmt(cr['min'])} | {fmt(cr['mean'])} | {fmt(cr['max'])} |"
            )
        lines.append("")
    return "\n".join(lines)


def run() -> dict:
    report = {
        "dataset": "Open Power System Data - Time series",
        "version": "2020-10-06",
        "doi": "https://doi.org/10.25832/time_series/2020-10-06",
        "files": {
            "60min": analyse_file(
                DATA_DIR / "time_series_60min_singleindex.csv", "h", KEY_COLUMNS_60MIN
            ),
            "15min": analyse_file(
                DATA_DIR / "time_series_15min_singleindex.csv", "15min", KEY_COLUMNS_15MIN
            ),
        },
    }
    out_json = REPORT_DIR / "integrity_report.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    out_md = REPORT_DIR / "integrity_report.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(to_markdown(report))
    print(f"[integrity] wrote {out_json}")
    print(f"[integrity] wrote {out_md}")
    return report


if __name__ == "__main__":
    run()
