"""Reward function for System 1 (CNN-LSTM) training.

Combines three signal components:
  1. Voltage-regulation reward — penalises deviation from 1.0 pu
  2. Loss-reduction reward — penalises active-power losses
  3. Constraint penalty — hard penalty for voltage violations

All weights are tuneable.  The reward is normalised per-timestamp so the
cumulative reward over a trajectory is comparable across different system
sizes and loading levels.
"""

from __future__ import annotations

import numpy as np


def reward_fn(
    obs: dict,
    prev_obs: dict | None,
    *,
    w_dev: float = 1.0,
    w_loss: float = 0.5,
    penalty_violation: float = -10.0,
) -> float:
    """Compute the one-step reward from the current observation.

    Parameters
    ----------
    obs : dict
        Current observation from the QSTS environment.
    prev_obs : dict or None
        Previous observation (unused for now; reserved for delta-reward).
    w_dev : float
        Weight for the voltage-deviation term (negative deviation from 1.0).
    w_loss : float
        Weight for the normalised loss term.
    penalty_violation : float
        Penalty added per voltage-violation bus-hour.

    Returns
    -------
    float
        Scalar reward (higher is better).
    """
    vm = obs["vm"]
    n_bus = len(vm)
    dev = float(np.mean(np.abs(vm - 1.0)))
    losses = obs.get("metrics", {}).get("total_losses_mw", 0.0)
    base_losses = 50.0
    norm_losses = losses / base_losses if base_losses > 0 else 0.0
    n_viol = int(obs.get("metrics", {}).get("n_voltage_violations", 0))
    r = -(w_dev * dev) - (w_loss * norm_losses) + (penalty_violation * n_viol)
    return float(r)


def reward_batch(
    observations: list[dict],
    *,
    w_dev: float = 1.0,
    w_loss: float = 0.5,
    penalty_violation: float = -10.0,
) -> float:
    """Cumulative reward over a trajectory."""
    total = 0.0
    prev = None
    for obs in observations:
        total += reward_fn(obs, prev, w_dev=w_dev, w_loss=w_loss,
                           penalty_violation=penalty_violation)
        prev = obs
    return total
