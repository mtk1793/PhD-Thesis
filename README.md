# CAPSM PhD Thesis - Delivery Package

## November 8, 2026: licensed PSS/E 33 evidence and 301-page thesis edition

The [PSS/E 33 evidence reconciliation](thesis_updates/2026-11-08/PSSE33_EVIDENCE_RECONCILIATION.md) now documents a separately executed licensed IEEE 39-bus AC QSTS campaign. Chapter source addenda are appended to [Chapter 10](chapters_md/ch10.md), [Chapter 11](chapters_md/ch11.md), [Chapter 12](chapters_md/ch12.md) and [Chapter 13](chapters_md/ch13.md). This later study is **not** proof of real-time HIL, dynamics or historical claims, and it does **not** establish controller superiority or N−1 security in the tested window.

A 301-page Word edition of the thesis was rendered separately from these repository Markdown updates. **The 301-page DOCX and the source evidence ZIP have not been committed to GitHub** and should not be confused with the existing DOCX binaries in the root. This repository update changes the textual source/evidence reconciliation only. See the dated record for numeric provenance, limitations and delivery details.


## PSS/E v35 simulation-first implementation (November 2026)

The new [psse_capsm/](psse_capsm/) module adds an isolated PSS/E v35
quasi-static AC simulation workflow aligned with the September 2026 CAPSM
defence presentation and the September 30 scientific rebuild. It includes
RAW editing, FACTS/EV static equivalents, physically constrained EV dispatch,
candidate-specific exact AC evaluations, scenario logging, an offline test
suite, and a presentation traceability/audit document.

**Status:** code available for review; PSS/E licence-specific import, API
compatibility and convergence are not verified by the authoring environment.
It does not replace the existing PYPOWER results, HIL evidence, final
thesis numbers, or the current PyTorch controller implementation.

See [simulation README](psse_capsm/README.md),
[presentation alignment](psse_capsm/docs/PRESENTATION_ALIGNMENT.md), and
[validation gates](psse_capsm/docs/VALIDATION_GATES.md).


This package contains the complete PhD thesis written from the mtk1793/PhD-Thesis
repository and the CAPSM_Thesis_Writing_Plan.md 90-day plan.

## Contents
- CAPSM_Thesis_AcademicPaper_2026-09-09.docx  - FINAL THESIS (Word, 13 chapters + references + appendices)
- chapters_md/                                 - Markdown sources for all chapters (edit + rebuild)
- figures/                                     - All 44 thesis figures (7 repo results + 37 generated)
- eq_cache/                                    - 107 rendered equation PNGs (400 dpi)
- factsheet/CAPSM_FACTSHEET.md                 - Single source of truth (verified numbers, equations, references)
- scripts/                                     - gen_figures.py, render_equations.py, build_thesis.py
- README.md                                    - This file

## Rebuild after editing
    cd scripts
    python render_equations.py   # re-render equation PNGs
    python build_thesis.py       # rebuild the Word document

## Provenance
All quantitative results trace to the capsim_sim phase reports (Phase 0-6) of the
PhD-Thesis repository. Stage-1 measured results, HIL-campaign results, and design
targets are labelled as such throughout the thesis.
