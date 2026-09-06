# Phase 0 Report - Real-Data Foundation and Verified Acquisition

**Project:** CAPSM Stage-1 offline validation (Python rebuild)
**Status:** Complete
**Date:** 2026-09-06

## 1. What Was Done

The previous implementation (`HIL_Project/python`) claimed OPSD support but its
loader ignored the real data and always generated synthetic sinusoidal
profiles, meaning all previously reported simulation numbers were produced from
artificial data. This phase establishes a verified, fully reproducible
real-data foundation for the entire Stage-1 rebuild:

1. A new clean package (`capsim_sim`) was created, independent of the legacy
   code, containing a streaming downloader with cryptographic verification and
   an automated integrity analysis pipeline.
2. Both OPSD time-series files were downloaded from the official data platform
   and verified by size and SHA-256 hash. A provenance manifest records the
   dataset version (2020-10-06), DOI, official attribution string, download
   date, and file hashes.
3. A data integrity analysis was executed on both files, quantifying temporal
   coverage, missing timestamps, duplicate timestamps, NaN counts, and gap
   structure for every German national and control-area series required by
   the CAPSM experiments.

Because the raw files exceed GitHub's 100 MB size limit, they are excluded
from version control by a `.gitignore` rule; the committed provenance manifest
and downloader make acquisition deterministic and verifiable on any machine.

## 2. Data Source (for thesis Chapter 10 / data section)

- **Dataset:** Open Power System Data (OPSD), Data Package *Time series*,
  version 2020-10-06.
- **DOI:** https://doi.org/10.25832/time_series/2020-10-06
- **Primary source:** ENTSO-E Transparency Platform (real measured values
  published by transmission system operators and power exchanges).
- **Geography:** Germany (national) plus the four German control areas
  (50Hertz, Amprion, TenneT GER, TransnetBW) for spatial disaggregation.
- **Resolution:** hourly (60-min file, 50,401 rows) and 15-minute
  (15-min file, 201,604 rows).
- **Verified files (SHA-256 in `data/raw/provenance_manifest.json`):**

| File | Bytes | SHA-256 (first 16) |
|---|---|---|
| time_series_60min_singleindex.csv | 130,339,665 | 6a7f2bc571314cbf |
| time_series_15min_singleindex.csv | 112,072,477 | 194f3ee7d110d043 |

**Attribution:** Open Power System Data. 2020. Data Package Time series.
Version 2020-10-06. https://doi.org/10.25832/time_series/2020-10-06.
(Primary data: ENTSO-E Transparency Platform.)

## 3. Integrity Results (real measurements)

### 3.1 Hourly file (2015-01-01 to 2020-09-30 UTC; 50,401 hourly records)

| Series | NaN | NaN % | Gaps > 2 h | Mean (MW) |
|---|---|---|---|---|
| DE load actual | 1 | 0.002% | 0 | 55,492.5 |
| DE load forecast (day-ahead) | 25 | 0.050% | 1 | 54,791.4 |
| DE solar generation actual | 104 | 0.206% | 5 | 4,566.0 |
| DE wind generation actual | 75 | 0.149% | 3 | 11,552.2 |
| DE wind onshore actual | 73 | 0.145% | 3 | 9,581.5 |
| DE wind offshore actual | 75 | 0.149% | 3 | 1,970.5 |
| 50Hertz load / solar / wind | 1 / 15 / 1 | <=0.03% | 0-2 | 10,404.5 / 1,177.3 / 3,724.3 |
| Amprion load / solar / wind | 1 / 14 / 1 | <=0.03% | 0-2 | 20,943.0 / 1,051.5 / 1,857.2 |
| TenneT load / solar / wind | 1 / 8 / 1 | <=0.02% | 0-1 | 17,184.7 / 1,692.7 / 5,725.3 |
| TransnetBW load / solar / wind | 1 / 15 / 1 | <=0.03% | 0-2 | 6,960.5 / 641.0 / 248.0 |

### 3.2 Day-ahead electricity price (DE-LU bidding zone)

- **Coverage:** 2018-09-30 to 2020-09-30 only (17,540 hourly values); the
  ENTSO-E Transparency price feed for the DE-LU zone begins October 2018, so
  the remaining 65.2% of the file range is legitimately absent rather than
  corrupt.
- **Statistics:** min -90.01, mean 35.81, max 200.04 EUR/MWh. The series
  contains real negative-price hours, which are directly relevant to the
  EV V2G/G2V scheduling and economic-dispatch experiments.

### 3.3 15-minute file

Confirms the same series at higher resolution (201,604 quarter-hourly
records, 2015-01-01 to 2020-09-30); NaN rates are consistent with the hourly
file (load 0.003%, solar 0.208%, wind 0.151%).

## 4. Findings That Shape the Experimental Design

1. **Load, wind, and solar data are effectively complete.** German national
   and control-area load series are missing a single hour in five and a half
   years; solar and wind are missing roughly 0.15-0.2% of hours. These series
   can drive the full QSTS (quasi-static time-series) simulation without
   any imputation for most analyses.
2. **Time-based dataset splits are well supported.** The five-and-a-half-year
   span allows a strict chronological split (training: 2015-2017, validation:
   2018, test: 2019-2020) with no temporal leakage.
3. **Price-based experiments are constrained to October 2018 onward.** Any
   experiment whose reward or objective uses day-ahead prices (economic
   dispatch, V2G scheduling, cost-savings analysis) must use the
   2018-10 to 2020-09 window, which still provides two full years and
   17,540 hours of real prices, including negative-price events.
4. **Gap policy (to be implemented in Phase 1).** Short gaps of up to two
   steps will be linearly interpolated and flagged; longer gaps will be
   excluded from metric aggregation rather than imputed. No synthetic or
   randomly generated profiles will be introduced anywhere in the pipeline.
5. **Control-area series enable spatial disaggregation.** Load, solar, and
   wind are available for all four German TSO control areas, allowing
   geographically differentiated allocation onto IEEE test-system buses
   instead of a single national scaling factor.

## 5. Artifacts Produced

- `capsm/data/download.py` - streaming download, size + SHA-256 verification,
  provenance manifest writer
- `capsm/data/integrity.py` - coverage, NaN census, gap-run analysis, JSON +
  Markdown report generation
- `scripts/phase0_data.py` - one-command reproduction of this phase
- `data/raw/provenance_manifest.json` - committed provenance record
- `data/integrity_report.json`, `data/integrity_report.md` - committed
  integrity results

## 6. Verification Performed

- Both downloads completed and passed the size threshold check.
- SHA-256 hashes computed and recorded; re-running the script with files
  present skips downloads and re-verifies hashes.
- Integrity analysis executed on all 19 key hourly columns and 6 key
  15-minute columns; counts cross-checked against file dimensions
  (50,401 and 201,604 rows respectively).
