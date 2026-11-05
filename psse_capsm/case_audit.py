"""Audit a candidate PSS/E v33 RAW file before running CAPSM experiments.

Structural checks only. A PASS does not imply successful Siemens PSS/E
import, AC power-flow convergence, or numerical equivalence to MATPOWER.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from .case import RawCase, fields

def audit(path, require_ieee39=True):
    path = Path(path)
    file_bytes = path.read_bytes()
    case = RawCase.read(path)
    bus_ids = case.bus_ids()
    generators = case.generators()
    branches = case.branch_records()
    buses = {}
    for index in case.section_indices["BUS"]:
        fields_bus = fields(case.lines[index])
        buses[int(float(fields_bus[0]))] = int(float(fields_bus[3]))
    result = {
        "filename": path.name,
        "sha256": hashlib.sha256(file_bytes).hexdigest(),
        "base_mva": case.base_mva,
        "n_bus": len(bus_ids),
        "n_gen": len(generators),
        "n_branch_total": len(branches),
        "n_line": len(case.section_indices["BRANCH"]),
        "n_transformer_two_winding": len(branches)-len(case.section_indices["BRANCH"]),
        "slack_bus_ids": [b for b,k in buses.items() if k==3],
        "bus39_type": buses.get(39),
        "unique_bus_ids": len(bus_ids)==len(set(bus_ids)),
        "unrated_branches": sum(int(x[3]<=0) for x in branches if x[4]),
        "unresolved_branch_buses": [list(x[:2]) for x in branches if x[0] not in buses or x[1] not in buses],
        "supported_raw_revision": int(float(fields(case.lines[0])[2]))==33,
        "errors": [],
    }
    if not result["unique_bus_ids"]:
        result["errors"].append("duplicate bus numbers")
    if result["unresolved_branch_buses"]:
        result["errors"].append("branch references nonexistent bus")
    if not result["supported_raw_revision"]:
        result["errors"].append("RAW revision is not 33; this editor is for v33 import compatibility")
    if require_ieee39:
        if result["n_bus"] != 39:
            result["errors"].append("expected 39 buses")
        if result["n_gen"] != 10:
            result["errors"].append("expected 10 generators")
        if result["n_branch_total"] != 46:
            result["errors"].append("expected 46 AC branches including transformers")
        if result["n_line"] != 34:
            result["errors"].append("expected 34 non-transformer branches")
        if result["slack_bus_ids"] != [31]:
            result["errors"].append("case39 benchmark expects bus 31 slack")
        if result["bus39_type"] != 2:
            result["errors"].append("case39 benchmark expects bus 39 PV")
    result["status"] = "PASS_STRUCTURAL" if not result["errors"] else "FAIL_STRUCTURAL"
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--case",required=True)
    ap.add_argument("--output")
    ap.add_argument("--generic",action="store_true")
    args=ap.parse_args()
    report=audit(args.case,require_ieee39=not args.generic)
    result=json.dumps(report,indent=2)
    print(result)
    if args.output:
        Path(args.output).write_text(result+"\n",encoding="utf-8")
    if report["errors"]:
        raise SystemExit(2)

if __name__=="__main__":
    main()
