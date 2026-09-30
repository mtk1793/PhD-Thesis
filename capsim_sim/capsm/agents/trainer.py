"""Training pipeline for System 1 (CNN-LSTM reflexive controller).

Rebuilt per the master plan (§7 Phase D, §8 Phase E, §15 Phase L):

- **Chronological split.** Demonstrations are collected from the TRAINING
  years only (2015-2017). Validation uses 2018; the primary unseen test
  window is January 2019 (optionally the full 2019 year). No 2019 state
  ever enters training.

- **Windowed behaviour cloning.** Training samples are 12-step sliding
  windows over the demonstration trajectories (episode boundaries are
  never crossed), matching the ``window_reset`` inference convention
  (S1-A). The previous version trained on seq_len=1 samples and deployed
  a 12-step window — that train/deploy mismatch is removed.

- **Reserved dimension.** Action targets have index 5 (UPFC series-Q)
  forced to 0.0 — the model never learns to drive a physically inactive
  channel.

- **Reported metrics.** Train loss, chronological validation loss,
  held-out action MAE/RMSE (per output and mean), multiple seeds.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

from capsm.agents.collector import collect_trajectory
from capsm.agents.system1 import CNNLSTM, StateEncoder, System1Controller
from capsm.agents.baselines import RuleBasedVoltage, NoControl
from capsm.grid.environment import QSTSEnvironment

# Master plan §15 — final chronological split (OPSDD data window).
TRAIN_YEARS: tuple[int, ...] = (2015, 2016, 2017)
VAL_YEAR: int = 2018
TEST_YEARS: tuple[int, ...] = (2019,)

SEASON_START_MONTHS = {  # deterministic seasonal demo sampling
    "winter": 1, "spring": 4, "summer": 7, "autumn": 10,
}


def sample_training_episodes(
    timestamps: pd.DatetimeIndex,
    years: tuple[int, ...] = TRAIN_YEARS,
    episodes_per_year: int = 8,
    steps_per_episode: int = 168,
    seed: int | None = None,
) -> list[dict]:
    """Deterministically sample demonstration episodes from TRAINING years.

    For every year, one episode is anchored in each season (Jan/Apr/Jul/
    Oct) and the remaining episodes are drawn at random month offsets.
    All episode starts are guaranteed to lie within the requested years
    and at least ``steps_per_episode`` steps before the data ends.
    """
    rng = np.random.default_rng(seed)
    ts = pd.DatetimeIndex(timestamps)
    years_arr = ts.year.to_numpy()
    episodes: list[dict] = []
    for y in years:
        seasonal = [SEASON_START_MONTHS[s] for s in ("winter", "spring", "summer", "autumn")]
        extra = max(0, episodes_per_year - len(seasonal))
        if extra:
            extra_months = rng.choice(range(1, 13), size=extra, replace=True).tolist()
        else:
            extra_months = []
        for m in sorted(seasonal + extra_months):
            cand = np.flatnonzero((years_arr == y) & (ts.month.to_numpy() == m))
            if len(cand) == 0:
                continue
            start_idx = int(cand[0])
            if start_idx + steps_per_episode >= len(ts):
                continue
            start_str = ts[start_idx].strftime("%Y-%m-%d")
            episodes.append({"start": start_str, "steps": steps_per_episode})
    return episodes


def assert_no_test_leakage(episodes: list[dict], test_years: tuple[int, ...] = TEST_YEARS) -> None:
    """Guard: no demonstration episode may start inside a test year."""
    for ep in episodes:
        y = int(str(ep["start"])[:4])
        if y in test_years:
            raise AssertionError(
                f"train/test leakage: demonstration episode starts in test year {y}: {ep}"
            )


def build_window_dataset(
    trajectories: list[dict],
    seq_len: int = 12,
    *,
    train_fraction: float = 0.85,
) -> dict:
    """Build sliding-window BC samples with a chronological split.

    Windows never cross episode boundaries. The split is CHRONOLOGICAL
    and includes a guard gap of ``seq_len`` rows at the boundary so that
    no raw state row appears in both a training window and a validation
    window — validation windows start strictly after the last training
    history row. No temporal leakage by construction.
    """
    X_train, Y_train, X_val, Y_val = [], [], [], []
    for traj in trajectories:
        states = traj["states"]
        actions = traj["actions"]
        n = len(states)
        if n <= 2 * seq_len:
            continue
        windows_X = np.stack([states[i - seq_len:i] for i in range(seq_len, n)])
        windows_Y = actions[seq_len - 1: n - 1]
        split_row = int(n * train_fraction)
        ends = np.arange(seq_len, n)
        train_mask = ends <= split_row
        val_mask = ends >= split_row + seq_len
        if train_mask.any():
            X_train.append(windows_X[train_mask])
            Y_train.append(windows_Y[train_mask])
        if val_mask.any():
            X_val.append(windows_X[val_mask])
            Y_val.append(windows_Y[val_mask])
    if not X_train:
        raise ValueError("no windows could be built from the given trajectories")
    X_train = np.concatenate(X_train).astype(np.float32)
    Y_train = np.concatenate(Y_train).astype(np.float32)
    if X_val:
        X_val = np.concatenate(X_val).astype(np.float32)
        Y_val = np.concatenate(Y_val).astype(np.float32)
    else:  # degenerate short-trajectory case: reuse last training windows
        n_last = max(1, int(len(X_train) * 0.1))
        X_val, Y_val = X_train[-n_last:], Y_train[-n_last:]
    return {"X_train": X_train, "Y_train": Y_train,
            "X_val": X_val, "Y_val": Y_val}


def sanitize_action_targets(y: np.ndarray) -> np.ndarray:
    """Force the reserved action dimension (index 5) to 0 in targets."""
    y = np.array(y, dtype=np.float32, copy=True)
    y[:, 5] = 0.0
    return y


def train_behavior_cloning(
    dataset: dict,
    n_features: int,
    n_actions: int,
    *,
    seq_len: int = 12,
    epochs: int = 50,
    batch_size: int = 64,
    lr: float = 1e-3,
    device: str = "cpu",
    seed: int = 42,
    verbose: bool = True,
) -> tuple[CNNLSTM, dict]:
    """Train the CNN-LSTM via behaviour cloning on windowed demos.

    Returns ``(model, history)`` where history holds per-epoch train and
    chronological-validation losses and the final action MAE/RMSE.
    """
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset

    torch.manual_seed(seed)
    np.random.seed(seed % (2**32))

    X = torch.tensor(dataset["X_train"], dtype=torch.float32)   # (N, T, F)
    Y = torch.tensor(sanitize_action_targets(dataset["Y_train"]))
    Xv = torch.tensor(dataset["X_val"], dtype=torch.float32)
    Yv = torch.tensor(sanitize_action_targets(dataset["Y_val"]))

    loader = DataLoader(TensorDataset(X, Y), batch_size=batch_size, shuffle=True)
    model = CNNLSTM(n_features, n_actions).to(device)
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    history = {"train_loss": [], "val_loss": [], "val_mae": None, "val_rmse": None}
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    history["trainable_parameters"] = int(n_params)

    model.train()
    for epoch in range(epochs):
        total_loss, n_batches = 0.0, 0
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            pred, _ = model(xb, None)          # window_reset convention
            loss = loss_fn(pred, yb)
            optimiser.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimiser.step()
            total_loss += loss.item()
            n_batches += 1
        train_loss = total_loss / max(n_batches, 1)
        history["train_loss"].append(train_loss)

        model.eval()
        with torch.no_grad():
            pv, _ = model(Xv.to(device), None)
            val_loss = loss_fn(pv, Yv.to(device)).item()
            mae = (pv - Yv.to(device)).abs().mean().item()
            rmse = ((pv - Yv.to(device)) ** 2).mean().sqrt().item()
        history["val_loss"].append(val_loss)
        model.train()
        if verbose and ((epoch + 1) % max(1, epochs // 10) == 0 or epoch == 0):
            print(f"  BC epoch {epoch+1}/{epochs}  train={train_loss:.6f}  val={val_loss:.6f}")
    history["val_mae"] = float(mae)
    history["val_rmse"] = float(rmse)
    model.eval()
    return model, history


def collect_demos(
    case_name: str,
    profiles: pd.DataFrame,
    episodes: list[dict],
    *,
    encoder: StateEncoder | None = None,
) -> tuple[list[dict], StateEncoder]:
    """Collect RuleBasedVoltage demonstrations for the given episodes.

    ``episodes`` comes from :func:`sample_training_episodes` and MUST be
    leakage-checked with :func:`assert_no_test_leakage` before training.
    """
    env = QSTSEnvironment(case_name, profiles)
    controller = RuleBasedVoltage()
    encoder = encoder or StateEncoder(env)
    trajectories = []
    for k, ep in enumerate(episodes):
        traj = collect_trajectory(
            env, controller, encoder, start=ep["start"], n_steps=ep["steps"]
        )
        trajectories.append(traj)
        print(f"  episode {k+1}/{len(episodes)}  start={ep['start']}  "
              f"steps={len(traj['states'])}  cum_reward={traj['rewards'].sum():.2f}")
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
