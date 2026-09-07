"""Quasi-Static Time-Series (QSTS) power system environment on real data.

Each step advances one timestamp of the real OPSD-driven profiles, applies
the current controller actions (FACTS setpoints, EV dispatch), runs an AC
power flow with PYPOWER, and returns the system observation plus metrics.

Contingencies (line trips) and cyber events (FDI) are injected on top of
the real operating conditions and are always reported as such.
"""

import copy
from typing import Callable

import numpy as np
import pandas as pd
from pypower.api import ppoption, runpf
from pypower.idx_brch import PF, PT, RATE_A
from pypower.idx_bus import BUS_TYPE, PD, QD, REF
from pypower.idx_gen import GEN_BUS, PG, PMAX

from capsm.data.disaggregate import build_bus_loads, build_renewables, get_case
from capsm.grid.ev_fleet import EVFleet, default_ev_fleet
from capsm.grid.facts import default_facts
from capsm.grid.metrics import metrics_from_ppc
from capsm.grid import events as evt

VM_COL = 7
VA_COL = 8


class QSTSEnvironment:
    def __init__(
        self,
        case_name: str,
        profiles: pd.DataFrame,
        regional: bool = True,
        wind_penetration: float = 0.20,
        solar_penetration: float = 0.10,
        facts: list | None = None,
        ev_fleet: EVFleet | None = None,
        dt_hours: float = 1.0,
        curtail_share: float = 0.90,
        gen_factor_min: float = 0.20,
        gen_factor_max: float = 1.50,
        tune_gen_voltages: float = 1.04,
    ):
        self.case_name = case_name
        self.base_ppc = get_case(case_name)
        if tune_gen_voltages is not None:
            self._tune_gen_voltages(tune_gen_voltages)
        self.dt = dt_hours
        self.bus_ids = self.base_ppc["bus"][:, 0].astype(int)
        self._bus_pos = {int(b): i for i, b in enumerate(self.bus_ids)}
        self.curtail_share = curtail_share
        self.gen_factor_min = gen_factor_min
        self.gen_factor_max = gen_factor_max

        self.bus_loads = build_bus_loads(case_name, profiles, regional=regional)
        renewables = build_renewables(case_name, profiles, wind_penetration, solar_penetration)
        self.re_sites = renewables
        self.timestamps = self.bus_loads.index
        self.n_steps = len(self.timestamps)

        self.facts = facts if facts is not None else default_facts(case_name)
        self.ev_fleet = ev_fleet if ev_fleet is not None else default_ev_fleet(case_name)
        if self.ev_fleet is not None:
            self.ev_fleet.dt = dt_hours

        self.ppopt = ppoption(VERBOSE=0, OUT_ALL=0)
        self.rng = np.random.default_rng(0)
        self.t = 0
        self.ppc = None
        self._tripped: list[tuple[int, int]] = []

        self.base_net_load = float(np.sum(self.base_ppc["bus"][:, PD]))
        base_result, base_ok = runpf(copy.deepcopy(self.base_ppc), self.ppopt)
        if base_ok:
            self.loss_est_mw = float(np.sum(base_result["branch"][:, PF] + base_result["branch"][:, PT]))
        else:
            self.loss_est_mw = 0.01 * self.base_net_load
        self.curtailment_hours = 0

    def _tune_gen_voltages(self, vcap: float) -> None:
        """Cap generator voltage setpoints at vcap (base-case preparation).

        The raw IEEE cases ship with VG setpoints above the 1.05 p.u.
        planning limit (e.g., bus 36 in case39 at 1.064), which would
        register as violations unrelated to the real-data operation under
        study. Setpoints above the cap are reduced to it (both in the gen
        matrix, which is what the power flow regulates to, and the bus
        initial-voltage column); all other case data are untouched.
        """
        from pypower.idx_gen import VG

        gen = self.base_ppc["gen"]
        high = gen[:, VG] > vcap
        self._n_vg_tuned = int(high.sum())
        if high.any():
            gen[high, VG] = vcap
            gen_buses = set(gen[high, GEN_BUS].astype(int).tolist())
            bus = self.base_ppc["bus"]
            for i in range(bus.shape[0]):
                if int(bus[i, 0]) in gen_buses:
                    bus[i, VM_COL] = min(bus[i, VM_COL], vcap)

    def reset(self, start: str | None = None, seed: int | None = None) -> dict:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.ppc = copy.deepcopy(self.base_ppc)
        self._tripped = []
        self.curtailment_hours = 0
        for d in self.facts:
            if hasattr(d, "series"):
                d.set(0.0, 0.0)
                d.series._orig_x = {}
            else:
                d.set(0.0)
        if self.ev_fleet is not None:
            self.ev_fleet.reset()
        if start is not None:
            self.t = int(np.searchsorted(self.timestamps, pd.Timestamp(start, tz="UTC")))
        return self._solve(controls=None)

    def step(self, controls: dict | None = None) -> dict:
        self.t += 1
        if self.t >= self.n_steps:
            self.t = self.n_steps - 1
        return self._solve(controls)

    def _apply_controls(self, controls: dict | None) -> None:
        if not controls:
            return
        for name, value in controls.get("facts", {}).items():
            dev = next((d for d in self.facts if d.name == name), None)
            if dev is not None:
                if hasattr(dev, "series"):
                    b, k = value if isinstance(value, (list, tuple)) else (value, value)
                    dev.set(b, k)
                elif hasattr(dev, "k_min"):
                    dev.set(float(value))
                else:
                    dev.set(float(value))
        if self.ev_fleet is not None and "ev" in controls:
            self.ev_fleet.dispatch(controls["ev"])

    def _solve(self, controls: dict | None, load_scale: float = 1.0) -> dict:
        assert self.ppc is not None, "call reset() first"
        ppc = copy.deepcopy(self.base_ppc)
        self._apply_controls(controls)
        for d in self.facts:
            d.apply(ppc)
        ts = self.timestamps[self.t]
        load_vec = self.bus_loads.iloc[self.t].to_numpy() * load_scale
        ppc["bus"][:, PD] = load_vec
        ppc["bus"][:, QD] = self._build_qd(load_vec)

        re_mw: dict[int, float] = {}
        if len(self.re_sites.columns):
            row = self.re_sites.iloc[self.t]
            for col, mw in row.items():
                bus = int(col.split("_bus_")[1])
                re_mw[bus] = re_mw.get(bus, 0.0) + float(mw)
        load_sum = float(np.sum(load_vec))
        re_total = -sum(re_mw.values())
        if re_total > self.curtail_share * load_sum and re_total > 0:
            scale = self.curtail_share * load_sum / re_total
            re_mw = {b: v * scale for b, v in re_mw.items()}
            self.curtailment_hours += 1
        for b, mw in re_mw.items():
            i = self._bus_pos[b]
            ppc["bus"][i, PD] += mw

        if self.ev_fleet is not None:
            self.ev_fleet.apply(ppc)

        net_load = float(np.sum(ppc["bus"][:, PD]))
        factor = (net_load + self.loss_est_mw) / (self.base_net_load + self.loss_est_mw)
        factor = min(max(factor, self.gen_factor_min), self.gen_factor_max)
        self._redispatch(ppc, factor)

        for f_bus, t_bus in self._tripped:
            evt.trip_branch(ppc, f_bus, t_bus)
        result, success = runpf(ppc, self.ppopt)
        obs = {
            "timestamp": ts,
            "converged": bool(success),
            "vm": result["bus"][:, VM_COL].copy(),
            "va": result["bus"][:, VA_COL].copy(),
            "branch_pf": result["branch"][:, PF].copy(),
            "branch_pt": result["branch"][:, PT].copy(),
            "total_load_mw": float(np.sum(load_vec)),
            "total_gen_mw": float(np.sum(result["gen"][:, PG])) if success else None,
            "metrics": metrics_from_ppc(result) if success else {},
            "ev_state": self.ev_fleet.state() if self.ev_fleet else None,
        }
        self.ppc = result
        return obs

    def _redispatch(self, ppc: dict, factor: float) -> None:
        """Scale non-slack generator setpoints proportionally to net load."""
        ref_buses = set(ppc["bus"][ppc["bus"][:, BUS_TYPE] == REF, 0].astype(int).tolist())
        gen = ppc["gen"]
        for i in range(gen.shape[0]):
            if int(gen[i, GEN_BUS]) in ref_buses:
                continue
            new_pg = gen[i, PG] * factor
            pmax = gen[i, PMAX]
            if pmax > 0:
                new_pg = min(new_pg, pmax)
            gen[i, PG] = new_pg

    def _qd_ratio(self) -> np.ndarray:
        base_pd = self.base_ppc["bus"][:, PD]
        base_qd = self.base_ppc["bus"][:, QD]
        ratio = np.zeros_like(base_qd)
        nz = base_pd > 0
        ratio[nz] = base_qd[nz] / base_pd[nz]
        return ratio

    def _build_qd(self, load_vec: np.ndarray) -> np.ndarray:
        """Reactive load at constant per-bus power factor (flat case exact)."""
        qd = self.base_ppc["bus"][:, QD].copy()
        nz = load_vec > 0
        base_pd = self.base_ppc["bus"][:, PD]
        scale = np.ones_like(load_vec)
        scale[nz] = load_vec[nz] / base_pd[nz]
        return qd * scale

    def trip_line(self, from_bus: int, to_bus: int) -> None:
        if (from_bus, to_bus) not in self._tripped:
            self._tripped.append((from_bus, to_bus))

    def restore_line(self, from_bus: int, to_bus: int) -> None:
        if (from_bus, to_bus) in self._tripped:
            self._tripped.remove((from_bus, to_bus))

    def run(self, controls_fn: Callable | None = None, start=None, n_steps: int | None = None,
            on_event: Callable | None = None) -> pd.DataFrame:
        """Run a full QSTS trajectory and return a metrics DataFrame."""
        obs = self.reset(start=start)
        rows = [self._row(obs)]
        n = n_steps if n_steps is not None else self.n_steps - self.t - 1
        for _ in range(n):
            controls = controls_fn(obs, self) if controls_fn else None
            if on_event is not None:
                on_event(self, obs)
            obs = self.step(controls)
            rows.append(self._row(obs))
        return pd.DataFrame(rows).set_index("timestamp")

    def _row(self, obs: dict) -> dict:
        row = {"timestamp": obs["timestamp"], **obs["metrics"],
               "total_load_mw": obs["total_load_mw"], "converged": obs["converged"],
               "total_gen_mw": obs["total_gen_mw"]}
        if obs["ev_state"]:
            row["ev_soc_mean"] = float(np.mean(list(obs["ev_state"]["soc"].values())))
            row["ev_p_total"] = float(np.sum(list(obs["ev_state"]["p"].values())))
        return row
