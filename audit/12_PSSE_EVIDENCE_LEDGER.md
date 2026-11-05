# E6 – PSS/E validation evidence ledger (new, pending)

This ledger tracks new measured results from CAPSM PSS/E v35 simulation.
It is **not** part of historical E1 (PYPOWER), E2 (HIL),
E3 (non-HIL replication), E4 (design targets), E5 (literature).

| Claim ID | Experiment | Measure | Status | Required provenance |
|---|---|---|---|---|
| PSSE-001 | IEEE39 base-case AC | Bus, gen, line/transformer counts | PENDING_PSSE_RUN | RAW hash, PSS/E version, solved .sav, logs |
| PSSE-002 | IEEE39 no control | Voltage/thermal/loss baseline | PENDING_PSSE_RUN | Timestamp profile hash and result JSONL |
| PSSE-003 | SVC control | Sensitivity and reactive response | PENDING_PSSE_RUN | Pre/post AC cases and BL units |
| PSSE-004 | STATCOM-at-39 | Voltage response and generator Q | PENDING_PSSE_RUN | Comparison against relocated shunt |
| PSSE-005 | TCSC 16–17 | Branch X and flow changes | PENDING_PSSE_RUN | Branch identity, X, terminal MW/MVAr |
| PSSE-006 | UPFC 26 surrogate | Shunt/series proxy response | PENDING_PSSE_RUN | Explicit proxy model and limitations |
| PSSE-007 | EV 3/8/15 | MW and SoC energy balance | PENDING_PSSE_RUN | Fleet state transitions and efficiency |
| PSSE-008 | QIRL 32 exact | Candidate-dependent rewards | PENDING_PSSE_RUN | Identical-state raw snapshot checks |
| PSSE-009 | Contingency | N−1 outage and restoration | PENDING_PSSE_RUN | Branch trip records and convergence |
| PSSE-010 | PyTorch System 1 | Held-out 2019 closed loop | NOT_IMPLEMENTED | Train/val/test hashes and checkpoint |
| PSSE-011 | Integrated CAPSM | S1/S2/Arbiter comparison | NOT_IMPLEMENTED | Frozen models, matched scenarios |
| PSSE-012 | Dynamics | RMS disturbance behaviour | NOT_IMPLEMENTED | Validated DYR, time-domain outputs |

PSS/E code changes are not evidence that a simulator result has been obtained.
The development environment does not contain a licensed PSS/E v35 runtime.
All numerical result fields remain unset until local runs are completed
and their raw output files are archived.

Case39 source-data correction: MATPOWER case39.m has bus **31 as slack
(type 3)** and bus **39 as PV (type 2)**. Earlier thesis audit notes
called bus 39 the slack bus. This was a classification error. A shunt at
a generator-regulated PV bus may still show little voltage effect because
the generator regulates the bus voltage.
