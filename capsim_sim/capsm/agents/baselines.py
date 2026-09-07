"""Baseline controllers for CAPSM benchmarking.

All controllers share one interface: act(obs, env) -> controls dict for
the QSTS environment. They use only locally available measurements
(voltage at the device bus), as conventional local controllers do.
"""

import numpy as np


class NoControl:
    name = "no_control"

    def act(self, obs, env):
        return {}

    def reset(self):
        pass


class RuleBasedVoltage:
    """Droop-style volt/VAR control: b = Kp * (Vref - V_local)."""

    name = "rule_based"

    def __init__(self, kp: float = 5.0, vref: float = 1.0):
        self.kp = kp
        self.vref = vref

    def reset(self):
        pass

    def act(self, obs, env):
        if not obs.get("converged"):
            return {}
        facts = {}
        for d in env.facts:
            if hasattr(d, "series"):
                pos = int(np.flatnonzero(env.bus_ids == d.shunt.bus)[0])
                err = self.vref - obs["vm"][pos]
                facts[d.name] = [self.kp * err, 0.0]
            elif hasattr(d, "k_min"):
                facts[d.name] = 0.0
            else:
                pos = int(np.flatnonzero(env.bus_ids == d.bus)[0])
                err = self.vref - obs["vm"][pos]
                facts[d.name] = self.kp * err
        return {"facts": facts}


class PIDVoltage:
    """PI volt/VAR control with per-device integral state."""

    name = "pid"

    def __init__(self, kp: float = 4.0, ki: float = 0.5, vref: float = 1.0):
        self.kp = kp
        self.ki = ki
        self.vref = vref
        self._integral: dict[str, float] = {}

    def reset(self):
        self._integral = {}

    def act(self, obs, env):
        if not obs.get("converged"):
            return {}
        facts = {}
        for d in env.facts:
            if hasattr(d, "series"):
                pos = int(np.flatnonzero(env.bus_ids == d.shunt.bus)[0])
                err = self.vref - obs["vm"][pos]
                self._integral[d.name] = self._integral.get(d.name, 0.0) + err
                facts[d.name] = [self.kp * err + self.ki * self._integral[d.name], 0.0]
            elif hasattr(d, "k_min"):
                facts[d.name] = 0.0
            else:
                pos = int(np.flatnonzero(env.bus_ids == d.bus)[0])
                err = self.vref - obs["vm"][pos]
                self._integral[d.name] = self._integral.get(d.name, 0.0) + err
                facts[d.name] = self.kp * err + self.ki * self._integral[d.name]
        return {"facts": facts}


BASELINES = [NoControl, RuleBasedVoltage, PIDVoltage]


def run_controller(env, controller, start=None, n_steps=None, with_trip=None):
    """Run one controller over the horizon; returns a metrics DataFrame.

    with_trip: (timestamp_str, from_bus, to_bus, restore_after_steps) to
    inject a contingency mid-run (None restore = permanent trip).
    """
    import pandas as pd

    controller.reset()
    trip = with_trip
    injected = False
    injected_at = None

    obs = env.reset(start=start)
    rows = [env._row(obs)]
    n = n_steps if n_steps is not None else env.n_steps - env.t - 1
    for _ in range(n):
        controls = controller.act(obs, env)
        if trip is not None and not injected:
            ts_str, f_bus, t_bus, restore_after = trip
            if str(env.timestamps[env.t + 1]) >= ts_str:
                env.trip_line(f_bus, t_bus)
                injected = True
                injected_at = len(rows)
                print(f"[{controller.name}] trip {f_bus}-{t_bus} injected at {env.timestamps[env.t + 1]}")
        obs = env.step(controls)
        rows.append(env._row(obs))
        if injected and trip is not None and trip[3] is not None:
            if len(rows) - injected_at >= trip[3]:
                env.restore_line(trip[1], trip[2])
                trip = None
                print(f"[{controller.name}] line restored")
    return pd.DataFrame(rows).set_index("timestamp")
