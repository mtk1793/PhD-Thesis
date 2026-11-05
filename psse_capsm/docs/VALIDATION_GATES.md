# PSS/E simulation scientific validation gates

1. **Provenance:** Case SHA-256, source benchmark, PSS/E minor version, Python
   version, FNSL settings and solver log archived with every run.
2. **Topology:** Exact 39 buses, 10 machines and 46 electrical branches,
   including 12 two-winding transformers. Reject unsupported 3-winding
   models until a separate mapping is validated.
3. **Base case:** Compare bus voltages/angles, generation, reactive power,
   line and transformer MVA flows and total losses against benchmark.
4. **Physical control:** B pu to MVAr scaling, shunt sign, TCSC branch-X
   response, UPFC proxy honesty, no duplicate loads, and EV SoC invariance.
5. **Isolation:** Every QIRL candidate starts from immutable RAW/EV state.
   SoC changes exactly once only if a final solve converges.
6. **Contingencies:** Trip/restore timestamps, original branch status,
   exact same pre-fault state and no automatic omission of non-convergence.
7. **Learning:** Train 2015–17, validation 2018, held-out test 2019.
   Freeze normalization statistics and model checkpoint. Preserve 12-step
   temporal window, canonical feature order, reserved action index 5.
8. **Comparisons:** NoControl, droop, PI, S1, S2, CAPSM, greedy, softmax,
   random and placement ablations on identical scenarios; 10+ seeds for
   stochastic variants and paired block-bootstrap confidence intervals.
9. **Metrics:** Voltage violation bus-hours and severity, maximum/p95
   deviations, both-end branch MVA loading, missing thermal ratings,
   losses, EV feasibility, solve failures, switching and algorithm timing.
10. **Evidence:** PSS/E new evidence ledger separate from PYPOWER Stage-1,
    HIL reports, defence design targets and external literature.
11. **Non-claims:** Hourly power flow does not substantiate millisecond
    fault detection, Lyapunov dynamic stability or HIL real-time timing.
