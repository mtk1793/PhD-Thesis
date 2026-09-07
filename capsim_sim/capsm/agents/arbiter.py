"""Metacognitive Arbiter — coordinates System 1 and System 2.

Architecture (thesis Section 4.2, Algorithm 4.3):
  u = α · u1 + (1 − α) · u2
  α = sigmoid(C1 − τ)

Where:
  u1 = System 1 (CNN-LSTM) action
  u2 = System 2 (QIRL) action
  C1 = System 1 confidence (voltage deviation from 1.0)
  τ = threshold (configurable, default 0.03 p.u.)

When the system is stable (C1 < τ), α → 1 (System 1 dominates).
When the system is stressed (C1 > τ), α → 0 (System 2 dominates).
"""

from __future__ import annotations

import numpy as np


class MetacognitiveArbiter:
    """Blends System 1 and System 2 actions based on system stress.

    The blending weight α determines how much each system contributes:
    - α ≈ 1: System 1 dominates (stable conditions, fast response)
    - α ≈ 0: System 2 dominates (stressed conditions, coordinated optimisation)
    """

    def __init__(
        self,
        system1,
        system2,
        threshold: float = 0.03,
        tau: float = 50.0,
    ) -> None:
        self.system1 = system1
        self.system2 = system2
        self.threshold = threshold
        self.tau = tau
        self.name = "metacognitive_arbiter"
        self._alpha_history: list[float] = []

    def _sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    def _compute_alpha(self, obs: dict) -> float:
        """Compute blending weight from system stress."""
        vm = obs["vm"]
        c1 = float(np.mean(np.abs(vm - 1.0)))
        alpha = self._sigmoid(self.tau * (self.threshold - c1))
        return alpha

    def act(self, obs: dict, env) -> dict:
        """Blend System 1 and System 2 actions based on confidence."""
        alpha = self._compute_alpha(obs)
        self._alpha_history.append(alpha)
        ctrl1 = self.system1.act(obs, env)
        ctrl2 = self.system2.act(obs, env)
        blended = self._blend_controls(ctrl1, ctrl2, alpha)
        return blended

    def _blend_controls(self, c1: dict, c2: dict, alpha: float) -> dict:
        """Linearly blend two control dicts."""
        facts = {}
        all_keys = set(list(c1.get("facts", {}).keys()) +
                       list(c2.get("facts", {}).keys()))
        for key in all_keys:
            v1 = c1.get("facts", {}).get(key, 0.0)
            v2 = c2.get("facts", {}).get(key, 0.0)
            if isinstance(v1, (list, tuple)):
                blended = [alpha * v1[i] + (1 - alpha) * v2[i]
                           for i in range(len(v1))]
                facts[key] = blended
            else:
                facts[key] = alpha * float(v1) + (1 - alpha) * float(v2)
        ev = {}
        all_ev = set(list(c1.get("ev", {}).keys()) +
                     list(c2.get("ev", {}).keys()))
        for key in all_ev:
            v1 = c1.get("ev", {}).get(key, 0.0)
            v2 = c2.get("ev", {}).get(key, 0.0)
            ev[key] = alpha * float(v1) + (1 - alpha) * float(v2)
        return {"facts": facts, "ev": ev}

    def reset(self) -> None:
        self.system1.reset()
        self.system2.reset()
        self._alpha_history.clear()

    @property
    def alpha_history(self) -> list[float]:
        return self._alpha_history.copy()
