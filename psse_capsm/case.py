"""Conservative PSS/E v33 RAW editor for CAPSM quasi-static experiments.

Runs under Python 3.8+ with standard library only. Retains untouched RAW
records verbatim. Any edits are explicit and written to a *temporary copy*.
The original benchmark is never modified.
"""
from __future__ import annotations
import copy
import csv
import re
from pathlib import Path

SECTIONS = ("BUS", "LOAD", "FIXED SHUNT", "GENERATOR", "BRANCH", "TRANSFORMER")
_TRANSITION = re.compile(r"^\s*0\s*/\s*END OF .*?,\s*BEGIN\s+(.+?)\s+DATA", re.I)
_NUMERIC = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?$")


def fields(record):
    content = record.split(" / ", 1)[0].strip()
    return [v.strip() for v in next(csv.reader([content], delimiter=",", quotechar="'", skipinitialspace=True))]


def fmt(items):
    def quote(v):
        s = str(v).strip()
        if _NUMERIC.fullmatch(s):
            return s.replace("D", "E")
        return "'" + s.replace("'", "''") + "'"
    return ", ".join(quote(x) for x in items)


def _is_data(line):
    s = line.strip()
    return bool(s and not s.startswith(("0 /", "Q", "@", "!")))


class RawCase:
    def __init__(self, text):
        self.lines = text.splitlines()
        self.section_indices = {k: [] for k in SECTIONS}
        self.section_end = {}
        self._reindex()
        if len(self.section_indices["BUS"]) == 0:
            raise ValueError("No bus records found; expected PSS/E v33-compatible RAW")
        self.base_mva = float(fields(self.lines[0])[1])

    @classmethod
    def read(cls, path):
        return cls(Path(path).read_text(encoding="utf-8-sig", errors="replace"))

    def clone(self):
        return copy.deepcopy(self)

    def _reindex(self):
        self.section_indices = {k: [] for k in SECTIONS}
        self.section_end = {}
        section = "BUS"
        for index, line in enumerate(self.lines):
            transition = _TRANSITION.search(line)
            if transition:
                self.section_end[section] = index
                section = transition.group(1).strip().upper()
                continue
            if section in self.section_indices and index >= 3 and _is_data(line):
                self.section_indices[section].append(index)

    def _mutate(self, section, match, edit, required=True):
        count = 0
        for i in self.section_indices[section]:
            row = fields(self.lines[i])
            if match(row):
                edit(row)
                self.lines[i] = fmt(row)
                count += 1
        if required and not count:
            raise KeyError("No matching %s record" % section)
        return count

    def bus_ids(self):
        return [int(float(fields(self.lines[i])[0])) for i in self.section_indices["BUS"]]

    def branch_records(self):
        result = []
        for i in self.section_indices["BRANCH"]:
            r = fields(self.lines[i])
            result.append((int(r[0]), int(r[1]), r[2], float(r[6]), int(float(r[13])) if len(r) > 13 else 1))
        return result

    def generators(self):
        return [(int(fields(self.lines[i])[0]), fields(self.lines[i])[1]) for i in self.section_indices["GENERATOR"]]

    def load_buses(self):
        return [int(float(fields(self.lines[i])[0])) for i in self.section_indices["LOAD"]]

    def set_load_scale(self, scale):
        if scale < 0:
            raise ValueError("load scale must be nonnegative")
        for i in self.section_indices["LOAD"]:
            r = fields(self.lines[i])
            # PL, QL columns of PSS/E v33 load record; preserve power factor.
            if len(r) < 7:
                raise ValueError("Malformed PSS/E load record at line %d" % (i + 1))
            r[5] = str(float(r[5]) * scale)
            r[6] = str(float(r[6]) * scale)
            self.lines[i] = fmt(r)

    def add_load(self, bus, identity, p_mw, q_mvar=0.0):
        bus = int(bus)
        if bus not in self.bus_ids():
            raise KeyError("load references missing bus %d" % bus)
        identity = str(identity)
        if len(identity) > 2:
            raise ValueError("PSS/E load identifier must be at most two characters")
        for i in self.section_indices["LOAD"]:
            r = fields(self.lines[i])
            if int(float(r[0])) == bus and r[1] == identity:
                raise ValueError("duplicate load id %s at bus %d" % (identity, bus))
        if "LOAD" not in self.section_end:
            raise ValueError("RAW LOAD section delimiter missing")
        line = fmt([bus, identity, 1, 1, 1, p_mw, q_mvar, 0, 0, 0, 0, 1, 1, 0])
        self.lines.insert(self.section_end["LOAD"], line)
        self._reindex()

    def set_fixed_shunt(self, bus, identity, susceptance_pu):
        bus = int(bus)
        identity = str(identity)
        if bus not in self.bus_ids():
            raise KeyError("shunt references missing bus %d" % bus)
        if len(identity) > 2:
            raise ValueError("fixed shunt identifier at most two characters")
        # PSS/E BL is MVAr at 1 pu, not a per-unit number.
        b_mvar = float(susceptance_pu) * self.base_mva
        count = self._mutate("FIXED SHUNT",
            lambda r: int(float(r[0])) == bus and r[1] == identity,
            lambda r: r.__setitem__(4, str(b_mvar)), required=False)
        if not count:
            if "FIXED SHUNT" not in self.section_end:
                raise ValueError("RAW FIXED SHUNT section delimiter missing")
            self.lines.insert(self.section_end["FIXED SHUNT"], fmt([bus, identity, 1, 0, b_mvar]))
            self._reindex()

    def set_branch_x(self, from_bus, to_bus, ckt, compensation):
        k = float(compensation)
        if not (-0.5 <= k <= 0.7):
            raise ValueError("series compensation outside supported interval")
        def matches(r):
            a, b = int(float(r[0])), int(float(r[1]))
            return {a, b} == {int(from_bus), int(to_bus)} and r[2] == str(ckt)
        def update(r):
            r[4] = str(float(r[4]) * (1.0 - k))
        self._mutate("BRANCH", matches, update)

    def trip_branch(self, from_bus, to_bus, ckt="1"):
        def matches(r):
            return {int(float(r[0])), int(float(r[1]))} == {int(from_bus), int(to_bus)} and r[2] == str(ckt)
        self._mutate("BRANCH", matches, lambda r: r.__setitem__(13, "0"))

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")
        return path
