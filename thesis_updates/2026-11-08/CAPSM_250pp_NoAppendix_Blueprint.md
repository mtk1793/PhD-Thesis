# CAPSM PhD Thesis — Expansion Blueprint to ≥250 pp Main Text (No Appendix)

**Source manuscript:** `C:\Users\mtk17\Downloads\CAPSM_PhD_Thesis_Final_313pg_2026-11-08.docx`
**Source current size:** ≈106,000 words of body text across Chapters 1–13 plus Appendices A–E.
**Source current main-text length:** ≈150 pages including figures and tables.
**Explicit target:** ≥250 pages of **main text only**, with **no separate appendix**.
**Required net addition:** ≈+100 pages, i.e. ≈+50,000–60,000 words of new substantive content plus new figures, tables, derivations, pseudocode, worked examples and literature critique.
**Rule of thumb used throughout:** 450–550 words per typeset body page once figures and tables are counted.

---

## 0. How To Use This Blueprint

- Read Section 1 before writing anything; it fixes the rules that keep the expansion honest and non-padding.
- Section 2 gives the master page/word arithmetic and the chapter-level quota table.
- Section 3 maps every Appendix A–E artefact to a body location; there is no appendix in the final thesis.
- Section 4 defines the global standards for equations, figures, tables, pseudocode, literature and status tags.
- Section 5 is the chapter-by-chapter, subsection-by-subsection writing plan.
- Every subsection entry has the same shape: current state, gap, paragraph plan, equations, figures, tables, pseudocode, literature, worked example, status tag, acceptance test.
- Section 6 reconciles the page budget after drafting.
- Section 7 is the pre-expansion checklist.
- Section 8 is the post-expansion integration and cross-reference checklist.
- Section 9 lists prohibited padding techniques.
- Section 10 is the claim-integrity ledger that must remain true after expansion.
- Section 11 is the figure inventory to commission.
- Section 12 is the table inventory to commission.
- Section 13 is the equation inventory to number.
- Section 14 is the algorithm inventory to typeset.
- Section 15 is the literature-addition worksheet.
- Section 16 is the per-chapter acceptance scorecard.
- Section 17 is the drafting order and time plan.

---

## 1. Hard Constraints

### 1.1 Substance constraint

- Every added page must contain at least one of the following:
  - a numbered equation with symbols and units defined;
  - a figure with a caption, axis units and a stated source;
  - a table with headers and at least one worked row;
  - a pseudocode block with inputs and outputs;
  - a worked numerical substitution;
  - a critical literature comparison;
  - a limitation, threat-to-validity or falsifiability discussion.
- A page that only restates earlier conclusions does not count toward the target.
- A page that only reformats existing material does not count toward the target.

### 1.2 No-appendix constraint

- Appendix A disappears; its reproduction and environment content moves into Chapter 10 and a short evidence section in Chapter 11.
- Appendix B disappears; its claim-reconciliation table moves into Chapter 1 (contribution truth table) and Chapter 13 (evidence boundaries).
- Appendix C disappears; its audit matrix moves into Chapter 10 (claim classes) and Chapter 12 (limits).
- Appendix D disappears; its 41-case cross-solver table moves into Chapter 11, typeset landscape and renumbered.
- Appendix E disappears; its 168-row baseline trajectory is condensed into daily summaries, key-hour extracts and three figures inside Chapter 11.
- Row-level data that cannot fit in the body is retained only in the archive and referenced by hash; it is not reproduced as an appendix.

### 1.3 Honesty constraint

- Chapters 1–9 currently contain forward-looking or past-tense claims about HIL, OPAL-RT, PINN, HMARL and fault-accuracy results.
- Every such claim must be converted to protocol or future tense and status-tagged.
- The execution-versus-efficacy distinction established in Chapters 10–13 must be preserved and extended.
- Design targets must never be presented as measured results.
- Negative results must not be softened; they are the credibility anchor of the thesis.

### 1.4 Formatting constraint

- Do not enlarge font, margins, line spacing, paragraph spacing, or figure whitespace to reach the page target.
- Do not insert blank pages, filler figures, or repeated acknowledgements.
- Do not split a table across many pages to inflate page count.
- Do not duplicate the same figure under a new number.

### 1.5 Consistency constraint

- Choose one spelling convention (optimisation, modelling, localisation, normalisation, behaviour) and apply it globally.
- Choose one abbreviation policy: define at first use and again in the nomenclature table.
- Choose one tense policy: present tense for design and methods, past tense for executed experiments, future tense for planned campaigns.
- Choose one symbol convention: vectors bold lower-case, matrices bold upper-case, scalars italic.

### 1.6 Cross-reference constraint

- Recompute every section, table, figure, equation and algorithm number after moving appendix content.
- Update every in-text reference and every forward reference.
- Regenerate the list of figures, list of tables, list of algorithms and nomenclature.
- Verify no reference points to a deleted appendix label.

---

## 2. Master Page And Word Arithmetic

### 2.1 Current estimate

- Existing Chapters 1–13 body text: ≈106,000 words.
- Existing figures and tables: ≈45–55 items.
- Existing main-text pages: ≈150.
- Existing appendices A–E: ≈45 pages (to be absorbed, not retained).

### 2.2 Target estimate

- Target main-text words: ≈160,000–170,000.
- Target main-text pages: ≈255–290.
- Net new words: ≈55,000–65,000.
- Net new figures: ≈55–70.
- Net new tables: ≈35–45.
- Net new numbered equations: ≈70–90.
- Net new algorithms: ≈6.

### 2.3 Chapter quota table

| Chapter | Current pp | Added pp | Target pp | New words |
|---|---:|---:|---:|---:|
| 1 Introduction | 12 | +6 | 18 | +4,000 |
| 2 Literature Review | 16 | +14 | 30 | +7,000 |
| 3 Proposed Framework | 20 | +14 | 34 | +7,000 |
| 4 Advanced AI Architecture | 18 | +12 | 30 | +6,000 |
| 5 Placement Methodology | 10 | +8 | 18 | +4,000 |
| 6 Stability | 10 | +8 | 18 | +4,000 |
| 7 Fault Detection | 10 | +8 | 18 | +4,000 |
| 8 EV/DER | 12 | +8 | 20 | +4,000 |
| 9 Coordinated Control | 10 | +8 | 18 | +4,000 |
| 10 Methodology | 14 | +8 | 22 | +4,500 |
| 11 Results | 16 | +10 | 26 | +5,500 |
| 12 Discussion | 8 | +6 | 14 | +3,000 |
| 13 Conclusions | 4 | +4 | 8 | +2,000 |
| 14 Absorbed Evidence (new) | 0 | +22 | 22 | +11,000 |
| Front matter additions | 0 | +6 | 6 | +3,000 |
| **Total** | **≈150** | **≈+130** | **≈280** | **≈+70,000** |

### 2.4 Trim rule

- If the draft exceeds 290 pp, trim Chapter 14 first:
  - condense Appendix E rows to daily summaries only;
  - condense Appendix D to best/worst per device plus a pointer to archive;
  - keep all equations and proofs.
- Never trim Chapter 10 or Chapter 12 honesty material to meet the page target.

---

## 3. Appendix Absorption Map

### 3.1 Appendix A → Chapter 10 (Section 10.12) and Chapter 11 (Section 11.12)

- Evidence index E-B through E-G.
- Primary record paths.
- Scope per evidence ID.
- Archive filename `CAPSM_PSSE33_evidence_2026-11-08.zip` (no `(1)`).
- SHA-256 manifest hash.
- Per-artefact SHA-256.
- Reproduction commands.
- Environment table.
- PSS/E licence note.

### 3.2 Appendix B → Chapter 1 (Section 1.7) and Chapter 13 (Section 13.2)

- Original design claim versus disposition.
- Claim-to-evidence table with status tags.
- Explicit list of excluded claims.

### 3.3 Appendix C → Chapter 10 (Section 10.8) and Chapter 12 (Section 12.9)

- Claim class → executed observation → permitted inference → not established.
- Statistical estimands (Δ-L).
- Conventions.
- Evidence-level result summary.

### 3.4 Appendix D → Chapter 11 (Section 11.3)

- Full 41-case cross-solver table.
- Landscape typesetting.
- Fixed tags (no identifier split across lines).
- PASS = numerical agreement, not controllability.

### 3.5 Appendix E → Chapter 11 (Section 11.2)

- 168-row baseline condensed to daily summary table.
- Key-hour extracts.
- Three trajectory figures.
- Non-converged rows treated as failure events, not zero values.

---

## 4. Global Content Standards

### 4.1 Equation standard

- Number per chapter: (3.1), (3.2), … restart in each chapter.
- Define every symbol immediately after first use on the same page.
- State units: p.u., MW, MVAr, kV, Hz, s, ms, MWh, EUR.
- Use consistent sign conventions; declare them before first use.
- Give one worked numeric substitution per major derivation chapter (3, 4, 5, 8).
- Check PDF rendering of exponents and minus signs.
- Fix the known abstract defect `5.26×10 ⁴⁻` → `5.26×10^{-4}`.

### 4.2 Figure standard

- Vector format (PDF/SVG) wherever possible.
- Axis labels include units.
- Caption below the figure, beginning with the figure number.
- Source line beneath the caption when generated from the archive.
- Colour-blind-safe palette; never encode meaning by colour alone.
- Every figure referenced in text before it appears.
- Register every figure in the list of figures.

### 4.3 Table standard

- Header row states quantity, symbol and unit.
- No identifier split across lines (fix Appendix D tags).
- Landscape orientation for the 41-case table and the N-1 summary.
- Repeat header rows across page breaks.
- Register every table in the list of tables.
- Align numeric columns on the decimal point.

### 4.4 Pseudocode standard

- One algorithm environment per method.
- Numbered algorithm, numbered lines.
- Inputs and outputs listed before the body.
- Complexity stated where relevant.
- Use a fixed style: `for`, `while`, `if`, `return`, `sample`.
- Keep line length within the text block.

### 4.5 Literature standard

- Add 2–3 representative citations per subsection.
- Each citation gets one sentence: contribution plus critical limitation relevant to CAPSM.
- Avoid over-reliance on a single source (for example [50]).
- Prefer sources published within the last five years where available.
- Flag outdated sources (for example WEO 2023) and update to the latest edition.

### 4.6 Status-tag vocabulary

- **Design:** specified but not implemented.
- **Method:** implemented as a procedure or model definition.
- **Implemented:** present in the codebase and executed offline.
- **Measured:** produced numbers in the archive.
- **Validated:** independently reproduced or cross-checked.
- **Future work:** planned, not executed.

### 4.7 Claim-integrity rule

- Every device, controller, experiment and target carries exactly one status tag.
- Every table and figure caption inherits the status of its underlying evidence.
- Any sentence that mixes designed and measured content must be split into two sentences, each tagged.

---

## 5. Chapter-By-Chapter Expansion Blueprint

### Chapter 1 — Introduction (Target 18 pp, +6 pp, +4,000 words)

#### 1.1 Background on Power-System Challenges in the Renewable Era

**Current state:** qualitative narrative on renewable growth, inverter displacement, bidirectional flows, complexity, cybersecurity and market friction.
**Gap:** no quantified capacity trajectory, no swing-equation link from inertia to RoCoF, no minimal FDI worked example, no quantitative-impact column in Table 1.1.

**Paragraph plan:**
- P1: global capacity growth sentence with solar/wind/hydro numbers and IRENA citation; add the capacity-versus-energy caveat.
- P2: ramp-rate paragraph with the German OPSD three-hour ramp; convert 28 GW over 3 h into 9.33 GW/h and state the reserve implication.
- P3: reduced-inertia paragraph; define H; write the swing equation; derive Δf/Δt ≈ ΔP/(2H_sys); cite low-inertia literature; note H_sys is not observable at every bus.
- P4: cybersecurity paragraph; write z = h(x) + e + a; give the two-measurement one-state example; explain why a ∈ col(H) leaves the residual unchanged; explain PTP alignment.
- P5: transition paragraph linking the five challenges to the three capability gaps that motivate CAPSM.

**Equations to add:**
- (1.1) Swing equation: (2H/ω_s)·d²δ/dt² = P_m − P_e.
  - H: inertia constant [s].
  - ω_s: synchronous speed [rad/s].
  - δ: rotor angle [rad].
  - P_m, P_e: mechanical and electrical power [p.u.].
- (1.2) RoCoF approximation: df/dt ≈ ΔP/(2H_sys).
  - ΔP: power imbalance [p.u.].
  - H_sys: system inertia constant [s].
- (1.3) FDI measurement model: z = h(x) + e + a.
  - z: measurement vector.
  - h(·): measurement function.
  - x: state vector.
  - e: noise.
  - a: attack vector.

**Figures to add:**
- Figure 1.1: global installed renewable capacity 2010–2023.
  - X-axis: year [—].
  - Y-axis: installed capacity [GW].
  - Series: solar, wind, hydro.
  - Caption draft: "Figure 1.1. Global installed renewable capacity by technology, 2010–2023. Capacity is not energy; capacity factors differ across technologies. Source: IRENA."
  - Source line: IRENA capacity statistics.
- Figure 1.2: challenge-to-capability map.
  - Left column: five challenges.
  - Right column: three CAPSM capabilities.
  - Arrows: one per mapped pair.
  - Caption draft: "Figure 1.2. Mapping from system challenges to CAPSM capabilities."

**Tables to add:**
- Table 1.1 expansion: add a "Quantitative impact" column.
  - Column 1: challenge.
  - Column 2: mechanism.
  - Column 3: quantitative impact with units.
  - Column 4: CAPSM response.
  - Sample row: reduced inertia | fewer synchronous machines | RoCoF ↑ for fixed ΔP | fast reflex control.

**Worked example:**
- 28 GW over 3 h → 28/3 = 9.33 GW/h average ramp.
- State that intra-window peaks can exceed the average.
- State the reserve implication in MW.

**Literature:**
- IRENA capacity statistics — contribution: authoritative capacity series; limitation: capacity, not energy.
- Low-inertia review — contribution: RoCoF framing; limitation: system-level H not bus-observable.
- FDI/state-estimation survey — contribution: attack taxonomy; limitation: assumes full network observability.

**Status:** Context/Design. No measured content in this subsection.
**Acceptance:** figure 1.1 has units and a source line; equations (1.1)–(1.3) define all symbols; Table 1.1 has a unit-bearing quantitative column.

#### 1.2 Evolution of FACTS Devices

**Current state:** Hingorani/Gyugyi history, device families, IEEE 39-bus placement, response-time table.
**Gap:** no defining equations per device, no capability figure, no modelling-fidelity column, no forward reference to the executed neutralisation findings.

**Paragraph plan:**
- P1: brief history and the two FACTS families (shunt/series) with the defining quantity of each.
- P2: SVC derivation and operating range.
- P3: STATCOM derivation and the V–I capability curve; explain why a converter is a current source.
- P4: TCSC derivation and the operational band [0.3, 0.7].
- P5: UPFC derivation and the lossless DC-link balance assumption; state how losses break it.
- P6: forward reference: bus-39 shunt neutralised by generator regulation; UPFC series modelled as X-compensation proxy.

**Equations to add:**
- (1.4) SVC reactive power: ΔQ = B·V².
  - B: shunt susceptance [p.u.].
  - V: bus voltage magnitude [p.u.].
  - B ∈ [−B_max, +B_max].
- (1.5) STATCOM reactive current: I_q ∈ [−I_max, +I_max].
  - I_q: reactive current [p.u.].
  - I_max: converter current limit [p.u.].
- (1.6) TCSC effective reactance: X_eff(k) = (1 − k)·X_line.
  - k: compensation degree [—], k ∈ [0, 1].
  - X_line: line reactance [p.u.].
  - Operational band k ∈ [0.3, 0.7].
- (1.7) UPFC lossless DC-link balance: P_sh = −P_se.
  - P_sh: shunt converter active power [p.u.].
  - P_se: series converter active power [p.u.].

**Figures to add:**
- Figure 1.3: STATCOM V–I capability curve.
  - X-axis: bus voltage [p.u.].
  - Y-axis: reactive current [p.u.].
  - Shape: constant-current region then constant-power region.
  - Caption draft: "Figure 1.3. Idealised STATCOM voltage–current capability."
- Figure 1.4: TCSC effective reactance versus compensation degree.
  - X-axis: k [—].
  - Y-axis: X_eff/X_line [—].
  - Annotation: operational band [0.3, 0.7].
  - Caption draft: "Figure 1.4. TCSC effective reactance as a function of compensation degree."

**Tables to add:**
- Table 1.2 expansion: columns device | defining equation | rating range | PSS/E steady-state fidelity | known limitation.
  - Sample row: SVC | ΔQ = B·V² | ±(50–300) MVAr | susceptance injection | no dynamics.

**Literature:**
- Hingorani and Gyugyi — contribution: canonical FACTS taxonomy; limitation: predates converter-dominated grids.
- STATCOM control review — contribution: V–I behaviour; limitation: idealised converter.
- TCSC modelling paper — contribution: reactance model; limitation: sub-synchronous interaction not covered.

**Status:** Design/Context; device models are Method.
**Acceptance:** four defining equations present; two capability figures present; Table 1.2 has a fidelity column; forward reference to Chapter 11 included.

#### 1.3 Integration of EVs into Smart Grids (V2G/G2V)

**Current state:** Kempton/Tomic V2G potential, charging reviews, aggregated station model.
**Gap:** no direction-dependent energy equation, no worked SoC example, no cluster table, no service-timescale matrix.

**Paragraph plan:**
- P1: V2G concept and the two directions (V2G, G2V).
- P2: station energy-balance derivation with direction-dependent efficiency.
- P3: worked numeric example (50 MW / 100 MWh station).
- P4: charger technology: single-stage versus two-stage, bidirectional DC-DC, isolation.
- P5: fleet clusters and their flexibility characteristics.
- P6: service-timescale fit: primary/secondary/tertiary versus EV power/energy limits.

**Equations to add:**
- (1.8) Charging energy update: E_{t+1} = E_t + η·P·Δt/C.
  - E: state of charge [—].
  - η: one-way efficiency [—].
  - P: charging power [p.u. or MW].
  - Δt: step [s or h].
  - C: station energy capacity [MWh].
- (1.9) Discharging energy update: E_{t+1} = E_t − P·Δt/(η·C).
  - Same symbols; P > 0 denotes charging by convention.

**Worked example:**
- C = 100 MWh, E = 0.5, P = 25 MW, η = 0.92, Δt = 1 h.
- Battery energy removed = 25 MWh.
- AC energy delivered = 25 × 0.92 = 23 MWh.
- New SoC = 0.5 − 25/100 = 0.25.
- State the round-trip deficit explicitly.

**Figures to add:**
- Figure 1.5: EV charging topologies (single-stage, two-stage with DC-DC, isolated).
  - Three panels, labelled (a), (b), (c).
  - Caption draft: "Figure 1.5. EV charger topologies relevant to bidirectional operation."

**Tables to add:**
- Table 1.3: EV fleet clusters.
  - Columns: cluster | typical plug-in window | dwell duration | power [kW] | price sensitivity | flexibility rating.
  - Sample row: overnight residential | 18:00–07:00 | 8–12 h | 7–11 | high | high.
- Table 1.4: service–timescale matrix.
  - Columns: service | timescale | power need | energy need | EV fit.
  - Sample row: primary frequency | seconds | high | low | converter-limited.

**Literature:**
- Kempton and Tomic — contribution: V2G value framing; limitation: assumes fleet availability.
- Charging review — contribution: topology taxonomy; limitation: little on degradation.
- Aggregation study — contribution: station equivalence; limitation: homogeneity assumption.

**Status:** Method; frequency-regulation strategies are Design.
**Acceptance:** equations (1.8)/(1.9) with sign convention; worked example reconciles MWh and MW correctly; two tables present.

#### 1.4 Research Motivation

**Current state:** technical, economic and environmental imperatives; data honesty; AI plausibility.
**Gap:** economic example lacks arithmetic; data-honesty argument lacks a reproducibility citation; AI-insufficiency argument lacks a sample-efficiency number.

**Paragraph plan:**
- P1: technical imperative restated with the Chapter 1.1 numbers.
- P2: economic worked illustration and its caveat.
- P3: environmental imperative tied to curtailment avoidance.
- P4: data honesty: synthetic versus observed profiles and reproducibility.
- P5: AI insufficiency: constraint violation risk and sample inefficiency; why a hybrid frame.

**Worked example:**
- 0.05% loss reduction on a 10 GW system = 5 MW.
- At 50 EUR/MWh: 5 × 50 = 250 EUR/h.
- Over a year at 8,760 h: ≈2.19 MEUR.
- Caveat: illustrative, not a claim for IEEE 39-bus.
- Correct any earlier 19 MEUR figure or explain its basis.

**Tables to add:**
- Table 1.5: motivation-to-objective map.
  - Columns: imperative | metric | design target | objective.
  - Sample row: technical | voltage violation count | minimise | O1.

**Status:** Context.
**Acceptance:** every arithmetic claim reconciles; caveat present; no unlabelled extrapolation.

#### 1.5 Problem Statement

**Current state:** coordinated real-time control; Kahneman metaphor; five gaps.
**Gap:** no formal research questions; no scope box; gaps not each mapped to a response.

**Paragraph plan:**
- P1: define the control problem in one formal sentence (objective, constraints, horizon).
- P2: the dual-process metaphor and why it fits.
- P3: RQ1 stated and unpacked.
- P4: RQ2 stated and unpacked.
- P5: RQ3 stated and unpacked.
- P6: RQ4 stated and unpacked.
- P7: RQ5 stated and unpacked.
- P8: scope box in words.

**Research questions to add:**
- RQ1: Can a dual-process architecture separate reflexive and deliberative FACTS–EV control over a shared action interface?
- RQ2: Can a deliberative optimiser decide under uncertainty within supervisory cycles?
- RQ3: Can coordinated FACTS–EV control be formulated in one constrained action space?
- RQ4: Can faults be detected and localised from heterogeneous telemetry?
- RQ5: Can the framework be validated through a staged campaign?

**Scope box content:**
- Studied: offline PSS/E 33.4 AC quasi-static analysis.
- Studied: IEEE 39-bus benchmark.
- Studied: German OPSD profiles mapped to the benchmark.
- Not studied: EMT dynamics.
- Not studied: hardware execution.
- Not studied: measured PINN or HMARL performance.
- Not studied: dynamic security.

**Tables to add:**
- Table 1.6: gap → research question → response.
  - Columns: gap | RQ | thesis response | chapter.
  - Sample row: no shared action space | RQ3 | nine-dimensional action box | Ch 3–4.

**Status:** Context/Problem definition.
**Acceptance:** five RQs enumerated; scope box explicit; each gap mapped to a response.

#### 1.6 Research Objectives

**Current state:** O1–O5 with quantitative design targets.
**Gap:** no traceability table; targets not labelled design-only; achieved status not stated honestly.

**Paragraph plan:**
- P1: O1 statement plus why it is a design target.
- P2: O2 statement plus why it is a design target.
- P3: O3 statement plus why it is a design target.
- P4: O4 statement plus why it is a design target.
- P5: O5 statement plus the honest convergence status.
- P6: how each objective is revisited in Chapters 10–13.

**Tables to add:**
- Table 1.7: requirements traceability.
  - Columns: objective | gap | design target | measurement method | success criterion | achieved status.
  - Sample row: O5 | convergence | 100% | solver status | all steps converge | not achieved (132/168).
- Table 1.8: objective-to-chapter map.
  - Columns: objective | primary chapter | evidence ID.
  - Sample row: O1 | Ch 11 | E-D.

**Status:** Design targets.
**Acceptance:** every target labelled design-only; O5 status honest; traceability table complete.

#### 1.7 Original Contributions

**Current state:** nine contributions stated.
**Gap:** no per-contribution technical paragraph; no evidence ID; no explicit reconciliation of overclaims.

**Paragraph plan:**
- P1: contribution 1 technical detail and evidence status.
- P2: contribution 2 technical detail and evidence status.
- P3: contribution 3 technical detail and evidence status.
- P4: contribution 4 technical detail and evidence status.
- P5: contribution 5 technical detail and evidence status.
- P6: contribution 6 technical detail and evidence status.
- P7: contribution 7 technical detail and evidence status.
- P8: contribution 8 technical detail and evidence status.
- P9: contribution 9 technical detail and evidence status.
- P10: summary of what is and is not claimed.

**Explicit reconciliations to write:**
- Contribution 2: no quantum speedup; amplitude-based Boltzmann candidate selection only.
- Contribution 3: sigmoid arbiter not validated; measured `arbiter_exact` selects among 31 random plus 1 learned proposal.
- Contribution 5: fault detection is design only; no measured accuracy.
- Contribution 8: HIL is methodology only; no hardware execution in this edition.
- Contribution 9: test count is 52 collected, 49 passed, 3 skipped (licence-gated).

**Tables to add:**
- Table 1.9: contribution truth table.
  - Columns: # | contribution | chapter | evidence ID | status | what is not claimed.
  - Sample row: 2 | QIRL selection | 3 | E-E | Method | quantum advantage.

**Status:** Mixed; table must be truthful.
**Acceptance:** nine rows in truth table; each overclaim reconciled; no untagged claim.

#### 1.8 Thesis Organization

**Current state:** one paragraph per chapter.
**Gap:** chapter summaries too short; no dependency figure; no reader's guide.

**Paragraph plan:**
- P1: Chapter 2 summary in 3–4 sentences with evidence status.
- P2: Chapter 3 summary.
- P3: Chapter 4 summary.
- P4: Chapters 5–9 summary as the design/method block.
- P5: Chapter 10 summary as methodology.
- P6: Chapter 11 summary as evidence.
- P7: Chapters 12–13 summary as discussion and conclusions.
- P8: Chapter 14 summary as absorbed evidence.

**Figures to add:**
- Figure 1.6: chapter dependency graph.
  - Nodes: Ch1 … Ch14.
  - Edges: Ch1→Ch2→Ch3→Ch4→Ch10→Ch11→Ch12→Ch13; side edges Ch3→Ch5–9.
  - Caption draft: "Figure 1.6. Chapter dependency graph. Solid edges show the main argument path; side edges show design branches."

**Reader's guide box:**
- If you want measured results only, read Chapters 10–11 and Chapter 14.
- If you want architecture, read Chapters 3–9.
- If you want limits, read Chapters 10 and 12.

**Status:** Synthesis.
**Acceptance:** dependency figure present; every chapter summarised in 3–4 sentences; reader's guide present.

---

### Chapter 2 — Literature Review (Target 30 pp, +14 pp, +7,000 words)

#### 2.1 Evolution of AI Applications in Power Systems

**Current state:** six eras, timeline figure, Table 2.1.
**Gap:** thin per-era coverage; no DRL algorithm table; no hardware-validation scarcity discussion.

**Paragraph plan:**
- P1: era I (expert systems) with two new citations and one limitation each.
- P2: era II (shallow ML) with two new citations and limitations.
- P3: era III (deep learning) with two new citations and limitations.
- P4: era IV (DRL) with the algorithm table introduced.
- P5: era V (physics-informed) with scarcity-of-validation critique.
- P6: era VI (hybrid/cognitive) with positioning of CAPSM.
- P7: synthesis: what the eras show about validation gaps.

**Tables to add:**
- Table 2.1 expansion: era | representative methods | strength | weakness | validation level.
- Table 2.2: DRL algorithms in power systems.
  - Columns: algorithm | typical application | constraint handling | known limitation.
  - Sample row: DDPG | continuous voltage control | reward shaping | sample inefficiency.

**Figures to add:**
- Figure 2.1 update: AI-era timeline with hardware-validation markers.
  - X-axis: year [—].
  - Markers: surveys and first hardware demonstrations.
  - Caption draft: "Figure 2.1. Evolution of AI in power systems with hardware-validation milestones."

**Literature:**
- Expert-system review — contribution: early rule-based control; limitation: brittle.
- Deep-learning grid review — contribution: representation learning; limitation: data hunger.
- DRL survey — contribution: algorithm taxonomy; limitation: simulation-only evaluation.
- PINN review — contribution: physics constraints; limitation: training cost.
- Safe-RL survey — contribution: constraint guarantees; limitation: conservative.

**Status:** Literature survey.
**Acceptance:** two new citations per era; DRL table present; timeline markers present.

#### 2.2 FACTS Devices and Their Applications

**Current state:** classification tree, device descriptions, Table 2.2 response orders.
**Gap:** no derivations in this chapter; no capability figure; no fidelity column; no neutralisation forward reference.

**Paragraph plan:**
- P1: classification tree explained in words.
- P2: shunt devices with the SVC derivation cross-referenced to (1.4).
- P3: series devices with the TCSC derivation cross-referenced to (1.6).
- P4: combined devices with the UPFC balance cross-referenced to (1.7); discuss losses here.
- P5: applications per family.
- P6: modelling fidelity in PSS/E.
- P7: forward reference to the Chapter 11 neutralisation evidence.

**Equations to add:**
- (2.1) SVC susceptance injection into Y-bus.
  - ΔY_ii = jB.
  - B: susceptance [p.u.].
- (2.2) TCSC branch reactance update.
  - X_branch ← X_line − ΔX.
  - ΔX: inserted compensation [p.u.].
- (2.3) UPFC equivalent current injection.
  - I_inj = (V_se)/(jX_se).
  - V_se: series voltage [p.u.].
  - X_se: series reactance [p.u.].

**Figures to add:**
- Figure 2.2: FACTS classification tree.
- Figure 2.3: device capability panels (STATCOM V–I; TCSC X–k).
  - Two panels, labelled (a) and (b).

**Tables to add:**
- Table 2.3: device modelling fidelity.
  - Columns: device | defining equation | rating range | PSS/E model | limitation.
  - Sample row: UPFC | (2.3) | 100–300 MVA | series X proxy | no independent shunt.

**Literature:**
- FACTS textbook — contribution: taxonomy; limitation: legacy focus.
- TCSC modelling — contribution: reactance control; limitation: SSR omitted.
- UPFC review — contribution: capability; limitation: cost.

**Status:** Method/Design.
**Acceptance:** three equations; two figures; fidelity table; forward reference present.

#### 2.3 AI Approaches for Decision-Making in Power Grids

**Current state:** RL framing, safe RL, MPC, PINNs, imitation, stability assessment.
**Gap:** mathematics of each approach not written; no comparison table.

**Paragraph plan:**
- P1: RL formulation: state, action, reward, transition.
- P2: constrained policy optimisation and the Lagrangian.
- P3: Lyapunov-based safety.
- P4: MPC formulation and AC-OPF nonconvexity.
- P5: PINN residual loss.
- P6: imitation learning and distribution shift.
- P7: synthesis table and CAPSM positioning.

**Equations to add:**
- (2.4) RL objective: J(θ) = E[Σ γ^t r_t].
  - θ: policy parameters.
  - γ: discount factor [—].
  - r_t: reward at t.
- (2.5) Lagrangian: L = J(θ) + λ·J_c(θ).
  - J_c: constraint cost.
  - λ: multiplier.
- (2.6) Lyapunov condition: V̇(x) < 0.
  - V: candidate function.
  - x: state.
- (2.7) MPC objective: min Σ (x−x_ref)ᵀQ(x−x_ref) + uᵀRu.
  - Q, R: weights.
- (2.8) PINN loss: L = L_data + λ_phys·||f(x,u)||².
  - f: physics residual.

**Tables to add:**
- Table 2.4: method comparison.
  - Columns: method | strength | weakness | grid fit | real-time feasibility.
  - Sample row: MPC | constraints | compute | strong | limited at sub-second.

**Literature:**
- Safe-RL — contribution: guarantees; limitation: conservative.
- MPC review — contribution: constraint handling; limitation: cost.
- PINN paper — contribution: physics loss; limitation: out-of-envelope.
- Imitation study — contribution: sample efficiency; limitation: shift.

**Status:** Method/Context.
**Acceptance:** five equations; comparison table; each method has a limitation sentence.

#### 2.4 EV and V2G/G2V Architectures

**Current state:** Kempton/Tomic, charging reviews, topologies, V2H/V2X.
**Gap:** no topology detail, no aggregation justification, no degradation model, no market trade-off.

**Paragraph plan:**
- P1: V2G/G2V/V2H/V2X definitions.
- P2: charger topologies in detail.
- P3: aggregation and the law of large numbers.
- P4: heterogeneity caveat.
- P5: battery degradation model.
- P6: market services and the revenue-versus-degradation trade-off.

**Equations to add:**
- (2.9) Aggregation: P_station = Σ_i P_i.
  - P_i: vehicle power [MW].
- (2.10) Degradation throughput: Q_loss = f(E_th, k_e).
  - E_th: throughput energy [MWh].
  - k_e: degradation coefficient.
- (2.11) Throughput cost: c_deg = k_e·E_th.
  - c_deg: degradation cost [EUR].

**Figures to add:**
- Figure 2.4: charger topology comparison.
- Figure 2.5: revenue-versus-degradation trade-off.
  - X-axis: discharged energy [MWh].
  - Y-axis: net value [EUR].

**Tables to add:**
- Table 2.5: V2G services.
  - Columns: service | timescale | revenue basis | degradation risk.
  - Sample row: frequency regulation | seconds–minutes | capacity payment | high.

**Literature:**
- Kempton and Tomic — contribution: V2G value; limitation: fleet assumptions.
- Degradation study — contribution: cycle cost; limitation: chemistry-specific.
- Market study — contribution: revenue streams; limitation: regulatory variance.

**Status:** Method/Design.
**Acceptance:** aggregation and degradation equations; topology figure; trade-off figure.

#### 2.5 Brain-Inspired AI Frameworks

**Current state:** dual-process metaphor, RL substrate.
**Gap:** no mapping of Kahneman to control, no related cognitive architectures, no QIRL precedents.

**Paragraph plan:**
- P1: dual-process theory summary.
- P2: mapping reflex and deliberation onto control timescales.
- P3: error modes of each system.
- P4: ACT-R and SOAR in brief; relevance and irrelevance.
- P5: quantum-cognition precedents as metaphor.
- P6: Boltzmann rationality and the amplitude update.

**Equations to add:**
- (2.12) Boltzmann choice: P(a) ∝ exp(β·r(a)).
  - β: inverse temperature.
  - r(a): reward of action a.
- (2.13) Born-rule probability: P(a_i) = |α_i|².
  - α_i: amplitude [—].

**Tables to add:**
- Table 2.6: cognitive-architecture comparison.
  - Columns: architecture | memory | learning | control fit.
  - Sample row: ACT-R | declarative/procedural | production rules | weak.

**Literature:**
- Kahneman — contribution: dual-process framing; limitation: descriptive.
- ACT-R — contribution: cognitive modelling; limitation: not control.
- Quantum-cognition review — contribution: amplitude models; limitation: no hardware claim.

**Status:** Context/Design.
**Acceptance:** two equations; mapping paragraph; explicit "metaphor only" statement.

#### 2.6 Assessment of Existing Technologies for DER Integration

**Current state:** communication standards and DER integration.
**Gap:** no standards table, no latency-budget implication.

**Paragraph plan:**
- P1: IEC 61850 role and latency.
- P2: IEEE 1547 role and ride-through.
- P3: IEEE C37.118 role and reporting rate.
- P4: IEEE 1588 role and alignment.
- P5: implication for the fusion layer and reflex path.

**Tables to add:**
- Table 2.7: standards matrix.
  - Columns: standard | role | typical latency | CAPSM tier.
  - Sample row: GOOSE | substation messaging | ~3 ms | reflex.

**Literature:**
- IEC 61850 overview — contribution: substation semantics; limitation: configuration complexity.
- IEEE 1547 — contribution: interconnection; limitation: jurisdiction variance.
- C37.118 — contribution: synchrophasors; limitation: reporting latency.

**Status:** Method/Context.
**Acceptance:** standards table; latency implication paragraph.

#### 2.7 Gap Analysis and Motivation for Hybrid Frameworks

**Current state:** five gaps mapped to CAPSM responses.
**Gap:** Gap 5 thin; no gap-response table.

**Paragraph plan:**
- P1: Gap 1 and response.
- P2: Gap 2 and response.
- P3: Gap 3 and response.
- P4: Gap 4 and response.
- P5: Gap 5 (theory–practice divide) in detail.
- P6: survey MIL/SIL/PIL/CHIL/PHIL practice.
- P7: why hardware validation is rare.
- P8: gap-response table introduced.

**Tables to add:**
- Table 2.8: gap-response matrix.
  - Columns: gap | existing limitation | thesis response | chapter | evidence status.

**Literature:**
- HIL survey — contribution: practice map; limitation: cost.
- Offline-AI study — contribution: algorithmic novelty; limitation: no hardware.

**Status:** Context/Design.
**Acceptance:** Gap 5 gets a full paragraph; matrix complete.

#### 2.8 Real-Time Simulation and HIL Validation

**Current state:** OPAL-RT family, HIL hierarchy.
**Gap:** hierarchy undefined; no timing budget; no certification discussion; no pipeline figure.

**Paragraph plan:**
- P1: define MIL, SIL, PIL, CHIL, PHIL with input/output boundaries.
- P2: OPAL-RT/RT-LAB detail.
- P3: timing budget across protection, FACTS, EV, controller.
- P4: certification practice.
- P5: validation pipeline and gates.
- P6: explicit statement that HIL is future work in this edition.

**Tables to add:**
- Table 2.9: validation levels.
  - Columns: level | plant | controller | fidelity | cost.
  - Sample row: CHIL | simulated | hardware | high | medium.
- Table 2.10: timing budget.
  - Columns: function | deadline | margin.
  - Sample row: reflex FACTS | 5 ms | 2 ms.

**Figures to add:**
- Figure 2.6: validation pipeline MIL→SIL→PIL→CHIL.
  - Gates between stages.

**Literature:**
- RT simulation review — contribution: tool comparison; limitation: vendor-specific.
- CHIL/PHIL survey — contribution: fidelity; limitation: interface effects.

**Status:** Method/Context; HIL execution Future work.
**Acceptance:** five levels defined; timing table; pipeline figure; future-work label explicit.

---

### Chapter 3 — Proposed Framework (Target 34 pp, +14 pp, +7,000 words)

#### 3.1 Framework Overview and Design Philosophy

**Current state:** high-level overview and design philosophy.
**Gap:** no full architecture figure, no nomenclature table, no explicit design axioms.

**Paragraph plan:**
- P1: the sensing-to-actuation loop in words.
- P2: why two systems and one interface.
- P3: timescale separation rationale.
- P4: feasibility-by-construction rationale.
- P5: traceability rationale.
- P6: chapter roadmap.

**Figures to add:**
- Figure 3.1: end-to-end architecture.
  - Blocks: sensing → estimation → fusion → System 1 → System 2 → arbiter → actuators → network → measurement.
  - Feedback arrow from measurement to sensing.
  - Caption draft: "Figure 3.1. CAPSM end-to-end control loop."
- Figure 3.2: layered view (physical, control, coordination, decision).

**Tables to add:**
- Table 3.1: nomenclature for Chapter 3.
  - Columns: symbol | meaning | unit.
  - Sample row: B | shunt susceptance | p.u.
- Table 3.2: design axioms.
  - Columns: axiom | rationale | consequence.

**Status:** Design.
**Acceptance:** architecture figure matches code module layout; nomenclature complete.

#### 3.2 Brain-Inspired Dual-Process Control Architecture

**Current state:** System 1, System 2 and blending described qualitatively.
**Gap:** operators not formalised; blending contract not stated; no feasibility proof.

**Paragraph plan:**
- P1: formalise System 1 as f_1(x) → u_1 with latency τ_1.
- P2: formalise System 2 as f_2(x) → candidate set → u_2 with latency τ_2.
- P3: define the stress signal s(t).
- P4: define the blending law.
- P5: state the feasibility assumption.
- P6: prove Proposition 3.1.
- P7: discuss non-convex constraints (SoC) handled by the filter.

**Equations to add:**
- (3.1) System 1 map: u_1 = f_1(x).
  - x: observation vector.
  - u_1: reflex action.
  - τ_1 ≤ 5 ms.
- (3.2) System 2 map: u_2 = argmin_{a ∈ A_c} J(a; x).
  - A_c: candidate set.
  - J: counterfactual cost.
  - τ_2 ≤ 50 ms.
- (3.3) Blending: u = σ(s)·u_1 + (1 − σ(s))·u_2.
  - σ(s) = 1/(1 + e^{−s}).
  - s: stress signal.
- (3.4) Proposition 3.1: if u_1, u_2 ∈ U and U is convex, then u ∈ U.
  - Proof by convexity: u is a convex combination with weights in [0,1].

**Tables to add:**
- Table 3.3: action box (9 dimensions).
  - Columns: index | device | low | high | meaning | status.
  - Row 1: 0 | SVC_14 | −0.5 | 0.5 | susceptance [p.u.] | active.
  - Row 2: 1 | STATCOM_39 | −1.0 | 1.0 | reactive [p.u.] | active.
  - Row 3: 2 | TCSC_16_17 | 0.3 | 0.7 | compensation [—] | active.
  - Row 4: 3 | UPFC_26_shunt | −0.5 | 0.5 | shunt [p.u.] | active.
  - Row 5: 4 | UPFC_26_series_proxy | −0.5 | 0.5 | X proxy [p.u.] | active.
  - Row 6: 5 | UPFC_26_series_Q_RESERVED | 0.0 | 0.0 | reserved | never emitted.
  - Row 7: 6 | EV_3 | −50 | 50 | MW | active.
  - Row 8: 7 | EV_8 | −50 | 50 | MW | active.
  - Row 9: 8 | EV_15 | −50 | 50 | MW | active.

**Status:** Design/Method.
**Acceptance:** Proposition 3.1 stated and proved; action table matches code constants exactly.

#### 3.3 Multi-Layer Coordination Architecture

**Current state:** layers described; service matrix qualitative.
**Gap:** no tier-interaction figure, no timescale table, no standards mapping.

**Paragraph plan:**
- P1: local layer and its devices.
- P2: regional layer and its devices.
- P3: system layer and slack participation.
- P4: information flow between layers.
- P5: communication requirements per layer.
- P6: service matrix with basis column.

**Figures to add:**
- Figure 3.3: tier interaction.
  - Three horizontal bands: local, regional, system.
  - Vertical arrows for upward measurement and downward setpoints.

**Tables to add:**
- Table 3.4: layer timescales.
  - Columns: layer | period | decision | communication.
  - Sample row: local | 5 ms | shunt setpoint | GOOSE.
- Table 3.5: service matrix with basis.
  - Columns: service | layer | basis | status.

**Status:** Design.
**Acceptance:** tier figure present; timescale table matches Chapter 3.9 periods.

#### 3.4 Mathematical Modelling of Integrated Components

**Current state:** models summarised.
**Gap:** no full AC derivation, Jacobian, Newton iteration, worked example, device injection detail, SoC invariance proof, domain-transfer mathematics.

##### 3.4.1 AC Power Flow

**Paragraph plan:**
- P1: nodal power balance statement.
- P2: derive P_i and Q_i.
- P3: define the Jacobian blocks.
- P4: Newton update and convergence test.
- P5: PV/PQ switching and Q-limit enforcement.
- P6: worked two-iteration three-bus example.

**Equations to add:**
- (3.5) Active injection: P_i = V_i Σ_j V_j (G_ij cos θ_ij + B_ij sin θ_ij).
  - V_i: voltage magnitude [p.u.].
  - θ_ij = θ_i − θ_j [rad].
  - G_ij, B_ij: admittance components [p.u.].
- (3.6) Reactive injection: Q_i = V_i Σ_j V_j (G_ij sin θ_ij − B_ij cos θ_ij).
- (3.7) Mismatch: F(x) = [ΔP; ΔQ].
- (3.8) Newton update: Δx = −J⁻¹F(x).
  - J: Jacobian.
- (3.9) Convergence: ||F(x)||_∞ < ε.
  - ε: tolerance [p.u.].

**Tables to add:**
- Table 3.6: Jacobian blocks.
  - Columns: block | shape | derived from.
  - Sample row: ∂P/∂θ | n×n | (3.5).

**Worked example:**
- Three-bus system with specified loads.
- Iteration 1: compute F(x_0); solve (3.8); update.
- Iteration 2: recompute mismatch; show reduction.
- State the converged tolerance.

**Status:** Method.
**Acceptance:** worked example shows two iterations with numbers.

##### 3.4.2 FACTS Device Models

**Paragraph plan:**
- P1: shunt susceptance insertion into Y-bus.
- P2: series reactance modification into branch admittance.
- P3: UPFC equivalent current injection.
- P4: PV-bus Q-limit enforcement and PV→PQ transition.
- P5: equivalence note to MATPOWER `pf.enforce_q_lims`.

**Equations to add:**
- (3.10) Shunt insertion: Y_ii ← Y_ii + jB.
- (3.11) Series update: y_ij ← 1/(jX_branch).
- (3.12) UPFC injection: I_inj = V_se/(jX_se).
- (3.13) Q-limit switch: if Q_g ∉ [Q_min, Q_max] then bus becomes PQ.

**Tables to add:**
- Table 3.7: device-to-model map.
  - Columns: device | PSS/E call | model change | limitation.
  - Sample row: SVC_14 | set_fixed_shunt | Y_ii | static.

**Status:** Method.
**Acceptance:** all four model changes have equations and a code-call mapping.

##### 3.4.3 EV Fleet Aggregation and SoC Dynamics

**Paragraph plan:**
- P1: per-vehicle energy model.
- P2: station aggregation.
- P3: direction-dependent efficiency.
- P4: SoC clamp.
- P5: invariance proof by induction.

**Equations to add:**
- (3.14) Energy update: E_{t+1} = clamp(E_t + η^{sign}·P·Δt/C, E_min, E_max).
- (3.15) Proposition 3.2: if E_0 ∈ [E_min, E_max], then E_t ∈ [E_min, E_max] for all t.
  - Proof: clamp preserves the interval; induction on t.

**Status:** Method.
**Acceptance:** invariance proof complete; clamp defined.

##### 3.4.4 DER Integration and Environment Dispatch

**Paragraph plan:**
- P1: exogenous renewables as negative load.
- P2: synthetic mapping from OPSD to IEEE 39-bus.
- P3: load scaling rule.
- P4: feasibility caveat.

**Equations to add:**
- (3.16) Net load: P_net = P_load − P_res.
- (3.17) Scaling: P_i^39 = P_i^base·κ_t.
  - κ_t: time-varying load factor.

**Status:** Method.
**Acceptance:** mapping rule explicit; caveat present.

#### 3.5 Quantum-Inspired Reinforcement Learning

**Current state:** QIRL described; theorem stated.
**Gap:** full formulation and proof absent; convergence figure absent; status label unclear.

**Paragraph plan:**
- P1: candidate set and amplitude initialisation.
- P2: reward definition.
- P3: amplitude update.
- P4: Born-rule sampling.
- P5: Theorem 3.1 and proof.
- P6: tunnelling rule.
- P7: what it is not (no quantum hardware, no credit assignment).
- P8: convergence illustration.

**Equations to add:**
- (3.18) Initial amplitudes: α_i = 1/√32.
- (3.19) Reward: r(a) = −ΔV − 0.05·N_viol − effort.
- (3.20) Amplitude update: α_i ← α_i·exp(β·r_i)/Z.
  - β = 5.0.
  - Z: normaliser.
- (3.21) Born rule: P(a_i) = |α_i|².
- (3.22) Theorem 3.1: P(a_i)/P(a_j) ∈ [e^{−βΔ}, e^{βΔ}], Δ = max|r|.
  - Proof: ratio of exponentials; offset invariance.

**Figures to add:**
- Figure 3.4: probability-mass evolution over 10 steps.
  - X-axis: step.
  - Y-axis: P(a_i).
  - Series: selected action, mean action.

**Pseudocode to add:**
- Algorithm 3.1: QIRL candidate selection.
  1: initialise α ← uniform
  2: for each step do
  3:   sample candidates from |α|²
  4:   score candidates exactly
  5:   update α by (3.20)
  6:   apply tunnelling with fraction 0.1
  7:   return best candidate
  8: end for

**Status:** Method (implemented); efficacy unresolved.
**Acceptance:** theorem proved; explicit "not RL in the strict sense" statement; convergence figure present.

#### 3.6 Multi-Modal Fault Detection and Localisation

**Current state:** detection concept described.
**Gap:** no WLS derivation, no stealth proof, no autoencoder score, no feature table.

**Paragraph plan:**
- P1: measurement model.
- P2: WLS estimate.
- P3: residual and chi-square test.
- P4: stealth-attack proposition.
- P5: autoencoder score.
- P6: per-class features.
- P7: status of accuracy targets.

**Equations to add:**
- (3.23) Measurement: z = h(x) + e.
- (3.24) WLS estimate: x̂ = argmin (z − h(x))ᵀR⁻¹(z − h(x)).
- (3.25) Residual: r = z − h(x̂).
- (3.26) Test statistic: J = rᵀR⁻¹r ~ χ²_m.
- (3.27) Threshold: J > χ²_{m,1−α}.
- (3.28) Stealth attack: a = Hc ⇒ r unchanged.
  - H: measurement Jacobian.
- (3.29) Autoencoder score: e_rec = ||x − x̂||².

**Tables to add:**
- Table 3.8: fault classes and features.
  - Columns: class | signature | discriminating feature | design target.
  - Sample row: SLG | zero-sequence | I_0 magnitude | 97.2%.

**Status:** Design; HIL execution Future work.
**Acceptance:** stealth proof present; targets labelled design-only.

#### 3.7 Coordinated Control Strategies

**Current state:** strategies described.
**Gap:** reward equation missing; multi-rate figure missing; objective mapping missing.

**Paragraph plan:**
- P1: reward composition.
- P2: multi-rate loop.
- P3: objective-to-asset mapping.
- P4: trade-off discussion.
- P5: why no Pareto front in this edition.

**Equations to add:**
- (3.30) Reward: R = −w_v·ΔV − w_l·ΔLoss − w_viol·N_viol.
  - w_v = 1.0, w_l = 0.5, w_viol = −10.
  - ΔV in p.u.; ΔLoss in MW; N_viol count.

**Figures to add:**
- Figure 3.5: multi-rate control loop.
  - Timelines at 5 ms, 10 ms, 50 ms, 1 h.

**Tables to add:**
- Table 3.9: objective-to-asset map.
  - Columns: objective | asset | tier | narrowest deadline.
  - Sample row: voltage support | SVC | local | 5 ms.

**Status:** Design/Method; measured results only in Chapter 11.
**Acceptance:** reward equation with units; multi-rate figure; mapping table.

#### 3.8 Practical Implementation Considerations

**Current state:** implementation notes.
**Gap:** no edge/fog/central table, no communication table, no ride-through assumptions.

**Paragraph plan:**
- P1: edge/fog/central split.
- P2: determinism versus optimality.
- P3: communication infrastructure.
- P4: DER ride-through assumptions.

**Tables to add:**
- Table 3.10: compute placement.
  - Columns: layer | functions | priority.
  - Sample row: edge | reflex | determinism.
- Table 3.11: communication infrastructure.
  - Columns: standard | role | rate | latency.

**Status:** Design.
**Acceptance:** both tables present; ride-through paragraph cites IEEE 1547.

#### 3.9 HIL-Ready Architecture Design

**Current state:** HIL-ready design described.
**Gap:** core assignment table missing; period inequalities absent; solver stack detail thin; explicit "not executed" label absent.

**Paragraph plan:**
- P1: core assignment.
- P2: period inequality system.
- P3: solver stack.
- P4: embedded realisation.
- P5: budget visualisation.
- P6: explicit status label.

**Equations to add:**
- (3.31) Period chain: τ_1 ≤ 5 ms; τ_arb ≤ 10 ms; τ_2 ≤ 50 ms.
- (3.32) End-to-end: τ_1 + τ_arb + τ_comm ≤ 20 ms.

**Figures to add:**
- Figure 3.6: timing budget.
  - Horizontal bars per path against deadlines.
  - Caption draft: "Figure 3.6. Reflex and deliberative timing budgets against protection-grade deadlines."

**Tables to add:**
- Table 3.12: core assignment.
  - Columns: core | region/function | period.
  - Row 1: Core 1 | northern + System 1 | 5 ms.
  - Row 2: Core 2 | southern + System 2 | 50 ms.
  - Row 3: Core 3 | arbiter + comms | 10 ms.
  - Row 4: Core 4 | I/O + logging | 1 ms.

**Status:** Design; execution Future work.
**Acceptance:** explicit sentence "HIL-ready design, not executed HIL"; period table consistent with Chapter 2.8.

#### 3.10 Summary and Transition

**Paragraph plan:**
- P1: restate each section contribution.
- P2: design-versus-measured box.
- P3: transition to Chapter 4.

**Tables to add:**
- Table 3.13: Chapter 3 status box.
  - Columns: element | status.
  - Sample row: action box | Implemented.

**Status:** Synthesis.
**Acceptance:** every Chapter 3 element carries a status tag.

---

### Chapter 4 — Advanced AI Control Architecture (Target 30 pp, +12 pp, +6,000 words)

#### 4.1 System Design Specifications and Requirements

**Current state:** specifications table.
**Gap:** traceability columns missing; action contract not explicit; reserved-index treatment thin.

**Paragraph plan:**
- P1: requirement list.
- P2: action-interface contract.
- P3: TCSC band justification.
- P4: reserved index 5 treatment.
- P5: non-negotiability of the interface.

**Tables to add:**
- Table 4.1: requirements traceability.
  - Columns: requirement | gap | target | verification | status.
- Table 4.2: action space (repeat of Table 3.3, cross-referenced).
  - Note that duplication is intentional for chapter stand-alone readability.

**Status:** Design/Specification.
**Acceptance:** reserved index pinned to zero in code and documented; contract stated.

#### 4.2 Development of the Brain-Inspired AI Framework

**Current state:** System 1, System 2, arbiter described.
**Gap:** parameter derivation absent; QIRL pseudocode absent; arbiter proof absent; measured-versus-designed arbiter distinction absent.

##### 4.2.1 System 1 (CNN–LSTM)

**Paragraph plan:**
- P1: input schema (159 features).
- P2: convolutional block detail.
- P3: LSTM block detail.
- P4: dense output and activation.
- P5: parameter-count derivation.
- P6: training protocol.
- P7: data split.

**Equations to add:**
- (4.1) Convolution: y_k = φ(Σ w_k * x + b_k).
- (4.2) LSTM state update: f_t, i_t, o_t, c_t, h_t.
- (4.3) Parameter total: N = N_conv + N_lstm + N_dense = 137,418.

**Table to add:**
- Table 4.3: parameter budget.
  - Columns: block | parameters | computation.
  - Sample row: conv1 | 4,352 | 0.9 MFLOP.

**Status:** Implemented/Measured.
**Acceptance:** parameter arithmetic sums to 137,418 exactly.

##### 4.2.2 System 2 (QIRL)

**Paragraph plan:**
- P1: candidate generation.
- P2: counterfactual scoring via solver.
- P3: amplitude update.
- P4: sampling.
- P5: tunnelling.
- P6: complexity analysis.

**Pseudocode to add:**
- Algorithm 4.1: QIRL step.
  1: inputs x, A_c, β
  2: for a in A_c do
  3:   r(a) ← score(a; x)
  4: end for
  5: update α by (3.20)
  6: sample a* from |α|²
  7: apply tunnelling
  8: return a*

**Complexity paragraph:**
- System 2 cost O(|A_c| × solver_calls).
- System 1 cost O(parameters).
- State the 5.8 s measured decision cost in Chapter 11.

**Status:** Implemented.
**Acceptance:** pseudocode matches code; complexity stated.

##### 4.2.3 Metacognitive Arbiter

**Paragraph plan:**
- P1: sigmoid weight.
- P2: five modes.
- P3: transition conditions.
- P4: feasibility proof.
- P5: measured arbiter difference.

**Equations to add:**
- (4.4) Sigmoid: σ(s) = 1/(1 + e^{−s}).
- (4.5) Proposition 4.1: blended action feasible if both inputs feasible.

**Tables to add:**
- Table 4.4: arbiter modes.
  - Columns: mode | condition | action.
  - Sample row: override | s > threshold | System 2.

**Status:** Implemented/Measured (selective).
**Acceptance:** explicit statement that sigmoid arbiter is not validated; measured behaviour described.

#### 4.3 Multi-Layer Control Hierarchy Implementation

**Paragraph plan:**
- P1: tier-to-module mapping.
- P2: data ownership.
- P3: RAW snapshot isolation.
- P4: energy-state reset.

**Tables to add:**
- Table 4.5: module map.
  - Columns: tier | module | file.
  - Sample row: reflex | System 1 | controls.py.

**Status:** Implemented.
**Acceptance:** module table matches repository filenames.

#### 4.4 Data Flow Architecture

**Paragraph plan:**
- P1: step sequence.
- P2: data volumes.
- P3: latency per stage.
- P4: failure handling.

**Figures to add:**
- Figure 4.1: sequence diagram.
  - Participants: sensor, encoder, System 1, System 2, arbiter, solver.

**Tables to add:**
- Table 4.6: data volumes.
  - Columns: stage | payload | per step | per episode.

**Status:** Implemented.
**Acceptance:** latency per stage consistent with Chapter 3.9.

#### 4.5 Real-Time Adaptation Mechanisms

**Paragraph plan:**
- P1: online retraining triggers.
- P2: mode switching.
- P3: safe fallback.
- P4: fallback activation conditions.

**Tables to add:**
- Table 4.7: adaptation triggers.
  - Columns: trigger | threshold | action.

**Status:** Design/Specification.
**Acceptance:** fallback conditions explicit and testable.

#### 4.6 Validation Framework and Methodology

**Paragraph plan:**
- P1: V-model.
- P2: test layers.
- P3: pass/fail criteria.
- P4: execution status.
- P5: test-count reconciliation.

**Figures to add:**
- Figure 4.2: V-model.

**Tables to add:**
- Table 4.8: test layer matrix.
  - Columns: layer | scope | pass criterion | status.
- Table 4.9: test count.
  - Columns: collected | passed | skipped | reason.
  - Row: 52 | 49 | 3 | licence-gated.

**Status:** Method/Implemented (partial).
**Acceptance:** 52/49/3 stated identically everywhere.

#### 4.7 Computational Implementation for Real-Time Deployment

**Paragraph plan:**
- P1: worker architecture.
- P2: PSS/E call walkthrough.
- P3: timing instrumentation.
- P4: environment table.

**Figures to add:**
- Figure 4.3: worker architecture.
  - Python 3.11 orchestrator → Python 2.7 worker → PSS/E 33.4.

**Tables to add:**
- Table 4.10: environment.
  - Columns: component | version | note.
  - Row: PSS/E | 33.4.0.0 | licensed.
  - Row: worker Python | 2.7 32-bit | psspy.
  - Row: orchestrator Python | 3.11 | venv.
- Table 4.11: API call inventory.
  - Columns: call | purpose | returns.

**Status:** Implemented.
**Acceptance:** environment matches Chapter 10.12 and Chapter 14.

#### 4.8 Conclusion

**Paragraph plan:**
- P1: map components to evidence chapters.
- P2: map to future work.

**Status:** Synthesis.
**Acceptance:** no measured claim without evidence ID.

---

### Chapter 5 — FACTS and EV Placement Methodology (Target 18 pp, +8 pp, +4,000 words)

#### 5.1 Optimisation Problem Formulation

**Current state:** placement described qualitatively.
**Gap:** no formal optimisation statement; no sensitivity-based siting; no nonconvexity discussion.

**Paragraph plan:**
- P1: decision variables (type, location, rating).
- P2: objective function composition.
- P3: constraints (voltage, thermal, Q, budget).
- P4: nonconvexity and why heuristics.
- P5: sensitivity-based siting.
- P6: relation to the executed configuration.

**Equations to add:**
- (5.1) Decision vector: x = {type_d, bus_d, rating_d}.
- (5.2) Objective: min J = w_v·Σ|V_i − 1| + w_l·P_loss + w_c·C_inv.
  - w_v, w_l, w_c: weights.
  - C_inv: investment cost [EUR].
- (5.3) Voltage constraint: V_min ≤ V_i ≤ V_max.
- (5.4) Thermal constraint: |S_br| ≤ S_br^max.
- (5.5) Q constraint: Q_d ∈ [Q_min, Q_max].
- (5.6) Budget: Σ C_inv,d ≤ C_max.
- (5.7) Shunt sensitivity: ∂V_i/∂Q_d.
- (5.8) Series sensitivity: ∂P_br/∂X_d.

**Tables to add:**
- Table 5.1: formulation summary.
  - Columns: element | expression | units.
  - Sample row: objective | (5.2) | mixed.

**Status:** Method/Design.
**Acceptance:** full optimisation statement with units; nonconvexity explained.

#### 5.2 Genetic Algorithm Based Placement

**Current state:** GA mentioned.
**Gap:** no encoding, operators, pseudocode or convergence plot.

**Paragraph plan:**
- P1: chromosome encoding.
- P2: fitness function.
- P3: selection.
- P4: crossover.
- P5: mutation.
- P6: elitism.
- P7: convergence behaviour.

**Equations to add:**
- (5.9) Fitness: F = 1/(1 + J).
- (5.10) Mutation rate schedule: μ_g = μ_0·α^g.

**Pseudocode to add:**
- Algorithm 5.1: GA placement.
  1: initialise population P_0
  2: evaluate fitness by (5.9)
  3: for g = 1..G do
  4:   select parents by tournament
  5:   crossover with p_c
  6:   mutate with μ_g
  7:   retain elite
  8:   evaluate offspring
  9: end for
  10: return best individual

**Figures to add:**
- Figure 5.1: GA convergence (illustrative, labelled).

**Status:** Method/Design.
**Acceptance:** pseudocode complete; illustrative figure labelled.

#### 5.3 Particle Swarm Optimisation Based Tuning

**Current state:** PSO mentioned.
**Gap:** no particle dynamics, parameter schedule or pseudocode.

**Paragraph plan:**
- P1: particle state.
- P2: velocity update.
- P3: position update.
- P4: inertia schedule.
- P5: parameter selection.
- P6: stopping rule.

**Equations to add:**
- (5.11) Velocity: v_i ← ω·v_i + c1·r1·(p_i − x_i) + c2·r2·(g − x_i).
  - ω: inertia.
  - c1, c2: cognitive and social coefficients.
  - r1, r2: uniform randoms.
- (5.12) Position: x_i ← x_i + v_i.

**Pseudocode to add:**
- Algorithm 5.2: PSO tuning.
  1: initialise positions and velocities
  2: evaluate
  3: for k = 1..K do
  4:   update v by (5.11)
  5:   update x by (5.12)
  6:   update personal and global best
  7: end for
  8: return global best

**Figures to add:**
- Figure 5.2: PSO convergence.
  - X-axis: iteration.
  - Y-axis: best cost.

**Status:** Method/Design.
**Acceptance:** both update equations and pseudocode present.

#### 5.4 Deep Reinforcement Learning Controller Design

**Current state:** DRL controller described.
**Gap:** no state/action/reward specification; no constraint-handling discussion.

**Paragraph plan:**
- P1: state space.
- P2: action space.
- P3: reward.
- P4: algorithm choice.
- P5: replay and target networks.
- P6: why candidate evaluation replaced pure DRL online.

**Tables to add:**
- Table 5.2: DRL specification.
  - Columns: element | definition | dimension.
  - Sample row: state | voltages, flows | 159.

**Status:** Design; not measured controller.
**Acceptance:** explicit statement that DRL is a design reference not the executed controller.

#### 5.5 Quantum-Inspired Candidate Selection for Real-Time Dispatch

**Paragraph plan:**
- P1: candidate generation link to Chapter 3.5.
- P2: exact scoring.
- P3: interface with placement.
- P4: limitation.

**Status:** Method (implemented in selector).
**Acceptance:** cross-reference to Algorithm 3.1; no duplication of proof.

#### 5.6 Transfer Learning for Cross-Domain Knowledge Transfer

**Paragraph plan:**
- P1: source domain (OPSD).
- P2: target domain (IEEE 39-bus).
- P3: transfer mechanism.
- P4: expected benefit.
- P5: negative-transfer risk.

**Tables to add:**
- Table 5.3: domain differences.
  - Columns: property | source | target.
  - Sample row: frequency | 50 Hz | 60 Hz.

**Status:** Design.
**Acceptance:** negative-transfer risk stated.

#### 5.7 Placement Validation

**Paragraph plan:**
- P1: experiment design.
- P2: baselines.
- P3: metrics.
- P4: statistical test.
- P5: honest statement about optimality.

**Tables to add:**
- Table 5.4: validation plan.
  - Columns: condition | devices | metric | expected.

**Status:** Future work/Design.
**Acceptance:** explicit "engineering configuration, not verified optimum" sentence.

#### 5.8 Chapter Summary

**Paragraph plan:**
- P1: link placement to Chapter 11 neutralisation.
- P2: link to future work.

**Status:** Synthesis.
**Acceptance:** forward reference to bus-39 STATCOM result present.

---

### Chapter 6 — Stability Enhancement Using Deep Learning (Target 18 pp, +8 pp, +4,000 words)

#### 6.1 Transient Stability Assessment Approaches

**Paragraph plan:**
- P1: time-domain simulation.
- P2: direct methods.
- P3: ML screening.
- P4: comparison.
- P5: distribution shift.

**Tables to add:**
- Table 6.1: approach comparison.
  - Columns: approach | strength | weakness | real-time fit.
  - Sample row: time-domain | accurate | slow | offline.

**Status:** Context.
**Acceptance:** comparison table; distribution-shift caveat.

#### 6.2 CNN-LSTM Architecture for Real-Time Stability Assessment

**Paragraph plan:**
- P1: inputs.
- P2: window length.
- P3: outputs.
- P4: architecture.
- P5: training data generation.
- P6: metrics.
- P7: design versus measured.

**Equations to add:**
- (6.1) Input tensor: X ∈ R^{T×F}.
  - T: window length.
  - F: features.
- (6.2) Output: y = P(stable | X).
- (6.3) Margin: M = V_crit − V_operating.

**Figures to add:**
- Figure 6.1: CNN-LSTM architecture for stability.

**Tables to add:**
- Table 6.2: stability metrics.
  - Columns: metric | definition | target.
  - Sample row: false-negative | missed unstable | <1%.

**Status:** Design; no measured stability results in archive.
**Acceptance:** explicit statement that stability is not measured.

#### 6.3 Voltage Stability Enhancement Techniques

**Paragraph plan:**
- P1: PV curve.
- P2: continuation power flow.
- P3: nose point.
- P4: margin.
- P5: corrective actions.
- P6: FACTS coordination.

**Equations to add:**
- (6.4) Continuation: F(x, λ) = 0.
- (6.5) Margin: m = (λ_max − λ_0)/λ_0.

**Figures to add:**
- Figure 6.2: PV curve with nose point.
  - X-axis: load [p.u.].
  - Y-axis: voltage [p.u.].

**Status:** Method/Design.
**Acceptance:** PV figure and margin equation present.

#### 6.4 Custom ML Models for Grid Stability

**Paragraph plan:**
- P1: model variant A.
- P2: model variant B.
- P3: selected architecture rationale.
- P4: split and overfitting checks.

**Tables to add:**
- Table 6.3: model variants.
  - Columns: model | parameters | strength | weakness.

**Status:** Design.
**Acceptance:** at least two variants described with rationale.

#### 6.5 Integration with the System 1 Reflex Path

**Paragraph plan:**
- P1: data flow.
- P2: trigger logic.
- P3: safe setpoint.
- P4: latency budget.

**Figures to add:**
- Figure 6.3: stability-to-reflex data flow.

**Status:** Design.
**Acceptance:** latency budget consistent with 5 ms reflex.

#### 6.6 Chapter Summary

**Paragraph plan:**
- P1: design foundation.
- P2: future measurement plan.

**Status:** Synthesis.
**Acceptance:** no measured stability claim.

---

### Chapter 7 — Fault Detection and Localisation (Target 18 pp, +8 pp, +4,000 words)

#### 7.1 AI-Based Fault Detection and Localisation Approaches

**Paragraph plan:**
- P1: signature-based.
- P2: model-based residual.
- P3: data-driven.
- P4: telemetry roles (PMU, SCADA, inverter).
- P5: comparison.

**Tables to add:**
- Table 7.1: detection approaches.
  - Columns: approach | data | strength | weakness.
  - Sample row: residual | SCADA | interpretable | model-dependent.

**Status:** Context.
**Acceptance:** comparison table; telemetry roles stated.

#### 7.2 Multi-Modal Data Fusion Architecture

**Paragraph plan:**
- P1: signal-level fusion.
- P2: feature-level fusion.
- P3: decision-level fusion.
- P4: PTP alignment.
- P5: attention weights.

**Equations to add:**
- (7.1) Feature map: φ_i(x_i).
- (7.2) Fused feature: φ_fused = Σ α_i·φ_i(x_i).
  - α_i: attention weights.
- (7.3) Softmax attention: α_i = e^{w_i}/Σ e^{w_j}.

**Figures to add:**
- Figure 7.1: fusion architecture.

**Status:** Design.
**Acceptance:** three fusion levels defined; attention equation present.

#### 7.3 Anomaly Detection Methods

**Paragraph plan:**
- P1: WLS residual (cross-ref Chapter 3.6).
- P2: chi-square test.
- P3: Theorem 7.1 proof.
- P4: Proposition 7.1a stealth proof.
- P5: autoencoder score.
- P6: threshold setting.

**Equations to add:**
- (7.4) Residual: r = z − h(x̂).
- (7.5) Test: J = rᵀR⁻¹r.
- (7.6) Threshold: J > χ²_{m,1−α}.
- (7.7) Theorem 7.1: under H_0, J ~ χ²_m.
- (7.8) Proposition 7.1a: a = Hc ⇒ r invariant.
- (7.9) Autoencoder score: e_rec = ||x − x̂||².

**Status:** Design/Method.
**Acceptance:** full proofs present; false-alarm guarantee stated.

#### 7.4 Classification Algorithms for Fault Type Identification

**Paragraph plan:**
- P1: fault classes.
- P2: features per class.
- P3: classifier choice.
- P4: design-target accuracy table.
- P5: status label.

**Tables to add:**
- Table 7.2: classes and features.
  - Columns: class | signature | feature.
- Table 7.3: design-target accuracy.
  - Columns: class | target accuracy | status.
  - Row: three-phase | 97.2% | design.
  - Row: SLG | 96.1% | design.
  - Row: LL | 95.0% | design.
  - Row: DLG | 94.6% | design.
  - Row: high-impedance | 88.5% | design.

**Status:** Design targets.
**Acceptance:** every accuracy labelled design target, not measured.

#### 7.5 Response Time Optimisation

**Paragraph plan:**
- P1: sliding window.
- P2: Proposition 7.2 proof.
- P3: incremental features.
- P4: compression as latency instrument.
- P5: deployment mapping.
- P6: baseline definition for 37% and 61.4%.

**Equations to add:**
- (7.10) Window: W samples, stride s.
- (7.11) Latency bound: τ ≤ (s + 1)·t_s ≤ (W + 1)·t_s.
- (7.12) Proposition 7.2: with s ≤ W, worst-case detection ≤ W + 1 samples.

**Status:** Design targets.
**Acceptance:** the 37% and 61.4% figures have a defined baseline; otherwise remove.

#### 7.6 Proposed HIL Validation of Fault Detection

**Rewrite mandatory.**
**Current defect:** text claims execution ("was exercised on OPAL-RT", "Section 7.6 reports detection-side outcome", "elaborated in Chapter 11").
**Required conversion:**
- Remove all past-tense execution claims.
- State the protocol in future/protocol tense.
- List scenario families: normal, physical faults, renewable stress, cyber FDI, EV disturbance.
- List metrics: latency, accuracy, false positives.
- Describe offline-versus-HIL comparison methodology.
- Label status Future work/Protocol.

**Paragraph plan:**
- P1: objective of the proposed campaign.
- P2: scenario families.
- P3: metrics.
- P4: comparison method.
- P5: acceptance criteria.
- P6: explicit non-execution statement.

**Tables to add:**
- Table 7.4: HIL protocol.
  - Columns: scenario | injection | expected detection | metric.
  - Sample row: SLG | phase-A fault | within W+1 | latency.

**Status:** Future work/Protocol.
**Acceptance:** zero past-tense execution claims in the section; grep for "OPAL-RT" returns only future/protocol context.

#### 7.7 Chapter Summary

**Paragraph plan:**
- P1: design summary.
- P2: no fault data in archive.
- P3: future work.

**Status:** Synthesis.
**Acceptance:** explicit "no fault data in PSSE33 archive" sentence.

---

### Chapter 8 — EV Integration and DER Management (Target 20 pp, +8 pp, +4,000 words)

#### 8.1 EV Fleet Modelling Approaches

**Paragraph plan:**
- P1: per-vehicle model.
- P2: aggregation derivation.
- P3: station sizing arithmetic.
- P4: availability model.
- P5: cluster expansion.

**Equations to add:**
- (8.1) Aggregation: P_station = Σ_{i=1}^{N} P_i.
- (8.2) Vehicle count: N = P_station/P_vehicle.
- (8.3) Availability: A(t) = E[plugged in at t].

**Worked example:**
- P_station = 50 MW; P_vehicle = 40 kW.
- N ≈ 1,250 at 40 kW.
- With 40 kWh packs, energy ≈ 50 MWh.
- State the heterogeneity caveat.

**Figures to add:**
- Figure 8.1: availability patterns by cluster.
  - X-axis: hour of day.
  - Y-axis: available power [MW].

**Tables to add:**
- Table 8.1: cluster parameters (expanded).
  - Columns: cluster | N share | power | dwell | availability.

**Status:** Method.
**Acceptance:** sizing arithmetic reconciles; availability figure present.

#### 8.2 Bidirectional Power Flow Management

**Paragraph plan:**
- P1: charger topology.
- P2: round-trip efficiency derivation.
- P3: energy accounting.
- P4: SoC update with bounds.

**Equations to add:**
- (8.4) Charging energy: E_charge = |P|·Δt/η.
- (8.5) Discharge energy: E_dis = η·|P|·Δt.
- (8.6) Net deficit: ΔE = |P|·Δt·(1/η − η).
- (8.7) Round-trip: η_rt = η².
- (8.8) SoC update: E_{t+1} = clamp(E_t ± …, E_min, E_max).

**Worked example:**
- η = 0.92 ⇒ η_rt = 0.8464.
- Multiplier 1/η_rt ≈ 1.18.
- State the 18% energy overhead.

**Figures to add:**
- Figure 8.2: charger topology.
- Figure 8.3: round-trip efficiency versus η.

**Tables to add:**
- Table 8.2: efficiency accounting.
  - Columns: direction | AC energy | battery energy | loss.

**Status:** Method.
**Acceptance:** η_rt derivation correct; overhead multiplier correct.

#### 8.3 Coordinated V2G/G2V Frequency Regulation

**Paragraph plan:**
- P1: droop law.
- P2: secondary control.
- P3: aggregate balance.
- P4: Proposition 8.2 proof.
- P5: aggregator MILP.
- P6: honest framing.

**Equations to add:**
- (8.9) Droop: ΔP = −Δf/R_f.
  - R_f: droop [Hz/MW].
- (8.10) Secondary: dΔP/dt = −K_I·Δf.
- (8.11) Aggregate balance: M·df/dt = ΔP_g + ΔP_EV − ΔP_L.
- (8.12) Proposition 8.2: if K_I > 0, Δf_ss = 0.
- (8.13) MILP objective: min Σ (c_t·p_t + λ_sw·u_t).
- (8.14) SoC window: E_min ≤ E_t ≤ E_max.

**Pseudocode to add:**
- Algorithm 8.1: V2G/G2V mode transition.
  1: read Δf, SoC
  2: if Δf < −f_dB and SoC > E_min then
  3:   discharge
  4: else if Δf > f_dB and SoC < E_max then
  5:   charge
  6: else
  7:   idle
  8: end if

**Status:** Design (not measured).
**Acceptance:** Proposition 8.2 proved; explicit non-measurement caveat repeated.

#### 8.4 Load Forecasting with Uncertainty Quantification

**Paragraph plan:**
- P1: features.
- P2: model choice.
- P3: prediction intervals.
- P4: coverage and sharpness.
- P5: controller coupling.

**Equations to add:**
- (8.15) Prediction interval: [ŷ − q, ŷ + q].
- (8.16) Coverage: P(y ∈ interval) ≥ 1 − α.

**Tables to add:**
- Table 8.3: UQ metrics.
  - Columns: metric | definition | target.

**Status:** Design.
**Acceptance:** coverage definition present.

#### 8.5 DER Coordination Strategies

**Paragraph plan:**
- P1: shared voltages and flows.
- P2: control-fighting risk.
- P3: shared interface resolution.

**Status:** Design.
**Acceptance:** control-fighting example given.

#### 8.6 Proposed HIL Validation of V2G Coordination

**Paragraph plan:**
- P1: protocol.
- P2: scenarios.
- P3: metrics.
- P4: comparison plan.

**Status:** Future work.
**Acceptance:** protocol tense only.

#### 8.7 Chapter Summary

**Paragraph plan:**
- P1: measured versus design.
- P2: link clipping results.
- P3: link future work.

**Tables to add:**
- Table 8.4: EV clipping summary.
  - Columns: channel | requested | applied.
  - Row: EV_3 | −50 MW | −27.6 MW.
  - Row: EV_8 | +50 MW | +43.478 MW.

**Status:** Synthesis.
**Acceptance:** clipping numbers match Chapter 11 exactly.

---

### Chapter 9 — Coordinated Control Using Hybrid AI (Target 18 pp, +8 pp, +4,000 words)

#### 9.1 Hierarchical Multi-Agent Reinforcement Learning

**Paragraph plan:**
- P1: agent decomposition.
- P2: communication.
- P3: learning objective.
- P4: honest status.

**Status:** Design/Future work.
**Acceptance:** explicit "HMARL not measured in archive" statement.

#### 9.2 Coordinated Control of FACTS and EV Fleets

**Paragraph plan:**
- P1: conflict resolution.
- P2: shared interface.
- P3: feasibility filter.
- P4: control-fighting example and resolution.

**Figures to add:**
- Figure 9.1: coordination sequence.

**Tables to add:**
- Table 9.1: coordination rules.
  - Columns: conflict | resolution | tier.

**Status:** Implemented (interface); benefit not measured.
**Acceptance:** interface link to Chapter 3.2 action box.

#### 9.3 Integration of DERs within the Control Framework

**Paragraph plan:**
- P1: setpoint entry.
- P2: constraints.
- P3: exogenous treatment.

**Status:** Method.
**Acceptance:** constraints enumerated.

#### 9.4 Adaptive Control Strategies

**Paragraph plan:**
- P1: gain scheduling.
- P2: retraining triggers.
- P3: fallback.

**Status:** Design.
**Acceptance:** triggers testable.

#### 9.5 Balancing Multiple Control Objectives

**Paragraph plan:**
- P1: Pareto formulation.
- P2: scalarisation.
- P3: why no Pareto front computed.
- P4: constraint-first filter.

**Equations to add:**
- (9.1) Multi-objective: min [f_1, f_2, f_3].
- (9.2) Scalarisation: min Σ w_k·f_k.
- (9.3) Feasibility filter: a ∈ U_feas.

**Status:** Method/Design.
**Acceptance:** explicit statement that no Pareto front is computed.

#### 9.6 Proposed HIL Validation of Coordinated Control

**Paragraph plan:**
- P1: protocol.
- P2: scenarios.
- P3: metrics.

**Status:** Future work.
**Acceptance:** protocol tense only.

#### 9.7 Chapter Summary

**Paragraph plan:**
- P1: map design to Chapter 11.
- P2: limitations.

**Status:** Synthesis.
**Acceptance:** no measured benefit claim.

---

### Chapter 10 — Testing and Validation Methodology (Target 22 pp, +8 pp, +4,500 words)

#### 10.1 Simulator and Benchmark Provenance

**Current state:** provenance summarised.
**Gap:** no consolidated environment table; no version pinning; no licence note in body.

**Paragraph plan:**
- P1: simulator identity and version.
- P2: worker/orchestrator split.
- P3: case revision.
- P4: solver options.
- P5: licence and reproducibility note.

**Tables to add:**
- Table 10.1: environment.
  - Columns: component | version | bitness | note.
  - Row: PSS/E | 33.4.0.0 | 32-bit | licensed.
  - Row: worker Python | 2.7 | 32-bit | psspy.
  - Row: orchestrator Python | 3.11 | 64-bit | venv.
  - Row: benchmark | IEEE 39-bus | — | revision 33 RAW.
- Table 10.2: solver options.
  - Columns: option | value | effect.

**Status:** Method.
**Acceptance:** environment table matches Chapter 4.7 and Chapter 14.

#### 10.2 Physical Representation and Action Feasibility

**Paragraph plan:**
- P1: action feasibility rules.
- P2: neutralised channels.
- P3: reserved index 5.
- P4: RAW snapshot isolation.
- P5: energy-state reset between candidates.

**Tables to add:**
- Table 10.3: feasibility rules.
  - Columns: dimension | rule | failure mode.

**Status:** Method.
**Acceptance:** isolation rules explicit enough to reproduce.

#### 10.3 Profiles and Chronological Sampling

**Paragraph plan:**
- P1: OPSD source.
- P2: train/validation/test windows.
- P3: price-profile alignment.
- P4: leakage check.

**Tables to add:**
- Table 10.4: data windows.
  - Columns: split | period | rows | use.
  - Row: train | 2015–2017 | — | fit.
  - Row: val | 2018 | — | tune.
  - Row: test | 2019 | 168 | evaluate.
- Table 10.5: price alignment.
  - Columns: series | period | alignment method.

**Status:** Method.
**Acceptance:** alignment window stated; leakage check explicit.

#### 10.4 Learning Bridge and Training Protocol

**Paragraph plan:**
- P1: feature construction.
- P2: windowing.
- P3: parameter budget.
- P4: checkpoint contract.
- P5: normalisation scope.

**Tables to add:**
- Table 10.6: feature schema.
  - Columns: channel | source | unit.
- Table 10.7: training protocol.
  - Columns: setting | value.

**Status:** Method/Implemented.
**Acceptance:** normalisation scope stated (train-only) and leakage excluded.

#### 10.5 Candidate Evaluation and Policy Definitions

**Paragraph plan:**
- P1: candidate count.
- P2: exact scoring.
- P3: isolation.
- P4: commit path.
- P5: call inventory resolving 816 versus 840.

**Tables to add:**
- Table 10.8: policy definitions.
  - Columns: policy | rule | source.
- Table 10.9: call inventory.
  - Columns: stage | calls | note.
  - Row: candidate scoring | 816 | per day.
  - Row: plus baseline | 840 | including reference.

**Status:** Method/Implemented.
**Acceptance:** 816 and 840 both explained; no unexplained discrepancy.

#### 10.6 Contingency Screening and Metrics

**Paragraph plan:**
- P1: N-1 definition.
- P2: 46 outages.
- P3: 24 hours.
- P4: per-policy counts.
- P5: non-convergence handling.
- P6: islanding classification.

**Tables to add:**
- Table 10.10: contingency set.
  - Columns: outage | type | count.
- Table 10.11: metrics.
  - Columns: metric | definition | unit.

**Status:** Method.
**Acceptance:** 264 non-convergent rows decomposed (10 transformers × 24 + line 16–19 × 24).

#### 10.7 Statistical Interpretation and Reproducibility

**Paragraph plan:**
- P1: estimand Δ-L.
- P2: bootstrap design.
- P3: multiple comparisons.
- P4: temporal dependence.
- P5: exploratory versus confirmatory.

**Equations to add:**
- (10.1) Estimand: Δ-L = L_policy − L_ref.
- (10.2) Bootstrap interval: [q_{α/2}, q_{1−α/2}].

**Status:** Method.
**Acceptance:** intervals labelled exploratory; temporal dependence acknowledged.

#### 10.8 Evidence Provenance and Controls on Scientific Claims (absorb App C)

**Paragraph plan:**
- P1: claim classes.
- P2: executed observation.
- P3: permitted inference.
- P4: not established.
- P5: summary table.

**Tables to add:**
- Table 10.12: claim-class matrix.
  - Columns: claim class | executed | permitted inference | not established.
  - Row: numerical agreement | cross-solver diff | transfer consistency | controllability.
  - Row: candidate comparison | counterfactual runs | directional difference | general efficacy.

**Status:** Method.
**Acceptance:** execution PASS never presented as efficacy PASS.

#### 10.9 Construction of Counterfactual Controller Comparisons

**Paragraph plan:**
- P1: counterfactual state construction.
- P2: matched inputs.
- P3: common-hour restriction.

**Status:** Method.
**Acceptance:** matching rule explicit.

#### 10.10 Failure Accounting and Contingency Categories

**Paragraph plan:**
- P1: convergence failure.
- P2: voltage violation.
- P3: thermal overload.
- P4: islanding.
- P5: non-converged rows as failures.

**Tables to add:**
- Table 10.13: failure taxonomy.
  - Columns: category | trigger | handling.

**Status:** Method.
**Acceptance:** failed rows never counted as zero loss.

#### 10.11 Domain-Transfer and Model-Representation Controls

**Paragraph plan:**
- P1: 50 Hz to 60 Hz mapping.
- P2: load scaling.
- P3: renewable allocation.
- P4: sensitivity statement.

**Tables to add:**
- Table 10.14: transfer map.
  - Columns: quantity | source | target | transform.

**Status:** Method.
**Acceptance:** transformation explicit and reversible.

#### 10.12 Threats to Validity and Reproduction (absorb App A)

**Paragraph plan:**
- P1: construct validity.
- P2: internal validity.
- P3: external validity.
- P4: statistical validity.
- P5: evidence index E-B to E-G.
- P6: archive hash and reproduction.

**Tables to add:**
- Table 10.15: threats-to-validity.
  - Columns: threat | type | mitigation | residual risk.
- Table 10.16: evidence index.
  - Columns: ID | scope | path | hash.
  - Row: E-B | base case | 01_base | …
  - Row: E-C | device cases | 02_devices | …
  - Row: E-D | candidate policy | 03_stage_e | …
  - Row: E-E | learning | 04_stage_f | …
  - Row: E-F | seeds | 05_stage_g | …
  - Row: E-G | N-1/timing | 06_stage_g | …
- Table 10.17: reproduction commands.
  - Columns: step | command.

**Status:** Method.
**Acceptance:** archive filename without `(1)`; SHA-256 cited.

---

### Chapter 11 — Results and Performance Analysis (Target 26 pp, +10 pp, +5,500 words)

#### 11.1 Base Case

**Paragraph plan:**
- P1: base-case setup.
- P2: cross-solver agreement.
- P3: per-bus voltage differences.
- P4: generator and branch differences.
- P5: loss breakdown.
- P6: security caveat.

**Tables to add:**
- Table 11.1: cross-solver base case.
  - Columns: quantity | MATPOWER | PSS/E | Δ.
- Table 11.2: base-case security.
  - Columns: metric | value | limit.
  - Row: voltage violations | 24/24 h | 0.
  - Row: thermal violations | 17/24 h | 0.
  - Row: max loading | 199.1% | 100%.

**Status:** Measured/Validated.
**Acceptance:** agreement presented as transfer consistency, not operational security.

#### 11.2 Time-Series Baseline (absorb App E)

**Paragraph plan:**
- P1: held-out week setup.
- P2: daily summary.
- P3: 132/168 convergence.
- P4: 36 non-convergent hours.
- P5: trajectory figures.
- P6: failure-event interpretation.

**Tables to add:**
- Table 11.3: daily summary.
  - Columns: date | load× | wind | solar | AC ok | Vmin | Vmax | violations | overloads | loss.
- Table 11.4: non-convergent hours.
  - Columns: hour | cause | classification.

**Figures to add:**
- Figure 11.1: daily loss profile.
  - X-axis: hour.
  - Y-axis: loss [MW].
- Figure 11.2: Vmin/Vmax envelope.
  - Y-axis: voltage [p.u.].
- Figure 11.3: violation and overload counts by hour.

**Status:** Measured.
**Acceptance:** failed hours shown as failure events, not zeros.

#### 11.3 Isolated Actuator Response (absorb App D)

**Paragraph plan:**
- P1: 41-case design.
- P2: table reading guide.
- P3: per-device interpretation.
- P4: STATCOM neutralisation.
- P5: UPFC proxy semantics.
- P6: PASS meaning.

**Tables to add:**
- Table 11.5: 41-case cross-solver (landscape).
  - Columns: case | device | setpoint | gate | ΔV | Δθ | ΔP | Δloss | agreement.
  - Include all 41 rows with fixed tags.
  - Note: bus-39 STATCOM neutralised.
  - Note: UPFC series is X-compensation proxy.

**Status:** Measured/Validated.
**Acceptance:** table fits landscape; no split tags; PASS defined as numerical agreement.

#### 11.4 Candidate-Policy Comparison

**Paragraph plan:**
- P1: policies compared.
- P2: mean losses.
- P3: deltas.
- P4: violation counts.
- P5: per-hour breakdown.
- P6: neutral-action discussion.

**Tables to add:**
- Table 11.6: policy comparison.
  - Columns: policy | mean loss | ΔL | violations | status.

**Figures to add:**
- Figure 11.4: per-hour loss by policy.

**Status:** Measured.
**Acceptance:** trade-off framed honestly.

#### 11.5 Learning Quality

**Paragraph plan:**
- P1: split table.
- P2: per-channel MAE.
- P3: constant-mean baseline.
- P4: rule-based droop baseline.
- P5: imitation versus closed loop.
- P6: the +0.0845 MW loss increase.

**Tables to add:**
- Table 11.7: learning metrics.
  - Columns: channel | MAE | baseline MAE.
  - Row: aggregate | 0.00311 | 0.00780.

**Status:** Measured.
**Acceptance:** rule-based droop recommended; performance limitation stated.

#### 11.6 Seeds

**Paragraph plan:**
- P1: seed design.
- P2: per-seed means.
- P3: pooled directional counts.
- P4: non-independence.
- P5: weather-versus-seed limitation.

**Tables to add:**
- Table 11.8: per-seed results.
  - Columns: seed | mean loss | ΔL | interval.
  - Row: pooled | — | — | 22 improved / 50 worsened.

**Status:** Measured.
**Acceptance:** intervals labelled exploratory.

#### 11.7 N-1 Screening

**Paragraph plan:**
- P1: screening setup.
- P2: converged counts.
- P3: divergence-set identity.
- P4: decomposition of 264.
- P5: 19–20 inclusion.
- P6: islanding analysis.
- P7: worst loading.
- P8: base-case insecurity.

**Tables to add:**
- Table 11.9: N-1 outcomes.
  - Columns: policy | converged | non-converged | total.
  - Row: — | 840 | 264 | 1,104.
- Table 11.10: divergence decomposition.
  - Columns: outage group | count.
  - Row: 10 transformers × 24 h | 240.
  - Row: line 16–19 × 24 h | 24.

**Status:** Measured.
**Acceptance:** 840/1,104 explained; worst loading 318.7%/318.5% stated.

#### 11.8 Timing

**Paragraph plan:**
- P1: per-call timing.
- P2: Stage E cost.
- P3: 32-candidate decision cost.
- P4: design-versus-measured.
- P5: no sub-50 ms deadline established.

**Tables to add:**
- Table 11.11: timing.
  - Columns: call | mean | median | p95.
  - Row: Stage E | 180.6 ms | — | —.
  - Row: 32-candidate decision | ≈5.8 s | — | —.

**Figures to add:**
- Figure 11.5: timing distribution.

**Status:** Measured.
**Acceptance:** explicit "no end-to-end sub-50 ms result" statement.

#### 11.9 Findings Supported

**Paragraph plan:**
- P1: list supported findings.
- P2: list unsupported findings.

**Tables to add:**
- Table 11.12: findings ledger.
  - Columns: finding | supported | evidence.

**Status:** Synthesis.
**Acceptance:** every finding has an evidence ID.

#### 11.10 Negative Efficacy Results

**Paragraph plan:**
- P1: greedy versus no control.
- P2: significance not persuasive.
- P3: expert worse than no control.
- P4: hybrid path limitation.
- P5: recommendations.

**Status:** Measured.
**Acceptance:** negative results not softened.

#### 11.11 Multiple-Comparison Discipline

**Paragraph plan:**
- P1: bootstrap detail.
- P2: intervals crossing zero.
- P3: autocorrelation.
- P4: exploratory versus family-wise.
- P5: pre-registration recommendation.

**Status:** Method/Measured.
**Acceptance:** no family-wise claim.

#### 11.12 Traceability and Reproduction

**Paragraph plan:**
- P1: configuration summary.
- P2: source filenames.
- P3: archive retention.
- P4: second-environment replication.
- P5: hash.
- P6: 816/840 resolution.

**Tables to add:**
- Table 11.13: traceability.
  - Columns: artefact | file | hash.

**Status:** Method.
**Acceptance:** archive hash present; filename consistent.

---

### Chapter 12 — Discussion and Engineering Implications (Target 14 pp, +6 pp, +3,000 words)

#### 12.1 Architecture and Empirical Contribution

**Paragraph plan:**
- P1: reconcile with Chapter 1 truth table.
- P2: design versus measured.
- P3: what the architecture contributes even without efficacy.

**Status:** Synthesis.
**Acceptance:** no contribution overstated.

#### 12.2 Numerical Validation Versus Control Benefit

**Paragraph plan:**
- P1: the bus-39 example.
- P2: perfect reproduction of an ineffective action.
- P3: implication.

**Status:** Discussion.
**Acceptance:** example present with numbers.

#### 12.3 Imitation Learning and Objective Alignment

**Paragraph plan:**
- P1: constant channels.
- P2: better imitation of a worse expert.
- P3: richer expert requirement.

**Status:** Discussion.
**Acceptance:** mechanism explained.

#### 12.4 Scenario Feasibility

**Paragraph plan:**
- P1: synthetic renewable allocation.
- P2: failed high-wind day.
- P3: 36 failed steps.
- P4: pre-outage overloads.
- P5: recommendations.

**Status:** Discussion.
**Acceptance:** failure count matches Chapter 11.

#### 12.5 Statistical and Computational Limits

**Paragraph plan:**
- P1: one day.
- P2: three seeds.
- P3: bootstrap limitations.
- P4: exploratory p-values.
- P5: compute budget.

**Status:** Discussion.
**Acceptance:** limits enumerated.

#### 12.6 Implications for Transmission Planning

**Paragraph plan:**
- P1: traceable operating points.
- P2: device labels insufficient.

**Status:** Discussion.
**Acceptance:** planning implication stated.

#### 12.7 Corrective Versus Preventive Planning

**Paragraph plan:**
- P1: pre-contingency feasibility first.
- P2: base envelope already violates limits.
- P3: planning additions.

**Status:** Discussion.
**Acceptance:** prioritisation stated.

#### 12.8 Lessons for Metacognitive Design

**Paragraph plan:**
- P1: arbitration against external targets.
- P2: arbiter components.
- P3: follow-on test design.
- P4: ablations list.

**Tables to add:**
- Table 12.1: ablation plan.
  - Columns: ablation | hypothesis | metric.

**Status:** Discussion.
**Acceptance:** ablation list actionable.

#### 12.9 Falsifiability and Consolidated Threats

**Paragraph plan:**
- P1: what would falsify the efficacy claim.
- P2: construct threat.
- P3: internal threat.
- P4: external threat.
- P5: statistical threat.

**Status:** Discussion.
**Acceptance:** falsifiability statement explicit.

---

### Chapter 13 — Conclusions and Future Work (Target 8 pp, +4 pp, +2,000 words)

#### 13.1 Conclusions Supported

**Paragraph plan:**
- P1: implementation feasibility.
- P2: traceability.
- P3: operational conclusion limited.

**Status:** Synthesis.
**Acceptance:** conclusions match evidence.

#### 13.2 Contributions and Evidence Boundaries (absorb App B)

**Paragraph plan:**
- P1: contribution table.
- P2: excluded claims.
- P3: evidence boundary statement.

**Tables to add:**
- Table 13.1: contributions with boundaries.
  - Columns: # | contribution | type | evidence | status | excluded claim.
  - Row: 2 | QIRL | method | E-E | Method | quantum advantage.
  - Row: 5 | fault detection | design | — | Design | measured accuracy.
  - Row: 8 | HIL methodology | design | — | Future | hardware execution.

**Status:** Synthesis.
**Acceptance:** excluded claims list complete.

#### 13.3 Priorities for the Next Campaign

**Paragraph plan:**
- P1: physical validity.
- P2: control authority.
- P3: learning quality.
- P4: comparison design.

**Tables to add:**
- Table 13.2: next-campaign plan.
  - Columns: priority | action | success criterion.
  - Row: physical validity | feasible base case | zero base violations.
  - Row: control authority | replace neutralised shunt | measurable ΔV.
  - Row: learning quality | richer expert | closed-loop loss reduction.
  - Row: comparison design | multiple seasons, more seeds | stable intervals.

**Status:** Future work.
**Acceptance:** each priority has a success criterion.

#### 13.4 Concluding Statement

**Paragraph plan:**
- P1: what the campaign achieved.
- P2: what remains contingent.

**Status:** Synthesis.
**Acceptance:** no unsupported efficacy claim.

---

### Chapter 14 — Absorbed Evidence and Reproduction (New Body Chapter, Target 22 pp, +11,000 words)

#### 14.1 Evidence Index and Reproduction (from App A)

**Paragraph plan:**
- P1: evidence hierarchy.
- P2: E-B base case.
- P3: E-C device cases.
- P4: E-D candidate policy.
- P5: E-E learning.
- P6: E-F seeds.
- P7: E-G N-1/timing.
- P8: environment and licence.
- P9: reproduction commands.

**Tables to add:**
- Table 14.1: evidence index.
- Table 14.2: environment.
- Table 14.3: reproduction commands.
- Table 14.4: artefact hashes.

**Status:** Method.
**Acceptance:** archive filename without `(1)`; hash cited; commands runnable.

#### 14.2 Claim Reconciliation (from App B)

**Paragraph plan:**
- P1: original claims.
- P2: dispositions.
- P3: residual risk.

**Tables to add:**
- Table 14.5: claim reconciliation.
  - Columns: original claim | disposition | evidence | status.

**Status:** Method.
**Acceptance:** every original claim has a disposition.

#### 14.3 Empirical Audit and Definitions (from App C)

**Paragraph plan:**
- P1: claim classes.
- P2: estimands.
- P3: conventions.
- P4: result summary.

**Tables to add:**
- Table 14.6: audit matrix.
  - Columns: class | executed | permitted | not established.
- Table 14.7: conventions.
  - Columns: convention | definition.

**Status:** Method.
**Acceptance:** no inference beyond permitted column.

#### 14.4 Device-by-Device Cross-Solver Evidence (from App D)

**Paragraph plan:**
- P1: design.
- P2: reading guide.
- P3: exceptions.
- P4: PASS meaning.

**Tables to add:**
- Table 14.8: 41-case table (landscape).

**Status:** Measured/Validated.
**Acceptance:** all 41 rows present; tags fixed.

#### 14.5 Held-Out Baseline Trajectory (from App E)

**Paragraph plan:**
- P1: week setup.
- P2: daily summary.
- P3: key hours.
- P4: failures.

**Tables to add:**
- Table 14.9: daily summary.
- Table 14.10: key-hour extract.

**Figures to add:**
- Figure 14.1: loss trajectory.
- Figure 14.2: voltage envelope.
- Figure 14.3: violation counts.

**Status:** Measured.
**Acceptance:** condensed, not full 168 rows; failures shown.

---

## 6. Page And Word Budget Reconciliation

| Component | Words | Pages |
|---|---:|---:|
| Existing main text | ~106,000 | ~150 |
| Ch 1 expansion | +4,000 | +6 |
| Ch 2 expansion | +7,000 | +14 |
| Ch 3 expansion | +7,000 | +14 |
| Ch 4 expansion | +6,000 | +12 |
| Ch 5 expansion | +4,000 | +8 |
| Ch 6 expansion | +4,000 | +8 |
| Ch 7 expansion | +4,000 | +8 |
| Ch 8 expansion | +4,000 | +8 |
| Ch 9 expansion | +4,000 | +8 |
| Ch 10 expansion | +4,500 | +8 |
| Ch 11 expansion | +5,500 | +10 |
| Ch 12 expansion | +3,000 | +6 |
| Ch 13 expansion | +2,000 | +4 |
| Ch 14 (absorbed) | +11,000 | +22 |
| Front matter | +3,000 | +6 |
| **Total** | **~175,000** | **~286** |

- Target 250 pp is exceeded by ~36 pp of margin.
- If trimming is needed, reduce Chapter 14 first; keep Chapters 10 and 12 intact.

---

## 7. Pre-Expansion Checklist

- [ ] Read all of Chapters 1–13 in full.
- [ ] Rank subsections by brevity to set writing order.
- [ ] Decide whether Chapter 14 is a standalone chapter or folded into 10–11.
- [ ] Draft the nomenclature table before writing equations.
- [ ] Commission figures before writing their explanatory prose.
- [ ] Fix the abstract exponent defect.
- [ ] Fix cross-reference errors (§3.10 vs 3.9; §11.1 vs 11.2).
- [ ] Decide the test-count wording (52/49/3).
- [ ] Resolve 816 versus 840 with a call inventory.
- [ ] Confirm archive filename and hash.
- [ ] Choose spelling convention and enforce it.

---

## 8. Post-Expansion Integration Checklist

- [ ] Chapter 1 contribution table matches Chapter 13 boundaries.
- [ ] Chapter 10 threats-to-validity consolidates Chapters 11–12 material without duplication.
- [ ] Chapter 11 contains absorbed Appendix D and E content.
- [ ] No appendix remains; all appendix labels removed.
- [ ] All "HIL executed" claims converted to future/protocol tense.
- [ ] Test count identical everywhere.
- [ ] 816/840 explained.
- [ ] List of figures, tables and algorithms regenerated.
- [ ] All equation symbols defined.
- [ ] All tables have units in headers.
- [ ] All figures have units on axes and source lines.
- [ ] Spelling convention applied.
- [ ] Status tag on every device, controller and experiment.
- [ ] Cross-references verified after renumbering.
- [ ] PDF superscripts and minus signs checked.

---

## 9. Prohibited Padding Techniques

- Do not increase font size.
- Do not widen margins.
- Do not increase line spacing.
- Do not add blank pages.
- Do not duplicate figures with new numbers.
- Do not repeat conclusions across chapters.
- Do not add citations without critique.
- Do not split tables to inflate pages.
- Do not present design targets as measured.
- Do not soften negative results.
- Do not claim hardware execution.
- Do not claim measured frequency regulation.
- Do not claim measured transient stability.
- Do not claim measured fault accuracy.
- Do not claim a Pareto front that was not computed.
- Do not claim sub-50 ms end-to-end timing.

---

## 10. Claim-Integrity Ledger (Must Remain True)

| Claim area | Allowed statement | Prohibited statement |
|---|---|---|
| HIL execution | HIL-ready design and protocol | "validated on OPAL-RT" |
| Fault detection | design targets | "97.2% measured accuracy" |
| V2G regulation | control design | "regulation demonstrated" |
| Transient stability | ML screening design | "stability verified" |
| QIRL | amplitude-based selection | "quantum advantage" |
| Arbiter | sigmoid design; measured selection differs | "sigmoid arbiter validated" |
| HMARL | design direction | "HMARL implemented" |
| PINN | literature context | "PINN implemented" |
| Base case | numerical agreement | "operationally secure" |
| N-1 | screening with failures | "N-1 secure" |
| Timing | measured offline call times | "real-time deadline met" |
| Efficacy | directional, exploratory | "demonstrated benefit" |

---

## 11. Figure Inventory To Commission

- Figure 1.1: renewable capacity growth.
- Figure 1.2: challenge-to-capability map.
- Figure 1.3: STATCOM V–I curve.
- Figure 1.4: TCSC X–k curve.
- Figure 1.5: EV charger topologies.
- Figure 1.6: chapter dependency graph.
- Figure 2.1: AI-era timeline.
- Figure 2.2: FACTS classification tree.
- Figure 2.3: device capability panels.
- Figure 2.4: charger topology comparison.
- Figure 2.5: revenue-versus-degradation trade-off.
- Figure 2.6: validation pipeline.
- Figure 3.1: end-to-end architecture.
- Figure 3.2: layered view.
- Figure 3.3: tier interaction.
- Figure 3.4: probability-mass evolution.
- Figure 3.5: multi-rate loop.
- Figure 3.6: timing budget.
- Figure 4.1: sequence diagram.
- Figure 4.2: V-model.
- Figure 4.3: worker architecture.
- Figure 5.1: GA convergence.
- Figure 5.2: PSO convergence.
- Figure 6.1: CNN-LSTM architecture.
- Figure 6.2: PV curve.
- Figure 6.3: stability-to-reflex flow.
- Figure 7.1: fusion architecture.
- Figure 8.1: availability patterns.
- Figure 8.2: charger topology.
- Figure 8.3: round-trip efficiency.
- Figure 9.1: coordination sequence.
- Figure 11.1: daily loss profile.
- Figure 11.2: voltage envelope.
- Figure 11.3: violation counts.
- Figure 11.4: per-hour loss by policy.
- Figure 11.5: timing distribution.
- Figure 14.1: loss trajectory.
- Figure 14.2: voltage envelope (absorbed).
- Figure 14.3: violation counts (absorbed).

---

## 12. Table Inventory To Commission

- Table 1.1: challenges with quantitative impact.
- Table 1.2: FACTS devices with fidelity column.
- Table 1.3: EV fleet clusters.
- Table 1.4: service–timescale matrix.
- Table 1.5: motivation-to-objective map.
- Table 1.6: gap-to-research-question map.
- Table 1.7: requirements traceability.
- Table 1.8: objective-to-chapter map.
- Table 1.9: contribution truth table.
- Table 2.1: AI eras.
- Table 2.2: DRL algorithms.
- Table 2.3: device modelling fidelity.
- Table 2.4: method comparison.
- Table 2.5: V2G services.
- Table 2.6: cognitive architectures.
- Table 2.7: standards matrix.
- Table 2.8: gap-response matrix.
- Table 2.9: validation levels.
- Table 2.10: timing budget.
- Table 3.1: nomenclature.
- Table 3.2: design axioms.
- Table 3.3: action box.
- Table 3.4: layer timescales.
- Table 3.5: service matrix.
- Table 3.6: Jacobian blocks.
- Table 3.7: device-to-model map.
- Table 3.8: fault classes.
- Table 3.9: objective-to-asset map.
- Table 3.10: compute placement.
- Table 3.11: communication infrastructure.
- Table 3.12: core assignment.
- Table 3.13: Chapter 3 status.
- Table 4.1: requirements traceability.
- Table 4.2: action space.
- Table 4.3: parameter budget.
- Table 4.4: arbiter modes.
- Table 4.5: module map.
- Table 4.6: data volumes.
- Table 4.7: adaptation triggers.
- Table 4.8: test layers.
- Table 4.9: test count.
- Table 4.10: environment.
- Table 4.11: API calls.
- Table 5.1: formulation summary.
- Table 5.2: DRL specification.
- Table 5.3: domain differences.
- Table 5.4: validation plan.
- Table 6.1: approach comparison.
- Table 6.2: stability metrics.
- Table 6.3: model variants.
- Table 7.1: detection approaches.
- Table 7.2: fault classes and features.
- Table 7.3: design-target accuracy.
- Table 7.4: HIL protocol.
- Table 8.1: cluster parameters.
- Table 8.2: efficiency accounting.
- Table 8.3: UQ metrics.
- Table 8.4: EV clipping summary.
- Table 9.1: coordination rules.
- Table 10.1: environment.
- Table 10.2: solver options.
- Table 10.3: feasibility rules.
- Table 10.4: data windows.
- Table 10.5: price alignment.
- Table 10.6: feature schema.
- Table 10.7: training protocol.
- Table 10.8: policy definitions.
- Table 10.9: call inventory.
- Table 10.10: contingency set.
- Table 10.11: metrics.
- Table 10.12: claim-class matrix.
- Table 10.13: failure taxonomy.
- Table 10.14: transfer map.
- Table 10.15: threats-to-validity.
- Table 10.16: evidence index.
- Table 10.17: reproduction commands.
- Table 11.1: cross-solver base case.
- Table 11.2: base-case security.
- Table 11.3: daily summary.
- Table 11.4: non-convergent hours.
- Table 11.5: 41-case table.
- Table 11.6: policy comparison.
- Table 11.7: learning metrics.
- Table 11.8: per-seed results.
- Table 11.9: N-1 outcomes.
- Table 11.10: divergence decomposition.
- Table 11.11: timing.
- Table 11.12: findings ledger.
- Table 11.13: traceability.
- Table 12.1: ablation plan.
- Table 13.1: contributions with boundaries.
- Table 13.2: next-campaign plan.
- Table 14.1: evidence index.
- Table 14.2: environment.
- Table 14.3: reproduction commands.
- Table 14.4: artefact hashes.
- Table 14.5: claim reconciliation.
- Table 14.6: audit matrix.
- Table 14.7: conventions.
- Table 14.8: 41-case table (absorbed).
- Table 14.9: daily summary (absorbed).
- Table 14.10: key-hour extract.

---

## 13. Equation Inventory To Number

- (1.1) swing equation.
- (1.2) RoCoF approximation.
- (1.3) FDI measurement model.
- (1.4) SVC reactive power.
- (1.5) STATCOM current limit.
- (1.6) TCSC effective reactance.
- (1.7) UPFC DC-link balance.
- (1.8) charging energy update.
- (1.9) discharging energy update.
- (2.1) SVC susceptance injection.
- (2.2) TCSC branch reactance update.
- (2.3) UPFC equivalent current injection.
- (2.4) RL objective.
- (2.5) Lagrangian.
- (2.6) Lyapunov condition.
- (2.7) MPC objective.
- (2.8) PINN loss.
- (2.9) aggregation.
- (2.10) degradation throughput.
- (2.11) throughput cost.
- (2.12) Boltzmann choice.
- (2.13) Born-rule probability.
- (3.1) System 1 map.
- (3.2) System 2 map.
- (3.3) blending law.
- (3.4) feasibility proposition.
- (3.5) active injection.
- (3.6) reactive injection.
- (3.7) mismatch vector.
- (3.8) Newton update.
- (3.9) convergence test.
- (3.10) shunt insertion.
- (3.11) series update.
- (3.12) UPFC injection.
- (3.13) Q-limit switch.
- (3.14) clamped energy update.
- (3.15) SoC invariance.
- (3.16) net load.
- (3.17) load scaling.
- (3.18) initial amplitudes.
- (3.19) QIRL reward.
- (3.20) amplitude update.
- (3.21) Born rule.
- (3.22) ratio bound theorem.
- (3.23) measurement model.
- (3.24) WLS estimate.
- (3.25) residual.
- (3.26) chi-square statistic.
- (3.27) threshold.
- (3.28) stealth attack.
- (3.29) autoencoder score.
- (3.30) reward composition.
- (3.31) period chain.
- (3.32) end-to-end latency.
- (4.1) convolution.
- (4.2) LSTM update.
- (4.3) parameter total.
- (4.4) sigmoid weight.
- (4.5) arbiter feasibility.
- (5.1) decision vector.
- (5.2) placement objective.
- (5.3) voltage constraint.
- (5.4) thermal constraint.
- (5.5) Q constraint.
- (5.6) budget.
- (5.7) shunt sensitivity.
- (5.8) series sensitivity.
- (5.9) GA fitness.
- (5.10) mutation schedule.
- (5.11) PSO velocity.
- (5.12) PSO position.
- (6.1) input tensor.
- (6.2) stability output.
- (6.3) stability margin.
- (6.4) continuation equation.
- (6.5) load margin.
- (7.1) feature map.
- (7.2) fused feature.
- (7.3) attention softmax.
- (7.4) residual.
- (7.5) chi-square test.
- (7.6) threshold.
- (7.7) Theorem 7.1.
- (7.8) stealth proposition.
- (7.9) autoencoder score.
- (7.10) sliding window.
- (7.11) latency bound.
- (7.12) Proposition 7.2.
- (8.1) aggregation.
- (8.2) vehicle count.
- (8.3) availability.
- (8.4) charging energy.
- (8.5) discharge energy.
- (8.6) net deficit.
- (8.7) round-trip efficiency.
- (8.8) SoC update.
- (8.9) droop law.
- (8.10) secondary control.
- (8.11) aggregate balance.
- (8.12) Proposition 8.2.
- (8.13) MILP objective.
- (8.14) SoC window.
- (8.15) prediction interval.
- (8.16) coverage.
- (9.1) multi-objective.
- (9.2) scalarisation.
- (9.3) feasibility filter.
- (10.1) estimand.
- (10.2) bootstrap interval.

---

## 14. Algorithm Inventory To Typeset

- Algorithm 3.1: QIRL candidate selection.
- Algorithm 4.1: QIRL step.
- Algorithm 5.1: GA placement.
- Algorithm 5.2: PSO tuning.
- Algorithm 8.1: V2G/G2V mode transition.
- Algorithm 10.1: contingency screening call sequence.

For each algorithm:
- list inputs;
- list outputs;
- state complexity;
- cross-reference the equation it implements;
- cross-reference the code module.

---

## 15. Literature-Addition Worksheet

- For each subsection, add 2–3 citations.
- For each citation record: author, year, venue, contribution, limitation, relevance to CAPSM.
- Prefer post-2020 sources where the field moved.
- Replace WEO 2023 with the latest edition.
- Flag any claim currently resting on a single source.
- Add a critical sentence to the text, not just a citation.
- Keep the reference list consistent with the chosen citation style.
- Avoid citation padding without critique.

Suggested additions by chapter:
- Ch 2: DRL surveys, safe-RL surveys, PINN reviews, HIL surveys.
- Ch 3: QIRL/quantum-cognition, WLS/FDI, AC power flow.
- Ch 4: CNN-LSTM, parameter-efficient networks, real-time inference.
- Ch 5: GA/PSO placement, sensitivity methods.
- Ch 6: transient stability ML, continuation power flow.
- Ch 7: anomaly detection, fault classification, PTP.
- Ch 8: V2G aggregation, battery degradation, MILP dispatch.
- Ch 9: HMARL, multi-agent control, Pareto methods.
- Ch 10: reproducibility, statistical inference, threats-to-validity.
- Ch 11: cross-solver validation, benchmark studies.

---

## 16. Per-Chapter Acceptance Scorecard

For every chapter, confirm:
- [ ] Page target met or exceeded.
- [ ] Word target met.
- [ ] Every subsection has a paragraph plan executed.
- [ ] Every listed equation present and numbered.
- [ ] Every listed figure present with caption, units and source.
- [ ] Every listed table present with units and headers.
- [ ] Every listed algorithm present with inputs/outputs.
- [ ] Every claim carries a status tag.
- [ ] No appendix reference remains.
- [ ] Cross-references correct.
- [ ] Spelling consistent.
- [ ] No prohibited padding.
- [ ] Negative results preserved.

Chapter-specific checks:
- Ch 1: contribution truth table present; O5 honest.
- Ch 2: DRL table and standards table present.
- Ch 3: action box matches code; propositions proved.
- Ch 4: parameter arithmetic sums to 137,418.
- Ch 5: optimisation statement complete.
- Ch 6: no measured stability claim.
- Ch 7: no past-tense HIL claim; baseline for 37%/61.4% defined.
- Ch 8: η_rt arithmetic correct.
- Ch 9: no Pareto-front claim.
- Ch 10: claim-class matrix present; threats consolidated.
- Ch 11: 840/1,104 explained; timing honest.
- Ch 12: falsifiability statement present.
- Ch 13: excluded-claims list complete.
- Ch 14: archive hash and filename correct.

---

## 17. Drafting Order And Time Plan

**Phase 1 — Foundations (before prose).**
- Fix the abstract exponent.
- Fix cross-reference errors.
- Build the nomenclature table.
- Build the figure and table inventories.
- Confirm the archive hash and filename.
- Decide Chapter 14 placement.

**Phase 2 — Mathematical chapters.**
- Write Chapter 3 equations and proofs.
- Write Chapter 4 parameter derivation and pseudocode.
- Write Chapter 5 optimisation formulation.
- Write Chapter 8 efficiency derivation.

**Phase 3 — Evidence chapters.**
- Absorb Appendix D into Chapter 11.3.
- Absorb Appendix E into Chapter 11.2.
- Absorb Appendix A into Chapter 10.12 and Chapter 14.1.
- Absorb Appendix C into Chapter 10.8.
- Absorb Appendix B into Chapters 1.7 and 13.2.

**Phase 4 — Literature and context.**
- Expand Chapter 2 with citation worksheet.
- Expand Chapter 1 background with quantified data.
- Expand Chapters 5–9 design detail.

**Phase 5 — Discussion and conclusions.**
- Expand Chapter 12.
- Expand Chapter 13.
- Add falsifiability statement.

**Phase 6 — Integration.**
- Renumber everything.
- Regenerate lists of figures, tables, algorithms.
- Verify every cross-reference.
- Run the acceptance scorecard.
- Check page count against the 250-page target.

**Phase 7 — Final checks.**
- PDF rendering of exponents and minus signs.
- Colour-blind-safe figure check.
- Table header repetition on page breaks.
- Archive reproduction test in a clean environment.
- Final honesty pass over every status tag.

---

*End of expansion blueprint.*
