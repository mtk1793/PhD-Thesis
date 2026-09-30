# 11 — Chapter Revision Tracker (Phase Y execution log)

Every edit below was applied to `chapters_md/` in this revision. Status:
DONE = applied; PENDING-USER = requires the user's rerun data or decision.

## Front matter (00_front_matter.md)
- DONE — Added explicit conservative title (master plan §34): "...Coordinated FACTS–EV Control in DER-Rich Power Systems with Controller-Hardware-in-the-Loop Validation".
- DONE — Abstract rewritten per §33: 9-part structure; only evidence-labelled numbers; explicit scope boundary ("directly controllable assets are the FACTS devices and three aggregated EV stations; renewable DERs provide the variable operating environment"); Stage-1 figures explicitly marked as superseded by the retrained pipeline; limitation sentence added; no nine-contribution list.
- DONE — Keywords: "quantum-inspired reinforcement learning" → "quantum-inspired candidate selection".

## Chapter 1 (ch01.md)
- DONE — §1.5 problem statement narrowed to FACTS–EV in DER-rich systems; explicit "no experiment claims direct DER control" scope boundary paragraph (§28 Phase Y Ch1 Add).
- DONE — Gap 3 wording: "FACTS devices and DERs" → "FACTS devices and EV fleets".
- DONE — Gap 5: "The overwhelming majority" replaced by grounded prevalence statement.
- DONE — §1.6 restructured: objectives stated first (O1–O5 fixed), design targets second, all labelled E4; 99.9% constraint-compliance target replaced by "compliance by construction via admissibility envelope" (master plan §6/§14).
- DONE — Table 1.3: O3 label "Coordinated FACTS–DER control" → "Coordinated FACTS–EV control"; O2 compliance wording fixed.
- DONE — §1.7 C2: counterfactual candidate scoring stated; "no quantum speedup; no quantum hardware involved" disclaimer added; framed as interpretable amplitude-based formulation (§10 Phase G).
- DONE — §1.7 C6: "AI-based optimal placement" → "FACTS and EV placement methodology"; explicit non-claim of optimality (§13 Phase J Route B).
- DONE — §1.8 chapter organisation updated for the Chapter 5 rename.

## Chapter 2 (ch02.md)
- DONE — "no established practice exists" converted to a scoped claim: documented targeted search (Scopus/IEEE Xplore, query families named) with "absence of a found precedent within a documented search" phrasing (§28 Ch2). USER: fill exact search dates/queries in project records.

## Chapter 3 (ch03.md)
- DONE — §3.2: "32 candidates scored in parallel against the current network state" → counterfactual evaluation with Evaluator A (exact AC) / Evaluator B (sensitivity surrogate) referenced to Chapter 4.
- DONE — "immediately transferable to new operating regions" removed/replaced with honest scoping.
- DONE — §3.5: tunnelling respects reserved index 5; planning horizon sentence aligned to Option 2 (single-step; reserved for future work).
- KEPT — Theorem 3.1 (Boltzmann characterisation) — correct and implementation-linked. 58–59% DQN target retained with design-target label. 86.7% retained with (HIL campaign) label — provenance to be confirmed via audit/04.

## Chapter 4 (ch04.md)
- DONE — Action interface: reserved index 5 enforcement documented at the interface level (pinned in candidates, tunnelling, System 1 post-processing, excluded from effort penalty, never emitted, regression-tested) (§6 Phase C).
- DONE — Equation (4.10) REPLACED: candidate-independent reward (mean|Vm−1| − 0.05·n_viol − 0.001‖a_i‖² on unchanged state) → formal candidate-dependent counterfactual reward r_i = −w_V J_V(vm̃_i) − w_viol J_viol(vm̃_i) − w_L J_L(L̃_i) − w_T J_T(f̃_i) − w_SoC J_SoC(a_i) − w_u J_u(a_i, a_prev), matching capsm/agents/evaluators.py exactly (§5 Phase B).
- DONE — Evaluator A / Evaluator B described with the required validation metrics and a pointer to the exact-vs-surrogate results section.
- DONE — Algorithm 4.2 rewritten to counterfactual scoring; reserved index noted in tunnelling line.
- DONE — "requires no offline training whatsoever" clarified: no fitted value function, but per-step power-flow evaluation cost (computational, not statistical, freedom).
- DONE — §4.2.2 closing: single-step scope sentence added.
- DONE — §4.5 hidden-state policy: S1-A window+reset declared THE convention for training and inference; Stage-1 mixed convention retired; S1-B/S1-C kept as ablation variants only (§8 Phase E).
- DONE — §4.6 training: chronological split 2015–2017/2018/2019 documented (deterministic seasonal sampling, window guard-gap, reserved-index-free targets, multi-seed, MAE/RMSE reporting); Stage-1 Jan-2019-on-Jan-2019 training explicitly named as leakage and superseded (§7 Phase D).
- KEPT — 137,418 trainable parameters derivation and ~250K overhead clarification (§9 Phase F) — already correct.

## Chapter 5 (ch05.md)
- DONE — Title: "AI-Based Optimal Placement..." → "FACTS and EV Placement Methodology and Deployment Configuration" (§13 Phase J Route B).
- DONE — Intro: optimality non-claim; GA/PSO described as assessed methods; deployed configuration = engineering configuration.
- DONE — §5.4: "treats each decision as a small OPF" → "constrained candidate search"; Eq (5.13) replaced by counterfactual candidate-dependent reward (aliases Eq 4.10).
- DONE — §5.5 renamed: "Quantum-Enhanced Reinforcement Learning for Optimal Power Flow" → "Quantum-Inspired Candidate Selection for Real-Time Coordinated Dispatch" (removes both "quantum-enhanced" and "optimal" mislabels).

## Chapter 6 (ch06.md)
- DONE — Parameter statement: exact 137,418 trainable; ~250K labelled as storage/optimiser-state overhead (§9 Phase F).

## Chapter 8 (ch08.md)
- DONE — Scenario generation: planning-horizon wording aligned to Option 2 ("reserved... since the deployed controller performs one-step candidate optimisation").

## Chapter 9 (ch09.md)
- DONE — Phase T (§23): explicit scope statement that headline results come from the dual-process core, NOT the seven-agent hierarchy; H-MARL repositioned as scalability extension (E3); new Table 9.1 "Core CAPSM vs H-MARL extension" (headline results / HIL deployed / agents / mechanism / evidence class / role).
- DONE — Figure 9.1 narrative: "adopted here" → "examined here as an extension".

## Chapter 11 (ch11.md)
- DONE — Evidence taxonomy paragraph (E1–E5) added at chapter head (§2).
- DONE — Revision note added: Stage-1 figures superseded by retrained pipeline outputs; SSOT file named; HIL Part B unaffected; 11.4 extended to include exact-vs-surrogate validation.
- PENDING-USER — After reruns: replace Stage-1 table values from `audit/10_FINAL_NUMBERS_SSOT.yaml`; add master result table at 11.0; add 11.14 statistical-significance subsection from phase8 report.

## Chapter 12 (ch12.md)
- DONE — Limitation 4 rewritten to honest single-step wording (System 2 performs one-step candidate optimisation; horizon reserved).

## Chapter 13 (ch13.md)
- DONE — Table 13.1 rebuilt: O1–O9 inconsistency FIXED; now nine contributions C1–C9 mapped to the SAME five objectives O1–O5 as Chapter 1, with the fixed matrix (O1→C1,C3; O2→C2,C3; O3→C4,C6; O4→C5; O5→C7,C8,C9) (§27 Phase X).
- DONE — C2 row: counterfactual evaluators + superseded labels; C4 row: 137,418 parameters + enforced reserved index; C9 row: "multi-system pipeline portability" replaces "transferable knowledge representation" (§24 Phase U).
- DONE — Closing commentary rewritten (C2 as interpretable Boltzmann formulation; no quantum advantage claim).
- DONE — Limitation table + seams paragraph + future-work direction 1: honest single-step wording.

## Acceptance-gate status (§36)
- Gate 1 Code integrity: PASS (26/26 P0 tests; suite runs locally).
- Gate 2 Data integrity: TOOLING READY (split enforced in code + tests; hashes produced by phase0/phase1 runs on user machine).
- Gate 3 Result integrity: PENDING (reruns on user machine; SSOT ready).
- Gate 4 HIL integrity: PENDING (audit/04 ledger to be completed with run IDs/raw logs).
- Gate 5 Claim integrity: LEDGERS CREATED (audit/03); every new paragraph carries evidence labels.
- Gate 6 Mathematical integrity: Eq 4.10/5.13 now match code; Theorems 3.1/4.1 remain valid (they concern the amplitude update, unchanged).
- Gate 7 Thesis consistency: O1–O5 / C1–C9 aligned (ch01 ↔ ch13); parameter counts aligned (ch04/ch06/ch13); action-space description aligned (ch03/ch04/ch05).
- Gate 8 Document quality: PENDING (docx rebuild; TOC/LoF/LoT regeneration in Word; cross-references).
