import time
import numpy as np
import torch
import pytest

from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.collector import collect_trajectory, _flatten_action
from capsm.agents.baselines import RuleBasedVoltage, NoControl
from capsm.agents.trainer import collect_demos, train_behavior_cloning
from capsm.data.opsd import load_opsd
from capsm.grid.environment import QSTSEnvironment


@pytest.fixture(scope="module")
def profiles():
    return load_opsd(start="2019-01-10", end="2019-01-14")


@pytest.fixture(scope="module")
def env(profiles):
    return QSTSEnvironment("case39", profiles)


@pytest.fixture(scope="module")
def encoder(env):
    return StateEncoder(env)


# ── State encoder tests ────────────────────────────────────────────

def test_encoder_shape(env, encoder):
    obs = env.reset(start="2019-01-10")
    raw = encoder.encode(obs)
    assert raw.dtype == np.float32
    assert raw.shape == (encoder.n_features,)


def test_encoder_deterministic(env, encoder):
    obs = env.reset(start="2019-01-10")
    v1 = encoder.encode(obs)
    v2 = encoder.encode(obs)
    np.testing.assert_array_equal(v1, v2)


# ── CNN-LSTM model tests ───────────────────────────────────────────

def test_model_forward_shape():
    model = CNNLSTM(n_features=160, n_actions=9)
    x = torch.randn(4, 12, 160)
    actions, hidden = model(x)
    assert actions.shape == (4, 9)
    assert hidden[0].shape == (1, 4, 128)


def test_model_forward_deterministic():
    model = CNNLSTM(n_features=160, n_actions=9)
    model.eval()
    x = torch.randn(2, 12, 160)
    a1, _ = model(x)
    a2, _ = model(x)
    torch.testing.assert_close(a1, a2)


def test_model_hidden_carry():
    model = CNNLSTM(n_features=160, n_actions=9)
    model.eval()
    x = torch.randn(1, 12, 160)
    a1, h1 = model(x)
    x2 = torch.randn(1, 12, 160)
    a2, h2 = model(x2, hidden=h1)
    assert a2.shape == (1, 9)
    assert not torch.allclose(h1[0], h2[0])


# ── System1Controller inference tests ──────────────────────────────

def test_controller_act_returns_valid_controls(env, encoder):
    model = CNNLSTM(encoder.n_features, 9)
    ctrl = System1Controller(model, encoder)
    obs = env.reset(start="2019-01-10")
    controls = ctrl.act(obs, env)
    assert "facts" in controls
    assert "SVC_14" in controls["facts"]
    assert "STATCOM_39" in controls["facts"]
    assert "UPFC_26" in controls["facts"]
    assert isinstance(controls["facts"]["UPFC_26"], list)


def test_controller_within_device_limits(env, encoder):
    model = CNNLSTM(encoder.n_features, 9)
    ctrl = System1Controller(model, encoder)
    obs = env.reset(start="2019-01-10")
    controls = ctrl.act(obs, env)
    svc = controls["facts"]["SVC_14"]
    assert -0.5 - 1e-9 <= svc <= 0.5 + 1e-9
    statcom = controls["facts"]["STATCOM_39"]
    assert -1.0 - 1e-9 <= statcom <= 1.0 + 1e-9
    tcsc = controls["facts"]["TCSC_16_17"]
    assert 0.3 - 1e-9 <= tcsc <= 0.7 + 1e-9


def test_controller_inference_time(env, encoder):
    model = CNNLSTM(encoder.n_features, 9)
    ctrl = System1Controller(model, encoder)
    obs = env.reset(start="2019-01-10")
    ctrl.act(obs, env)
    t0 = time.perf_counter()
    for _ in range(100):
        ctrl.act(obs, env)
    elapsed_ms = (time.perf_counter() - t0) * 1000 / 100
    assert elapsed_ms < 20.0, f"Inference too slow: {elapsed_ms:.1f} ms"
    ctrl.reset()


def test_controller_reset_clears_state(env, encoder):
    model = CNNLSTM(encoder.n_features, 9)
    ctrl = System1Controller(model, encoder)
    obs = env.reset(start="2019-01-10")
    ctrl.act(obs, env)
    assert len(ctrl._window) > 0
    ctrl.reset()
    assert len(ctrl._window) == 0
    assert ctrl._hidden is None


# ── Trajectory collection tests ────────────────────────────────────

def test_collect_trajectory_shapes(env, encoder):
    ctrl = RuleBasedVoltage()
    traj = collect_trajectory(env, ctrl, encoder, start="2019-01-10", n_steps=24)
    assert traj["states"].shape == (24, encoder.n_features)
    assert traj["actions"].shape == (24, 9)
    assert traj["rewards"].shape == (24,)


def test_flatten_action():
    ctrl = {"facts": {"SVC_14": 0.1, "STATCOM_39": -0.2, "TCSC_16_17": 0.5,
                       "UPFC_26": [0.3, -0.1]}, "ev": {"3": 10.0, "8": -5.0, "15": 0.0}}
    a = _flatten_action(ctrl)
    assert a.shape == (9,)
    assert a[0] == pytest.approx(0.1)
    assert a[1] == pytest.approx(-0.2)
    assert a[2] == pytest.approx(0.5)
    assert a[3] == pytest.approx(0.3)
    assert a[6] == pytest.approx(10.0)


# ── Behavior cloning training tests ────────────────────────────────

def test_behavior_cloning_reduces_loss(profiles):
    env = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env)
    trajs, _ = collect_demos("case39", profiles, n_episodes=2, steps_per_episode=48)
    model = train_behavior_cloning(trajs, encoder.n_features, 9, epochs=20,
                                   batch_size=32, verbose=False)
    assert model is not None
    ctrl = System1Controller(model, encoder)
    obs = env.reset(start="2019-01-10")
    controls = ctrl.act(obs, env)
    assert "facts" in controls


def test_trained_model_converges(profiles):
    env = QSTSEnvironment("case39", profiles)
    encoder = StateEncoder(env)
    trajs, _ = collect_demos("case39", profiles, n_episodes=1, steps_per_episode=48)
    model = train_behavior_cloning(trajs, encoder.n_features, 9, epochs=10,
                                   batch_size=32, verbose=False)
    ctrl = System1Controller(model, encoder)
    obs = env.reset(start="2019-01-10")
    ctrl.act(obs, env)
    for _ in range(23):
        controls = ctrl.act(obs, env)
        obs = env.step(controls)
    assert obs["converged"]
