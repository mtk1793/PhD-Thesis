# Phase 2 Report - QSTS Grid Environment on Real Data

**Project:** CAPSM Stage-1 offline validation (Python rebuild)
**Status:** Complete (16/16 unit tests passing; 100% power-flow convergence on all test systems)
**Date:** 2026-09-06

## 1. What Was Built

1. **QSTS environment** (`capsm/grid/environment.py`): each step takes one
   timestamp of the real OPSD profiles, applies controller actions, runs an
   AC power flow with PYPOWER (Newton), and returns the observation
   (bus voltage magnitudes/angles, branch flows) plus system metrics.
   Real German load shapes at native case magnitudes, real wind/solar
   injections at designated buses, real control-area disaggregation.
2. **FACTS models** (`capsm/grid/facts.py`): SVC and STATCOM as controllable
   shunt susceptance, TCSC as controllable series reactance
   (X_eff = (1-k)X), UPFC as combined shunt + series. Thesis placement on
   IEEE 39-bus: SVC@14, STATCOM@39, TCSC 16-17, UPFC@26.
3. **EV fleet** (`capsm/grid/ev_fleet.py`): three aggregated V2G/G2V
   stations (buses 3, 8, 15; 50 MW / 100 MWh each) with SoC dynamics,
   efficiency losses, and SoC bounds.
4. **Events** (`capsm/grid/events.py`): line trip/restore (branch status)
   and false-data-injection on the observation layer (sensor attack
   model). All events are injected contingencies on top of real operating
   conditions and reported as such.
5. **Metrics** (`capsm/grid/metrics.py`): losses, voltage deviation,
   min/max voltage, line loading, violation counts.

## 2. Two Documented Modelling Rules (required for convergence)

Running real profiles through the raw IEEE cases exposed a genuine
modelling problem: on low-load, high-wind nights (real German New Year
conditions, e.g., 2019-01-01 00:00 UTC) net load collapses to under half
the base case while wind approaches the full 20% penetration target. With
fixed base-case generator setpoints the slack must absorb a multi-GW
imbalance and the Newton power flow diverges. Two standard, explicitly
documented rules resolve this:

- **Renewable curtailment rule:** if total wind+solar injection would
  exceed 90% of the current load, injections are scaled down to that cap.
  This mirrors actual TSO curtailment practice. In January 2019 it
  activates in 15 of 721 hours (2.1%) - real, rare, extreme hours.
- **Proportional generation redispatch:** non-slack generator P setpoints
  scale with net load (factor clipped to [0.2, 1.5], capped at Pmax);
  the slack bus balances. This is the classical QSTS dispatch
  approximation.

With these rules the environment converges for **100% of timestamps** on
every test system (below). Both rules are configurable and their
activation is counted and reported (no hidden data manipulation).

## 3. Verification Results (real OPSD data, January 2019)

| System | Steps | Converged | Mean losses (MW) | min Vm (p.u.) | ms/step |
|---|---|---|---|---|---|
| IEEE 39 (full month) | 721 | 721 (100%) | 46.1 | 0.877 | 7.8 |
| IEEE 9 (week) | 145 | 145 (100%) | 4.4 | 0.925 | ~2 |
| IEEE 14 (week) | 145 | 145 (100%) | 9.2 | 0.990 | ~3 |
| IEEE 118 (week) | 145 | 145 (100%) | 220.0 | 0.773 | ~15 |

Uncontrolled IEEE 39-bus, January 2019 (the stress the CAPSM controllers
must address):
- Total load range: 3,861 - 7,748 MW (real German shape on native scale)
- Losses: mean 46.1 MW, peak 245.4 MW
- Voltages: min 0.877 p.u., max 1.074 p.u.; mean deviation 0.029 p.u.
- Voltage-limit violations: 2,847 bus-hours (0.95 / 1.05 p.u. limits)
- Overloaded lines: 900 line-hours; peak line loading 4.40 x rating
- Renewable curtailment activated: 15 hours (2.1% of the month)

## 4. Contingency Injection (line 16-17 trip, 2019-01-15 12:00 UTC)

Under real operating conditions at the moment of injection:
- Losses rise from 51.1 MW (pre-event mean) to 58.7 MW (+14.9%)
- Minimum system voltage: 0.951 p.u. during the contingency window
- Power flow remains converged (N-1 secure for this contingency at this
  operating point), and restoration returns the system to the exact
  pre-contingency state (verified numerically in tests)

## 5. Unit Tests (16 total; 8 data-layer from Phase 1 + 8 grid-layer)

- Power flow through the environment matches a direct PYPOWER run exactly
  when profiles are flat (validates the load/renewable/EV/FACTS plumbing)
- SVC raises its local voltage; TCSC changes its branch flow (same-timestep
  comparisons, device effects isolated from load changes)
- EV dispatch respects power and SoC bounds across 20+ consecutive steps
- Line trip changes flows; restoration reproduces the pre-event flows
  bit-for-bit
- FDI corrupts only the targeted measurements
- Full QSTS trajectory returns a complete metrics frame

## 6. Figures Produced (usable in thesis)

- `fig_p2_qsts_case39_jan2019.png` - one-month uncontrolled QSTS: load,
  losses, voltage envelope vs 0.95/1.05 limits
- `fig_p2_line_trip.png` - contingency response: losses and min-voltage
  around the injected trip

## 7. Notes for Thesis Writing

- The convergence failure without redispatch/curtailment is itself a
  reportable finding: it demonstrates why fixed-setpoint baselines are
  invalid under deep renewable penetration, and motivates the dispatch
  model used throughout.
- The 15 curtailment hours are real extreme events (renewables above 90%
  of load at national scale) - they can be cross-referenced with the
  Phase 1 ramp-event tables as scenario anchors.
- All voltages/flows/losses above are real-data-driven results, suitable
  for Chapter 10 (simulation platform) and Chapter 11 (uncontrolled
  baseline) of the thesis.

## 8. Base-Case VG Tuning (applied retroactively)

The raw IEEE 39-bus case ships with generator voltage setpoints up to
1.064 p.u. (bus 36), above the 1.05 p.u. planning limit. These cause
persistent violations inherent to the case data, not to real-data
operation. Generator VG setpoints are capped at 1.04 p.u. in the
environment constructor (documented, configurable). This removed
~2,386 false-positive violation bus-hours, leaving 2,847 genuine
operational violations for the baselines to address.
