# Phase 1 Report - Real-Data Layer: Loading, Gap Policy, Disaggregation

**Project:** CAPSM Stage-1 offline validation (Python rebuild)
**Status:** Complete (8/8 unit tests passing)
**Date:** 2026-09-06

## 1. What Was Done

1. **OPSD loader** (`capsm/data/opsd.py`): reads the verified hourly file,
   selects the 18 German national and control-area series, parses UTC
   timestamps, removes duplicates, and caches the result as a parquet file
   (`data/processed/opsd_de_60min.parquet`, 50,401 hourly records).
2. **Documented gap policy** (the only data modification in the pipeline):
   gaps of up to two consecutive steps are filled by time-based linear
   interpolation and flagged in per-column boolean masks
   (`*_interp`); longer gaps and boundary gaps remain NaN and are excluded
   from metric aggregation. Nothing else is ever altered or synthesised.
3. **Temporal splits** for machine-learning work without temporal leakage:
   training 2015-2017, validation 2018, test 2019 to September 2020. A
   separate price window (October 2018 onward) governs all economic
   experiments, reflecting the actual availability of the DE-LU day-ahead
   price feed.
4. **Disaggregation** (`capsm/data/disaggregate.py`): maps the real German
   profiles onto the IEEE test systems:
   - Bus active loads follow the real national load shape (or, regionally,
     the four control-area shapes 50Hertz / Amprion / TenneT / TransnetBW,
     with bus-group sizes matching each area's real mean share of national
     load: 18.8% / 37.7% / 31.0% / 12.5%).
   - The magnitude of each case's total load equals the case's native base
     load, so power-flow behaviour stays within the case's designed range
     (e.g., IEEE 39-bus total 6,254 MW).
   - Wind and solar injections follow the real German generation profiles,
     scaled to a configurable long-run penetration (default: 20% wind,
     10% solar of native mean load) and placed at designated buses as
     negative load.
5. **Extreme-event mining**: the largest real renewable ramp events (1-hour
   and 3-hour windows) were extracted from the measured series for later use
   as stress scenarios (Phase 6).
6. **Unit tests** (8 tests): gap-policy semantics, split disjointness, load
   share normalisation, profile conservation (bus loads reproduce the
   national shape exactly), penetration targeting, and verification that
   the committed sample week is genuine measured data.

## 2. Gap-Policy Results on the Full Dataset

| Series | Interpolated (<= 2 h) | Left NaN |
|---|---|---|
| Load actual | 1 | 0 |
| Load forecast | 1 | 24 |
| Solar generation | 0 | 104 |
| Wind onshore | 1 | 72 |
| Wind offshore | 3 | 72 |
| Day-ahead price | 5 | 32,856 (pre-Oct-2018 absence) |

Interpretation: after the policy, the national load series is 100% complete
across 2015-2020; solar and wind retain 72-104 missing hours (0.14-0.21%),
which are excluded from aggregation rather than imputed. The price NaN
count corresponds exactly to the period before the ENTSO-E DE-LU price feed
began (verified: 2018-09-30 to 2020-09-30, 17,540 real price points).

## 3. Dataset Splits (for thesis methodology section)

| Split | Period | Hours |
|---|---|---|
| Training | 2015-01-01 to 2017-12-31 | 26,304 |
| Validation | 2018-01-01 to 2018-12-31 | 8,760 |
| Test | 2019-01-01 to 2020-09-30 | 15,336 |
| Price window | 2018-09-30 to 2020-09-30 | 17,540 prices |

## 4. Renewable Penetration Setup (per test system)

Default penetration: 20% wind, 10% solar (long-run means, of native base
load). Placement sites are documented modelling assumptions:

| Case | Native base load (MW) | Mean wind (MW) | Mean solar (MW) | Wind buses | Solar buses |
|---|---|---|---|---|---|
| IEEE 9 | 315 | 62.9 | 31.4 | 7 | 9 |
| IEEE 14 | 259 | 51.7 | 25.8 | 4, 9 | 6, 13 |
| IEEE 39 | 6,254 | 1,249.0 | 624.1 | 4, 14 | 8, 15 |
| IEEE 118 | 4,242 | 847.2 | 423.3 | 10, 25, 49 | 12, 34, 71 |
| IEEE 300 | 23,526 | 4,698.4 | 2,347.7 | 17, 57, 121 | 33, 90, 195 |

The maximum instantaneous renewable share reaches 115.7% of native base
load, mirroring the real German phenomenon of renewable output exceeding
demand during low-load, high-wind/sun hours (e.g., 2019 holidays) - these
are the operating conditions that stress-test the CAPSM voltage and
congestion control.

## 5. Extreme Real Events Mined (Phase 6 stress scenarios)

- Largest 1-hour ramp: +20,040 MW up and -20,128 MW down (combined wind +
  solar, national).
- Largest 3-hour ramp: +28,390 MW up and -23,588 MW down.
- The 40 largest events per window are stored in
  `results/phase1/ramp_events_1h.csv` and `ramp_events_3h.csv` with
  timestamps, ramp magnitude, and start/end levels, ready for direct use as
  reproducible scenario injections.

## 6. Figures Produced (usable in thesis)

- `fig_p1_load_weeks.png` - real winter vs summer weekly load traces
- `fig_p1_diurnal_seasonal.png` - mean diurnal load by season
- `fig_p1_top_ramp.png` - the largest 3-h renewable ramp with load overlay
- `fig_p1_duration_curves.png` - 2019 wind and solar duration curves

## 7. Verification Performed

- 8/8 unit tests pass, including exact conservation checks (bus-level loads
  reproduce the national profile times the native base load to numerical
  precision) and penetration targeting to 1e-9 relative tolerance.
- The gap policy was validated on synthetic NaN patterns (test fixture
  only) to confirm short gaps are filled, long gaps are left as NaN, and
  valid points are never modified.
- A one-week slice of genuine OPSD data (192 hourly records,
  `tests/data/sample_opsd_week.csv`) is committed so the test suite runs
  without the 124 MB download.

## 8. Notes for Thesis Writing

- Data-modification transparency: only linear interpolation of gaps of at
  most two steps is applied; every filled value is flagged and countable
  (report in `results/phase1/gap_policy_report.json`). This directly
  addresses the "real data integrity" question an examiner will ask.
- The negative-price hours (min -90.01 EUR/MWh) in the price window are
  directly usable in the V2G/G2V scheduling experiments: charging during
  negative prices is a real, observed economic phenomenon.
