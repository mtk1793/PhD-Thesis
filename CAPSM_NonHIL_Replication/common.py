from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

SEED = 42


def seed_everything(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    try:
        torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception:
        pass


def load_real_opsd(path: str | Path | None = None) -> pd.DataFrame:
    """Load real OPSD data.

    Search order:
      1) explicit path,
      2) capsim_sim/data/processed/opsd_de_60min.parquet in a parent checkout,
      3) capsim_sim/data/raw/time_series_60min_singleindex.csv in a parent checkout,
      4) bundled real OPSD sample week committed in the thesis repository.

    The bundled sample is genuine measured OPSD data and is used for CI/smoke runs.
    Full thesis runs should point to the verified 2020-10-06 OPSD package.
    """
    candidates: list[Path] = []
    if path:
        candidates.append(Path(path))
    cwd = Path.cwd()
    for base in [cwd, ROOT, *ROOT.parents]:
        candidates += [
            base / "capsim_sim/data/processed/opsd_de_60min.parquet",
            base / "capsim_sim/data/raw/time_series_60min_singleindex.csv",
            base / "capsim_sim/tests/data/sample_opsd_week.csv",
        ]
    candidates.append(DATA / "sample_opsd_week.csv")

    for p in candidates:
        if not p.exists():
            continue
        if p.suffix == ".parquet":
            df = pd.read_parquet(p)
        else:
            df = pd.read_csv(p)
        # Normalize the full OPSD schema into the compact thesis schema.
        ren = {
            "DE_load_actual_entsoe_transparency": "load_actual_mw",
            "DE_load_forecast_entsoe_transparency": "load_forecast_mw",
            "DE_solar_generation_actual": "solar_mw",
            "DE_wind_offshore_generation_actual": "wind_offshore_mw",
            "DE_wind_onshore_generation_actual": "wind_onshore_mw",
            "DE_LU_price_day_ahead": "price_day_ahead_eur",
            "utc_timestamp": "timestamp",
        }
        df = df.rename(columns={k: v for k, v in ren.items() if k in df.columns})
        required = ["timestamp", "load_actual_mw", "solar_mw", "wind_offshore_mw", "wind_onshore_mw"]
        if all(c in df.columns for c in required):
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            if "load_forecast_mw" not in df:
                df["load_forecast_mw"] = df["load_actual_mw"]
            if "price_day_ahead_eur" not in df:
                df["price_day_ahead_eur"] = np.nan
            df["wind_mw"] = df["wind_offshore_mw"].fillna(0) + df["wind_onshore_mw"].fillna(0)
            df["renewable_mw"] = df["wind_mw"] + df["solar_mw"].fillna(0)
            df["load_ramp_mw"] = df["load_actual_mw"].diff().fillna(0)
            df["renewable_ramp_mw"] = df["renewable_mw"].diff().fillna(0)
            df["forecast_error_mw"] = (df["load_actual_mw"] - df["load_forecast_mw"]).fillna(0)
            df.attrs["source_path"] = str(p)
            df.attrs["is_full_opsd"] = "sample_opsd_week.csv" not in p.name
            return df.reset_index(drop=True)
    raise FileNotFoundError("No OPSD data found")


def robust_scale(x: np.ndarray, q: float = 0.98) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    den = np.nanquantile(np.abs(x), q)
    if not np.isfinite(den) or den < 1e-12:
        den = 1.0
    return np.clip(x / den, -2.0, 2.0)


def operating_features(df: pd.DataFrame) -> np.ndarray:
    load = robust_scale(df["load_actual_mw"].to_numpy())
    renew = robust_scale(df["renewable_mw"].to_numpy())
    lramp = robust_scale(df["load_ramp_mw"].to_numpy())
    rramp = robust_scale(df["renewable_ramp_mw"].to_numpy())
    ferr = robust_scale(df["forecast_error_mw"].to_numpy())
    solar = robust_scale(df["solar_mw"].fillna(0).to_numpy())
    return np.column_stack([load, renew, lramp, rramp, ferr, solar]).astype(np.float32)


def write_json(name: str, payload: dict) -> Path:
    path = RESULTS / name
    path.write_text(json.dumps(payload, indent=2, default=float), encoding="utf-8")
    return path
