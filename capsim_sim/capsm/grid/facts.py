"""Static var compensator and FACTS device models for PYPOWER QSTS.

Devices are modelled as direct steady-state admittance modifications, which
is the standard quasi-static representation:

- SVC: controllable shunt susceptance at a bus (thyristor-controlled).
- STATCOM: controllable shunt susceptance with a wider range (VSC-based,
  modelled here in its steady-state linear operating region).
- TCSC: controllable series reactance on a branch (effective reactance
  X_eff = (1 - k) * X, k in [0, k_max]).
- UPFC: combined shunt susceptance at a bus and series compensation on a
  branch.
"""

import numpy as np
from pypower.idx_brch import BR_X
from pypower.idx_bus import BS


class ShuntCompensator:
    """SVC or STATCOM: controllable shunt susceptance at a bus."""

    def __init__(self, name: str, kind: str, bus: int, b_min: float, b_max: float):
        self.name = name
        self.kind = kind
        self.bus = bus
        self.b_min = b_min
        self.b_max = b_max
        self.b = 0.0

    def set(self, value: float) -> float:
        self.b = float(min(max(value, self.b_min), self.b_max))
        return self.b

    def apply(self, ppc: dict) -> None:
        idx = np.flatnonzero(ppc["bus"][:, 0] == self.bus)
        for i in idx:
            ppc["bus"][i, BS] = ppc["bus"][i, BS] + self.b


class SeriesCompensator:
    """TCSC: controllable series compensation on a branch."""

    def __init__(self, name: str, from_bus: int, to_bus: int, k_min: float = 0.0, k_max: float = 0.7):
        self.name = name
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.k_min = k_min
        self.k_max = k_max
        self.k = 0.0
        self._orig_x: dict[int, float] = {}

    def _branch_indices(self, ppc: dict) -> np.ndarray:
        f = ppc["branch"][:, 0] == self.from_bus
        t = ppc["branch"][:, 1] == self.to_bus
        return np.flatnonzero(f & t)

    def set(self, value: float) -> float:
        self.k = float(min(max(value, self.k_min), self.k_max))
        return self.k

    def apply(self, ppc: dict) -> None:
        for i in self._branch_indices(ppc):
            if i not in self._orig_x:
                self._orig_x[i] = ppc["branch"][i, BR_X]
            ppc["branch"][i, BR_X] = (1.0 - self.k) * self._orig_x[i]


class UPFC:
    """Combined shunt susceptance and series compensation."""

    def __init__(self, name: str, bus: int, from_bus: int, to_bus: int,
                 b_min: float = -0.5, b_max: float = 0.5, k_max: float = 0.5):
        self.name = name
        self.shunt = ShuntCompensator(f"{name}_shunt", "UPFC", bus, b_min, b_max)
        self.series = SeriesCompensator(f"{name}_series", from_bus, to_bus, 0.0, k_max)

    def set(self, b: float, k: float) -> None:
        self.shunt.set(b)
        self.series.set(k)

    def apply(self, ppc: dict) -> None:
        self.shunt.apply(ppc)
        self.series.apply(ppc)


def default_facts(case_name: str) -> list:
    """Thesis placement for the primary test system (IEEE 39-bus)."""
    if case_name != "case39":
        return []
    return [
        ShuntCompensator("SVC_14", "SVC", 14, -0.5, 0.5),
        ShuntCompensator("STATCOM_39", "STATCOM", 39, -1.0, 1.0),
        SeriesCompensator("TCSC_16_17", 16, 17, 0.0, 0.7),
        UPFC("UPFC_26", 26, 26, 28),
    ]
