"""System metrics computed from a converged power-flow solution."""

import numpy as np
from pypower.idx_brch import PF, PT, RATE_A


def metrics_from_ppc(ppc: dict) -> dict:
    bus = ppc["bus"]
    branch = ppc["branch"]
    vm = bus[:, 7]
    losses = float(np.sum(branch[:, PF] + branch[:, PT]))
    rate = branch[:, RATE_A]
    rate_safe = np.where(rate > 0, rate, np.inf)
    loading = np.abs(branch[:, PF]) / rate_safe
    return {
        "losses_mw": losses,
        "vm_mean": float(np.mean(vm)),
        "vm_min": float(np.min(vm)),
        "vm_max": float(np.max(vm)),
        "voltage_deviation_pu": float(np.mean(np.abs(vm - 1.0))),
        "max_line_loading": float(np.max(loading)),
        "n_overloaded_lines": int(np.sum(loading > 1.0)),
        "n_voltage_violations": int(np.sum((vm < 0.95) | (vm > 1.05))),
    }
