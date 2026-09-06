# CAPSM Stage-1 Simulation (Real-Data Rebuild)

Offline Python validation of the CAPSM (Cognitive Adaptive Power System
Management) framework, rebuilt from scratch and driven **exclusively by real
measured data** from the Open Power System Data (OPSD) platform.

## Data

- Dataset: OPSD Time series, version 2020-10-06
- DOI: https://doi.org/10.25832/time_series/2020-10-06
- Primary source: ENTSO-E Transparency Platform (real measured load, wind,
  solar, day-ahead prices; Germany 2015 to mid-2020, hourly and 15-minute)
- Raw CSVs are too large for git and are excluded via `.gitignore`.
  Reproduce them with:

```bash
python scripts/phase0_data.py
```

This downloads both files, verifies their size and SHA-256 hash, and writes
`data/raw/provenance_manifest.json` plus `data/integrity_report.{json,md}`.

## Package layout

```
capsim_sim/
  capsm/
    data/        download, integrity, (phase 1: opsd loader, disaggregation)
    grid/        (phase 2: PYPOWER QSTS environment, FACTS, EV, events)
    agents/      (phase 4-6: system1, system2, arbiter, baselines)
  scripts/       phase entry points
  configs/       experiment configurations
  tests/         unit tests
  data/          raw + processed data (gitignored)
  results/       generated tables and figures
  reports/       per-phase thesis write-ups
```

## Attribution

Open Power System Data. 2020. Data Package Time series. Version 2020-10-06.
https://doi.org/10.25832/time_series/2020-10-06. (Primary data: ENTSO-E
Transparency Platform.)
