"""System metrics computed from a converged power-flow solution."""

import numpy as np
from pypower.idx_brch import PF, PT, RATE_A

VM_MIN = 0.95
VM_MAX = 1.05


def metrics_from_ppc(ppc: dict) -> dict:
    bus = ppc["bus"]
    branch = ppc["branch"]
    vm = bus[:, 7]
    losses = float(np.sum(branch[:, PF] + branch[:, PT]))
    rate = branch[:, RATE_A]
    rate_safe = np.where(rate > 0, rate, np.inf)
    loading = np.abs(branch[:, PF]) / rate_safe
    # Phase-P severity metric: squared voltage-limit exceedance (p.u.^2)
    severity = float(np.sum(
        np.maximum(0.0, VM_MIN - vm) ** 2 + np.maximum(0.0, vm - VM_MAX) ** 2
    ))
    dev = np.abs(vm - 1.0)
    return {
        "losses_mw": losses,
        "vm_mean": float(np.mean(vm)),
        "vm_min": float(np.min(vm)),
        "vm_max": float(np.max(vm)),
        "voltage_deviation_pu": float(np.mean(dev)),
        "p95_voltage_dev_pu": float(np.percentile(dev, 95)),
        "violation_severity_pu2": severity,
        "max_line_loading": float(np.max(loading)),
        "n_overloaded_lines": int(np.sum(loading > 1.0)),
        "thermal_overload_severity": float(np.sum(np.maximum(0.0, loading - 1.0) ** 2)),
        "n_voltage_violations": int(np.sum((vm < VM_MIN) | (vm > VM_MAX))),
    }
