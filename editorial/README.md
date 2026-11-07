# CAPSM editorial revision staging (2026-11-07)

This directory stages the academic-writing update separately from the canonical experimental chapters.

## Files
- `STYLE_GUIDE_2026-11-07.md`: actionable academic writing conventions, claim-boundary rules and phrase examples.
- `REVISED_SECTIONS_2026-11-07.md`: revised prose for core CAPSM sections, with the Chapter 11 results placeholder.
- `../references/academic_writing_guidance.bib`: nine Zotero-compatible entries from official or university-hosted writing guidance.

## Status and restrictions
The editorial revision is **not** a complete line-by-line rewrite of every chapter and has **not** been inserted into the canonical `chapters_md/` sources. This staging avoids accidental loss of equations, figures, citations, or historical evidence while the PSS/E programme remains unverified. Older manuscripts and experimental results are unchanged.

When reconciling `chapters_md/`, preserve original technical citation numbering and original argument/data; inspect each passage for scientific accuracy before adopting a rewrite. The university-writing bibliography is a separate collection and must not replace the power-engineering bibliography.

**Results rule:** Chapter 11 in the editorial revision remains `[RESULTS SECTION: UNDER DEVELOPMENT]`. Its original repository file is left unchanged for provenance only; it must not be interpreted as newly validated PSS/E evidence.

## Technical issues requiring review
1. The UPFC series active-power description does not match a branch-reactance PSS/E proxy.
2. S2 candidate evaluation is one-step and software-based; neither quantum speedup nor multistep planning is measured.
3. The 9-D action representation has only eight physically active elements.
4. Smooth arbitration and convex setpoint blending do not prove network-wide security or Lyapunov dynamic stability.
5. Archived HIL and Stage-1 results are separate from PSS/E and require their own verifiable provenance.
6. All numerical statements in the new PSS/E results and conclusions remain pending licensed experiments.

## Zotero import
In Zotero: `File → Import → A file`, select `references/academic_writing_guidance.bib`. These are institutional guides, not approximately 50 analysed dissertations.
