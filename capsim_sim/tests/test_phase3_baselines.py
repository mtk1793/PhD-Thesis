import numpy as np
import pytest

from capsm.agents.baselines import NoControl, PIDVoltage, RuleBasedVoltage, run_controller
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment
from capsm.grid.stability import loading_margin


@pytest.fixture(scope="module")
def profiles_week():
    return load_opsd(start="2019-01-10", end="2019-01-14")


def _env(profiles):
    return QSTSEnvironment("case39", profiles)


def test_rule_based_controls_within_device_limits(profiles_week):
    env = _env(profiles_week)
    ctrl = RuleBasedVoltage()
    env.reset(start="2019-01-10")
    obs = env._solve(None)
    controls = ctrl.act(obs, env)
    for name, value in controls["facts"].items():
        dev = next(d for d in env.facts if d.name == name)
        if isinstance(value, list):
            assert dev.shunt.b_min - 1e-9 <= value[0] <= dev.shunt.b_max + 1e-9
        elif hasattr(dev, "k_min"):
            assert dev.k_min - 1e-9 <= value <= dev.k_max + 1e-9
        else:
            assert dev.b_min - 1e-9 <= value <= dev.b_max + 1e-9


def test_rule_based_reduces_voltage_deviation(profiles_week):
    env = _env(profiles_week)
    df_none = run_controller(env, NoControl(), start="2019-01-10", n_steps=72)
    env2 = _env(profiles_week)
    df_rule = run_controller(env2, RuleBasedVoltage(), start="2019-01-10", n_steps=72)
    assert df_rule["voltage_deviation_pu"].mean() <= df_none["voltage_deviation_pu"].mean()
    assert df_rule["n_voltage_violations"].sum() <= df_none["n_voltage_violations"].sum()


def test_pid_keeps_integral_state_bounded(profiles_week):
    env = _env(profiles_week)
    ctrl = PIDVoltage()
    env.reset(start="2019-01-10")
    obs = env._solve(None)
    for _ in range(24):
        controls = ctrl.act(obs, env)
        obs = env.step(controls)
    for name, value in ctrl._integral.items():
        assert np.isfinite(value)
    assert obs["converged"]


def test_run_controller_returns_full_frame(profiles_week):
    env = _env(profiles_week)
    df = run_controller(env, NoControl(), start="2019-01-10", n_steps=48)
    assert len(df) == 49
    assert {"losses_mw", "vm_min", "total_gen_mw"} <= set(df.columns)
    assert df["converged"].all()


def test_loading_margin_reasonable(profiles_week):
    env = _env(profiles_week)
    env.reset(start="2019-01-12")
    lm = loading_margin(env)
    assert lm is not None
    assert 1.0 < lm <= 3.0
    assert env.curtailment_hours == 0


def test_loading_margin_lower_at_heavier_hour(profiles_week):
    env = _env(profiles_week)
    env.reset(start="2019-01-12")
    lm_valley = loading_margin(env)
    load_by_t = env.bus_loads.sum(axis=1)
    peak_t = int(np.argmax(load_by_t[:24].to_numpy()))
    env.t = peak_t
    env._solve(None)
    lm_peak = loading_margin(env)
    assert lm_peak < lm_valley
