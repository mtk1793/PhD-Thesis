#!/usr/bin/env python3
"""Non-destructive CAPSM thesis revision: preserve 2026-09-30 Word manuscript.

Source: CAPSM_Thesis_Final_Rebuild_2026-09-30.docx
Output: CAPSM_Thesis_AcademicPaper_Updated_2026-11-04.docx

Only claims supported by the source evidence ledgers can be called measured.
The PSS/E simulation module is an engineering implementation pending local
licensed PSS/E verification, so this document records its methods but DOES NOT
invent PSS/E results or claim completed PyTorch/PSS/E full integration.

Execute at repo root:
    python -m pip install python-docx
    python scripts/update_thesis_psse_nov2026.py
"""
from pathlib import Path
from datetime import datetime, timezone
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "CAPSM_Thesis_Final_Rebuild_2026-09-30.docx"
FALLBACK = ROOT / "CAPSM_Thesis_AcademicPaper_2026-09-09.docx"
OUTPUT = ROOT / "CAPSM_Thesis_AcademicPaper_Updated_2026-11-04.docx"

NEW_TITLE = ("Cognitive Adaptive Power System Management (CAPSM): "
             "A Dual-Process AI Framework for Coordinated FACTS and EV Control "
             "with Reproducible Power-System Simulation")

ABSTRACT = (
    "The growing penetration of renewable generation and flexible electric "
    "vehicle (EV) fleets creates a coordination problem for transmission "
    "networks: multiple controllable resources must respond to changing "
    "operating conditions while respecting voltage, thermal, generator, "
    "device and energy constraints. This thesis develops Cognitive Adaptive "
    "Power System Management (CAPSM), a dual-process architecture combining "
    "a fast CNN–LSTM System 1 policy, a deliberative System 2 based on "
    "candidate-specific quantum-inspired action selection, and a "
    "stress-dependent Metacognitive Arbiter. The common nine-position "
    "interface coordinates simplified FACTS equivalents and three "
    "aggregated EV stations; one UPFC series-Q position is reserved and "
    "remains inactive in the current physical model. The research "
    "distinguishes measured findings from the earlier PYPOWER quasi-static "
    "time-series campaign, supplementary replication experiments, "
    "hardware-in-the-loop records, and proposed design targets. Following "
    "the September 2026 scientific rebuild, historical Stage-1 performance "
    "figures are identified as superseded where the revised leakage-free "
    "training and counterfactual evaluation require new measurements. "
    "A new PSS®E v35 simulation-first implementation provides a route for "
    "independent benchmark validation, AC power-flow-based control "
    "evaluation, contingencies, physically constrained EV dispatch and "
    "machine-readable datasets for PyTorch learning. The PSS®E software "
    "layer has passed offline regression checks but has not yet been "
    "validated by executing the licensed PSS®E solver; therefore no "
    "numerical PSS®E superiority, convergence or real-time performance "
    "claim is made. The central thesis contribution is the explicit "
    "architectural and experimental formulation of dual-process "
    "coordination with evidence-bounded engineering validation. "
    "The remaining experiments required for final quantitative conclusions "
    "are identified and independently traceable."
)

def set_text_keep_style(p, text):
    if not p.runs:
        p.add_run(text)
        return
    p.runs[0].text = text
    for r in p.runs[1:]:
        r.text = ""

def locate(doc, target):
    for p in doc.paragraphs:
        if target.lower() in p.text.strip().lower():
            return p
    return None

def before(marker, text, style=None):
    p = marker.insert_paragraph_before(text, style=style)
    if style is None:
        p.style = "Normal"
    p.paragraph_format.space_after = Pt(6)
    if text:
        for r in p.runs:
            r.font.name = "Times New Roman"
            if style is None:
                r.font.size = Pt(12)
    return p

def heading(marker, title, level=2):
    return before(marker, title, "Heading %d" % level)

def table_before(doc, marker, headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = "Table Grid"
    for j,v in enumerate(headers):
        t.cell(0,j).text = v
    for i,row in enumerate(rows,1):
        for j,v in enumerate(row):
            t.cell(i,j).text = v
    for cell in t.rows[0].cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(9)
    for row in t.rows[1:]:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
    # Relocate the created table to just before the destination heading.
    marker._p.addprevious(t._tbl)
    return t

def update_title_and_abstract(doc):
    old_first = "Cognitive Adaptive Power System Management"
    title_changed = False
    for p in doc.paragraphs[:25]:
        if old_first in p.text and not title_changed:
            set_text_keep_style(p, NEW_TITLE)
            title_changed = True
        elif p.text.strip() == "September 2026":
            set_text_keep_style(p, "November 2026")
    # The latest rebuild already contains an evidence-bounded abstract.
    # Replace its body with one explicitly accounting for E6/PSS/E.
    abstract_heading = None
    for i,p in enumerate(doc.paragraphs):
        if p.text.strip() == "Abstract":
            abstract_heading = i
            break
    if abstract_heading is not None:
        for p in doc.paragraphs[abstract_heading+1:abstract_heading+8]:
            s=p.text.strip()
            if len(s)>250 and not s.startswith(("Keywords", "Chapter")):
                set_text_keep_style(p, ABSTRACT)
                break
    doc.core_properties.title = NEW_TITLE
    doc.core_properties.subject = ("CAPSM doctoral manuscript – revised simulation-first "
                                    "PSS/E v35 and PyTorch research pathway")
    doc.core_properties.comments = (
        "November 2026 revision. PSS/E results are pending licensed validation. "
        "Historical E1 and E2 results must retain evidence qualifiers."
    )
    doc.core_properties.modified = datetime(2026,11,4,12,0,0, tzinfo=timezone.utc)
    return title_changed, abstract_heading is not None

def add_methodology(doc):
    marker=locate(doc,"Chapter 11:")
    if marker is None:
        marker=locate(doc,"Chapter 11")
    if marker is None:
        raise ValueError("Chapter 11 heading not found; cannot insert Chapter 10 methodology")

    heading(marker,"10.13 Independent PSS®E v35 and PyTorch Simulation Extension",2)
    before(marker,(
        "The November 2026 extension is an additional simulation and reproducibility "
        "pathway, rather than a retroactive reclassification of the earlier PYPOWER "
        "or OPAL-RT campaigns. It is documented by the psse_capsm module and the "
        "PSS/E evidence ledger (E6). The module implements RAW-case construction, "
        "a PSS/E v35 AC solver interface, operating-profile scenario generation, "
        "FACTS and EV control equivalents, and exact counterfactual candidate "
        "evaluations. The development environment does not contain a licensed "
        "PSS/E solver, and therefore no completed PSS/E convergence or "
        "performance result is asserted. This section specifies the physical "
        "interpretation and the acceptance criteria that must precede a "
        "doctoral results claim."
    ))

    heading(marker,"10.13.1 IEEE 39-Bus Benchmark and Provenance",3)
    before(marker,(
        "The primary test system is the 39-bus New England benchmark with "
        "10 generators, 34 conventional branch records, and 12 two-winding "
        "transformers. The total of 46 measured AC branches is required by "
        "the canonical 160-feature state encoder. In the MATPOWER case39 "
        "source, bus 31 is the slack bus and bus 39 is a voltage-controlled "
        "PV bus; earlier descriptions of bus 39 as the slack bus were "
        "incorrect. Before conducting experiments, the RAW data must be "
        "audited against the source benchmark, imported into PSS/E v35, "
        "solved under a documented FNSL configuration, and saved as a native "
        "solved case. Bus-voltage magnitudes and angles, generator dispatch, "
        "branch terminal MVA, losses and transformer parameters must be "
        "reconciled. Structural validation alone is insufficient to "
        "establish numerical equivalence or power-flow convergence."
    ))
    before(marker,(
        "For the reference configuration, the SVC is placed at bus 14, the "
        "STATCOM equivalent at bus 39, the TCSC on the 16–17 branch, and "
        "the UPFC equivalent at bus 26 with series-action proxy on 26–28. "
        "The bus-39 shunt is retained to preserve comparability with the "
        "historical deployment, but its impact must be interpreted in light "
        "of the generator-regulated voltage state. Alternative device "
        "placements constitute separate experiments and must not be "
        "reported as the same controller configuration."
    ))

    heading(marker,"10.13.2 Physical Action Representation",3)
    before(marker,(
        "The shared CAPSM action vector contains nine positions, of which "
        "eight are presently active. Its entries represent SVC and STATCOM "
        "susceptance, TCSC compensation, UPFC shunt susceptance, a simplified "
        "UPFC series reactance control, the reserved UPFC series-Q channel, "
        "and three aggregated EV real-power commands. Action index 5 is "
        "forced to zero at candidate generation, inference and action "
        "evaluation, and is excluded from the action-effort penalty. "
        "This constraint prevents a physically inactive quantity from "
        "contributing to apparent optimisation gains."
    ))
    before(marker,(
        "SVC, STATCOM and UPFC shunt equivalents are represented by fixed "
        "susceptance records in the quasi-static case. PSS/E fixed-shunt "
        "BL values are reactive power in MVAr at 1.0 p.u. bus voltage, "
        "so an equivalent susceptance specified in per-unit must be "
        "multiplied by the system MVA base before being entered into RAW "
        "data. TCSC and UPFC series proxies alter effective branch "
        "reactance, with a representative relation Xeff = (1 − k) X. "
        "These controls are engineering abstractions, not validated "
        "switching-converter or dynamic FACTS models. Their use supports "
        "AC operating-point comparisons, not electromagnetic-transient "
        "or converter-interaction conclusions."
    ))

    heading(marker,"10.13.3 EV, Renewable and Time-Series Scenarios",3)
    before(marker,(
        "The three EV stations are located at buses 3, 8 and 15. Each "
        "station has a nominal ±50 MW active-power range, 100 MWh "
        "aggregate energy capacity, a 0.2–0.9 state-of-charge envelope "
        "and 0.92 charge/discharge efficiency. Dispatch is first limited "
        "by instantaneous MW ratings and then by feasible stored-energy "
        "transitions. Charging and V2G discharging must use distinct "
        "efficiency directions, and each accepted action updates SoC "
        "exactly once. Candidate evaluation is read-only and must never "
        "advance the live fleet state. Nonconvergent network solutions "
        "must not be rewarded or silently omitted."
    ))
    before(marker,(
        "Hourly load, wind and solar trajectories are prepared from the "
        "Open Power System Data German series. Training statistics are "
        "derived exclusively from 2015–2017, validation uses 2018, "
        "and held-out testing uses 2019. The German measurements provide "
        "real temporal variability, while their spatial assignment to "
        "IEEE test-network buses is synthetic and requires explicit "
        "documentation. A 50 Hz German input profile does not change "
        "the 60 Hz nominal frequency of the IEEE 39-bus network. "
        "The baseline scaling and bus-level reactive-power treatment "
        "must be frozen before controller comparisons."
    ))

    heading(marker,"10.13.4 Candidate-Specific AC Evaluation and Rewards",3)
    before(marker,(
        "System 2 initially evaluates 32 admissible candidate actions. "
        "For each candidate, the PSS/E adapter loads an identical "
        "pre-action network snapshot, applies that candidate's FACTS "
        "and EV controls, solves AC power flow, and extracts a "
        "candidate-specific post-action observation. Once candidate "
        "ranking is complete, exactly one action is selected for the "
        "actual transition. This avoids an earlier implementation "
        "error in which candidate scores were evaluated against an "
        "unchanged operating state. In the exact reference implementation "
        "these power-flow solves are sequential; a candidate count of "
        "32 does not imply 32 parallel PSS/E executions."
    ))
    before(marker,(
        "The candidate reward combines normalised mean voltage deviation, "
        "squared voltage-limit violation severity, normalised active "
        "losses, squared thermal overload severity, EV energy "
        "infeasibility, and control effort. The reserved UPFC channel "
        "does not contribute to effort. In thermal assessment, apparent "
        "power at both branch terminals must be compared with the "
        "appropriate MVA rating. A missing branch rating is recorded "
        "as missing information, not interpreted as a secure operating "
        "condition. Nonconvergence is a distinct adverse outcome. "
        "Exact AC results establish reference candidate ordering for "
        "later evaluation of sensitivity-based surrogates."
    ))

    heading(marker,"10.13.5 PyTorch Learning and Closed-Loop Integration",3)
    before(marker,(
        "The PSS/E simulation process remains separate from the modern "
        "PyTorch training process because the Python versions supported "
        "by particular PSS/E v35 installations need not match current "
        "machine-learning dependencies. The simulation writes timestamped "
        "JSONL trajectories with pre-action observations, physical "
        "outcomes, applied actions, candidate diagnostics and EV states. "
        "A subsequent data adapter will map these measurements into "
        "the fixed IEEE 39-bus 160-feature ordering: 39 × 2 bus "
        "quantities, 46 branch measurements, 10 × 2 generator quantities, "
        "four FACTS devices × 2, three EV stations × 2, and two "
        "additional scalar features. The 12-step CNN–LSTM input window "
        "and window_reset temporal convention must be identical in "
        "training and testing."
    ))
    before(marker,(
        "Training and model selection must use only the training and "
        "validation partitions. Frozen checkpoints and frozen feature "
        "normalisers are then evaluated in the 2019 held-out window. "
        "The full CAPSM experiment compares NoControl, droop, PI, "
        "System 1, System 2, fixed blending, hard switching and the "
        "stress-dependent Metacognitive Arbiter on identical scenarios. "
        "An improvement in imitation loss is not evidence of improved "
        "network performance. Controller usefulness is determined by "
        "closed-loop violations, losses, secure operation, EV "
        "feasibility and computation cost."
    ))

    heading(marker,"10.13.6 Acceptance Gates and Claim Boundaries",3)
    before(marker,(
        "The proposed evidence sequence is: (i) independent source-case "
        "and RAW structural checks; (ii) licensed PSS/E import, base-case "
        "convergence and numerical reconciliation; (iii) one-device-at-a-time "
        "physical-response tests; (iv) deterministic profile and "
        "contingency execution; (v) exact candidate snapshot-isolation "
        "and reward tests; (vi) leakage-free System 1 training and "
        "held-out inference; and (vii) matched controller comparisons "
        "with repeated seeds and paired statistical uncertainty estimates. "
        "No gate can be inferred solely from a successful Python unit test."
    ))
    table_before(doc, marker,
        ["Gate", "Required evidence", "Current status"],
        [
            ["Source-case audit", "RAW hash, topology, benchmark mapping", "Offline structural tooling available"],
            ["Licensed base case", "PSS/E v35 solved case, bus/branch logs", "Pending local validation"],
            ["FACTS/EV fidelity", "Device-by-device MW, MVAr, X, SoC tests", "Pending local validation"],
            ["Candidate evaluation", "Independent snapshot and reward tests in PSS/E", "Pending local validation"],
            ["PyTorch System 1", "Frozen checkpoint and 2019 PSS/E closed-loop test", "Not implemented in E6"],
            ["Integrated CAPSM", "Matched controllers, uncertainty, ablations", "Not implemented in E6"],
            ["Dynamic/real-time claims", "Validated DYR or traceable HIL logs", "Outside E6 QSTS scope"]
        ])
    before(marker,(
        "PSS/E quasi-static AC studies may support voltage and thermal-security "
        "claims but do not establish transient stability, electromagnetic "
        "switching behaviour, fault-detection latency, Lyapunov stability "
        "of the physical plant or hardware real-time deadlines. Each of "
        "those claims requires a separate validated model and measurement "
        "pathway. The new experiment register is maintained in "
        "audit/12_PSSE_EVIDENCE_LEDGER.md."
    ))

def add_results_status(doc):
    marker=locate(doc,"Chapter 12:")
    if marker is None:
        marker=locate(doc,"Chapter 12")
    if marker is None:
        raise ValueError("Chapter 12 heading not found")
    heading(marker,"11.12 Independent PSS/E Validation: Experiment Status",2)
    before(marker,(
        "The E6 evidence register was created after the earlier offline "
        "and HIL reports. The new PSS/E simulation code is a reproducible "
        "research tool, but a successful offline regression suite is not "
        "a licensed PSS/E simulation result. At the time of the "
        "November 2026 manuscript revision, the following PSS/E claims "
        "remain either awaiting local validation or not implemented. "
        "No numerical performance values are imputed to these experiments."
    ))
    table_before(doc,marker,["ID", "Study", "Result status"],[
        ["PSSE-001", "IEEE39 base-case convergence and benchmark comparison", "PENDING_PSSE_RUN"],
        ["PSSE-002", "NoControl hourly QSTS voltage, thermal and losses", "PENDING_PSSE_RUN"],
        ["PSSE-003 to 006", "FACTS device-response and placement studies", "PENDING_PSSE_RUN"],
        ["PSSE-007", "EV energy/SoC and MW response in PSS/E", "PENDING_PSSE_RUN"],
        ["PSSE-008 to 009", "QIRL exact candidates and N−1 contingency", "PENDING_PSSE_RUN"],
        ["PSSE-010", "Frozen PyTorch System 1 on held-out PSS/E scenarios", "NOT_IMPLEMENTED"],
        ["PSSE-011", "Integrated dual-process CAPSM comparison", "NOT_IMPLEMENTED"],
        ["PSSE-012", "PSS/E RMS dynamic disturbance campaign", "NOT_IMPLEMENTED"]
    ])
    before(marker,(
        "The historical PYPOWER Stage-1 numbers reproduced earlier in "
        "Chapter 11 are archival context only when the September 30 "
        "single-source-of-truth ledger assigns them a SUPERSEDED or "
        "PENDING_RERUN status. Hardware-in-the-loop values labelled "
        "FROZEN_PENDING_PROVENANCE must not be treated as independently "
        "verified hardware measurements without the original run "
        "identifiers and traceable logs. Published final-result comparisons "
        "will be updated only after the corresponding E1, E2 or E6 "
        "evidence gate has been passed."
    ))

def add_conclusion_status(doc):
    marker=locate(doc,"References")
    # Locate the standalone References heading, not an earlier sentence or
    # automatic TOC entry. 
    marker=None
    for p in doc.paragraphs:
        if p.text.strip() == "References":
            marker=p
            break
    if marker is None:
        return
    heading(marker,"13.7 Evidence-Bounded Conclusions of the PSS/E Extension",2)
    before(marker,(
        "The new PSS/E extension establishes a reproducible engineering "
        "interface for evaluating the CAPSM control architecture against "
        "independent AC power-system calculations. Its contribution to "
        "the current manuscript is methodological: physically explicit "
        "FACTS and EV actions, isolated counterfactual evaluations, "
        "trackable operating profiles, and an evidence register that "
        "separates proposed experiments from actual solver measurements. "
        "The code itself does not demonstrate an improvement in voltage "
        "security or losses; those conclusions require the outstanding "
        "licensed PSS/E campaigns, frozen PyTorch checkpoints and "
        "matched controller comparisons. Future work should proceed "
        "through the stated acceptance gates rather than interpreting "
        "design targets or inherited PYPOWER/HIL values as PSS/E evidence."
    ))

def assert_quality(doc, output):
    paragraphs=[p.text for p in doc.paragraphs]
    joined="\n".join(paragraphs)
    chapters=[i for i in range(1,14)
              if any(("Chapter %d:"%i) in t for t in paragraphs)]
    if len(chapters) != 13:
        raise RuntimeError("Expected all 13 chapters; found %s" % chapters)
    required=[
        "Independent PSS®E v35 and PyTorch Simulation Extension",
        "Independent PSS/E Validation: Experiment Status",
        "Evidence-Bounded Conclusions of the PSS/E Extension",
        "PENDING_PSSE_RUN", "NOT_IMPLEMENTED"
    ]
    missing=[x for x in required if x not in joined]
    if missing:
        raise RuntimeError("Missing required revision text: %s" % missing)
    image_count=len(doc.inline_shapes)
    if image_count<15:
        raise RuntimeError("Figure loss suspected: only %d inline figures" % image_count)
    if output.stat().st_size < 1_000_000:
        raise RuntimeError("Small output file suggests original content was lost")
    return {"chapters":chapters,"inline_images":image_count,
            "paragraphs":len(paragraphs),"tables":len(doc.tables),
            "bytes":output.stat().st_size}

def main():
    source=INPUT if INPUT.exists() else FALLBACK
    if not source.exists():
        raise FileNotFoundError("Neither canonical nor historical thesis source found")
    print("Source:",source.name)
    doc=Document(str(source))
    changed,abstract_found=update_title_and_abstract(doc)
    if not changed or not abstract_found:
        raise RuntimeError("Source title/abstract not found; refusing destructive rebuild")
    add_methodology(doc)
    add_results_status(doc)
    add_conclusion_status(doc)
    doc.save(str(OUTPUT))
    print("Output:",OUTPUT.name)
    print("QA:",assert_quality(Document(str(OUTPUT)),OUTPUT))

if __name__=="__main__":
    main()
