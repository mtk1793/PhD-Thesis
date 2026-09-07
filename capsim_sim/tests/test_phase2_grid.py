import copy

import numpy as np
import pandas as pd
import pytest
from pypower.api import ppoption, runpf

from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment
from capsm.grid.events import apply_fdi, restore_branch, trip_branch
from capsm.grid.facts import SeriesCompensator, ShuntCompensator, default_facts


@pytest.fixture(scope="module")
def profiles_month():
    return load_opsd(start="2019-01-01", end="2019-01-31")


def _constant_profiles():
    idx = pd.date_range("2019-01-01", periods=24, freq="h", tz="UTC")
    df = pd.DataFrame({"load_actual_mw": 55492.0}, index=idx)
    df["wind_onshore_mw"] = 9581.5
    df["wind_offshore_mw"] = 1970.5
    df["solar_mw"] = 4566.0
    return df


def _env(profiles, case="case39", **kw):
    return QSTSEnvironment(case, profiles, **kw)


def test_first_step_converges_with_real_data(profiles_month):
    env = _env(profiles_month)
    obs = env.reset(start="2019-01-01")
    assert obs["converged"]
    assert obs["metrics"]["vm_min"] > 0.9
    assert 3000 < obs["total_load_mw"] < 9000


def test_matches_direct_pypower_when_profile_is_flat():
    env = QSTSEnvironment("case39", _constant_profiles(), regional=False,
                          wind_penetration=0.0, solar_penetration=0.0)
    obs = env.reset()
    base, _ = runpf(env.base_ppc, ppoption(VERBOSE=0, OUT_ALL=0))
    assert np.allclose(obs["vm"], base["bus"][:, 7], atol=1e-6)
    from pypower.idx_brch import PF, PT
    direct_losses = float(np.sum(base["branch"][:, PF] + base["branch"][:, PT]))
    assert abs(obs["metrics"]["losses_mw"] - direct_losses) < 1e-4


def test_svc_raises_local_voltage(profiles_month):
    env = _env(profiles_month)
    env.reset(start="2019-01-15")
    obs0 = env._solve(None)
    pos14 = int(np.flatnonzero(env.bus_ids == 14)[0])
    obs1 = env._solve({"facts": {"SVC_14": 0.5}})
    assert obs1["vm"][pos14] > obs0["vm"][pos14]


def test_tcsc_changes_branch_flow(profiles_month):
    env = _env(profiles_month)
    env.reset(start="2019-01-15")
    obs0 = env._solve(None)
    f = env.base_ppc["branch"][:, 0] == 16
    t = env.base_ppc["branch"][:, 1] == 17
    br = int(np.flatnonzero(f & t)[0])
    obs1 = env._solve({"facts": {"TCSC_16_17": 0.5}})
    assert abs(obs1["branch_pf"][br] - obs0["branch_pf"][br]) > 1e-6


def test_ev_dispatch_and_soc_bounds(profiles_month):
    env = _env(profiles_month)
    env.reset(start="2019-01-15")
    obs_c = env.step({"ev": {3: 40.0, 8: 40.0, 15: 40.0}})
    assert obs_c["ev_state"]["soc"][3] > 0.5
    obs_d = env.step({"ev": {3: -50.0, 8: -50.0, 15: -50.0}})
    assert obs_d["ev_state"]["p"][3] == -50.0
    for _ in range(20):
        obs_d = env.step({"ev": {3: -50.0, 8: -50.0, 15: -50.0}})
    assert obs_d["ev_state"]["soc"][3] >= 0.2 - 1e-9


def test_line_trip_and_restore(profiles_month):
    env = _env(profiles_month)
    env.reset(start="2019-01-15")
    obs0 = env._solve(None)
    env.trip_line(16, 17)
    obs1 = env._solve(None)
    assert obs1["converged"]
    assert not np.allclose(obs1["branch_pf"], obs0["branch_pf"])
    env.restore_line(16, 17)
    obs2 = env._solve(None)
    assert np.allclose(obs2["branch_pf"], obs0["branch_pf"], atol=1e-6)


def test_fdi_corrupts_only_targets(profiles_month):
    env = _env(profiles_month)
    obs = env.reset(start="2019-01-15")
    clean = obs["vm"].copy()
    bad = apply_fdi(obs, targets=[4, 14], bias=0.08, rng=np.random.default_rng(0))
    assert np.allclose(bad["vm"][[4, 14]], clean[[4, 14]] + 0.08, atol=0.01)
    others = [i for i in range(len(clean)) if i not in (4, 14)]
    assert np.allclose(bad["vm"][others], clean[others])
    assert bad["fdi_active"]


def test_qsts_run_produces_metrics_frame(profiles_month):
    env = _env(profiles_month)
    df = env.run(start="2019-01-01", n_steps=48)
    assert len(df) == 49
    assert df["converged"].all()
    assert (df["losses_mw"] > 0).all()
    assert "ev_soc_mean" in df.columns
