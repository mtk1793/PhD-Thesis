# CHANGELOG — Final Scientific Rebuild (2026-09-30)

Executed against `CAPSM_Thesis_Final_Rebuild_Master_Plan_2026-09-30.md`.
Baseline commit: c888156 (master). Historical results preserved; all new
outputs are versioned. Full per-chapter detail: `audit/11_CHAPTER_REVISION_TRACKER.md`.

## P0 — Blocking code fixes (Gate 1)

### Phase B — QIRL candidate-dependent physical evaluation
- NEW `capsim_sim/capsm/agents/evaluators.py`:
  - **Evaluator A** `ExactPowerFlowEvaluator`: per-candidate counterfactual AC power flow through the environment's own `_solve` pipeline, wrapped in a per-candidate snapshot/restore so no candidate contaminates the next.
  - **Evaluator B** `SensitivitySurrogateEvaluator`: first-order Taylor surrogate (dV/du, dFlow/du, dLoss/du by finite differences over the 8 active dimensions), refreshed every N steps; ~0.33 PF/step amortised vs 32 PF/step exact.
  - **Formal reward** (`compute_reward`): r = −wV·J_V − w_viol·J_viol − wL·J_L − wT·J_th − wSoC·J_SoC − wu·J_u; every term normalised and candidate-dependent; the reserved dimension is excluded from effort. Single shared implementation for both evaluators.
  - `ev_infeasibility_of`: read-only EV SoC-guard feasibility (request-time arithmetic).
- REWRITE `capsim/agents/system2.py`: candidate-dependent single-step QIRL; selection modes `qirl|softmax|greedy|random` (ablation matrix of §10); tunnelling and candidate-refresh flags; reserved index pinned at init/tunnel/selection; honest single-step docstring (no planning claims); diagnostics (`last_evaluation`, `evaluator_power_flows`).
- The old reward (identical base score for all candidates + ‖a‖² effort) is retired.

### Phase C — reserved action index
- Index 5 (UPFC series-Q) enforced neutral everywhere: System 2 candidates + tunnelling; System 1 inference post-processing (`a[5] = 0.0`); effort penalty excludes it; `vector_to_controls` never emits it; ACTION_LO/HI pin it to 0.
- Regression tests added (master-plan names): `test_reserved_action_q_always_zero`, `test_reserved_action_q_not_in_reward`, `test_reserved_action_q_not_sent_to_environment` (in `tests/test_p0_fixes.py`).

### Phase D — train/test leakage
- REWRITE `capsim/agents/trainer.py`: chronological split TRAIN 2015–2017 / VAL 2018 / TEST 2019; deterministic seasonal demo sampling (`sample_training_episodes`); `assert_no_test_leakage` guard; `build_window_dataset` builds 12-step sliding windows (episode-boundary-safe, guard-gap so no raw row is shared between train and val); `sanitize_action_targets` zeroes index 5; train/val loss + MAE/RMSE per output; multi-seed.
- REWRITE `capsim_sim/scripts/phase4_system1.py` (v2): leakage-free training, 2018 imitation metrics, unseen Jan-2019 (optional full-2019) evaluation, baselines on the same window, per-seed latency, results versioned to `results/phase4_v2/`.

### Phase E — System 1 recurrence convention
- `capsim/agents/system1.py`: explicit `temporal_mode` — `window_reset` (S1-A, DEFAULT; matches windowed BC training), `streaming_persistent` (S1-B), `window_persistent` (S1-C, ablation-only legacy). Training and inference now share one convention.

### Phase I/O support
- `capsim/agents/arbiter.py`: ablation modes `sigmoid` (deployed default, unchanged behaviour) / `hard` / `fixed`; optional safe mode and hysteresis; `arbitration_summary()` diagnostics (mean/std alpha, dominance %, transitions/day).
- `capsm/grid/metrics.py`: Phase-P metrics added at source — `violation_severity_pu2`, `p95_voltage_dev_pu`, `thermal_overload_severity` — now flow into every results DataFrame.

## Rerun & analysis scripts (Gates 2–5 tooling)
- REWRITE `scripts/phase5_system2.py` (v2): exact/surrogate evaluator choice, per-seed aggregates, evaluator timing, `results/phase5_v2/`.
- REWRITE `scripts/phase6_arbiter.py` (v2): frozen Phase-4 checkpoint, full controller set, arbitration diagnostics, `results/phase6_v2/`.
- NEW `scripts/phase5b_surrogate_validation.py`: exact-vs-surrogate campaign (Pearson, Spearman, top-1, top-3 overlap, voltage MAE, overload MAE, ms timing, PF counts).
- NEW `scripts/phase7_ablations.py`: QIRL ablations (random/greedy/softmax/softmax+refresh/no-tunnel/QIRL) × seeds; arbiter ablations (S1 only/S2 only/fixed 50-50/hard/sigmoid/CAPSM) × seeds → `results/phase7/ablation_rows.csv`.
- NEW `scripts/phase8_statistics.py`: mean/SD/median/IQR/95% CI, lag-1 autocorrelation, paired moving-block bootstrap CIs (i.i.d. t-tests demoted), statistical-vs-engineering significance split.
- NEW `scripts/phase4b_seasonal.py`: full-2019 monthly evaluation + extreme windows (max ±3 h ramps, high-RE/low-load, high-load/low-RE).

## Tests
- NEW `capsim_sim/tests/test_p0_fixes.py`: 26 tests on synthetic OPSD-shaped profiles (no dataset needed) — **26/26 pass locally**. Covers: reserved-index triple, candidate-dependence, snapshot-restore purity, surrogate PF-count + ranking (Spearman > 0.7), Born-rule = Boltzmann equivalence, chronological-split no-overlap, leakage guard, temporal modes, arbiter modes, and the placement finding below.
- Full suite: 15 passed + 37 data-availability errors (OSPD raw CSV not in repo; run `phase0_data.py` first). No regression introduced.
- **FINDING**: `test_statcom_on_slack_bus_has_no_voltage_effect` proves the deployed STATCOM (bus 39) sits on the IEEE-39 slack bus and cannot move voltage — corroborates the placement limitation and motivates Phase J re-optimisation.

## Thesis text (Phase Y)
- `chapters_md/00_front_matter.md`: conservative title added; abstract rewritten per §33 (evidence labels, scope boundary, superseded-values note, limitation sentence).
- `ch01.md`: scope boundary; FACTS–EV narrowing; O1–O5 objectives-first structure; C2/C6 corrected (no quantum speedup; placement methodology).
- `ch02.md`: novelty claim scoped to a documented search.
- `ch03.md`: counterfactual evaluation; transferability claim removed; single-step scope; reserved index in tunnelling.
- `ch04.md`: **Eq (4.10) replaced** with the formal candidate-dependent counterfactual reward (matches code exactly); Evaluator A/B described; Algorithm 4.2 rewritten; index-5 enforcement documented at the interface; S1-A/S1-B/S1-C conventions documented with S1-A default; chronological-split training section; single-step scope.
- `ch05.md`: title → "FACTS and EV Placement Methodology and Deployment Configuration"; optimality non-claims; §5.5 renamed (no "Quantum-Enhanced"/"Optimal Power Flow"); Eq (5.13) → counterfactual reward.
- `ch06.md`: 137,418 trainable vs ~250K stored-state clarification.
- `ch08.md`, `ch12.md`: honest single-step planning wording.
- `ch09.md`: H-MARL repositioned as scalability extension (E3) with core-vs-extension Table 9.1.
- `ch11.md`: E1–E5 evidence taxonomy + revision note at chapter head; §11.4 extended to exact-vs-surrogate validation.
- `ch13.md`: **O1–O9 inconsistency fixed** — nine contributions C1–C9 mapped to the same five objectives O1–O5 as Chapter 1 (fixed matrix); "transferable knowledge representation" → "multi-system pipeline portability"; parameter count fixed; single-step limitation wording.

## Audit (master plan §3)
- NEW `audit/README.md`, `audit/03_CLAIM_EVIDENCE_LEDGER.csv` (34 claims, E1–E5),
  `audit/04_HIL_EVIDENCE_LEDGER.csv` (11 HIL claims, provenance fields, status),
  `audit/10_FINAL_NUMBERS_SSOT.yaml` (SSOT with FROZEN / SUPERSEDED / PENDING_RERUN),
  `audit/11_CHAPTER_REVISION_TRACKER.md` (per-chapter log + gate status).

## Build
- `scripts/build_thesis.py`: title updated; output → `CAPSM_Thesis_Final_Rebuild_2026-09-30.docx` (original 2026-09-09 docx preserved untouched).
- Rebuilt document generated from the revised `chapters_md/`.

## What only you can do (needs the real dataset / HIL lab)
1. `python capsim_sim/scripts/phase0_data.py` (download ~1 GB OPSD), then the rerun chain (audit/README.md).
2. Fill `audit/04_HIL_EVIDENCE_LEDGER.csv` run IDs + raw logs; downgrade or drop any HIL claim that stays without provenance.
3. Freeze `audit/10_FINAL_NUMBERS_SSOT.yaml`, regenerate result figures/tables, update abstract numbers, rebuild docx.
4. Optional Phase J Route A: run a real placement optimisation (GA/PSO scripts can reuse `phase7` harness); the slack-bus STATCOM finding suggests meaningful headroom.
