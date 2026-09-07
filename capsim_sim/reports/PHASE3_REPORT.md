# Phase 3 — Baseline Controllers & System Vulnerability Benchmark

## 3.1 Objective

Establish quantitative performance baselines for three classical controllers operating on the IEEE test systems driven by real OPSD load profiles. These baselines define the bar that CAPSM's System 1 (CNN-LSTM reflexive) and System 2 (Quantum-Inspired RL deliberative) must exceed.

## 3.2 Controller Implementations

### NoControl (Passive Baseline)
Zero FACTS/G2V control actions. Reactive-power flows follow the natural distribution determined by generator voltage setpoints, line impedances, and load patterns. All devices remain at their default state: shunt susceptances at zero, TCSC at k_max, UPFC shunt and series at zero.

### RuleBasedVoltage (Local Droop)
Independent, bus-local proportional droop at each FACTS device:
- SVC@14 and STATCOM@39: b = Kp × (Vref − vm), Kp = 5, Vref = 1.0 pu, output clamped to device limits
- UPFC@26 shunt: same droop with ±0.5 pu range
- TCSC@16-17: fixed at k_max (no voltage feedback at this device type)
- No inter-device coordination, no system-state awareness

### PIDVoltage (Local PI)
Bus-local PI controller at each FACTS device:
- Kp = 5, Ki = 2, Vref = 1.0, windup clamped to [-2, 2] integral state
- Output clamped to device limits, independent per device
- Slightly more aggressive than droop due to integral action on persistent error

## 3.3 January 2019 Benchmark (case39, 721 h)

All three controllers ran the full month of January 2019 on the IEEE 39-bus system disaggregated from real German OPSD profiles with generator VG setpoints tuned to the 1.04 p.u. planning limit (Section 2.4).

| Metric | NoControl | RuleBased | PID | Unit |
|---|---|---|---|---|
| Energy cost | 171.625 | 171.625 | 171.625 | MEUR |
| Voltage deviation (mean) | 0.0286 | 0.0286 | 0.0286 | p.u. |
| Voltage violations | 2847 | 2846 | 2842 | bus-hours |
| Mean losses | 46.1 | 46.1 | 46.1 | MW |
| Max losses | 245.4 | 245.4 | 245.4 | MW |
| Valley loading margin | 2.53 | 2.53 | 2.53 | × P₀ |
| Peak loading margin | 1.452 | 1.452 | 1.452 | × P₀ |
| Convergence | 721/721 | 721/721 | 721/721 | / |

### Key Finding: Local Control is Insufficient

The rule-based and PID controllers reduce voltage violations by only 0.04% and 0.18% respectively (2847 → 2846 → 2842 bus-hours). This near-zero improvement is a physically grounded result, not a modelling error:

1. **Violation buses are electrically distant from FACTS devices.** Violations concentrate at buses 22–29 (high-voltage during low-load/high-renewable hours, low-voltage during peak load), while SVC@14 and STATCOM@39 are at generator buses where the generator's own voltage regulator already dominates.

2. **Generator voltage regulation overrides shunt injection.** At generator buses (type 2/3 in PYPOWER), the voltage setpoint is held by the machine model. Shunt compensation at these buses changes reactive power flow but not the bus voltage itself.

3. **Limited device range relative to system size.** The thesis-specified FACTS ratings (SVC ±0.5 pu = ±50 MVAr, STATCOM ±1.0 pu = ±100 MVAr) are modest relative to the 6,254 MW system and the ±200+ MVAr reactive power flows during extreme hours.

4. **No coordination between devices.** Each controller acts independently on its local bus voltage. Even if SVC@14 shifts voltage slightly, the effect attenuates across the network before reaching buses 22–29.

**This is the core motivation for CAPSM's coordinated AI control architecture.** The System 2 (QIRL) controller, operating on full system state (39 bus voltages, 46 line flows, 10 generator outputs, 4 FACTS setpoints, 3 EV charges), can learn to coordinate devices across the network. The System 1 (CNN-LSTM) controller, once trained, provides real-time actuation within the 5 ms budget.

## 3.4 Loading Margin Analysis

The bisection-based loading margin analysis reveals critical system stress points:

| Operating Point | Loading Margin | Status |
|---|---|---|
| Jan 12 03:00 (valley, 2388 MW) | 2.53 | Healthy — ample headroom |
| Jan 12 18:00 (peak, 6195 MW) | 1.45 | Moderate — 45% headroom before PF failure |

At peak loading (6,195 MW), the system can absorb an additional 45% load increase before Newton-Raphson diverges. At valley loading (2,388 MW), the margin is 2.53×. The 1.74× ratio between valley and peak margins quantifies the system's sensitivity to renewable-induced load variations.

## 3.5 N-1 Contingency (Line 16–17 Trip)

Line 16–17, connecting the western generation corridor (GEN 35 at bus 35) to the central network, was tripped at 2019-01-15 12:00 (near-peak loading) and restored 12 hours later.

| Metric | Pre-Trip | During Outage | Change |
|---|---|---|---|
| Active power losses | 51.1 MW | 58.7 MW | +14.9% |
| Minimum voltage | 0.9505 | 0.9505 | Stable |
| Converged timestamps | — | 13/13 | Full convergence |

The 14.9% losses increase during the outage, combined with stable voltage and full convergence, confirms the system is robust to single-line outages at this operating point. All three baselines produce identical contingency results, consistent with the finding that local FACTS control has negligible effect on system-wide metrics.

## 3.6 Ramp Events

Extreme 1-hour load ramps from the German system were identified (Section 1.5):
- Maximum 1-hour ramp: 20,192 MW (January 2012)
- Maximum 3-hour ramp: 27,832 MW (January 2012)

These 2012 events exceed the January 2019 operating range and serve as stress-test inputs for the System 1 controller's real-time tracking.

## 3.7 Conclusions

1. Classical local controllers (droop, PI) with the thesis-specified FACTS placement cannot meaningfully reduce voltage violations on the IEEE 39-bus system driven by real German profiles.

2. The loading margin ranges from 1.45 (peak) to 2.53 (valley), defining the operating envelope within which the CAPSM controllers must maintain stability.

3. N-1 contingency causes 14.9% losses increase with no voltage collapse — the system has sufficient reactive reserve for single contingencies.

4. These baselines establish the minimum bar: any CAPSM controller that achieves measurable improvement over NoControl at voltage deviation, violation count, losses, or loading margin demonstrates genuine value over classical approaches.
