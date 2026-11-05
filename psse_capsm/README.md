# CAPSM – PSS/E v35 Simulation Layer (2026-11)

Simulation-first implementation based on the thesis defence presentation, with
the September 30, 2026 scientific rebuild as the authoritative code/evidence
baseline. **This does not modify historical PYPOWER/HIL results.**

## Scope actually implemented

- PSS/E v35 RAW import and fresh-case AC power-flow evaluation through psspy.
- IEEE 39-bus CAPSM fixed placements; 9-position control interface with
  **eight active dimensions**, reserved index 5 forced to zero.
- SVC@14, STATCOM@39, TCSC 16–17, UPFC-at-26 shunt and series-X proxy.
- EV aggregate charging/discharging at buses 3, 8, 15; per-station 100 MWh,
  ±50 MW, η=0.92; SoC must remain 0.2–0.9.
- OPSD-shaped hourly profiles: total load multiplier and renewable MW values.
  The data shape is real where actual OPSD input is supplied; the bus-wise
  allocation is a **synthetic research assumption**.
- NoControl, local droop, 32-candidate QIRL-style stochastic selection, and
  exact greedy selection. All exact candidates are assessed using independent
  fresh RAW imports of the same operating point.
- JSONL measurement/action trajectories for downstream PyTorch training.
- PSS/E run manifests never self-certify measured evidence.

## Important limits

This is an **AC QSTS prototype**, not the full CAPSM, full HIL, RMS dynamic,
PINN, HMARL, fault detection, or true UPFC converter model. PSS/E's license
and executable are unavailable in the development environment: import,
convergence, and vendor API behaviour require local verification.

The PSS/E v35 process should use the **Python version supported by the
installed 35.x minor version**. Do not force a modern PyTorch installation
into that interpreter. Use separate Python environments for PSS/E and Torch.
Current reference controller code remains in capsim_sim/capsm/agents.

## Input profiles

CSV header: timestamp,load_scale,wind_mw,solar_mw

The real OPSD 2020-10-06 hourly series should be transformed to this format
using the same train 2015–2017 / validate 2018 / test 2019 separation as the
revised thesis code. Wind is split evenly between buses 4 and 14; solar
between buses 8 and 15. Wind and solar are represented as **negative loads**,
not dynamic IBR models. Load reactive power scales with load active power.

## Commands (Windows, from repository root)

    py -3.9 -m pytest psse_capsm/tests -q

    python -m psse_capsm.run_simulation ^
      --case "C:\CAPSM\IEEE39_NewEngland_REPAIRED_v33.raw" ^
      --profiles "C:\CAPSM\profiles\jan2019.csv" ^
      --policy none --output psse_runs\none

    python -m psse_capsm.run_simulation ^
      --case "C:\CAPSM\IEEE39_NewEngland_REPAIRED_v33.raw" ^
      --profiles "C:\CAPSM\profiles\jan2019.csv" ^
      --policy qirl_exact --candidates 32 --seed 42 ^
      --output psse_runs\qirl_exact

Use --dry-run to check input transformations without importing PSS/E.
A valid converged IEEE 39-bus .raw case is required. The directory does not
claim its own arbitrary RAW case is an IEEE benchmark.

### PSS/E v35 integration

From a Siemens PTI-supported Python interpreter and configured PSSE module
paths, the adapter calls psseinit, read, fnsl, solved, busdat, macdat and
brnflo. Tested offline with a fake psspy adapter only; **real PSS/E must
validate function contracts** for your installed minor version.

### PyTorch integration stage

The simulation emits machine-readable JSONL containing pre-action state,
post-action result, the selected action, EV SoC, and scenario metadata.
The next integration stage maps these records to the canonical IEEE-39
160-feature StateEncoder and the September-30 CNN–LSTM checkpoint/training
pipeline. Do not train or publish a PSS/E-dependent controller until the
input feature mapping, action timing and simulator import tests pass.

## Scientific checks before use in Chapter 11

1. Verify IEEE-39 topology: 39 buses, 10 machines and 46 total AC branches
   including the 12 transformers.
2. Compare no-control PSS/E base-case voltages, branch powers, and losses with
   the source benchmark, documenting material differences.
3. Verify shunt sign and size: 1 p.u. equivalent B changes BL by 100 MVAr
   for a 100 MVA base, with actual reactive output depending on V squared.
4. Verify each FACTS proxy produces a consistent physical response.
5. Confirm EV applied MW, charging losses and SoC change exactly once per step.
6. Check same-state candidate determinism and full snapshot isolation.
7. Verify PSS/E branch loading from both ends in MVA; unrated branches are
   reported separately, never counted as secure.
8. Preserve separate evidence types: old Stage-1 (superseded); new measured
   PSS/E runs; design targets; independently traceable HIL results.

See docs/PRESENTATION_ALIGNMENT.md and docs/VALIDATION_GATES.md.
