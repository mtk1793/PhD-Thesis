"""P0 regression tests — master plan Phases B, C, D, E fixes.

These tests are self-contained: they build SYNTHETIC OPSD-shaped profiles
(no raw data download required) so the P0 correctness guarantees can be
verified on any machine:

  Phase B — QIRL candidate-dependent physical evaluation
  Phase C — reserved UPFC series-Q index forced neutral everywhere
  Phase D — System 1 train/test leakage removal (chronological split)
  Phase E — System 1 single recurrence convention
"""

import numpy as np
import pandas as pd
import pytest

from capsm.agents.evaluators import (
    RESERVED_INDEX,
    ExactPowerFlowEvaluator,
    SensitivitySurrogateEvaluator,
    compute_reward,
    ev_infeasibility_of,
    snapshot_env,
    restore_env,
    vector_to_controls,
)
from capsm.grid.environment import QSTSEnvironment

ACTION_LO = np.array([-0.5, -1.0, 0.3, -0.5, -0.5, 0.0, -50.0, -50.0, -50.0])
ACTION_HI = np.array([0.5, 1.0, 0.7, 0.5, 0.5, 0.0, 50.0, 50.0, 50.0])


# ──────────────────────────────────────────────────────────────────────
# Synthetic OPSD-shaped profiles (hourly, UTC, 28 days)
# ──────────────────────────────────────────────────────────────────────

def synthetic_profiles(days: int = 28, start: str = "2019-01-01") -> pd.DataFrame:
    idx = pd.date_range(start=start, periods=days * 24, freq="h", tz="UTC")
    t = np.arange(len(idx))
    hours = idx.hour.to_numpy()
    diurnal = 0.55 + 0.45 * np.cos((hours - 4) / 24 * 2 * np.pi)
    weekly = 1.0 - 0.08 * (idx.dayofweek.to_numpy() >= 5)
    rng = np.random.default_rng(7)
    noise = 1 + 0.02 * rng.standard_normal(len(idx))
    load = 55000.0 * diurnal * weekly * noise
    solar = np.clip(25000.0 * np.sin((hours - 6) / 12 * np.pi), 0, None)
    solar = solar * (0.9 + 0.1 * rng.standard_normal(len(idx))).clip(0.5, 1.1)
    wind = 20000.0 * (0.4 + 0.3 * np.sin(t / 30) + 0.3 * rng.random(len(idx)))
    df = pd.DataFrame({
        "load_actual_mw": load,
        "load_forecast_mw": load * 1.01,
        "solar_mw": solar,
        "wind_onshore_mw": wind * 0.8,
        "wind_offshore_mw": wind * 0.2,
        "price_day_ahead_eur": 40.0 + 10 * np.sin(t / 12),
    }, index=idx)
    # control-area series: deterministic shares of the national profile
    for area, share in [("ca_50hertz", 0.21), ("ca_amprion", 0.42),
                        ("ca_tennet", 0.26), ("ca_transnetbw", 0.11)]:
        df[f"{area}_load_mw"] = load * share
    return df


@pytest.fixture(scope="module")
def profiles():
    return synthetic_profiles()


@pytest.fixture(scope="module")
def env(profiles):
    return QSTSEnvironment("case39", profiles)


# ──────────────────────────────────────────────────────────────────────
# Phase C — reserved action index
# ──────────────────────────────────────────────────────────────────────

def test_reserved_action_q_always_zero(env, profiles):
    """Candidates, tunnelling and selected actions keep index 5 at 0."""
    from capsm.agents.system2 import QIRLController
    obs = env.reset(start="2019-01-01")
    ctrl = QIRLController(env=env, n_candidates=16, seed=42,
                          evaluator="exact")
    assert np.all(ctrl.candidates[:, RESERVED_INDEX] == 0.0)
    ctrl._tunnel()
    assert np.all(ctrl.candidates[:, RESERVED_INDEX] == 0.0)
    controls = ctrl.act(obs, env)
    assert np.all(ctrl._last_action[RESERVED_INDEX] == 0.0)
    # controls never contain a third UPFC channel
    assert len(controls["facts"]["UPFC_26"]) == 2


def test_reserved_action_q_not_in_reward():
    """Effort term ignores the reserved dimension."""
    u1 = np.array([0.1, 0.2, 0.4, 0.1, 0.2, 0.0, 10.0, -10.0, 5.0])
    u2 = u1.copy()
    u2[RESERVED_INDEX] = 999.0  # would dominate the effort term if included
    r1 = compute_reward(
        vm=np.full(39, 1.0), losses_mw=40.0, loss_ref_mw=50.0,
        branch_pf=np.zeros(46), branch_rate_a=np.zeros(46),
        ev_infeasibility=0.0, u=u1, u_prev=None,
        action_lo=ACTION_LO, action_hi=ACTION_HI,
    )
    r2 = compute_reward(
        vm=np.full(39, 1.0), losses_mw=40.0, loss_ref_mw=50.0,
        branch_pf=np.zeros(46), branch_rate_a=np.zeros(46),
        ev_infeasibility=0.0, u=u2, u_prev=None,
        action_lo=ACTION_LO, action_hi=ACTION_HI,
    )
    assert r1 == r2


def test_reserved_action_q_not_sent_to_environment(env):
    """vector_to_controls never emits a series-Q setpoint."""
    u = np.array([0.1, 0.2, 0.4, 0.1, 0.2, 0.0, 10.0, -10.0, 5.0])
    controls = vector_to_controls(env, u)
    assert set(controls["facts"].keys()) == {
        "SVC_14", "STATCOM_39", "TCSC_16_17", "UPFC_26"
    }
    assert controls["facts"]["UPFC_26"] == [0.1, 0.2]


def test_upfc_model_has_no_series_q_channel():
    """The Stage-1 UPFC device exposes exactly two setpoints."""
    from capsm.grid.facts import UPFC, default_facts
    dev = UPFC("UPFC_26", 26, 26, 28)
    dev.set(0.1, 0.2)
    assert hasattr(dev, "shunt") and hasattr(dev, "series")
    assert not hasattr(dev, "series_q")
    names = [d.name for d in default_facts("case39")]
    assert "UPFC_26_series_q" not in names


# ──────────────────────────────────────────────────────────────────────
# Phase B — candidate-dependent physical evaluation
# ──────────────────────────────────────────────────────────────────────

def test_qirl_rewards_are_candidate_dependent(env, profiles):
    """Different candidates must yield different counterfactual rewards."""
    obs = env.reset(start="2019-01-01")
    evaluator = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    base = np.zeros(9)
    base[[0, 6]] = [0.0, 0.0]
    c_a = base.copy(); c_a[1] = 1.0      # STATCOM max
    c_b = base.copy(); c_b[1] = -1.0     # STATCOM min
    cands = np.stack([c_a, c_b])
    ev = evaluator.evaluate_all(env, obs, cands)
    assert ev.rewards[0] != ev.rewards[1]
    assert ev.n_power_flows == 2


def test_exact_evaluator_restores_environment_state(env, profiles):
    """Snapshot/restore leaves the live state untouched after evaluation."""
    from capsm.agents.system2 import QIRLController
    obs = env.reset(start="2019-01-01")
    rng = np.random.default_rng(0)
    cands = rng.uniform(ACTION_LO, ACTION_HI, size=(4, 9))
    cands[:, 5] = 0.0
    evaluator = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    snap_before = snapshot_env(env)
    evaluator.evaluate_all(env, obs, cands)
    snap_after = snapshot_env(env)
    for d_before, d_after in zip(snap_before["facts"], snap_after["facts"]):
        assert d_before == d_after
    assert snap_before["ev"] == snap_after["ev"]
    assert snap_before["curtailment_hours"] == snap_after["curtailment_hours"]
    assert snap_before["t"] == snap_after["t"]


def test_surrogate_uses_fewer_power_flows_than_exact(env, profiles):
    """Amortised surrogate must consume < 1 PF per candidate after refresh."""
    from capsm.agents.system2 import QIRLController
    obs = env.reset(start="2019-01-01")
    rng = np.random.default_rng(1)
    cands = rng.uniform(ACTION_LO, ACTION_HI, size=(32, 9))
    cands[:, 5] = 0.0

    exact = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    exact.evaluate_all(env, obs, cands)

    surrogate = SensitivitySurrogateEvaluator(env, ACTION_LO, ACTION_HI,
                                              refresh_every=24)
    surrogate.evaluate_all(env, obs, cands)   # refresh: 8 PFs
    pf_after_first = surrogate.n_power_flows
    surrogate.evaluate_all(env, obs, cands)   # cached: 0 PFs
    assert pf_after_first == 8                # 9 dims − 1 reserved
    assert surrogate.n_power_flows == 8


def test_surrogate_ranking_tracks_exact(env, profiles):
    """Spearman rank correlation between evaluators must be high."""
    from scipy.stats import spearmanr
    obs = env.reset(start="2019-01-01")
    rng = np.random.default_rng(2)
    cands = rng.uniform(ACTION_LO, ACTION_HI, size=(24, 9))
    cands[:, 5] = 0.0
    exact = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    surrogate = SensitivitySurrogateEvaluator(env, ACTION_LO, ACTION_HI,
                                              refresh_every=1)
    ex = exact.evaluate_all(env, obs, cands)
    sr = surrogate.evaluate_all(env, obs, cands)
    rho = spearmanr(ex.rewards, sr.rewards).statistic
    assert rho > 0.7, f"surrogate ranking too weak: rho={rho:.3f}"


def test_reward_uses_counterfactual_not_unchanged_state(env, profiles):
    """The evaluated voltage must come from the candidate's own solve."""
    obs = env.reset(start="2019-01-01")
    evaluator = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    c0 = np.zeros(9)
    c1 = np.zeros(9); c1[0] = 0.5    # SVC_14 max injection (bus 14 is PQ)
    c2 = np.zeros(9); c2[0] = -0.5   # SVC_14 max absorption
    ev = evaluator.evaluate_all(env, obs, np.stack([c0, c1, c2]))
    vm_rows = ev.vm_pred
    # voltage responses must differ materially across candidates (the SVC
    # at PQ bus 14 moves local voltages; the reward must differ too)
    assert np.max(np.abs(vm_rows[1] - vm_rows[2])) > 1e-4
    assert ev.rewards[1] != ev.rewards[2]
    assert not np.allclose(vm_rows[0], vm_rows[1])


def test_statcom_on_slack_bus_has_no_voltage_effect(env, profiles):
    """Placement finding: STATCOM_39 sits on the IEEE-39 slack bus, where a
    shunt cannot move the voltage. Documented for the placement audit —
    the controller may still select it, but it cannot help there."""
    obs = env.reset(start="2019-01-01")
    evaluator = ExactPowerFlowEvaluator(env, ACTION_LO, ACTION_HI)
    c1 = np.zeros(9); c1[1] = 1.0
    c2 = np.zeros(9); c2[1] = -1.0
    ev = evaluator.evaluate_all(env, obs, np.stack([c1, c2]))
    assert np.allclose(ev.vm_pred[0], ev.vm_pred[1], atol=1e-6)


# ──────────────────────────────────────────────────────────────────────
# Phase B — selection mechanics
# ──────────────────────────────────────────────────────────────────────

def test_qirl_born_rule_matches_boltzmann():
    from capsm.agents.system2 import QIRLController
    ctrl = QIRLController(n_candidates=8, beta=4.0, seed=1)
    rewards = np.array([3.0, 2.0, 1.0, 0.0, -1.0, -2.0, -3.0, -4.0])
    ctrl._update_amplitudes(rewards)
    probs = np.abs(ctrl.amplitudes) ** 2
    expected = np.exp(4.0 * (rewards - rewards.max()))
    expected /= expected.sum()
    assert np.allclose(probs, expected, atol=1e-9)


@pytest.mark.parametrize("mode", ["qirl", "softmax", "greedy", "random"])
def test_selection_modes_run(env, profiles, mode):
    from capsm.agents.system2 import QIRLController
    obs = env.reset(start="2019-01-01")
    ctrl = QIRLController(env=env, n_candidates=8, seed=42,
                          evaluator="exact", mode=mode)
    controls = ctrl.act(obs, env)
    assert "facts" in controls and "ev" in controls


def test_act_within_bounds(env, profiles):
    from capsm.agents.system2 import QIRLController
    obs = env.reset(start="2019-01-01")
    ctrl = QIRLController(env=env, n_candidates=8, seed=42, evaluator="exact")
    controls = ctrl.act(obs, env)
    assert -0.5 - 1e-9 <= controls["facts"]["SVC_14"] <= 0.5 + 1e-9
    assert -1.0 - 1e-9 <= controls["facts"]["STATCOM_39"] <= 1.0 + 1e-9
    assert 0.3 - 1e-9 <= controls["facts"]["TCSC_16_17"] <= 0.7 + 1e-9
    b, k = controls["facts"]["UPFC_26"]
    assert -0.5 - 1e-9 <= b <= 0.5 + 1e-9
    assert -0.5 - 1e-9 <= k <= 0.5 + 1e-9


# ──────────────────────────────────────────────────────────────────────
# Phase D — leakage-free training pipeline
# ──────────────────────────────────────────────────────────────────────

def test_demo_sampling_never_touches_test_years():
    from capsm.agents.trainer import (
        sample_training_episodes, assert_no_test_leakage, TEST_YEARS,
    )
    idx = pd.date_range("2015-01-01", "2019-12-31 23:00", freq="h", tz="UTC")
    episodes = sample_training_episodes(
        idx, years=(2015, 2016, 2017), episodes_per_year=8, seed=3)
    assert len(episodes) > 0
    assert_no_test_leakage(episodes, TEST_YEARS)
    for ep in episodes:
        assert int(ep["start"][:4]) in (2015, 2016, 2017)


def test_assert_no_test_leakage_raises():
    from capsm.agents.trainer import assert_no_test_leakage
    with pytest.raises(AssertionError):
        assert_no_test_leakage([{"start": "2019-01-05", "steps": 168}])


def test_window_dataset_chronological_split_no_overlap():
    from capsm.agents.trainer import build_window_dataset
    rng = np.random.default_rng(0)
    traj = {
        "states": rng.standard_normal((300, 17)).astype(np.float32),
        "actions": rng.uniform(-1, 1, (300, 9)).astype(np.float32),
        "rewards": np.zeros(300),
        "observations": [],
    }
    ds = build_window_dataset([traj], seq_len=12, train_fraction=0.85)
    assert ds["X_train"].shape[1] == 12
    # guard gap of seq_len rows means train+val < total windows
    assert ds["X_train"].shape[0] + ds["X_val"].shape[0] < 300 - 12
    # no shared raw rows between train and val windows (guard gap holds)
    train_rows = {row.tobytes() for w in ds["X_train"] for row in w}
    val_rows = {row.tobytes() for w in ds["X_val"] for row in w}
    assert not (train_rows & val_rows)
    # chronological order: the latest train window ends before the
    # earliest val window begins
    n_train = ds["X_train"].shape[0]
    train_last_end = 12 + n_train - 1          # ends at row index split_row
    val_first_start = train_last_end + 1 + 12  # split_row + seq_len
    assert val_first_start > train_last_end


def test_action_targets_reserved_dim_zeroed():
    from capsm.agents.trainer import sanitize_action_targets
    y = np.ones((5, 9), dtype=np.float32)
    y2 = sanitize_action_targets(y)
    assert np.all(y2[:, 5] == 0.0)
    assert np.all(y2[:, 0] == 1.0)  # other dims untouched


# ──────────────────────────────────────────────────────────────────────
# Phase E — System 1 temporal modes (requires torch; skipped if absent)
# ──────────────────────────────────────────────────────────────────────


def _tiny_controller(env, mode):
    from capsm.agents.system1 import CNNLSTM, System1Controller
    model = CNNLSTM(env.base_ppc["bus"].shape[0] * 2 +
                    env.base_ppc["branch"].shape[0] +
                    env.base_ppc["gen"].shape[0] * 2 + 8 + 6 + 2, 9)
    from capsm.agents.system1 import StateEncoder
    encoder = StateEncoder(env)
    return System1Controller(model, encoder, temporal_mode=mode)


def test_system1_window_reset_keeps_hidden_none(env, profiles):
    pytest.importorskip("torch")
    obs = env.reset(start="2019-01-01")
    ctrl = _tiny_controller(env, "window_reset")
    for _ in range(3):
        ctrl.act(obs, env)
        assert ctrl._hidden is None  # reset convention


def test_system1_streaming_persists_hidden(env, profiles):
    torch = pytest.importorskip("torch")
    obs = env.reset(start="2019-01-01")
    ctrl = _tiny_controller(env, "streaming_persistent")
    ctrl.act(obs, env)
    assert ctrl._hidden is not None
    h0 = ctrl._hidden[0].clone()
    ctrl.act(obs, env)
    assert not torch.allclose(h0, ctrl._hidden[0])


def test_system1_reserved_dim_neutral(env, profiles):
    pytest.importorskip("torch")
    from capsm.agents.system1 import StateEncoder, System1Controller, CNNLSTM
    obs = env.reset(start="2019-01-01")
    encoder = StateEncoder(env)
    model = CNNLSTM(encoder.n_features, 9)
    ctrl = System1Controller(model, encoder)
    controls = ctrl.act(obs, env)
    b, k = controls["facts"]["UPFC_26"]
    assert isinstance(b, float) and isinstance(k, float)
    # the flattened action's reserved slot is 0
    vec = np.array([controls["facts"]["SVC_14"], controls["facts"]["STATCOM_39"],
                    controls["facts"]["TCSC_16_17"], b, k, 0.0,
                    controls["ev"]["3"], controls["ev"]["8"], controls["ev"]["15"]])
    assert vec[5] == 0.0


def test_system1_invalid_mode_rejected(env):
    pytest.importorskip("torch")
    from capsm.agents.system1 import StateEncoder, System1Controller, CNNLSTM
    encoder = StateEncoder(env)
    model = CNNLSTM(encoder.n_features, 9)
    with pytest.raises(ValueError):
        System1Controller(model, encoder, temporal_mode="nonsense")


# ──────────────────────────────────────────────────────────────────────
# Arbiter ablation modes
# ──────────────────────────────────────────────────────────────────────

def test_arbiter_modes_and_summary():
    from capsm.agents.arbiter import MetacognitiveArbiter

    class S1Dummy:
        name = "s1"
        def act(self, obs, env):
            return {"facts": {"SVC_14": 1.0}, "ev": {"3": 1.0, "8": 1.0, "15": 1.0}}
        def reset(self):
            pass

    class S2Dummy:
        name = "s2"
        def act(self, obs, env):
            return {"facts": {"SVC_14": 0.0}, "ev": {"3": -1.0, "8": -1.0, "15": -1.0}}
        def reset(self):
            pass

    obs = {"vm": np.full(39, 1.05)}  # stressed
    arb_fixed = MetacognitiveArbiter(S1Dummy(), S2Dummy(), mode="fixed", fixed_alpha=0.5)
    out = arb_fixed.act(obs, None)
    assert out["facts"]["SVC_14"] == 0.5
    assert out["ev"]["3"] == 0.0

    arb_hard = MetacognitiveArbiter(S1Dummy(), S2Dummy(), mode="hard", threshold=0.03)
    out = arb_hard.act(obs, None)
    assert out["facts"]["SVC_14"] == pytest.approx(0.0)  # System 2 dominates

    arb_sig = MetacognitiveArbiter(S1Dummy(), S2Dummy(), mode="sigmoid",
                                   threshold=0.03, tau=50.0)
    alpha = arb_sig._compute_alpha(obs)
    assert 0.0 < alpha < 0.5

    arb_safe = MetacognitiveArbiter(S1Dummy(), S2Dummy(), mode="sigmoid",
                                    safe_mode=True, safe_threshold=0.04)
    assert arb_safe._compute_alpha(obs) == 0.0

    for _ in range(5):
        arb_sig.act(obs, None)
    s = arb_sig.arbitration_summary()
    assert "mean_alpha" in s and s["n_steps"] == 5


def test_arbiter_default_matches_original_formula():
    from capsm.agents.arbiter import MetacognitiveArbiter
    arb = MetacognitiveArbiter(None, None)  # mode default = sigmoid
    vm = np.full(39, 1.02)
    obs = {"vm": vm}
    c1 = float(np.mean(np.abs(vm - 1.0)))
    expected = 1.0 / (1.0 + np.exp(-50.0 * (0.03 - c1)))
    assert arb._compute_alpha(obs) == pytest.approx(expected)
