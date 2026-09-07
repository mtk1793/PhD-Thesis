"""Event injection for the QSTS environment.

Two categories, both clearly labelled as injected events applied on top of
real measured operating conditions:
- Topology/impedance events: line trips and restorations (branch status).
- Measurement events: false data injection (FDI) on observed quantities,
  used to test the cyber-resilience of the CAPSM layers.
"""

import numpy as np
from pypower.idx_brch import BR_STATUS, BR_X


def trip_branch(ppc: dict, from_bus: int, to_bus: int) -> int:
    f = ppc["branch"][:, 0] == from_bus
    t = ppc["branch"][:, 1] == to_bus
    idx = np.flatnonzero(f & t)
    if len(idx) == 0:
        raise ValueError(f"branch {from_bus}-{to_bus} not found")
    ppc["branch"][idx, BR_STATUS] = 0
    return int(idx[0])


def restore_branch(ppc: dict, from_bus: int, to_bus: int) -> int:
    f = ppc["branch"][:, 0] == from_bus
    t = ppc["branch"][:, 1] == to_bus
    idx = np.flatnonzero(f & t)
    if len(idx) == 0:
        raise ValueError(f"branch {from_bus}-{to_bus} not found")
    ppc["branch"][idx, BR_STATUS] = 1
    return int(idx[0])


def apply_fdi(observation: dict, targets: list[int], bias: float, rng: np.random.Generator) -> dict:
    """Corrupt observed voltage magnitudes at target buses by an additive bias.

    Returns a new observation dict; the power-flow solution itself is not
    modified, mimicking a sensor/measurement-layer attack.
    """
    corrupted = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in observation.items()}
    vm = corrupted["vm"].copy()
    for b in targets:
        vm[b] = vm[b] + bias + rng.normal(0, 0.002)
    corrupted["vm"] = vm
    corrupted["fdi_active"] = True
    return corrupted
