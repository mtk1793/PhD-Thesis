# Audit Directory — Master Plan §3 Deliverables

Created 2026-09-30 during the final scientific rebuild
(`CAPSM_Thesis_Final_Rebuild_Master_Plan_2026-09-30.md`).

| File | Purpose | Status |
|---|---|---|
| 03_CLAIM_EVIDENCE_LEDGER.csv | Every quantitative claim with evidence class E1–E5 and the action taken | created; update values after reruns |
| 04_HIL_EVIDENCE_LEDGER.csv | One record per HIL claim with required provenance fields (§20) | created with status=MISSING provenance — fill run IDs and raw-log paths or downgrade wording |
| 10_FINAL_NUMBERS_SSOT.yaml | Single source of truth for all final thesis numbers | created; PENDING_RERUN fields fill from results/phase4_v2, phase5_v2, phase5b, phase6_v2, phase7, phase8 |
| 11_CHAPTER_REVISION_TRACKER.md | Complete per-chapter log of the Phase Y revision + acceptance-gate status | current |

Planned extensions (numbering reserved by the master plan):
01_THESIS_SCIENTIFIC_AUDIT.md, 02_CODE_THESIS_CONSISTENCY_MATRIX.md,
05_REFERENCE_AUDIT.md, 06_EQUATION_AND_NOTATION_AUDIT.md,
07_FIGURE_TABLE_AUDIT.md, 08_STATISTICAL_ANALYSIS_PLAN.md,
09_EXPERIMENT_RERUN_MATRIX.csv.

## Rerun procedure (fills the SSOT)

```bash
cd capsim_sim
python scripts/phase0_data.py          # download + verify OPSD raw data (~1 GB)
python scripts/phase4_system1.py       # leakage-free System 1 (2015-2017 train)
python scripts/phase5_system2.py       # System 2 counterfactual evaluation
python scripts/phase5b_surrogate_validation.py
python scripts/phase6_arbiter.py       # full CAPSM on unseen Jan-2019
python scripts/phase7_ablations.py     # QIRL + arbiter ablations, 10 seeds
python scripts/phase8_statistics.py    # block-bootstrap statistics
python scripts/phase4b_seasonal.py     # full-2019 seasonal + extreme windows
```

Then: copy the produced values into `10_FINAL_NUMBERS_SSOT.yaml` (status
FROZEN), regenerate the result tables/figures from those files, and only
then rebuild the Word thesis. Historical Stage-1 results in
`capsim_sim/results/phase1..6` are preserved untouched; all new outputs
are versioned (`*_v2`, `phase5b`, `phase7`, `phase8`, `phase4b`).

## Key finding recorded during the rebuild

The deployed STATCOM sits on IEEE-39 bus 39 — the slack bus — where shunt
compensation cannot move voltage (verified by regression test
`test_statcom_on_slack_bus_has_no_voltage_effect`). Together with the
already-documented placement limitation (violation cluster at buses 22–29
outside device reach), this strengthens the Phase J case for placement
re-optimisation and is consistent with the modest ~1% violation deltas.


## November 2026 PSS/E module and correction

A new [PSS/E evidence ledger](12_PSSE_EVIDENCE_LEDGER.md) (E6) records
prospective simulation experiments. It does not replace E1–E5.

**IEEE-39 bus identity correction:** The original MATPOWER case39.m (also
committed in HIL_Project/python/data/) identifies **bus 31 as the slack
bus** and **bus 39 as a generator-regulated PV bus**. The older paragraph
calling bus 39 the slack bus is incorrect. The observed low voltage
sensitivity of a fixed shunt at bus 39 is consistent with regulation at a
PV bus; it should not be attributed to slack-bus assignment. The original
audit text is preserved above as historical provenance.
