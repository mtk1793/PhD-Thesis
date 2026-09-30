"""Candidate evaluators for System 2 (QIRL) — Phase B of the rebuild plan.

This module implements the two evaluator architectures required by the
master plan (§5.1/§5.2):

Evaluator A — ``ExactPowerFlowEvaluator``
    Scientific ground truth. For every candidate action the environment
    is snapshot-wrapped and the candidate is applied through the
    environment's *own* pipeline (``QSTSEnvironment._solve``), i.e. the
    counterfactual network state is produced by exactly the same code path
    that would execute if the candidate were really applied at the current
    time step. One AC power flow per candidate. Slower than real time;
    used offline as the reference.

Evaluator B — ``SensitivitySurrogateEvaluator``
    Real-time candidate evaluator. A first-order Taylor model of the
    network response around the current operating point:

        V_hat      = V0      + S_V @ (u - u0)
        flow_hat   = flow0   + S_F @ (u - u0)
        losses_hat = losses0 + s_L @ (u - u0)

    The sensitivity matrices are obtained by finite differences on frozen
    environment snapshots (one power flow per *active* control dimension
    per refresh) and refreshed every ``refresh_every`` steps, so the
    amortised cost is a fraction of one power flow per step. Validated
    against Evaluator A by ``scripts/phase5b_surrogate_validation.py``.

Formal candidate reward (master plan §5.1, thesis Eq. 4.x)
---------------------------------------------------------
Every term is normalised and every term is candidate-dependent:

    r(u) = - wV   * J_V        mean absolute voltage deviation (p.u.)
           - wVio * J_viol     squared voltage-limit violation severity
           - wL   * J_L        losses / loss reference
           - wT   * J_th       squared thermal overload severity
           - wSoC * J_SoC      EV SoC infeasibility of the request
           - wU   * J_u        action effort (active dimensions only)

The reserved action dimension (UPFC series-Q, index 5) is excluded from
the effort term and from the sensitivity build because it is physically
inactive in the Stage-1 device models (``capsm/grid/facts.py``).
"""

from __future__ import annotations

import copy
import time
from dataclasses import dataclass

import numpy as np

# Reserved action index: UPFC_26 series-Q. The Stage-1 UPFC model
# implements only shunt susceptance + series compensation degree; there
# is no physically independent series-Q channel. The dimension is kept in
# the 9-D interface for forward compatibility but is forced to neutral.
RESERVED_INDEX = 5
VM_MIN = 0.95
VM_MAX = 1.05
NON_CONVERGED_PENALTY = -10.0


@dataclass
class RewardWeights:
    """Weights of the formal candidate reward (all terms normalised)."""

    w_V: float = 1.0
    w_viol: float = 10.0
    w_L: float = 0.5
    w_T: float = 5.0
    w_SoC: float = 2.0
    w_u: float = 0.01


@dataclass
class CandidateEvaluation:
    """Container for one evaluate-all call."""

    rewards: np.ndarray
    vm_pred: np.ndarray | None = None        # (n_candidates, n_bus)
    overload_pred: np.ndarray | None = None  # (n_candidates,)
    n_power_flows: int = 0                   # PFs consumed by this call
    elapsed_ms: float = 0.0
    refreshed: bool = False


# ──────────────────────────────────────────────────────────────────────
# Environment snapshot / restore helpers
# ──────────────────────────────────────────────────────────────────────

def snapshot_env(env) -> dict:
    """Capture every mutable part of the environment's power-flow state.

    ``QSTSEnvironment._solve`` mutates device setpoints, the EV fleet SoC,
    the curtailment counter and ``env.ppc``. The exact evaluator must undo
    all of these after each counterfactual candidate solve.
    """
    facts_state = []
    for d in env.facts:
        if hasattr(d, "series"):                      # UPFC
            facts_state.append(
                ("upfc", d.shunt.b, d.series.k, dict(d.series._orig_x))
            )
        elif hasattr(d, "k_min"):                     # SeriesCompensator
            facts_state.append(("series", d.k, dict(d._orig_x)))
        else:                                         # ShuntCompensator
            facts_state.append(("shunt", d.b))
    ev_state = None
    if env.ev_fleet is not None:
        ev_state = (dict(env.ev_fleet.soc), dict(env.ev_fleet.p))
    return {
        "facts": facts_state,
        "ev": ev_state,
        "curtailment_hours": env.curtailment_hours,
        "t": env.t,
        "ppc": None if env.ppc is None else copy.deepcopy(env.ppc),
    }


def restore_env(env, snap: dict) -> None:
    """Restore a snapshot produced by :func:`snapshot_env`."""
    for d, state in zip(env.facts, snap["facts"]):
        if state[0] == "upfc":
            d.shunt.b = state[1]
            d.series.k = state[2]
            d.series._orig_x = dict(state[3])
        elif state[0] == "series":
            d.k = state[1]
            d._orig_x = dict(state[2])
        else:
            d.b = state[1]
    if env.ev_fleet is not None and snap["ev"] is not None:
        soc, p = snap["ev"]
        env.ev_fleet.soc = dict(soc)
        env.ev_fleet.p = dict(p)
    env.curtailment_hours = snap["curtailment_hours"]
    env.t = snap["t"]
    env.ppc = copy.deepcopy(snap["ppc"]) if snap["ppc"] is not None else None


def vector_to_controls(env, u: np.ndarray) -> dict:
    """Map a flat action vector to the environment controls dict.

    The reserved dimension (index 5) is never emitted: the Stage-1 UPFC
    model exposes exactly two setpoints (shunt b, series k).
    """
    u = np.asarray(u, dtype=np.float64).flatten()
    facts: dict = {}
    for d in env.facts:
        if d.name == "SVC_14":
            facts["SVC_14"] = float(u[0])
        elif d.name == "STATCOM_39":
            facts["STATCOM_39"] = float(u[1])
        elif d.name == "TCSC_16_17":
            facts["TCSC_16_17"] = float(u[2])
        elif d.name == "UPFC_26":
            facts["UPFC_26"] = [float(u[3]), float(u[4])]
    ev = {}
    if env.ev_fleet is not None:
        buses = sorted(env.ev_fleet.stations.keys())
        for j, b in enumerate(buses):
            ev[str(b)] = float(u[6 + j])
    return {"facts": facts, "ev": ev}


def active_control_dims(n_actions: int = 9) -> np.ndarray:
    """Indices of physically active action dimensions (reserved excluded)."""
    return np.array([j for j in range(n_actions) if j != RESERVED_INDEX])


# ──────────────────────────────────────────────────────────────────────
# Formal reward (single shared implementation for both evaluators)
# ──────────────────────────────────────────────────────────────────────

def compute_reward(
    vm: np.ndarray,
    losses_mw: float,
    loss_ref_mw: float,
    branch_pf: np.ndarray,
    branch_rate_a: np.ndarray,
    ev_infeasibility: float,
    u: np.ndarray,
    u_prev: np.ndarray | None,
    action_lo: np.ndarray,
    action_hi: np.ndarray,
    weights: RewardWeights | None = None,
) -> float:
    """Formal, candidate-dependent reward (master plan §5.1).

    Every term is normalised; every term depends on the candidate ``u``.
    The reserved dimension is excluded from the effort term.
    """
    w = weights or RewardWeights()
    vm = np.asarray(vm, dtype=np.float64)

    # J_V — mean absolute voltage deviation (p.u.)
    j_v = float(np.mean(np.abs(vm - 1.0)))

    # J_viol — squared violation severity (Phase-P severity metric)
    sev = np.maximum(0.0, VM_MIN - vm) ** 2 + np.maximum(0.0, vm - VM_MAX) ** 2
    j_viol = float(np.sum(sev))

    # J_L — normalised losses
    j_l = float(losses_mw / loss_ref_mw) if loss_ref_mw > 0 else 0.0

    # J_th — squared thermal overload severity on rated branches
    rate_safe = np.where(branch_rate_a > 0, branch_rate_a, np.inf)
    loading = np.abs(branch_pf) / rate_safe
    j_th = float(np.sum(np.maximum(0.0, loading - 1.0) ** 2))

    # J_u — action effort over active dimensions only (reserved excluded)
    u = np.asarray(u, dtype=np.float64).flatten()
    act = active_control_dims(len(u))
    rng = action_hi[act] - action_lo[act]
    base = np.zeros(len(act)) if u_prev is None else np.asarray(u_prev, dtype=np.float64)[act]
    du = u[act] - base
    j_u = float(np.sum((du / rng) ** 2) / len(act))

    return float(
        -w.w_V * j_v
        - w.w_viol * j_viol
        - w.w_L * j_l
        - w.w_T * j_th
        - w.w_SoC * ev_infeasibility
        - w.w_u * j_u
    )


def ev_infeasibility_of(env, u: np.ndarray) -> float:
    """SoC infeasibility of an EV dispatch request (read-only).

    Mirrors the fleet's dispatch-guard arithmetic without mutating state:
    requested power clipped away (power limit or SoC window), normalised
    by the total fleet power rating.
    """
    if env.ev_fleet is None:
        return 0.0
    fleet = env.ev_fleet
    u = np.asarray(u, dtype=np.float64).flatten()
    buses = sorted(fleet.stations.keys())
    total_clipped = 0.0
    total_cap = 0.0
    for j, b in enumerate(buses):
        s = fleet.stations[b]
        p_req = float(u[6 + j])
        p_max = s["p_max_mw"]
        total_cap += p_max
        clipped = min(max(p_req, -p_max), p_max)
        soc_lo, soc_hi = s.get("soc_min", 0.2), s.get("soc_max", 0.9)
        if clipped > 0 and fleet.soc[b] >= soc_hi:
            clipped = 0.0
        if clipped < 0 and fleet.soc[b] <= soc_lo:
            clipped = 0.0
        total_clipped += abs(clipped - p_req)
    return total_clipped / total_cap if total_cap > 0 else 0.0


# ──────────────────────────────────────────────────────────────────────
# Evaluator A — exact counterfactual AC evaluation
# ──────────────────────────────────────────────────────────────────────

class ExactPowerFlowEvaluator:
    """Evaluator A: one AC power flow per candidate on a restored snapshot.

    Counterfactual states are produced by ``env._solve(controls)`` — the
    environment's own control/solve pipeline — wrapped in a snapshot so
    the live trajectory state is untouched. ``_solve`` does not advance
    the time index (only ``step`` does), so every candidate is evaluated
    at the current operating point.
    """

    def __init__(
        self,
        env,
        action_lo: np.ndarray,
        action_hi: np.ndarray,
        weights: RewardWeights | None = None,
    ) -> None:
        self.env = env
        self.action_lo = np.asarray(action_lo, dtype=np.float64)
        self.action_hi = np.asarray(action_hi, dtype=np.float64)
        self.weights = weights or RewardWeights()
        self.n_power_flows = 0

    def evaluate_all(
        self,
        env=None,
        obs: dict | None = None,
        candidates: np.ndarray | None = None,
        u_prev: np.ndarray | None = None,
    ) -> CandidateEvaluation:
        env = self.env if env is None else env
        candidates = np.atleast_2d(np.asarray(candidates, dtype=np.float64))
        n_cand = candidates.shape[0]
        rate_a = env.base_ppc["branch"][:, 3]
        loss_ref = max(env.loss_est_mw, 1e-6)

        t0 = time.perf_counter()
        snap = snapshot_env(env)
        rewards = np.zeros(n_cand, dtype=np.float64)
        vm_all = np.zeros((n_cand, env.base_ppc["bus"].shape[0]))
        overload = np.zeros(n_cand, dtype=np.int64)
        n_pf = 0
        try:
            for i in range(n_cand):
                # Reset to the live state before EVERY counterfactual: the
                # previous candidate's solve mutated device setpoints, EV
                # SoC and the curtailment counter, and candidate i+1 must
                # be evaluated from exactly the live operating point.
                restore_env(env, snap)
                u = candidates[i]
                # Request-time SoC-guard infeasibility (pre-dispatch state).
                infeas = ev_infeasibility_of(env, u)
                obs_i = env._solve(vector_to_controls(env, u))
                n_pf += 1
                vm = obs_i["vm"]
                branch_pf = obs_i["branch_pf"]
                losses = float(obs_i.get("metrics", {}).get("losses_mw", 0.0))
                vm_all[i] = vm
                if not obs_i.get("converged", False):
                    rewards[i] = NON_CONVERGED_PENALTY
                    continue
                rewards[i] = compute_reward(
                    vm, losses, loss_ref, branch_pf, rate_a,
                    infeas, u, u_prev,
                    self.action_lo, self.action_hi, self.weights,
                )
                loading = np.abs(branch_pf) / np.where(rate_a > 0, rate_a, np.inf)
                overload[i] = int(np.sum(loading > 1.0))
        finally:
            restore_env(env, snap)

        self.n_power_flows += n_pf
        return CandidateEvaluation(
            rewards=rewards,
            vm_pred=vm_all,
            overload_pred=overload,
            n_power_flows=n_pf,
            elapsed_ms=(time.perf_counter() - t0) * 1000.0,
        )


# ──────────────────────────────────────────────────────────────────────
# Evaluator B — sensitivity surrogate (real-time)
# ──────────────────────────────────────────────────────────────────────

class SensitivitySurrogateEvaluator:
    """Evaluator B: first-order Taylor surrogate of the network response.

    One refresh builds voltage/flow/loss sensitivities by finite
    differences over the *active* control dimensions (8 counterfactual
    solves through ``env._solve`` for the 9-D/1-reserved interface).
    Between refreshes all candidates are evaluated with one matrix
    product, orders of magnitude below the 50 ms budget.
    ``refresh_every=1`` linearises at every step (highest fidelity).
    """

    def __init__(
        self,
        env,
        action_lo: np.ndarray,
        action_hi: np.ndarray,
        weights: RewardWeights | None = None,
        refresh_every: int = 24,
        fd_step: float = 0.05,
    ) -> None:
        self.env = env
        self.action_lo = np.asarray(action_lo, dtype=np.float64)
        self.action_hi = np.asarray(action_hi, dtype=np.float64)
        self.weights = weights or RewardWeights()
        self.refresh_every = max(1, int(refresh_every))
        self.fd_step = fd_step
        self.n_power_flows = 0
        self._steps_since_refresh = self.refresh_every  # force first refresh
        self._S_V: np.ndarray | None = None
        self._S_F: np.ndarray | None = None
        self._s_L: np.ndarray | None = None
        self._u_ref: np.ndarray | None = None
        self._V0: np.ndarray | None = None
        self._F0: np.ndarray | None = None
        self._L0: float = 0.0
        self._rate_a: np.ndarray | None = None
        self._loss_ref: float = 1.0

    # ── current control point ────────────────────────────────────────
    def current_u(self, env) -> np.ndarray:
        u = np.zeros(len(self.action_lo), dtype=np.float64)
        for d in env.facts:
            if d.name == "SVC_14":
                u[0] = d.b
            elif d.name == "STATCOM_39":
                u[1] = d.b
            elif d.name == "TCSC_16_17":
                u[2] = d.k
            elif d.name == "UPFC_26":
                u[3] = d.shunt.b
                u[4] = d.series.k
        u[RESERVED_INDEX] = 0.0
        if env.ev_fleet is not None:
            buses = sorted(env.ev_fleet.stations.keys())
            for j, b in enumerate(buses):
                u[6 + j] = env.ev_fleet.p[b]
        return u

    # ── sensitivity refresh ──────────────────────────────────────────
    def refresh(self, env, obs: dict) -> None:
        """Rebuild sensitivities by finite differences (frozen snapshots)."""
        n_u = len(self.action_lo)
        act = active_control_dims(n_u)
        n_bus = env.base_ppc["bus"].shape[0]
        n_br = env.base_ppc["branch"].shape[0]

        u0 = self.current_u(env)
        V0 = np.asarray(obs["vm"], dtype=np.float64)
        F0 = np.asarray(obs["branch_pf"], dtype=np.float64)
        L0 = float(obs.get("metrics", {}).get("losses_mw", env.loss_est_mw))

        S_V = np.zeros((n_bus, n_u))
        S_F = np.zeros((n_br, n_u))
        s_L = np.zeros(n_u)

        snap = snapshot_env(env)
        try:
            for j in act:
                # Restore before each perturbation so no prior solve's EV
                # SoC / device mutation contaminates the next finite
                # difference.
                restore_env(env, snap)
                span = self.action_hi[j] - self.action_lo[j]
                h = self.fd_step * span
                u_pert = u0.copy()
                u_pert[j] = min(u0[j] + h, self.action_hi[j])
                obs_p = env._solve(vector_to_controls(env, u_pert))
                if obs_p.get("converged", False):
                    V1 = obs_p["vm"]
                    F1 = obs_p["branch_pf"]
                    L1 = float(obs_p.get("metrics", {}).get("losses_mw", L0))
                    dh = u_pert[j] - u0[j]
                    if abs(dh) > 1e-12:
                        S_V[:, j] = (V1 - V0) / dh
                        S_F[:, j] = (F1 - F0) / dh
                        s_L[j] = (L1 - L0) / dh
        finally:
            restore_env(env, snap)

        self.n_power_flows += len(act)
        self._S_V, self._S_F, self._s_L = S_V, S_F, s_L
        self._u_ref, self._V0, self._F0, self._L0 = u0, V0, F0, L0
        self._rate_a = env.base_ppc["branch"][:, 3]
        self._loss_ref = max(env.loss_est_mw, 1e-6)
        self._steps_since_refresh = 0

    # ── candidate evaluation ─────────────────────────────────────────
    def evaluate_all(
        self,
        env=None,
        obs: dict | None = None,
        candidates: np.ndarray | None = None,
        u_prev: np.ndarray | None = None,
    ) -> CandidateEvaluation:
        env = self.env if env is None else env
        candidates = np.atleast_2d(np.asarray(candidates, dtype=np.float64))
        t0 = time.perf_counter()

        refreshed = False
        if self._S_V is None or self._steps_since_refresh >= self.refresh_every:
            if obs is None:
                obs = env._last_obs if hasattr(env, "_last_obs") else None
            if obs is None:
                raise ValueError("surrogate needs an observation for the first refresh")
            self.refresh(env, obs)
            refreshed = True
        self._steps_since_refresh += 1

        du = candidates - self._u_ref[None, :]
        V_pred = self._V0[None, :] + du @ self._S_V.T
        F_pred = self._F0[None, :] + du @ self._S_F.T
        L_pred = np.maximum(self._L0 + du @ self._s_L, 0.0)

        n_cand = candidates.shape[0]
        rewards = np.zeros(n_cand)
        loading = np.abs(F_pred) / np.where(self._rate_a > 0, self._rate_a, np.inf)
        overload = np.sum(loading > 1.0, axis=1).astype(np.int64)
        for i in range(n_cand):
            rewards[i] = compute_reward(
                V_pred[i], float(L_pred[i]), self._loss_ref,
                F_pred[i], self._rate_a,
                ev_infeasibility_of(env, candidates[i]),
                candidates[i], u_prev,
                self.action_lo, self.action_hi, self.weights,
            )
        return CandidateEvaluation(
            rewards=rewards,
            vm_pred=V_pred,
            overload_pred=overload,
            n_power_flows=0,
            elapsed_ms=(time.perf_counter() - t0) * 1000.0,
            refreshed=refreshed,
        )


def make_evaluator(kind: str, env, action_lo, action_hi, **kwargs):
    """Factory used by System 2 and the experiment scripts."""
    kind = kind.lower()
    if kind in ("exact", "ac", "evaluator_a"):
        return ExactPowerFlowEvaluator(env, action_lo, action_hi, **kwargs)
    if kind in ("surrogate", "sensitivity", "evaluator_b"):
        return SensitivitySurrogateEvaluator(env, action_lo, action_hi, **kwargs)
    raise ValueError(f"unknown evaluator kind: {kind!r}")
