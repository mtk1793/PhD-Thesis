# CAPSM no-appendix expansion: integration control (8 November 2026)

**Status: source blueprint archived; 250-page main-text completion NOT VERIFIED.** The uploaded plan is a drafting specification, not completed prose, a measurement record, or a validated page count. Preserve the complete original Word source.

## Source mismatch

The latest `releases/2026-11-08/CAPSM_PhD_Thesis_Final_313pg_2026-11-08.docx` has **Appendices A–H**, not only A–E. Its contents list Appendix A around p.151, Appendix F p.164, Appendix G p.228, Appendix H p.300, and references from p.306. The 313-page overall document cannot be described as 313 pages of thesis main text. The source blueprint's 45-page total for appendices is therefore inapplicable to this edition.

## No-appendix absorption map

| Source | Body home | External preservation |
|---|---|---|
| A evidence index | Chapter 10 provenance and Chapter 14 audit | Original DOCX |
| B claim reconciliation | Sections 1.7 and 13.2; full register in Chapter 14 | Original DOCX |
| C audit, estimands and inference | Sections 10.8 and 12.9; full register in Chapter 14 | Original DOCX |
| D 41-device cross-solver table | Section 11.3 | Original DOCX |
| E 168-hour trajectory | Section 11.2 as daily/key-hour views with all failures | Original CSV/raw archive |
| F full N-1 catalogue | Section 11.7 only aggregated and diagnostic inference | Preserve complete catalogue externally |
| G 32-candidate action ledger | Sections 10.5 and 11.6 as summaries | Preserve row-level action records externally |
| H multi-seed policy ledger | Sections 11.6, 11.10 and 11.11 as interpreted estimates | Preserve row-level records externally |

Chapter 14 must explain reproduction, provenance, and claim auditing **without repeating full tables already placed in Chapter 11**. Bibliography remains end matter. Do not disguise raw appendices as a new chapter purely to meet a page quota.

## Mandatory mathematical repairs

1. **RoCoF:** With \(\Delta P\) in system-base per unit and inertia in seconds, \(df/dt\approx f_0\Delta P/(2H_{sys})\) in Hz/s. The blueprint omits \(f_0\).
2. **SoC:** For AC-side charge/discharge powers, \(s_{t+1}=s_t+\eta_c P_c\Delta t/C-P_d\Delta t/(\eta_d C)\). A 25 MW AC export at 92% efficiency removes 27.174 MWh of battery energy; for a 100-MWh fleet at initial 50% SoC, end SoC is 22.83%, not 25%.
3. **QIRL:** If amplitudes are multiplied by \(\exp(\beta r_i)\) and then probabilities are their squared magnitudes, the probability ratio is multiplied by \(\exp(2\beta(r_i-r_j))\), not \(\exp(\beta(r_i-r_j))\). State prior-distribution and reward-range assumptions. No quantum advantage is established.
4. **WLS:** Under full-rank linear Gaussian assumptions with m measurements and n fitted independent state variables, the residual quadratic statistic has approximately \(\chi^2_{m-n}\) distribution, not \(\chi^2_m\). Nonlinear and correlated cases require calibration.
5. **Constraint cost:** In \(R=-w_v D_v-w_l\Delta L-w_cN_{viol}\), require nonnegative \(w_c\) for violations to incur a penalty. A negative weight after a minus sign instead rewards violations.
6. **Frequency restoration:** \(K_I>0\) alone does not prove zero steady-state error; assume stable, feasible, unsaturated closed-loop operation.

## Evidence mapping from latest manuscript (not shifted blueprint mapping)

- E-B: base case, matched MATPOWER cross-check (`01_basecase`).
- E-C: profile provenance and held-out baseline (`02_stagec`).
- E-D: 41 isolated device cases (`03_stage_d`).
- E-E: candidate evaluation and policies (`04_stage_e`).
- E-F: 159-feature learning bridge (`05_stage_f`).
- E-G: three seeds, N-1 and timing (`06_stage_g`).

## Non-negotiable empirical boundaries

The 2019 held-out week has 132 convergent of 168 hours and 36 non-convergent; do not impute zero losses. For each tested policy, N-1 has 840 converged of 1,104 attempted cases and 264 non-converged. Bus-39 shunt control was neutralised; the UPFC series representation is a reactance proxy. The learned policy's observed 24-h loss change was +0.0845 MW vs no control, so it does not demonstrate superiority. A 32-candidate evaluation took about 5.8 s, not <50 ms. Offline tests are 52 collected, 49 passed and 3 licence-gated skipped. Numerical agreement is not operational security.

HIL, PINN, HMARL, dynamic stability, fault-detection accuracy and real-time end-to-end controller deadlines are **not measured by the PSSE33 archive**. Preserve separate evidence status for independent legacy experimental campaigns.

## Required release gate

Only label a thesis `250-page main text, no appendix` after (1) every original A–H location is accounted for; (2) all mathematics and cross-references are verified; (3) figures/tables are captioned, numbered and supported; (4) a PDF/DOCX rendering is visually checked; (5) the actual main-text page count excluding front matter and references is at least 250; and (6) substantive independent writing has been reviewed instead of page padding. Archive SHA-256 values must be computed from bytes, not invented.

The existing `references/CAPSM_2020_2026_200_crossref.bib` is a bibliographic candidate collection; independently verify which records are actually cited.