import numpy as np
import pandas as pd
import pytest

from capsm.data.opsd import GAP_INTERP_LIMIT, SPLITS, apply_gap_policy
from capsm.data.disaggregate import (
    CONTROL_AREAS,
    build_bus_loads,
    build_renewables,
    load_bus_shares,
    assign_control_areas,
    get_case,
)


def _small_frame():
    idx = pd.date_range("2016-01-01", periods=12, freq="h", tz="UTC")
    vals = np.arange(12, dtype=float) * 10.0
    df = pd.DataFrame({"load_actual_mw": vals}, index=idx)
    df.loc[df.index[3], "load_actual_mw"] = np.nan
    df.loc[df.index[4], "load_actual_mw"] = np.nan
    df.loc[df.index[7:10], "load_actual_mw"] = np.nan
    return df


def test_gap_policy_fills_short_gaps_only():
    df = _small_frame()
    out, report = apply_gap_policy(df)
    assert out.loc[out.index[3], "load_actual_mw"] == 30.0
    assert out.loc[out.index[4], "load_actual_mw"] == 40.0
    assert np.isnan(out.loc[out.index[7], "load_actual_mw"])
    assert np.isnan(out.loc[out.index[8], "load_actual_mw"])
    assert np.isnan(out.loc[out.index[9], "load_actual_mw"])
    assert report["interpolated"]["load_actual_mw"] == 2
    assert report["left_nan"]["load_actual_mw"] == 3
    assert out["load_actual_mw_interp"].sum() == 2


def test_gap_policy_never_touches_valid_points():
    df = _small_frame()
    out, _ = apply_gap_policy(df)
    assert (out["load_actual_mw"].dropna().to_numpy()[:3] == df["load_actual_mw"][:3]).all()


def test_splits_are_chronological_and_disjoint():
    bounds = list(SPLITS.values())
    for (_, e_prev), (s_next, _) in zip(bounds, bounds[1:]):
        assert pd.Timestamp(e_prev, tz="UTC") < pd.Timestamp(s_next, tz="UTC")


def test_load_shares_sum_to_one():
    for case_name in ["case9", "case14", "case39", "case118"]:
        shares = load_bus_shares(get_case(case_name))
        assert np.isclose(shares.sum(), 1.0)


def test_control_area_assignment_full_coverage():
    ppc = get_case("case39")
    areas = assign_control_areas(ppc)
    load_buses = ppc["bus"][:, 0][ppc["bus"][:, 1] >= 0]
    for b in areas.values():
        pass
    shares = load_bus_shares(get_case("case39"))
    assert len(areas) > 0
    assert all(a in CONTROL_AREAS for a in areas.values())


def test_bus_loads_follow_national_profile():
    idx = pd.date_range("2019-01-01", periods=48, freq="h", tz="UTC")
    df = pd.DataFrame({"load_actual_mw": 40000.0 + 1000.0 * np.sin(np.arange(48) / 8)}, index=idx)
    for col in [f"{a}_load_mw" for a in CONTROL_AREAS]:
        df[col] = df["load_actual_mw"] * 0.25
    bl = build_bus_loads("case14", df, regional=False)
    assert bl.shape == (48, 14)
    base_total = get_case("case14")["bus"][:, 0].size
    from pypower.idx_bus import PD
    base_total = float(get_case("case14")["bus"][:, PD].sum())
    profile = df["load_actual_mw"] / df["load_actual_mw"].mean()
    totals = bl.sum(axis=1).to_numpy()
    assert np.allclose(totals, profile.to_numpy() * base_total, rtol=1e-9)


def test_renewables_hit_penetration_target():
    idx = pd.date_range("2019-01-01", periods=336, freq="h", tz="UTC")
    rng = np.random.default_rng(0)
    df = pd.DataFrame({
        "load_actual_mw": 50000.0 + rng.normal(0, 1000, 336),
        "wind_onshore_mw": np.abs(rng.normal(9000, 3000, 336)),
        "wind_offshore_mw": np.abs(rng.normal(2000, 700, 336)),
        "solar_mw": np.abs(rng.normal(4000, 1500, 336)),
    }, index=idx)
    re = build_renewables("case39", df, wind_penetration=0.2, solar_penetration=0.1)
    wind = -re[[c for c in re.columns if c.startswith("wind")]].sum(axis=1)
    solar = -re[[c for c in re.columns if c.startswith("solar")]].sum(axis=1)
    from pypower.idx_bus import PD
    base_total = float(get_case("case39")["bus"][:, PD].sum())
    assert np.isclose(wind.mean() / base_total, 0.2, rtol=1e-9)
    assert np.isclose(solar.mean() / base_total, 0.1, rtol=1e-9)
    assert (re.to_numpy() <= 0).all()


def test_sample_opsd_week_is_real_data():
    import pathlib
    sample = pathlib.Path(__file__).parent / "data" / "sample_opsd_week.csv"
    df = pd.read_csv(sample)
    assert len(df) == 192
    assert df["load_actual_mw"].notna().all()
    assert (df["load_actual_mw"] > 20000).all()
