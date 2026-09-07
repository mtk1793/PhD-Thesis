"""System 1 — CNN-LSTM reflexive controller for CAPSM.

Architecture (thesis Section 4.2, Figure 6.1):
  CNN (spatial feature extraction across buses) → LSTM (temporal dynamics)
  → attention → FC → continuous action outputs for FACTS + EV dispatch.

Inference budget: <5 ms per step (verified in Phase 4 tests).
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn


class StateEncoder:
    """Maps a QSTS observation dict to a fixed-size flat feature vector.

    Feature layout (case39):
      bus_vm  (n_bus)          — bus voltage magnitudes
      bus_va  (n_bus)          — bus voltage angles (radians)
      branch  (n_branch)      — branch sending-end active power
      gen_p   (n_gen)          — generator active power output
      gen_q   (n_gen)          — generator reactive power output
      facts   (n_facts * 2)    — [shunt_b, series_k] per FACTS device
      ev      (n_ev * 2)       — [P, SoC] per EV station
      scalar  (2)              — total_load_mw, total_gen_mw
    """

    def __init__(self, env) -> None:
        self._env = env
        self.n_bus = int(env.base_ppc["bus"].shape[0])
        self.n_branch = int(env.base_ppc["branch"].shape[0])
        self.n_gen = int(env.base_ppc["gen"].shape[0])
        self.n_facts = len(env.facts)
        self.n_ev = len(env.ev_fleet.stations) if env.ev_fleet else 0
        self.n_features = (
            self.n_bus * 2
            + self.n_branch
            + self.n_gen * 2
            + self.n_facts * 2
            + self.n_ev * 2
            + 2
        )
        self._facts_order = [d.name for d in env.facts]
        self._ev_buses = (
            list(env.ev_fleet.stations.keys()) if env.ev_fleet else []
        )

    def encode(self, obs: dict) -> np.ndarray:
        """Encode a single observation into a flat float32 vector."""
        parts: list[np.ndarray] = []
        parts.append(obs["vm"].astype(np.float32))
        parts.append(obs["va"].astype(np.float32))
        parts.append(obs["branch_pf"].astype(np.float32))
        ppc = self._env.ppc if self._env.ppc is not None else self._env.base_ppc
        gen = ppc["gen"]
        parts.append(gen[:, 1].astype(np.float32))
        parts.append(gen[:, 2].astype(np.float32))
        facts_vec = np.zeros(self.n_facts * 2, dtype=np.float32)
        ev_vec = np.zeros(max(self.n_ev * 2, 0), dtype=np.float32)
        for i, name in enumerate(self._facts_order):
            dev = next(d for d in self._env.facts if d.name == name)
            if hasattr(dev, "series"):
                facts_vec[i * 2] = dev.shunt.b if hasattr(dev.shunt, "b") else 0.0
                facts_vec[i * 2 + 1] = dev.series.k if hasattr(dev.series, "k") else 0.0
            else:
                facts_vec[i * 2] = dev.b if hasattr(dev, "b") else 0.0
        parts.append(facts_vec)
        if self.n_ev > 0:
            ev_state = obs.get("ev_state")
            if ev_state is not None:
                soc = ev_state.get("soc", {})
                p = ev_state.get("p", {})
                for j, bus in enumerate(self._ev_buses):
                    ev_vec[j * 2] = float(p.get(bus, 0.0))
                    ev_vec[j * 2 + 1] = float(soc.get(bus, 0.5))
            parts.append(ev_vec)
        total_load = obs.get("total_load_mw", 0.0)
        total_gen = obs.get("total_gen_mw", 0.0) or 0.0
        parts.append(np.array([total_load, total_gen], dtype=np.float32))
        return np.concatenate(parts)


class CNNLSTM(nn.Module):
    """CNN-LSTM network for real-time FACTS + EV dispatch.

    Input:  (batch, seq_len, n_features)
    Output: (batch, n_actions)  — continuous control setpoints.
    """

    def __init__(
        self,
        n_features: int,
        n_actions: int,
        cnn_channels: list[int] | None = None,
        lstm_hidden: int = 128,
        fc_hidden: int = 64,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        if cnn_channels is None:
            cnn_channels = [64, 64]
        layers: list[nn.Module] = []
        in_ch = 1
        for out_ch in cnn_channels:
            layers.extend([
                nn.Conv1d(in_ch, out_ch, kernel_size=3, padding=1),
                nn.ReLU(),
            ])
            in_ch = out_ch
        layers.append(nn.AdaptiveAvgPool1d(1))
        self.cnn = nn.Sequential(*layers)
        self.lstm = nn.LSTM(
            input_size=cnn_channels[-1],
            hidden_size=lstm_hidden,
            batch_first=True,
        )
        self.attention = nn.Sequential(
            nn.Linear(lstm_hidden, lstm_hidden),
            nn.Tanh(),
            nn.Linear(lstm_hidden, 1),
        )
        self.fc = nn.Sequential(
            nn.Linear(lstm_hidden, fc_hidden),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(fc_hidden, n_actions),
        )
        self._lstm_hidden = lstm_hidden

    def forward(
        self, x: torch.Tensor, hidden: tuple | None = None
    ) -> tuple[torch.Tensor, tuple]:
        B, T, F = x.shape
        cnn_in = x.reshape(B * T, 1, F)
        cnn_out = self.cnn(cnn_in)
        cnn_out = cnn_out.squeeze(-1)
        cnn_out = cnn_out.reshape(B, T, -1)
        lstm_out, hidden = self.lstm(cnn_out, hidden)
        attn_w = self.attention(lstm_out)
        attn_w = torch.softmax(attn_w, dim=1)
        context = (lstm_out * attn_w).sum(dim=1)
        actions = self.fc(context)
        return actions, hidden

    def reset_hidden(self, batch_size: int, device: torch.device) -> tuple:
        h = torch.zeros(1, batch_size, self._lstm_hidden, device=device)
        c = torch.zeros(1, batch_size, self._lstm_hidden, device=device)
        return (h, c)


class System1Controller:
    """Inference wrapper: observation → FACTS controls dict + EV dispatch."""

    ACTION_NAMES = [
        "SVC_14",
        "STATCOM_39",
        "TCSC_16_17",
        "UPFC_26_shunt",
        "UPFC_26_series_p",
        "UPFC_26_series_q",
        "EV_3",
        "EV_8",
        "EV_15",
    ]
    ACTION_LO = np.array(
        [-0.5, -1.0, 0.3, -0.5, -0.5, -0.5, -50.0, -50.0, -50.0],
        dtype=np.float32,
    )
    ACTION_HI = np.array(
        [0.5, 1.0, 0.7, 0.5, 0.5, 0.5, 50.0, 50.0, 50.0],
        dtype=np.float32,
    )

    def __init__(
        self,
        model: CNNLSTM,
        encoder: StateEncoder,
        device: torch.device | str = "cpu",
    ) -> None:
        self.model = model
        self.encoder = encoder
        self.device = torch.device(device)
        self.model.eval()
        self._hidden = None
        self._window: list[np.ndarray] = []
        self.seq_len = 12

    @torch.no_grad()
    def act(self, obs: dict, env) -> dict:
        raw = self.encoder.encode(obs)
        self._window.append(raw)
        if len(self._window) > self.seq_len:
            self._window = self._window[-self.seq_len:]
        while len(self._window) < self.seq_len:
            self._window.insert(0, raw)
        x = torch.tensor(
            np.stack(self._window), dtype=torch.float32
        ).unsqueeze(0).to(self.device)
        actions, self._hidden = self.model(x, self._hidden)
        a = actions.cpu().numpy().flatten()
        a = np.clip(a, self.ACTION_LO, self.ACTION_HI)
        controls: dict = {"facts": {}, "ev": {}}
        controls["facts"]["SVC_14"] = float(a[0])
        controls["facts"]["STATCOM_39"] = float(a[1])
        controls["facts"]["TCSC_16_17"] = float(a[2])
        controls["facts"]["UPFC_26"] = [float(a[3]), float(a[4])]
        ev_power = {"3": float(a[6]), "8": float(a[7]), "15": float(a[8])}
        controls["ev"] = ev_power
        return controls

    def reset(self) -> None:
        self._hidden = None
        self._window.clear()
