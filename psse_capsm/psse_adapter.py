"""Licensed PSS/E v35 execution adapter. No torch or pandas imports.

Run in the Python environment shipped/supported by the installed PSS/E 35.x
minor release. The caller must configure Siemens PTI module paths first.
"""
from __future__ import annotations
import math
import time

class PsseUnavailable(RuntimeError):
    pass

class Psse35:
    def __init__(self, max_buses=2000, psspy_module=None):
        if psspy_module is None:
            try:
                import psse35  # noqa: F401
            except ImportError:
                pass
            try:
                import psspy
            except ImportError as exc:
                raise PsseUnavailable("PSS/E v35 psspy not found; use your licensed PSS/E-supported Python") from exc
        else:
            psspy = psspy_module
        self.p = psspy
        rc = self.p.psseinit(max_buses)
        if rc not in (0, None):
            raise RuntimeError("PSS/E psseinit ierr=%s" % rc)

    def _check(self, ierr, name):
        if ierr not in (0, None):
            raise RuntimeError("%s returned ierr=%s" % (name, ierr))

    def solve(self, raw_path, bus_ids, branches, generators):
        """Import RAW afresh each time to guarantee scenario/candidate isolation."""
        p = self.p
        started = time.perf_counter()
        self._check(p.read(0, str(raw_path)), "read")
        self._check(p.fnsl([0, 0, 0, 1, 1, 0, 99, 0]), "fnsl")
        if p.solved() != 0:
            return {"converged": False, "solved_code": p.solved(),
                    "elapsed_ms": (time.perf_counter() - started) * 1000}
        bus_vm, bus_ang = [], []
        for bus in bus_ids:
            ierr, value = p.busdat(bus, "PU")
            self._check(ierr, "busdat PU %d" % bus)
            bus_vm.append(float(value))
            ierr, value = p.busdat(bus, "ANGLE")
            self._check(ierr, "busdat ANGLE %d" % bus)
            bus_ang.append(float(value))
        gen_pq = []
        for bus, gid in generators:
            for key in ("P", "Q"):
                ierr, v = p.macdat(bus, str(gid), key)
                self._check(ierr, "macdat %d %s" % (bus, key))
                gen_pq.append(float(v))
        lines, losses, rating_missing = [], 0.0, 0
        for i, j, ckt, rate_a, status in branches:
            if status == 0:
                lines.append({"from": i, "to": j, "ckt": ckt, "in_service": False,
                              "s_from_mva": 0.0, "s_to_mva": 0.0, "pct_rate_a": None})
                continue
            ierr, forward = p.brnflo(i, j, str(ckt))
            self._check(ierr, "brnflo forward %d-%d" % (i, j))
            ierr, reverse = p.brnflo(j, i, str(ckt))
            self._check(ierr, "brnflo reverse %d-%d" % (j, i))
            losses += float((forward + reverse).real)
            percent = 100.0 * max(abs(forward), abs(reverse)) / rate_a if rate_a > 0 else None
            rating_missing += int(rate_a <= 0)
            lines.append({"from": i, "to": j, "ckt": ckt, "in_service": True,
                          "s_from_mva": float(abs(forward)), "s_to_mva": float(abs(reverse)),
                          "p_from_mw": float(forward.real), "pct_rate_a": percent})
        return {
            "converged": True, "vm": bus_vm, "va_deg": bus_ang,
            "bus_numbers": list(bus_ids), "gen_pq": gen_pq, "lines": lines,
            "losses_mw": losses,
            "voltage_deviation_pu": sum(abs(v - 1.0) for v in bus_vm) / len(bus_vm),
            "voltage_violation_count": sum((v < 0.95 or v > 1.05) for v in bus_vm),
            "voltage_violation_severity": sum(max(0, 0.95-v)**2 + max(0, v-1.05)**2 for v in bus_vm),
            "thermal_overload_severity": sum(max(0, x["pct_rate_a"]/100-1)**2
                                             for x in lines if x["pct_rate_a"] is not None),
            "thermal_overload_count": sum(x["pct_rate_a"] > 100
                                           for x in lines if x["pct_rate_a"] is not None),
            "unrated_branches": rating_missing,
            "elapsed_ms": (time.perf_counter() - started) * 1000,
        }
