"""Disaggregate German national OPSD series onto IEEE test-system buses.

Modelling assumptions (documented for the thesis):
- Each IEEE test system's total load follows the real German national load
  profile; bus-level loads scale proportionally to their base-case Pd share.
- Optionally, load buses are grouped into four regions that follow the real
  control-area profiles (50Hertz, Amprion, TenneT, TransnetBW), with group
  sizes matching each control area's real mean share of national load.
- Wind and solar injections follow the real German generation profiles,
  scaled so their long-run mean equals a configurable share of mean load
  (renewable penetration), and placed at designated buses as negative load.
"""

import importlib

import numpy as np
import pandas as pd
from pypower.idx_bus import PD

CONTROL_AREAS = ["ca_50hertz", "ca_amprion", "ca_tennet", "ca_transnetbw"]

CONTROL_AREA_SHARES = {
    "ca_50hertz": 10404.5,
    "ca_amprion": 20943.0,
    "ca_tennet": 17184.7,
    "ca_transnetbw": 6960.5,
}

RENEWABLE_SITES = {
    "case9": {"wind": [7], "solar": [9]},
    "case14": {"wind": [4, 9], "solar": [6, 13]},
    "case39": {"wind": [4, 14], "solar": [8, 15]},
    "case118": {"wind": [10, 25, 49], "solar": [12, 34, 71]},
    "case300": {"wind": [17, 57, 121], "solar": [33, 90, 195]},
}


def get_case(case_name: str) -> dict:
    mod = importlib.import_module(f"pypower.{case_name}")
    return getattr(mod, case_name)()


def load_bus_shares(ppc: dict) -> np.ndarray:
    pd_vec = ppc["bus"][:, PD].copy()
    total = pd_vec.sum()
    return pd_vec / total


def assign_control_areas(ppc: dict) -> dict[int, str]:
    """Group load buses (Pd > 0) into four regions matching real area shares."""
    load_buses = sorted(ppc["bus"][:, 0][ppc["bus"][:, PD] > 0].astype(int).tolist())
    n = len(load_buses)
    weights = np.array([CONTROL_AREA_SHARES[a] for a in CONTROL_AREAS])
    weights = weights / weights.sum()
    counts = np.maximum(1, np.round(weights * n).astype(int))
    counts[-1] = n - counts[:-1].sum()
    areas = {}
    i = 0
    for area, c in zip(CONTROL_AREAS, counts):
        for bus in load_buses[i : i + c]:
            areas[bus] = area
        i += c
    return areas


def build_bus_loads(case_name: str, df: pd.DataFrame, regional: bool = True) -> pd.DataFrame:
    """Per-bus active load [MW] for every timestamp.

    The shape follows the real German profiles; the magnitude keeps the test
    case's native total base load so power-flow behaviour stays within the
    case's designed operating range.
    regional=False: all buses follow the national profile.
    regional=True: bus groups follow their control-area profile.
    """
    ppc = get_case(case_name)
    buses = ppc["bus"][:, 0].astype(int)
    base = ppc["bus"][:, PD]
    if regional:
        areas = assign_control_areas(ppc)
        mat = np.zeros((len(df), len(buses)))
        for area in CONTROL_AREAS:
            profile = (df[f"{area}_load_mw"] / df[f"{area}_load_mw"].mean()).to_numpy()
            idx = np.array([areas.get(b) == area for b in buses])
            mat[:, idx] = np.outer(profile, base[idx])
        return pd.DataFrame(mat, index=df.index, columns=[f"bus_{b}" for b in buses])
    profile = (df["load_actual_mw"] / df["load_actual_mw"].mean()).to_numpy()
    out = pd.DataFrame(np.outer(profile, base), index=df.index, columns=[f"bus_{b}" for b in buses])
    return out


def build_renewables(
    case_name: str,
    df: pd.DataFrame,
    wind_penetration: float = 0.20,
    solar_penetration: float = 0.10,
) -> pd.DataFrame:
    """Wind and solar injections [MW] at designated buses (negative-load form).

    Shape follows the real German generation profiles; magnitude is set so
    the long-run mean equals penetration x the case's native mean load.
    """
    sites = RENEWABLE_SITES[case_name]
    ppc = get_case(case_name)
    mean_load = float(ppc["bus"][:, PD].sum())
    wind_total = df["wind_onshore_mw"] + df["wind_offshore_mw"]
    wind_profile = wind_total / wind_total.mean()
    solar_profile = df["solar_mw"] / df["solar_mw"].mean()
    out = pd.DataFrame(index=df.index)
    n_wind = len(sites["wind"])
    n_solar = len(sites["solar"])
    for b in sites["wind"]:
        out[f"wind_bus_{b}"] = -wind_profile * (wind_penetration * mean_load) / n_wind
    for b in sites["solar"]:
        out[f"solar_bus_{b}"] = -solar_profile * (solar_penetration * mean_load) / n_solar
    return out


def penetration_summary(case_name: str, df: pd.DataFrame, wind_penetration: float, solar_penetration: float) -> dict:
    ppc = get_case(case_name)
    mean_load = float(ppc["bus"][:, PD].sum())
    re = build_renewables(case_name, df, wind_penetration, solar_penetration)
    wind = -re[[c for c in re.columns if c.startswith("wind")]].sum(axis=1)
    solar = -re[[c for c in re.columns if c.startswith("solar")]].sum(axis=1)
    return {
        "case": case_name,
        "native_base_load_mw": mean_load,
        "mean_wind_mw": float(wind.mean()),
        "mean_solar_mw": float(solar.mean()),
        "wind_penetration": float(wind.mean() / mean_load),
        "solar_penetration": float(solar.mean() / mean_load),
        "max_renewable_share": float(((wind + solar) / mean_load).max()),
    }
