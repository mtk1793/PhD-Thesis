# Changelog

## Phase 0 - Scaffold and verified real-data acquisition

- Created `capsim_sim` package skeleton.
- Implemented `capsm/data/download.py`: streaming download of the two OPSD
  time-series files (60-min and 15-min singleindex), size check, SHA-256
  hashing, and a provenance manifest with the official OPSD citation and DOI.
- Implemented `capsm/data/integrity.py`: temporal coverage, missing
  timestamps, duplicate detection, NaN census, and gap-run analysis for all
  German national and control-area columns (load, solar, wind, prices).
- Added `scripts/phase0_data.py` entry point.
- Raw data files (124 MB and 107 MB) exceed GitHub's 100 MB limit, so they
  are gitignored; the manifest with hashes makes downloads verifiable and
  reproducible.

Verified: both files downloaded, size-verified, SHA-256 recorded; integrity
report generated and committed.

## Phase 1 - Real-data layer

- Implemented `capsm/data/opsd.py`: OPSD loader with parquet cache, documented
  gap policy (linear interpolation of gaps <= 2 steps, flagged; longer gaps
  left NaN), chronological train/val/test splits, price window, and
  extreme renewable ramp mining.
- Implemented `capsm/data/disaggregate.py`: bus-level load allocation from
  real German national/control-area profiles onto IEEE 9/14/39/118/300
  systems at native case magnitudes; renewable placement at documented
  buses at 20% wind / 10% solar penetration.
- 8 unit tests added (gap policy, splits, shares, conservation, penetration).
- Sanity figures + ramp event tables + penetration summary in
  `results/phase1/`; thesis write-up in `reports/PHASE1_REPORT.md`.

Verified: 8/8 tests pass; gap counts reconcile with Phase 0 integrity
report; price NaN count equals pre-October-2018 period exactly.
