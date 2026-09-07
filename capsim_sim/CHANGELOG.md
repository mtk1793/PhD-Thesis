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

## Phase 2 - QSTS grid environment on real data

- Implemented `capsm/grid/environment.py`: PYPOWER AC power flow per
  timestamp driven by real profiles; controller interface for FACTS
  setpoints and EV dispatch.
- Implemented FACTS models (SVC/STATCOM shunt, TCSC series, UPFC combined,
  thesis placement on IEEE 39-bus), aggregate EV V2G fleet (buses 3/8/15),
  event injection (line trips, FDI), and system metrics.
- Added two documented modelling rules required for convergence under deep
  renewable penetration: 90% renewable curtailment cap (activated 15 h in
  Jan 2019) and proportional generation redispatch with slack balancing.
- Fixed: pandas 3.0 iloc boolean-mask assignment silently dropping values
  (switched to numpy matrix construction); EV dispatch being overwritten by
  load assignment; reactive load now scales at constant power factor.
- 8 new unit tests (16 total, all passing); verification runs: 100%
  convergence on IEEE 9/14/39/118 over real Jan-2019 data; 7.8 ms/step on
  IEEE 39-bus; contingency injection validated (losses +23.2% on line
  16-17 trip).
- Artifacts in `results/phase2/`; thesis write-up in
  `reports/PHASE2_REPORT.md`.

Verified: 16/16 tests pass; month-long QSTS on case39 converged 721/721
steps; trip/restore reproduces pre-contingency flows exactly.

## Phase 3 - Baseline controllers and vulnerability benchmark

- Implemented `capsm/agents/baselines.py`: NoControl, RuleBasedVoltage (Kp=5
  local droop), PIDVoltage (Kp=5, Ki=2 local PI) at thesis FACTS locations.
- Implemented `capsm/grid/stability.py`: loading-margin bisection (binary
  search on load-scale factor until Newton diverges).
- Added base-case VG tuning: generator voltage setpoints capped at 1.04 pu
  to remove false-positive violations from raw IEEE case artifacts (e.g.,
  bus 36 in case39 at 1.064 pu).
- Fixed `run_controller` contingency injection: injected flag prevents
  re-firing every step; restore-after correctly triggers after delay.
- January 2019 benchmark (case39, 721 h): 2847 violation bus-hours
  (uncontrolled); rule-based reduces by 1 hour, PID by 5. Local droop/PI
  at SVC@14/STATCOM@39 is ineffective because violations concentrate at
  buses 22-29, electrically distant from device locations. Generator voltage
  regulation at device buses overrides shunt injection.
- Loading margins: valley (2388 MW) = 2.53x, peak (6195 MW) = 1.45x.
- N-1 contingency (line 16-17 trip at peak): +14.9% losses, min vm 0.951,
  full convergence — system robust to single contingencies.
- 6 new unit tests (22 total, all passing).
- Artifacts in `results/phase3/`; thesis write-up in
  `reports/PHASE3_REPORT.md`.

Verified: 22/22 tests pass; local controllers near-zero impact motivates
CAPSM coordinated AI control architecture.
