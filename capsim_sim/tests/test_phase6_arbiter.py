import numpy as np
import pytest

from capsm.agents.arbiter import MetacognitiveArbiter
from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.system2 import QIRLController
from capsm.agents.baselines import run_controller, NoControl
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment


@pytest.fixture(scope="module")
def profiles():
    return load_opsd(start="2019-01-10", end="2019-01-14")


@pytest.fixture(scope="module")
def env(profiles):
    return QSTSEnvironment("case39", profiles)


@pytest.fixture(scope="module")
def arbiter(env):
    encoder = StateEncoder(env)
    model = CNNLSTM(encoder.n_features, 9)
    s1 = System1Controller(model, encoder)
    s2 = QIRLController(n_candidates=8, seed=42)
    return MetacognitiveArbiter(s1, s2, threshold=0.03)


# ── Arbiter basic tests ────────────────────────────────────────────

def test_arbiter_act_returns_valid_controls(arbiter, env):
    obs = env.reset(start="2019-01-10")
    controls = arbiter.act(obs, env)
    assert "facts" in controls
    assert "ev" in controls
    assert "SVC_14" in controls["facts"]
    assert isinstance(controls["facts"]["UPFC_26"], list)


def test_arbiter_within_device_limits(arbiter, env):
    obs = env.reset(start="2019-01-10")
    controls = arbiter.act(obs, env)
    svc = controls["facts"]["SVC_14"]
    assert -0.5 - 1e-9 <= svc <= 0.5 + 1e-9
    statcom = controls["facts"]["STATCOM_39"]
    assert -1.0 - 1e-9 <= statcom <= 1.0 + 1e-9


def test_arbiter_alpha_stable_system(arbiter, env):
    obs = env.reset(start="2019-01-10")
    alpha = arbiter._compute_alpha(obs)
    assert 0.0 <= alpha <= 1.0


def test_arbiter_alpha_stressed_system(arbiter, env):
    obs = env.reset(start="2019-01-10")
    vm = obs["vm"].copy()
    vm[:] = 0.92
    obs_stressed = dict(obs, vm=vm)
    alpha = arbiter._compute_alpha(obs_stressed)
    assert alpha < 0.5


def test_arbiter_alpha_history(arbiter, env):
    arbiter.reset()
    obs = env.reset(start="2019-01-10")
    for _ in range(5):
        arbiter.act(obs, env)
    assert len(arbiter.alpha_history) == 5


def test_arbiter_converges(arbiter, env):
    arbiter.reset()
    obs = env.reset(start="2019-01-10")
    controls = arbiter.act(obs, env)
    for _ in range(23):
        controls = arbiter.act(obs, env)
        obs = env.step(controls)
    assert obs["converged"]


def test_arbiter_month_long(profiles):
    env = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env)
    model = CNNLSTM(encoder.n_features, 9)
    s1 = System1Controller(model, encoder)
    s2 = QIRLController(n_candidates=8, seed=42)
    arb = MetacognitiveArbiter(s1, s2, threshold=0.03)
    df = run_controller(env, arb, start="2019-01-10", n_steps=72)
    assert len(df) == 73
    assert df["converged"].all()
    assert df["voltage_deviation_pu"].mean() < 0.1


def test_arbiter_vs_no_control(profiles):
    env1 = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env1)
    model = CNNLSTM(encoder.n_features, 9)
    s1 = System1Controller(model, encoder)
    s2 = QIRLController(n_candidates=8, seed=42)
    arb = MetacognitiveArbiter(s1, s2, threshold=0.03)
    df_arb = run_controller(env1, arb, start="2019-01-10", n_steps=72)
    env2 = QSTSEnvironment("case39", profiles)
    df_none = run_controller(env2, NoControl(), start="2019-01-10", n_steps=72)
    assert df_arb["voltage_deviation_pu"].mean() <= df_none["voltage_deviation_pu"].mean()
    assert df_arb["n_voltage_violations"].sum() <= df_none["n_voltage_violations"].sum()
