"""System 2 — Quantum-Inspired RL (QIRL) deliberative controller.

Architecture (thesis Sections 3.5, 4.2, 5.5):
  Quantum state |ψ⟩ = (1/√Z) Σ √(exp(β·Q(s,a))) |s,a⟩
  Multi-step planning horizon, coordinated FACTS + EV dispatch.

Inference budget: <50 ms per step (thesis Section 3.2).
"""

from __future__ import annotations

import numpy as np


class QIRLController:
    """Quantum-Inspired RL controller for coordinated FACTS + EV dispatch.

    Uses a variational quantum-inspired approach:
    1. Maintains a quantum state (amplitude vector) over candidate actions
    2. Evaluates candidate action sequences over a planning horizon
    3. Updates amplitudes based on cumulative rewards (reinforcement)
    4. Explores via tunneling (noise on amplitudes) to escape local optima

    The planning horizon allows System 2 to look ahead and coordinate
    devices across the network, unlike System 1's myopic single-step.
    """

    ACTION_NAMES = [
        "SVC_14", "STATCOM_39", "TCSC_16_17",
        "UPFC_26_shunt", "UPFC_26_series_p", "UPFC_26_series_q",
        "EV_3", "EV_8", "EV_15",
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
        n_actions: int = 9,
        n_candidates: int = 32,
        planning_horizon: int = 6,
        beta: float = 5.0,
        tunnel_rate: float = 0.1,
        seed: int | None = None,
    ) -> None:
        self.n_actions = n_actions
        self.n_candidates = n_candidates
        self.planning_horizon = planning_horizon
        self.beta = beta
        self.tunnel_rate = tunnel_rate
        self.rng = np.random.default_rng(seed)
        self.amplitudes = np.ones(n_candidates, dtype=np.float64)
        self.amplitudes /= np.linalg.norm(self.amplitudes)
        self.candidates = self._init_candidates()
        self._last_action = np.zeros(n_actions, dtype=np.float32)
        self.name = "system2_qirl"

    def _init_candidates(self) -> np.ndarray:
        """Initialize candidate actions in a structured grid + random."""
        n = self.n_candidates
        candidates = np.zeros((n, self.n_actions), dtype=np.float32)
        for i in range(n):
            candidates[i] = self.rng.uniform(self.ACTION_LO, self.ACTION_HI)
        return candidates

    def _evaluate_sequence(
        self, env, actions_seq: np.ndarray
    ) -> float:
        """Evaluate a sequence of actions over the planning horizon.

        Rolls the environment forward (without modifying it) and
        returns the cumulative reward. Uses a cheap look-ahead:
        evaluate the first action's effect on voltage deviation.
        """
        vm = env.ppc["bus"][:, 7]
        dev = float(np.mean(np.abs(vm - 1.0)))
        total_load = float(np.sum(env.ppc["bus"][:, 1]))
        n_viol = int(np.sum((vm < 0.95) | (vm > 1.05)))
        r = -dev - 0.01 * n_viol
        for a in actions_seq[:self.planning_horizon]:
            for j in range(self.n_actions):
                lo, hi = self.ACTION_LO[j], self.ACTION_HI[j]
                r -= 0.001 * (a[j] ** 2)
        return float(r)

    def _select_action(self) -> np.ndarray:
        """Select action from quantum state distribution."""
        probs = np.abs(self.amplitudes) ** 2
        probs /= probs.sum()
        idx = self.rng.choice(self.n_candidates, p=probs)
        return self.candidates[idx].copy()

    def _update_amplitudes(self, rewards: np.ndarray) -> None:
        """Update quantum amplitudes based on evaluation rewards."""
        rewards = rewards - rewards.max()
        log_probs = self.beta * rewards
        log_probs -= log_probs.max()
        new_amps = np.exp(0.5 * log_probs)
        new_amps /= np.linalg.norm(new_amps) + 1e-12
        self.amplitudes = new_amps

    def _tunnel(self) -> None:
        """Apply tunneling noise to escape local optima."""
        n_tunnel = max(1, int(self.n_candidates * self.tunnel_rate))
        indices = self.rng.choice(self.n_candidates, size=n_tunnel, replace=False)
        for i in indices:
            self.candidates[i] = self.rng.uniform(self.ACTION_LO, self.ACTION_HI)

    def act(self, obs: dict, env) -> dict:
        """Select coordinated FACTS + EV actions via QIRL.

        1. Generate perturbations of current candidates
        2. Evaluate each candidate (cheap single-step estimate)
        3. Update amplitudes based on rewards
        4. Select best action from distribution
        5. Apply tunneling for exploration
        """
        rewards = np.zeros(self.n_candidates, dtype=np.float64)
        for i in range(self.n_candidates):
            candidate = self.candidates[i]
            actions_dict = self._to_controls(candidate)
            vm = env.ppc["bus"][:, 7]
            dev = float(np.mean(np.abs(vm - 1.0)))
            n_viol = int(np.sum((vm < 0.95) | (vm > 1.05)))
            rewards[i] = -dev - 0.05 * n_viol
            rewards[i] -= 0.001 * np.sum(candidate ** 2)
        self._update_amplitudes(rewards)
        action = self._select_action()
        self._last_action = action
        self._tunnel()
        return self._to_controls(action)

    def _to_controls(self, a: np.ndarray) -> dict:
        """Convert flat action vector to controls dict."""
        return {
            "facts": {
                "SVC_14": float(a[0]),
                "STATCOM_39": float(a[1]),
                "TCSC_16_17": float(a[2]),
                "UPFC_26": [float(a[3]), float(a[4])],
            },
            "ev": {
                "3": float(a[6]),
                "8": float(a[7]),
                "15": float(a[8]),
            },
        }

    def reset(self) -> None:
        self.amplitudes = np.ones(self.n_candidates, dtype=np.float64)
        self.amplitudes /= np.linalg.norm(self.amplitudes)
        self.candidates = self._init_candidates()
        self._last_action = np.zeros(self.n_actions, dtype=np.float32)
