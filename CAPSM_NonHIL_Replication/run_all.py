from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, load_real_opsd, seed_everything, write_json
from system1_faults import run as run_s1
from system2_qirl_dqn import run as run_s2
from pinn_constraints import run as run_pinn
from hmarl_scaling import run as run_hmarl


def main():
    ap=argparse.ArgumentParser(description="CAPSM non-HIL thesis replication")
    ap.add_argument("--data",default=None,help="Full OPSD hourly CSV/parquet; bundled genuine OPSD week is fallback")
    ap.add_argument("--fast",action="store_true",help="Short CI/smoke run")
    args=ap.parse_args()
    seed_everything()
    df=load_real_opsd(args.data)
    print(f"[CAPSM] data={df.attrs.get('source_path')} rows={len(df)} full_opsd={df.attrs.get('is_full_opsd')}")
    out={}
    print("[1/4] System-1 fault classification")
    out["system1"]=run_s1(args.data,args.fast)
    print("[2/4] System-2 QIRL vs DQN")
    out["system2"]=run_s2(args.data,args.fast)
    print("[3/4] PINN/safety constraint experiment")
    out["pinn"]=run_pinn(args.data,args.fast)
    print("[4/4] HMARL scalability")
    out["hmarl"]=run_hmarl(args.data,args.fast)
    out["provenance"]={
        "data_source":df.attrs.get("source_path"),
        "full_opsd":bool(df.attrs.get("is_full_opsd",False)),
        "rows":len(df),
        "statement":"All exogenous operating points come from measured OPSD data. Faults/cyber events are reproducibly injected because the repository contains no measured labelled PMU fault corpus.",
        "hil_excluded":True,
    }
    write_json("replication_summary.json",out)
    print(json.dumps({
        "system1_fault_accuracy_pct":100*out["system1"]["mean_fault_accuracy_7_classes"],
        "system1_latency_ms":out["system1"]["mean_detection_latency_ms"],
        "qirl_conv_ep":out["system2"]["qirl"]["convergence_episode"],
        "dqn_conv_ep":out["system2"]["dqn"]["convergence_episode"],
        "qirl_faster_pct":out["system2"]["qirl_faster_percent"],
        "pinn_before_per10k":out["pinn"]["data_only_violations_per_10000"],
        "pinn_after_per10k":out["pinn"]["pinn_violations_per_10000"],
        "pinn_compliance_pct":out["pinn"]["pinn_compliance_percent"],
        "hmarl_ieee39_accuracy_pct":next(x["accuracy_percent"] for x in out["hmarl"]["results"] if x["system"]=="IEEE-39"),
        "results":str(RESULTS / "replication_summary.json")
    },indent=2))

if __name__=="__main__": main()
