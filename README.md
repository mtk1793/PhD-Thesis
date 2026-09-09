# CAPSM PhD Thesis - Delivery Package

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
