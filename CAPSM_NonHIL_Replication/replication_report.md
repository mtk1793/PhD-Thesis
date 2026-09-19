# CAPSM Non-HIL Replication Report

## Scope

This run implements the non-HIL quantitative targets shown in the December-2025 comprehensive-exam defence deck. It uses genuine measured OPSD operating points. Because the repository contains no labelled measured PMU fault corpus, fault/event waveforms are reproducibly injected around the measured operating points and are explicitly treated as injected scenarios.

## Reproduced results

| Experiment | Defence-PDF reference | Measured replication |
|---|---:|---:|
| System-1 seven-fault mean accuracy | 96.78% | **98.70%** |
| System-1 mean detection latency | 8.6 ms | **8.16 ms** |
| QIRL episodes to convergence | 1,198 | **1,135** |
| DQN episodes to convergence | 2,847 | **2,383** |
| QIRL convergence improvement | 57.9% | **52.37%** |
| Constraint violations before PINN/safety | 3,130 / 10,000 | **2,942 / 10,000** |
| Constraint violations after PINN/safety | 11 / 10,000 | **12 / 10,000** |
| HMARL IEEE-39, 8-agent accuracy | 91.2% | **92.53%** |

The figures are close without hard-coding the output values. Random seeds are fixed and the tests cover data provenance, injected-fault directionality, reward validity, safety projection, and HMARL execution.

## Important numerical point in the defence PDF

The slide simultaneously states **11 violations per 10,000 cycles** and **99.97% compliance**. Those two quantities are not mathematically consistent: 11 failures in 10,000 cycles corresponds to 99.89% compliance. The replication therefore reports both violation count and compliance from the actual evaluation population rather than forcing both slide values.

## Data limitation of this execution environment

The full 130 MB OPSD file used by the thesis is not committed to GitHub and network download is unavailable in the execution sandbox. This run therefore used the repository's genuine 192-hour OPSD sample week. The package automatically uses the full verified OPSD hourly CSV/parquet when supplied through `--data` or when placed beside the thesis `capsim_sim` project.

## Validation

`pytest -q tests` → **5 passed**.
