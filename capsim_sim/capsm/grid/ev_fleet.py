"""Aggregate EV fleet with V2G/G2V capability at designated buses.

Each station models an aggregated fleet of electric vehicles as one
grid-scale battery (a standard reduction for transmission-level studies).
Charging is positive net load, V2G discharge is negative net load.
"""

from pypower.idx_bus import PD


class EVFleet:
    def __init__(self, stations: dict[int, dict], dt_hours: float = 1.0, eta: float = 0.92):
        """
        stations: {bus: {"p_max_mw": float, "capacity_mwh": float,
                         "soc_min": 0.2, "soc_max": 0.9, "soc_init": 0.5}}
        """
        self.stations = stations
        self.dt = dt_hours
        self.eta = eta
        self.soc = {b: s.get("soc_init", 0.5) for b, s in stations.items()}
        self.p = {b: 0.0 for b in stations}

    def reset(self) -> None:
        self.soc = {b: s.get("soc_init", 0.5) for b, s in self.stations.items()}
        self.p = {b: 0.0 for b in self.stations}

    def dispatch(self, setpoints: dict[int, float]) -> dict[int, float]:
        """Apply power setpoints (MW, charge>0, discharge<0) within SoC/limits."""
        for b, s in self.stations.items():
            p_req = float(setpoints.get(b, 0.0))
            p_max = s["p_max_mw"]
            p_req = min(max(p_req, -p_max), p_max)
            soc_lo, soc_hi = s.get("soc_min", 0.2), s.get("soc_max", 0.9)
            cap = s["capacity_mwh"]
            if p_req > 0 and self.soc[b] >= soc_hi:
                p_req = 0.0
            if p_req < 0 and self.soc[b] <= soc_lo:
                p_req = 0.0
            energy = p_req * self.dt
            if p_req > 0:
                new_soc = self.soc[b] + energy * self.eta / cap
            else:
                new_soc = self.soc[b] + energy / self.eta / cap
            if new_soc > soc_hi:
                new_soc = soc_hi
            if new_soc < soc_lo:
                new_soc = soc_lo
            self.soc[b] = new_soc
            self.p[b] = p_req
        return dict(self.p)

    def apply(self, ppc: dict) -> None:
        for b, p in self.p.items():
            idx = ppc["bus"][:, 0] == b
            ppc["bus"][idx, PD] = ppc["bus"][idx, PD] + p

    def state(self) -> dict:
        return {"soc": dict(self.soc), "p": dict(self.p)}


def default_ev_fleet(case_name: str) -> EVFleet | None:
    """Three aggregated V2G stations on the primary test system (buses 3, 8, 15)."""
    if case_name != "case39":
        return None
    stations = {
        3: {"p_max_mw": 50.0, "capacity_mwh": 100.0},
        8: {"p_max_mw": 50.0, "capacity_mwh": 100.0},
        15: {"p_max_mw": 50.0, "capacity_mwh": 100.0},
    }
    return EVFleet(stations)
