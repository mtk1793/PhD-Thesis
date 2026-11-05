"""Convert cleaned OPSD hourly CSV to CAPSM PSS/E QSTS scenario profiles.

CSV is expected to have the processed columns used by capsim_sim:
timestamp, load_actual_mw, wind_onshore_mw, wind_offshore_mw, solar_mw.

Only 2015–2017 train-window statistics scale the outputs. The target is an
IEEE test system (base load 6254 MW for case39), not a German-grid model.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import math
from pathlib import Path

def _float(value):
    v=float(value)
    if not math.isfinite(v):
        raise ValueError("NaN / infinity in cleaned OPSD profile")
    return v

def prepare(input_csv, output_csv, base_load_mw=6254.0, wind_share=.20,
            solar_share=.10):
    rows=[]
    with open(input_csv,"r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        required={"timestamp","load_actual_mw","wind_onshore_mw","wind_offshore_mw","solar_mw"}
        missing=required-set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing OPSD columns: "+", ".join(sorted(missing)))
        for source in reader:
            stamp=source["timestamp"].strip()
            year=int(stamp[:4])
            rows.append({"timestamp":stamp,"year":year,
                         "load":_float(source["load_actual_mw"]),
                         "wind":_float(source["wind_onshore_mw"])+_float(source["wind_offshore_mw"]),
                         "solar":_float(source["solar_mw"])})
    if not rows:
        raise ValueError("No OPSD rows")
    if len({r["timestamp"] for r in rows})!=len(rows):
        raise ValueError("Duplicate timestamps")
    if any(rows[i]["timestamp"]>=rows[i+1]["timestamp"] for i in range(len(rows)-1)):
        raise ValueError("Input OPSD timestamps must be strictly increasing")
    train=[r for r in rows if 2015<=r["year"]<=2017]
    if not train:
        raise ValueError("Missing 2015–2017 training data")
    def mean(key):
        return sum(r[key] for r in train)/len(train)
    load_ref, wind_ref, solar_ref=mean("load"),mean("wind"),mean("solar")
    if min(load_ref,wind_ref,solar_ref)<=0:
        raise ValueError("Training-period means must be positive")
    out=Path(output_csv);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["timestamp","load_scale","wind_mw","solar_mw"])
        writer.writeheader()
        for r in rows:
            writer.writerow({"timestamp":r["timestamp"],
                             "load_scale":format(r["load"]/load_ref,".8f"),
                             "wind_mw":format(r["wind"]/wind_ref*wind_share*base_load_mw,".6f"),
                             "solar_mw":format(r["solar"]/solar_ref*solar_share*base_load_mw,".6f")})
    return {"output":str(out),"n_rows":len(rows),"train_rows":len(train),
            "train_years":[2015,2016,2017],"validation_year":2018,
            "test_year":2019,"train_load_mean_mw":load_ref,
            "train_wind_mean_mw":wind_ref,"train_solar_mean_mw":solar_ref,
            "base_load_mw":base_load_mw,"wind_mean_target_mw":wind_share*base_load_mw,
            "solar_mean_target_mw":solar_share*base_load_mw}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--base-load-mw",type=float,default=6254)
    args=ap.parse_args()
    import json
    print(json.dumps(prepare(args.input,args.output,args.base_load_mw),indent=2))
if __name__=="__main__":
    main()
