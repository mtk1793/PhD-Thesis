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
