"""Trajectory collector for System 1 training.

Runs a controller through the QSTS environment and records
(observation, action, reward) tuples for supervised / RL training.
"""

from __future__ import annotations

import numpy as np

from capsm.agents.reward import reward_fn
from capsm.agents.system1 import StateEncoder
from capsm.grid.environment import QSTSEnvironment


def collect_trajectory(
    env: QSTSEnvironment,
    controller,
    encoder: StateEncoder,
    *,
    start: str | None = None,
    n_steps: int | None = None,
) -> dict:
    """Run a controller and return trajectories as numpy arrays.

    Returns
    -------
    dict with keys:
        states : np.ndarray, shape (T, n_features)
        actions : np.ndarray, shape (T, n_actions)
        rewards : np.ndarray, shape (T,)
        observations : list[dict]  — raw observations for reward recomputation
    """
    obs = env.reset(start=start)
    states: list[np.ndarray] = []
    actions: list[np.ndarray] = []
    observations: list[dict] = []
    rewards: list[float] = []
    T = n_steps if n_steps is not None else env.n_steps - env.t - 1
    prev_obs = None
    for _ in range(T):
        raw_state = encoder.encode(obs)
        states.append(raw_state)
        ctrl_out = controller.act(obs, env)
        observations.append(obs)
        action_vec = _flatten_action(ctrl_out)
        actions.append(action_vec)
        obs = env.step(ctrl_out)
        r = reward_fn(obs, prev_obs)
        rewards.append(r)
        prev_obs = obs
    return {
        "states": np.stack(states),
        "actions": np.stack(actions),
        "rewards": np.array(rewards, dtype=np.float32),
        "observations": observations,
    }


def _flatten_action(ctrl: dict) -> np.ndarray:
    """Convert a controls dict to a flat 9-dim action vector."""
    facts = ctrl.get("facts", {})
    svc = float(facts.get("SVC_14", 0.0))
    statcom = float(facts.get("STATCOM_39", 0.0))
    tcsc = float(facts.get("TCSC_16_17", 0.0))
    upfc = facts.get("UPFC_26", [0.0, 0.0])
    upfc_b = float(upfc[0]) if isinstance(upfc, (list, tuple)) else float(upfc)
    upfc_p = float(upfc[1]) if isinstance(upfc, (list, tuple)) and len(upfc) > 1 else 0.0
    ev = ctrl.get("ev", {})
    ev3 = float(ev.get("3", 0.0))
    ev8 = float(ev.get("8", 0.0))
    ev15 = float(ev.get("15", 0.0))
    return np.array([svc, statcom, tcsc, upfc_b, upfc_p, 0.0, ev3, ev8, ev15],
                    dtype=np.float32)
