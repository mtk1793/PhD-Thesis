"""System 2 — Quantum-inspired amplitude-based candidate-selection controller.

Rebuilt per the master plan (§5, §10, §11):

- **Candidate-dependent physical evaluation.** Every candidate action is
  scored on the *counterfactual* network state obtained by applying that
  candidate through the environment's own pipeline — never on the
  unchanged state. Two interchangeable evaluators are provided
  (``capsm/agents/evaluators.py``):

    * ``evaluator="exact"``     — Evaluator A, one AC power flow per
      candidate; offline scientific reference.
    * ``evaluator="surrogate"`` — Evaluator B, first-order sensitivity
      surrogate; real-time deployable (<<50 ms amortised).

- **Formal reward** (thesis Eq. 4.x): normalised voltage deviation,
  violation severity, losses, thermal overload, EV SoC feasibility and
  action effort. No candidate-independent voltage term.

- **Honest single-step scope.** System 2 performs coordinated *one-step*
  candidate optimisation. A multi-step planning horizon is reserved for
  future work and is NOT implemented here.

- **Reserved dimension.** Action index 5 (UPFC series-Q) is physically
  inactive in the Stage-1 device models; it is forced to 0.0 in the
  candidate set, excluded from the effort penalty, and never sent to the
  environment.

- **Selection modes** (used by the QIRL ablation campaign, §10):
  ``qirl`` (amplitude update + Born rule + tunnelling), ``softmax``
  (per-step Boltzmann sampling), ``greedy`` (best reward), ``random``.
"""

from __future__ import annotations

import numpy as np

from capsm.agents.evaluators import (
    RESERVED_INDEX,
    make_evaluator,
    active_control_dims,
)

ACTION_NAMES = [
    "SVC_14",               # 0 — shunt susceptance (p.u.)
    "STATCOM_39",           # 1 — shunt susceptance (p.u.)
    "TCSC_16_17",           # 2 — series compensation degree k
    "UPFC_26_shunt",        # 3 — shunt susceptance (p.u.)
    "UPFC_26_series_p",     # 4 — series compensation degree k
    "UPFC_26_series_q",     # 5 — RESERVED (neutral in Stage-1 models)
    "EV_3",                 # 6 — aggregate dispatch (MW, charge > 0)
    "EV_8",                 # 7 — aggregate dispatch (MW)
    "EV_15",                # 8 — aggregate dispatch (MW)
]
ACTION_LO = np.array(
    [-0.5, -1.0, 0.3, -0.5, -0.5, 0.0, -50.0, -50.0, -50.0],
    dtype=np.float32,
)
ACTION_HI = np.array(
    [0.5, 1.0, 0.7, 0.5, 0.5, 0.0, 50.0, 50.0, 50.0],
    dtype=np.float32,
)


class QIRLController:
    """Quantum-inspired amplitude-based stochastic candidate-selection controller.

    Per step:
      1. Evaluate all candidates on the counterfactual network state
         (Evaluator A or B) with the formal candidate-dependent reward.
      2. Reinforce amplitudes: |ψ_i|² ∝ exp(β·r_i)  (Boltzmann over reward).
      3. Select an action by the Born rule (or an ablation mode).
      4. Optionally re-inititalise a fraction of candidates (tunnelling).

    Selection modes (ablation campaign, master plan §10):
      - ``qirl``    : persistent amplitudes + Born rule + tunnelling
      - ``softmax`` : per-step Boltzmann sampling, no persistent amplitudes
      - ``greedy``  : argmax reward (deterministic)
      - ``random``  : uniform candidate choice
    """

    ACTION_NAMES = ACTION_NAMES
    ACTION_LO = ACTION_LO
    ACTION_HI = ACTION_HI

    def __init__(
        self,
        env=None,
        n_actions: int = 9,
        n_candidates: int = 32,
        beta: float = 5.0,
        tunnel_rate: float = 0.1,
        seed: int | None = None,
        evaluator: str = "surrogate",
        refresh_every: int = 24,
        mode: str = "qirl",
        candidate_refresh: bool = False,
        tunnel: bool = True,
        reward_weights=None,
    ) -> None:
        if n_actions != 9:
            raise ValueError("the CAPSM Stage-1 action interface is 9-dimensional")
        self.n_actions = n_actions
        self.n_candidates = n_candidates
        self.beta = beta
        self.tunnel_rate = tunnel_rate
        self.rng = np.random.default_rng(seed)
        self.mode = mode
        self.candidate_refresh = candidate_refresh
        self.tunnel_enabled = tunnel
        self.name = f"system2_qirl_{mode}"

        # Per-controller evaluator bound to the environment it acts in.
        # The env is injected on the first act() call if not given here.
        self._env = env
        self._evaluator_kind = evaluator
        self._evaluator = None
        self._refresh_every = refresh_every
        self._reward_weights = reward_weights

        self.amplitudes = np.ones(n_candidates, dtype=np.float64)
        self.amplitudes /= np.linalg.norm(self.amplitudes)
        self.candidates = self._init_candidates()
        self._last_action = np.zeros(n_actions, dtype=np.float32)
        self._last_evaluation = None  # CandidateEvaluation (diagnostics)

    # ── candidate management ─────────────────────────────────────────
    def _init_candidates(self) -> np.ndarray:
        """Random candidates with the reserved dimension pinned to 0."""
        candidates = self.rng.uniform(
            self.ACTION_LO.astype(np.float64),
            self.ACTION_HI.astype(np.float64),
            size=(self.n_candidates, self.n_actions),
        )
        candidates[:, RESERVED_INDEX] = 0.0
        return candidates.astype(np.float32)

    def _tunnel(self) -> None:
        """Re-initialise a fraction of candidates (exploration).

        The reserved dimension stays neutral and the bounds are respected.
        """
        if not self.tunnel_enabled or self.tunnel_rate <= 0:
            return
        n_tunnel = max(1, int(self.n_candidates * self.tunnel_rate))
        indices = self.rng.choice(self.n_candidates, size=n_tunnel, replace=False)
        fresh = self.rng.uniform(
            self.ACTION_LO.astype(np.float64),
            self.ACTION_HI.astype(np.float64),
            size=(n_tunnel, self.n_actions),
        )
        fresh[:, RESERVED_INDEX] = 0.0
        self.candidates[indices] = fresh.astype(np.float32)

    # ── amplitude / selection mechanics ─────────────────────────────
    def _update_amplitudes(self, rewards: np.ndarray) -> None:
        """|ψ_i| ∝ exp(β·r_i / 2); probabilities form a Boltzmann distribution."""
        shifted = rewards - rewards.max()
        log_probs = self.beta * shifted
        log_probs -= log_probs.max()
        new_amps = np.exp(0.5 * log_probs)
        new_amps /= np.linalg.norm(new_amps) + 1e-12
        self.amplitudes = new_amps

    def _select_action(self, rewards: np.ndarray | None = None) -> np.ndarray:
        if self.mode == "qirl":
            probs = np.abs(self.amplitudes) ** 2
            probs /= probs.sum()
            idx = self.rng.choice(self.n_candidates, p=probs)
        elif self.mode == "softmax":
            r = rewards - rewards.max()
            p = np.exp(self.beta * r)
            p /= p.sum()
            idx = self.rng.choice(self.n_candidates, p=p)
        elif self.mode == "greedy":
            idx = int(np.argmax(rewards))
        elif self.mode == "random":
            idx = int(self.rng.integers(self.n_candidates))
        else:
            raise ValueError(f"unknown selection mode: {self.mode!r}")
        return self.candidates[idx].copy()

    # ── main interface ───────────────────────────────────────────────
    def _bind_env(self, env) -> None:
        if self._evaluator is None:
            self._env = env
            self._evaluator = make_evaluator(
                self._evaluator_kind,
                env,
                self.ACTION_LO.astype(np.float64),
                self.ACTION_HI.astype(np.float64),
                weights=self._reward_weights,
                **({} if self._evaluator_kind == "exact"
                   else {"refresh_every": self._refresh_every}),
            )

    def act(self, obs: dict, env) -> dict:
        """One-step coordinated candidate optimisation.

        1. Evaluate every candidate on its counterfactual state.
        2. Update amplitudes (qirl mode) from the formal reward.
        3. Select an action by the mode's rule.
        4. Apply tunnelling / candidate refresh for exploration.
        """
        self._bind_env(env)
        u_prev = self._last_action.astype(np.float64)

        if self.candidate_refresh:
            self.candidates = self._init_candidates()

        evaluation = self._evaluator.evaluate_all(
            env, obs, self.candidates, u_prev=u_prev,
        )
        rewards = evaluation.rewards
        self._last_evaluation = evaluation

        if self.mode == "qirl":
            self._update_amplitudes(rewards)

        action = self._select_action(rewards)
        self._last_action = action
        self._tunnel()
        return self._to_controls(action)

    def _to_controls(self, a: np.ndarray) -> dict:
        """Convert the flat action vector to environment controls.

        The reserved dimension is asserted neutral and never emitted.
        """
        a = np.asarray(a, dtype=np.float64).flatten()
        assert a[RESERVED_INDEX] == 0.0, "reserved series-Q dimension must be neutral"
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
        self._last_evaluation = None

    # ── diagnostics ──────────────────────────────────────────────────
    @property
    def last_evaluation(self):
        """CandidateEvaluation from the most recent act() call."""
        return self._last_evaluation

    @property
    def evaluator_power_flows(self) -> int:
        """Total power flows consumed by the bound evaluator."""
        return 0 if self._evaluator is None else self._evaluator.n_power_flows
