"""Load and prepare the OPSD German time series for CAPSM experiments.

Reads the verified raw OPSD hourly file, selects the German national and
control-area series, applies a documented gap policy, and caches the result
as a parquet file for fast repeated access.

Gap policy: gaps of up to GAP_INTERP_LIMIT consecutive steps are filled by
time-based linear interpolation and flagged in a mask column; longer gaps
remain NaN and must be excluded from metric aggregation. No other values
are ever modified or synthesised.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
RAW_60MIN = DATA_DIR / "raw" / "time_series_60min_singleindex.csv"
CACHE = DATA_DIR / "processed" / "opsd_de_60min.parquet"

GAP_INTERP_LIMIT = 2

SPLITS = {
    "train": ("2015-01-01", "2017-12-31"),
    "val": ("2018-01-01", "2018-12-31"),
    "test": ("2019-01-01", "2020-09-30"),
}

PRICE_WINDOW = ("2018-09-30", "2020-09-30")

COLUMN_MAP = {
    "utc_timestamp": "timestamp",
    "DE_load_actual_entsoe_transparency": "load_actual_mw",
    "DE_load_forecast_entsoe_transparency": "load_forecast_mw",
    "DE_solar_generation_actual": "solar_mw",
    "DE_wind_onshore_generation_actual": "wind_onshore_mw",
    "DE_wind_offshore_generation_actual": "wind_offshore_mw",
    "DE_LU_price_day_ahead": "price_day_ahead_eur",
    "DE_50hertz_load_actual_entsoe_transparency": "ca_50hertz_load_mw",
    "DE_amprion_load_actual_entsoe_transparency": "ca_amprion_load_mw",
    "DE_tennet_load_actual_entsoe_transparency": "ca_tennet_load_mw",
    "DE_transnetbw_load_actual_entsoe_transparency": "ca_transnetbw_load_mw",
    "DE_50hertz_solar_generation_actual": "ca_50hertz_solar_mw",
    "DE_amprion_solar_generation_actual": "ca_amprion_solar_mw",
    "DE_tennet_solar_generation_actual": "ca_tennet_solar_mw",
    "DE_transnetbw_solar_generation_actual": "ca_transnetbw_solar_mw",
    "DE_50hertz_wind_generation_actual": "ca_50hertz_wind_mw",
    "DE_amprion_wind_onshore_generation_actual": "ca_amprion_wind_mw",
    "DE_tennet_wind_generation_actual": "ca_tennet_wind_mw",
    "DE_transnetbw_wind_onshore_generation_actual": "ca_transnetbw_wind_mw",
}


def _read_raw() -> pd.DataFrame:
    df = pd.read_csv(RAW_60MIN, usecols=list(COLUMN_MAP))
    df = df.rename(columns=COLUMN_MAP)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    return df.set_index("timestamp")


def _gap_runs_mask(s: pd.Series) -> pd.Series:
    isna = s.isna()
    run_id = (isna != isna.shift()).cumsum()
    run_len = isna.groupby(run_id).transform("sum")
    return isna & (run_len <= GAP_INTERP_LIMIT)


def apply_gap_policy(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    report = {"interpolated": {}, "left_nan": {}}
    out = df.copy()
    value_cols = [c for c in df.columns if not c.endswith("_interp")]
    for col in value_cols:
        short = _gap_runs_mask(df[col])
        n_short = int(short.sum())
        n_long = int(df[col].isna().sum()) - n_short
        if n_short:
            out.loc[short, col] = df[col].interpolate(method="time", limit=GAP_INTERP_LIMIT, limit_area="inside").loc[short]
        out[f"{col}_interp"] = short
        report["interpolated"][col] = n_short
        report["left_nan"][col] = n_long
    return out, report


def build_cache(force: bool = False) -> pd.DataFrame:
    if CACHE.exists() and not force:
        return pd.read_parquet(CACHE)
    df = _read_raw()
    df, _ = apply_gap_policy(df)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CACHE, index=True)
    return df


def load_opsd(
    start: str | None = None,
    end: str | None = None,
    split: str | None = None,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Load the processed OPSD hourly frame, optionally sliced by date or split."""
    df = build_cache()
    if split is not None:
        s, e = SPLITS[split]
        start, end = s, e
    if start is not None or end is not None:
        s = df.index.min() if start is None else pd.Timestamp(start, tz="UTC")
        e = df.index.max() if end is None else pd.Timestamp(end, tz="UTC")
        df = df.loc[s:e]
    if columns is not None:
        cols = list(columns) + [f"{c}_interp" for c in columns if f"{c}_interp" in df.columns]
        df = df[cols]
    return df


def mine_ramp_events(df: pd.DataFrame, top_n: int = 20, windows_h: tuple = (1, 3)) -> dict[int, pd.DataFrame]:
    """Find the largest real wind (+solar) ramps; used later as extreme-event scenarios."""
    total = df["wind_onshore_mw"].fillna(0) + df["wind_offshore_mw"].fillna(0) + df["solar_mw"].fillna(0)
    events = {}
    for w in windows_h:
        delta = total.diff(w)
        ramps = pd.DataFrame({
            "ramp_mw": delta,
            "level_start_mw": total.shift(w),
            "level_end_mw": total,
        }).dropna()
        top_up = ramps.nlargest(top_n, "ramp_mw").assign(direction="up")
        top_down = ramps.nsmallest(top_n, "ramp_mw").assign(direction="down")
        events[w] = pd.concat([top_up, top_down]).sort_values("ramp_mw", ascending=False)
    return events
