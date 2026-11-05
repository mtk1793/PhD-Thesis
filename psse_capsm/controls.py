"""Presentation-aligned nine-position FACTS/EV action and energy constraints."""
from __future__ import annotations
from dataclasses import dataclass
import math
from .case import RawCase

ACTION_NAMES = (
    "SVC_14", "STATCOM_39", "TCSC_16_17", "UPFC_26_shunt",
    "UPFC_26_series_proxy", "UPFC_26_series_Q_RESERVED", "EV_3", "EV_8", "EV_15"
)
LO = (-0.5, -1.0, 0.3, -0.5, -0.5, 0.0, -50.0, -50.0, -50.0)
HI = (0.5, 1.0, 0.7, 0.5, 0.5, 0.0, 50.0, 50.0, 50.0)
EV_BUSES = (3, 8, 15)
RESERVED = 5

@dataclass
class EVFleet:
    soc: tuple = (0.5, 0.5, 0.5)
    capacity_mwh: float = 100.0
    max_mw: float = 50.0
    eta: float = 0.92
    soc_min: float = 0.2
    soc_max: float = 0.9

    def dispatch(self, requests, hours=1.0, commit=False):
        if hours <= 0 or self.capacity_mwh <= 0 or not 0 < self.eta <= 1:
            raise ValueError("Invalid time step, capacity, or efficiency")
        if len(requests) != 3:
            raise ValueError("Expected three EV dispatch requests")
        outputs, next_soc = [], []
        for old_soc, requested in zip(self.soc, requests):
            p = max(-self.max_mw, min(self.max_mw, float(requested)))
            max_charge = max(0.0, (self.soc_max - old_soc) * self.capacity_mwh / (self.eta * hours))
            max_discharge = max(0.0, (old_soc - self.soc_min) * self.capacity_mwh * self.eta / hours)
            p = max(-max_discharge, min(p, max_charge))
            new_soc = old_soc + (p * hours * self.eta / self.capacity_mwh if p >= 0
                                 else p * hours / (self.eta * self.capacity_mwh))
            new_soc = max(self.soc_min, min(self.soc_max, new_soc))
            outputs.append(p)
            next_soc.append(new_soc)
        if commit:
            self.soc = tuple(next_soc)
        return tuple(outputs), tuple(next_soc)

    def copy(self):
        return EVFleet(tuple(self.soc), self.capacity_mwh, self.max_mw,
                       self.eta, self.soc_min, self.soc_max)


def clamp_action(action):
    if len(action) != 9:
        raise ValueError("CAPSM action length must be exactly 9")
    a = tuple(max(lo, min(hi, float(v))) for v, lo, hi in zip(action, LO, HI))
    if not all(math.isfinite(v) for v in a):
        raise ValueError("Nonfinite action")
    return a[:RESERVED] + (0.0,) + a[RESERVED+1:]


def apply_action(case: RawCase, action, fleet: EVFleet, hours=1.0,
                 statcom_bus=39, commit=False):
    """Edit *only* a fresh case clone; no PSS/E simulator or fleet mutation when commit=False.

    SVC/STATCOM/UPFC-shunt are fixed-B susceptance equivalents, NOT dynamic
    device models. UPFC series is an X compensation proxy, not injected P/Q.
    The slack-bus STATCOM is intentionally retained as the historical setup;
    relocation is an explicit experiment.
    """
    a = clamp_action(action)
    p_ev, soc = fleet.dispatch(a[6:9], hours=hours, commit=commit)
    case.set_fixed_shunt(14, "SV", a[0])
    case.set_fixed_shunt(statcom_bus, "ST", a[1])
    case.set_branch_x(16, 17, "1", a[2])
    case.set_fixed_shunt(26, "UP", a[3])
    case.set_branch_x(26, 28, "1", a[4])
    for bus, p in zip(EV_BUSES, p_ev):
        case.add_load(bus, "EV", p, 0.0)
    return {"action":a, "ev_mw":p_ev, "soc_next":soc, "statcom_bus":statcom_bus}
