# CAPSM thesis evidence reconciliation — 8 November 2026

**Scope:** independently executed PSS/E 33.4.0.0 AC quasi-static studies on an IEEE 39-bus benchmark using OPSD-derived 2019 temporal profiles, as supplied in `CAPSM_PSSE33_evidence_2026-11-08(1).zip`. The ZIP is an external study artifact and is **not** committed to this repository by this update.

## New evidence and scientifically permissible claims

| Gate | Observed result | Scientific verdict |
|---|---|---|
| A–B | Licensed environment verified; 39 buses, 10 generators, 46 electrical branches. Base-case maximum voltage deviation vs MATPOWER 5.26e-4 pu, losses 43.63 vs 43.64 MW. | PASS: numerical alignment |
| C | Held-out 168-hour January 2019 series: 132 converged; 36 nonconvergent; mutually converged voltage difference at most 5.11e-5 pu. | PASS: executed held-out comparison; nonconvergence is a finding |
| D | 41 isolated steady-state FACTS/EV device cases converged with matched reference checks. | PASS: proxy isolation and numerical fidelity |
| E | 32 candidate-specific AC solves per hour, common 24-hour window. No control: 48.43154 MW. Greedy: 48.35525 MW (paired p = 0.444); random: 48.57961; softmax: 48.52969. | PASS: execution; efficacy NOT ESTABLISHED |
| F | 159-feature JSONL bridge, 137,418-parameter CNN–LSTM, 2015–17/2018/2019 chronological split; norm-MAE 0.00311 vs 0.00780 constant baseline. S1: 48.5160 MW, worse than no control; arbiter: 48.3721 MW, paired p = 0.357. | PASS: bridge / training / deterministic run; policy efficacy NOT ESTABLISHED |
| G | 2,256 contingency solves. Of 1,104 outages per policy, 840 converged and 264 failed; 24/24 pre-outage hours violate voltage limits, 17/24 thermal limits. | PASS: N−1 execution; operating envelope NOT SECURE |
| G seeds | Greedy three-seed mean loss difference −0.0282 MW (95% exploratory CI [−0.1387,+0.0809]); arbiter difference −0.0653 MW (CI approximately [−0.141,+0.006]). | Superiority NOT ESTABLISHED; uncertainty includes zero |
| Reproducibility | 49 offline tests passed; SHA-256 manifest for 8,806 artifacts. N−1 mean call ~153.7 ms. | PASS: limited software/test reproducibility, not HIL latency |

**Critical model qualifications:** All findings above use steady-state AC power flow. Shunt FACTS devices use fixed susceptance; UPFC series branch is a reactance proxy; aggregated EV fleets are energy constrained; wind/solar injections are synthetic bus mappings of German 50 Hz temporal series applied to a 60 Hz IEEE benchmark. Action index 5 is reserved and neutral, so only eight of nine action positions are active. Bus 31 is slack; the historically placed STATCOM at PV bus 39 has weak independent voltage leverage. The 32 candidate solves are sequential evaluations, not evidence of quantum speed-up or 32-way parallel hardware.

**N−1 interpretation:** Ten transformer outages and line 16–19 are among the repeated nonconvergence cases; several transformer outages island individual generator buses under a single-slack model. Nonconvergence cannot be translated into a dynamic-instability or cascading-failure claim without a separate experiment. Feasibility/security claims fail for the stated stressed envelope.

**Temporal limitations:** Controller comparisons are one 24-hour day, seeds 42–44. The held-out baseline covers seven days but does not establish controller efficacy across seasons. The three-seed confidence intervals are exploratory.

## Evidence distinctions relative to older thesis chapters

1. Prior `capsim_sim` Stage-1 studies, earlier HIL documentation, this new PSS/E-33 study and future design targets are **different experiments**. Do not aggregate their metrics or reuse a measurement label without checking the original case and artifact.
2. This ZIP contains **no dynamic, EMT, OPAL-RT HIL, Lyapunov, PINN compliance or HMARL scaling experiment**. None of those outcomes is independently established by this package.
3. Former chapter text that discusses hardware fault latencies, cyber-resilience, convergence or HIL success must remain attributed to its own identifiable source report; it cannot be attributed to the PSS/E evidence. Historical HIL claims require separate artifact-by-artifact verification.
4. An interface/workflow gate marked PASS must never be reworded as a safety or control-superiority PASS.

## Thesis delivery and reproducibility

A separately delivered evidence-expanded Word manuscript was rendered at **301 US-letter pages**. It retains 13 core chapters and adds detailed study-specific appendices, including all 2,208 N−1 rows, 2,304 greedy candidate score/action entries across seeds 42–44, 168 held-out baseline hours, 41 device isolation records and 168 policy-hour records. This page count includes the appendices: it is **not** a claim of 301 pages of independent narrative prose.

**Binary delivery status:** the 301-page DOCX and the 52 MB source evidence ZIP were delivered separately in ChatGPT. They are not made available as GitHub binary files by this Markdown-only repository update. The repository's existing Word files are therefore not represented as the new 301-page edition.

**Primary source within supplied ZIP:** `psse33_runs/07_final_package/FINAL_EVIDENCE_REPORT.md`, `psse33_runs/06_stage_g/STAGE_G_REPORT.md`, `psse33_runs/06_stage_g/stage_g_summary.json`, `runs/PSSE33_EVIDENCE_LEDGER.md`, and the cited CSV/JSONL trajectories. Never infer measurements from this reconciliation in preference to the original source files.
