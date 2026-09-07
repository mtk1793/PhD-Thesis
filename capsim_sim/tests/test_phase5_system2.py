import time
import numpy as np
import pytest

from capsm.agents.system2 import QIRLController
from capsm.agents.baselines import run_controller, NoControl, RuleBasedVoltage
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment


@pytest.fixture(scope="module")
def profiles():
    return load_opsd(start="2019-01-10", end="2019-01-14")


@pytest.fixture(scope="module")
def env(profiles):
    return QSTSEnvironment("case39", profiles)


# ── QIRL basic tests ───────────────────────────────────────────────

def test_qirl_act_returns_valid_controls(env):
    ctrl = QIRLController(seed=42)
    obs = env.reset(start="2019-01-10")
    controls = ctrl.act(obs, env)
    assert "facts" in controls
    assert "ev" in controls
    assert "SVC_14" in controls["facts"]
    assert "STATCOM_39" in controls["facts"]
    assert isinstance(controls["facts"]["UPFC_26"], list)


def test_qirl_within_device_limits(env):
    ctrl = QIRLController(seed=42)
    obs = env.reset(start="2019-01-10")
    controls = ctrl.act(obs, env)
    svc = controls["facts"]["SVC_14"]
    assert -0.5 - 1e-9 <= svc <= 0.5 + 1e-9
    statcom = controls["facts"]["STATCOM_39"]
    assert -1.0 - 1e-9 <= statcom <= 1.0 + 1e-9
    tcsc = controls["facts"]["TCSC_16_17"]
    assert 0.3 - 1e-9 <= tcsc <= 0.7 + 1e-9


def test_qirl_amplitude_update():
    ctrl = QIRLController(n_candidates=8, seed=42)
    rewards = np.array([1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
    ctrl._update_amplitudes(rewards)
    probs = np.abs(ctrl.amplitudes) ** 2
    assert probs.sum() == pytest.approx(1.0, abs=1e-6)
    assert probs[0] > probs[-1]


def test_qirl_tunnel_explores():
    ctrl = QIRLController(n_candidates=8, tunnel_rate=0.5, seed=42)
    orig = ctrl.candidates.copy()
    ctrl._tunnel()
    n_changed = np.sum(np.any(ctrl.candidates != orig, axis=1))
    assert n_changed >= 3


def test_qirl_converges(env):
    ctrl = QIRLController(seed=42)
    obs = env.reset(start="2019-01-10")
    controls = ctrl.act(obs, env)
    for _ in range(23):
        controls = ctrl.act(obs, env)
        obs = env.step(controls)
    assert obs["converged"]


def test_qirl_reset_clears(env):
    ctrl = QIRLController(seed=42)
    obs = env.reset(start="2019-01-10")
    ctrl.act(obs, env)
    ctrl.reset()
    probs = np.abs(ctrl.amplitudes) ** 2
    assert np.allclose(probs, 1.0 / ctrl.n_candidates)


def test_qirl_inference_time(env):
    ctrl = QIRLController(n_candidates=16, seed=42)
    obs = env.reset(start="2019-01-10")
    ctrl.act(obs, env)
    t0 = time.perf_counter()
    for _ in range(50):
        ctrl.act(obs, env)
    elapsed_ms = (time.perf_counter() - t0) * 1000 / 50
    assert elapsed_ms < 100.0, f"QIRL too slow: {elapsed_ms:.1f} ms"


def test_qirl_month_long(env):
    ctrl = QIRLController(n_candidates=16, seed=42)
    df = run_controller(env, ctrl, start="2019-01-10", n_steps=72)
    assert len(df) == 73
    assert df["converged"].all()
    assert df["voltage_deviation_pu"].mean() < 0.1


def test_qirl_vs_no_control(profiles):
    env1 = QSTSEnvironment("case39", profiles)
    ctrl = QIRLController(n_candidates=16, seed=42)
    df_qirl = run_controller(env1, ctrl, start="2019-01-10", n_steps=72)
    env2 = QSTSEnvironment("case39", profiles)
    df_none = run_controller(env2, NoControl(), start="2019-01-10", n_steps=72)
    assert df_qirl["voltage_deviation_pu"].mean() <= df_none["voltage_deviation_pu"].mean()
    assert df_qirl["n_voltage_violations"].sum() <= df_none["n_voltage_violations"].sum()
