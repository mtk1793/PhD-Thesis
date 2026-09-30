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

    Ablation modes (master plan §12, Phase I):
    - ``mode="sigmoid"`` (default, deployed): α = sigmoid(tau·(c_th − c1)).
    - ``mode="hard"``: α ∈ {1, 0} switching at the threshold.
    - ``mode="fixed"``: constant α = ``fixed_alpha`` (e.g. 0.5 → 50/50 blend).

    ``safe_mode`` forces full System-2 authority (α = 0) whenever the
    stress exceeds ``safe_threshold`` regardless of mode. Default off;
    the deployed sigmoid behaviour is unchanged when defaults are used.
    ``hysteresis`` adds a switching deadband (hard mode only).
    """

    def __init__(
        self,
        system1,
        system2,
        threshold: float = 0.03,
        tau: float = 50.0,
        mode: str = "sigmoid",
        fixed_alpha: float = 0.5,
        safe_mode: bool = False,
        safe_threshold: float = 0.06,
        hysteresis: float = 0.0,
    ) -> None:
        if mode not in ("sigmoid", "hard", "fixed"):
            raise ValueError(f"unknown arbiter mode: {mode!r}")
        self.system1 = system1
        self.system2 = system2
        self.threshold = threshold
        self.tau = tau
        self.mode = mode
        self.fixed_alpha = fixed_alpha
        self.safe_mode = safe_mode
        self.safe_threshold = safe_threshold
        self.hysteresis = hysteresis
        self.name = f"metacognitive_arbiter_{mode}"
        self._alpha_history: list[float] = []
        self._stress_history: list[float] = []
        self._hard_state = 1.0  # last hard-switch state (1 = System 1)

    def _sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    def _stress(self, obs: dict) -> float:
        vm = obs["vm"]
        return float(np.mean(np.abs(vm - 1.0)))

    def _compute_alpha(self, obs: dict) -> float:
        """Compute blending weight from system stress."""
        c1 = self._stress(obs)
        if self.mode == "fixed":
            alpha = self.fixed_alpha
        elif self.mode == "hard":
            if self.hysteresis > 0:
                # switch to System 2 above c_th, back to System 1 only
                # once stress falls below c_th - hysteresis
                if c1 > self.threshold:
                    self._hard_state = 0.0
                elif c1 < self.threshold - self.hysteresis:
                    self._hard_state = 1.0
            else:
                self._hard_state = 1.0 if c1 <= self.threshold else 0.0
            alpha = self._hard_state
        else:  # sigmoid (deployed default)
            alpha = self._sigmoid(self.tau * (self.threshold - c1))
        if self.safe_mode and c1 > self.safe_threshold:
            alpha = 0.0
        return alpha

    def act(self, obs: dict, env) -> dict:
        """Blend System 1 and System 2 actions based on confidence."""
        alpha = self._compute_alpha(obs)
        self._alpha_history.append(alpha)
        self._stress_history.append(self._stress(obs))
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
        self._stress_history.clear()
        self._hard_state = 1.0

    @property
    def alpha_history(self) -> list[float]:
        return self._alpha_history.copy()

    @property
    def stress_history(self) -> list[float]:
        return self._stress_history.copy()

    def arbitration_summary(self, dt_hours: float = 1.0) -> dict:
        """Diagnostics required by the arbiter ablation campaign (§12)."""
        if not self._alpha_history:
            return {}
        a = np.asarray(self._alpha_history)
        transitions = int(np.sum(np.abs(np.diff(np.round(a * 100) / 100)) > 0.02))
        return {
            "mean_alpha": float(np.mean(a)),
            "std_alpha": float(np.std(a)),
            "pct_system1_dominates": float(np.mean(a > 0.67) * 100.0),
            "pct_system2_dominates": float(np.mean(a < 0.33) * 100.0),
            "transitions_per_day": float(transitions / max(len(a) * dt_hours / 24.0, 1e-9)),
            "n_steps": int(len(a)),
        }
