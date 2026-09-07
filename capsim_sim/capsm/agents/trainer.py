"""Training pipeline for System 1 (CNN-LSTM reflexive controller).

Supports two training phases:
  1. Behavior cloning — supervised learning from baseline controller demos
  2. Reward fine-tuning — PPO-style on-policy RL with the reward function

For the offline simulation, behavior cloning is the primary training
method. The model learns to imitate the RuleBasedVoltage controller and
is then fine-tuned with the reward signal to discover improvements.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from capsm.agents.collector import collect_trajectory
from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.baselines import RuleBasedVoltage, NoControl
from capsm.grid.environment import QSTSEnvironment


def train_behavior_cloning(
    trajectories: list[dict],
    n_features: int,
    n_actions: int,
    *,
    epochs: int = 50,
    batch_size: int = 64,
    lr: float = 1e-3,
    device: str = "cpu",
    verbose: bool = True,
) -> CNNLSTM:
    """Train the CNN-LSTM model via behavior cloning on collected demos.

    Parameters
    ----------
    trajectories : list of dict
        Each dict has 'states', 'actions' arrays from collect_trajectory.
    n_features, n_actions : int
        Input/output dimensions.
    epochs : int
        Number of training epochs.
    batch_size : int
        Mini-batch size.
    lr : float
        Learning rate.
    device : str
        Torch device.

    Returns
    -------
    CNNLSTM — trained model.
    """
    all_states = np.concatenate([t["states"] for t in trajectories])
    all_actions = np.concatenate([t["actions"] for t in trajectories])
    X = torch.tensor(all_states, dtype=torch.float32)
    Y = torch.tensor(all_actions, dtype=torch.float32)
    ds = TensorDataset(X, Y)
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True)
    model = CNNLSTM(n_features, n_actions).to(device)
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        n_batches = 0
        for xb, yb in loader:
            xb = xb.unsqueeze(1).to(device)  # (B, 1, F) — seq_len=1 for BC
            yb = yb.to(device)
            pred, _ = model(xb)
            loss = loss_fn(pred, yb)
            optimiser.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimiser.step()
            total_loss += loss.item()
            n_batches += 1
        if verbose and (epoch + 1) % 10 == 0:
            avg = total_loss / max(n_batches, 1)
            print(f"  BC epoch {epoch+1}/{epochs}  loss={avg:.6f}")
    model.eval()
    return model


def collect_demos(
    case_name: str,
    profiles,
    *,
    start: str = "2019-01-01",
    n_episodes: int = 3,
    steps_per_episode: int = 168,
) -> tuple[list[dict], StateEncoder]:
    """Collect demonstration trajectories from the RuleBasedVoltage controller.

    Returns
    -------
    trajectories : list of dict
    encoder : StateEncoder (fitted to the environment).
    """
    env = QSTSEnvironment(case_name, profiles)
    controller = RuleBasedVoltage()
    encoder = StateEncoder(env)
    trajectories = []
    for ep in range(n_episodes):
        ep_start = f"2019-01-{ep * 7 + 1:02d}"
        traj = collect_trajectory(env, controller, encoder, start=ep_start,
                                  n_steps=steps_per_episode)
        trajectories.append(traj)
        if (ep + 1) % 1 == 0:
            print(f"  episode {ep+1}/{n_episodes}  steps={len(traj['states'])}  "
                  f"cum_reward={traj['rewards'].sum():.2f}")
    return trajectories, encoder


def save_model(model: CNNLSTM, path: str | Path) -> None:
    """Save model weights to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), path)


def load_model(path: str | Path, n_features: int, n_actions: int,
               device: str = "cpu") -> CNNLSTM:
    """Load model weights from disk."""
    model = CNNLSTM(n_features, n_actions).to(device)
    model.load_state_dict(torch.load(path, map_location=device, weights_only=True))
    model.eval()
    return model
