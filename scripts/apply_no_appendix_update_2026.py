#!/usr/bin/env python3
"""Conservative CAPSM evidence-bound no-appendix DOCX integration.

This is a STRUCTURAL REVISION, not a claim to have completed a 250-page
substantive expansion. It preserves the original document and exports bulky
appendix tables as research data. Requires python-docx and lxml.
"""
from __future__ import annotations
import argparse, csv, json, re, zipfile
from copy import deepcopy
from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

APPENDIX_RE = re.compile(r'^\s*Appendix\s+([A-H])\s*[:\s]',re.I)
CHAPTER_RE = re.compile(r'^\s*Chapter\s+(\d{1,2})\s*[:\s]',re.I)
SECTION_RE = re.compile(r'^\s*(\d{1,2})\.(\d{1,2})(?:\s|\.)')
CORRECTED_MATH = [
('RoCoF under consistent frequency base',
 'For a system-base per-unit power deficit \u0394P and aggregated inertia H_sys (s), the initial frequency slope is df/dt \u2248 f_0\u0394P/(2H_sys), with negative sign for a generation deficit if \u0394P = P_generation \u2212 P_demand. The factor f_0 is mandatory when expressing df/dt in Hz/s. This approximation excludes primary response, damping, and fast converter control during the initial interval.'),
('Direction-consistent state of charge',
 'Let e_t be the fractional battery state, C the energy capacity (MWh), P_ch \u2265 0 the AC import (MW), and P_dis \u2265 0 the AC export (MW). Then e_{t+1} = e_t + \u03b7_ch P_ch \u0394t/C \u2212 P_dis \u0394t/(\u03b7_dis C). At 25 MW AC export for 1 h, \u03b7_dis = 0.92, C = 100 MWh and e_0 = 0.50, the battery delivers 25/0.92 = 27.174 MWh and ends at e_1 \u2248 0.2283. In contrast, 25 MWh battery depletion would produce 23 MW of AC export. These are different metering conventions.'),
('Amplitude update and correct probability ratio',
 'If amplitudes are updated as \u03b1_i\u2190\u03b1_i exp(\u03b2 r_i)/Z and then sampled via p_i = |\u03b1_i|\u00b2, the ratio after one update is p_i/p_j = (|\u03b1_i^{old}|\u00b2/|\u03b1_j^{old}|\u00b2) exp[2\u03b2(r_i\u2212r_j)]. Thus a \u03b2 rather than 2\u03b2 Boltzmann exponent describes a *probability* update, not this amplitude update. The stated QIRL ratio theorem must be restated with a specified initial distribution and reward-range assumption. Neither representation implies quantum speed-up.'),
('Weighted least squares residual test',
 'For a full-rank linear Gaussian model with m measurements and n estimated independent state variables, the whitened post-fit residual statistic follows \u03c7\u00b2 with m\u2212n degrees of freedom, not generally m. Constraints, bad-data screening, correlated noise, state-dependent Jacobians and parameter estimation can alter the null distribution. A fixed threshold needs calibration for the actual measurement system.'),
('Constraint penalty sign',
 'When reward is defined R = \u2212w_V D_V \u2212w_L \u0394L \u2212w_viol N_viol, a penalty weight w_viol must be nonnegative; using w_viol = \u221210 would *reward* violations. If the model is instead maximizing a weighted improvement, redefine signs explicitly and verify units or normalisation for each term.'),
('Integral frequency restoration qualification',
 'The statement K_I > 0 implies \u0394f_ss = 0 is not an unconditional theorem. Zero steady-state error follows only under appropriate closed-loop stability, sufficient actuator headroom, absence of bias/saturation, and a feasible constant-disturbance equilibrium. Stability and reachability require separate analysis.'),
]
STATUS = [
('AC cross-solver comparison','Validated for numerical agreement','Does not prove operating security or control efficacy'),
('OPSD/IEEE 39-bus held-out time series','Measured, with failed hours retained','132 converged of 168; failures are not zero loss'),
('41 isolated device cases','Measured / independently cross-checked','Bus-39 shunt neutralisation; UPFC series is a proxy'),
('CNN\u2013LSTM imitation','Measured in offline study','Accuracy is imitation, not closed-loop performance'),
('QIRL candidate selector','Implemented / assessed offline','No quantum hardware or quantum advantage'),
('Sigmoid blending arbiter','Design','Measured selector is not proof of the proposed blender'),
('Fault classification','Design targets only','No measured 97.2% fault accuracy in PSSE33 archive'),
('PINN and HMARL','Design / separate evidence scope','No PSSE33 implementation claims'),
('OPAL-RT HIL','Future work / protocol','No HIL execution in PSSE33 campaign'),
('N-1 security','Measured screening','840/1,104 converged; not N-1 secure'),
('Sub-50-ms control','Design target','Measured 32-candidate decision ~5.8 s'),
]
APP_MAP = {'A':'14.1 Evidence index and environment', 'B':'14.2 Claim reconciliation',
           'C':'14.3 Empirical audit and inference boundaries',
           'D':'11.3 Cross-solver device evidence', 'E':'11.2 Held-out trajectory evidence',
           'F':'archived external N-1 catalogue', 'G':'archived external action ledger',
           'H':'archived external policy and loss ledger'}

def node_text(node):
    return ''.join(t.text or '' for t in node.iter(qn('w:t'))).strip()

def append_paragraph(doc, before, text, style=None):
    p=doc.add_paragraph(style=style)
    p.add_run(text)
    el=p._p
    el.getparent().remove(el)
    before.addprevious(el)
    return el

def append_table(doc,before,rows):
    t=doc.add_table(rows=1,cols=len(rows[0]));t.style='Table Grid'
    for j,v in enumerate(rows[0]): t.rows[0].cells[j].text=str(v)
    for row in rows[1:]:
        cells=t.add_row().cells
        for j,v in enumerate(row): cells[j].text=str(v)
    el=t._tbl
    el.getparent().remove(el)
    before.addprevious(el)
    return el

def find_body_anchor(body,pattern, flags=re.I):
    rx=re.compile(pattern,flags)
    for child in body:
        if child.tag != qn('w:p'):continue
        tx=node_text(child)
        if rx.match(tx) and not re.search(r'\.{8,}',tx):return child
    return None

def set_heading(node,title):
    # Preserve paragraph properties only; all text becomes a plain new heading.
    for x in list(node):
        if x.tag!=qn('w:pPr'): node.remove(x)
    r=OxmlElement('w:r');t=OxmlElement('w:t');t.text=title;r.append(t);node.append(r)
    pp=node.find(qn('w:pPr'))
    if pp is None:pp=OxmlElement('w:pPr');node.insert(0,pp)
    pstyle=pp.find(qn('w:pStyle'))
    if pstyle is None:pstyle=OxmlElement('w:pStyle');pp.append(pstyle)
    pstyle.set(qn('w:val'),'Heading2' if title.startswith('14.') else 'Heading1')

def export_archival_rows(chunks,output_dir):
    archive=output_dir/'archive'
    archive.mkdir(exist_ok=True)
    counts={}
    for letter in 'FGH':
        group=chunks.get(letter,[])
        with (archive/f'Original_Appendix_{letter}_Data.tsv').open('w',encoding='utf-8',newline='') as f:
            writer=csv.writer(f,delimiter='\t')
            writer.writerow(['original_appendix','source_block','block_kind','content'])
            for i,node in enumerate(group):
                if node.tag==qn('w:tbl'):
                    for tr in node.findall(qn('w:tr')):
                        cols=[node_text(tc) for tc in tr.findall(qn('w:tc'))]
                        writer.writerow([letter,i,'table_row',' | '.join(cols)])
                else:
                    tx=node_text(node)
                    if tx:writer.writerow([letter,i,'paragraph',tx])
        counts[letter]=len(group)
    return counts

def replace_in_runs(doc):
    replacements={
      '5.26\u00d710 \u2074\u207b':'5.26\u00d710\u207b\u2074',
      '5.26\u00d710 \u207b\u2074':'5.26\u00d710\u207b\u2074',
      '5.26\u00d710\u2074\u207b':'5.26\u00d710\u207b\u2074',
      'CAPSM_PSSE33_evidence_2026-11-08(1).zip':'CAPSM_PSSE33_evidence_2026-11-08.zip',
    }
    count=0
    for p in doc.paragraphs:
        for r in p.runs:
            orig=r.text
            for a,b in replacements.items():r.text=r.text.replace(a,b)
            count+=r.text!=orig
    return count

def build(infile,outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    src=Path(infile)
    d=Document(src)
    body=d._element.body
    nodes=list(body)
    starts={}
    for index,el in enumerate(nodes):
        if el.tag!=qn('w:p'):continue
        txt=node_text(el)
        m=APPENDIX_RE.match(txt+' ')
        if m and not re.search(r'\.{8,}',txt) and len(txt)<110: starts[m.group(1).upper()]=index
    refs=[i for i,n in enumerate(nodes) if n.tag==qn('w:p') and re.match(r'^References\s*$',node_text(n),re.I)]
    if not starts or not refs:raise RuntimeError('Cannot identify original Appendix A-H and References; original source left intact')
    ref_idx=refs[-1]
    if max(starts.values())>=ref_idx:raise RuntimeError('Appendix sections not immediately before bibliography; check structure')
    chunks={}
    for letter,index in starts.items():
        stop=min([j for j in list(starts.values())+[ref_idx] if j>index])
        chunks[letter]=nodes[index:stop]
    archived=export_archival_rows(chunks,outdir)
    # Remove all appendix blocks from thesis, preserving references as end matter.
    for i in range(min(starts.values()),ref_idx):
        n=nodes[i]; n.getparent().remove(n)
    # Refresh references anchor in modified document.
    reference=find_body_anchor(body,r'^References\s*$')
    ch11_3=find_body_anchor(body,r'^11\.3\s')
    ch11_4=find_body_anchor(body,r'^11\.4\s')
    if ch11_3 is None or ch11_4 is None:raise RuntimeError('Section 11.3/11.4 not found; cannot position full device evidence')
    # Relocate D before 11.4, i.e. end of 11.3.
    insert=append_paragraph(d,ch11_4,'Device-effect cross-solver data (41 verified cases)','Heading 3')
    for node in chunks.get('D',[])[1:]:ch11_4.addprevious(node)
    # Relocate E before 11.3, at end of Section 11.2.
    append_paragraph(d,ch11_3,'Chronological held-out results and recorded solver failures','Heading 3')
    for node in chunks.get('E',[])[1:]:ch11_3.addprevious(node)
    # Chapter 14 archival explanations and original A-C content.
    append_paragraph(d,reference,'Chapter 14: Evidence Provenance, Reproduction and Claim Audit','Heading 1')
    append_paragraph(d,reference,'[Method] This chapter retains the complete experiment provenance and the claim reconciliation transferred from the former supplementary sections. Detailed 41-device and held-out trajectory records now appear in Sections 11.3 and 11.2 respectively. The original N-1, action, and policy row-level catalogues are supplied only as machine-readable research archive files, not as additional thesis appendices.')
    for letter in 'ABC':
        append_paragraph(d,reference,APP_MAP[letter],'Heading 2')
        for node in chunks.get(letter,[])[1:]:reference.addprevious(node)
    append_paragraph(d,reference,'14.4 External row-level data retention and limits','Heading 2')
    append_paragraph(d,reference,'[Method] The original Appendices F, G and H are preserved in separate TSV archival records and in the unmodified 313-page source manuscript. Appendix F comprised the complete N-1 contingency-screening catalogue; Appendix G comprised the three-seed, 32-candidate action ledger; Appendix H comprised the multi-seed policy-level comparison ledger. Their original pagination, identifiers and values remain auditable from the external archive without inflating the analytical argument or presenting raw rows as new evidence.')
    append_paragraph(d,reference,'[Measured] The PSS/E 33.4 campaign recorded 840 convergent outcomes among 1,104 N-1 cases per assessed policy, with 264 non-convergent outages. This is not evidence of an N-1 secure envelope. The 32-candidate decision time was approximately 5.8 s, which does not meet a sub-50-ms real-time design target.')
    append_paragraph(d,reference,'14.5 Claim-integrity matrix','Heading 2')
    append_table(d,reference,[('Claim area','Admissible evidence label','Not established')]+STATUS)
    append_paragraph(d,reference,'14.6 Mathematical corrections to the expansion blueprint','Heading 2')
    for title,bodytext in CORRECTED_MATH:
        append_paragraph(d,reference,title,'Heading 3')
        append_paragraph(d,reference,bodytext)
    # Supplemental technical notes in main argument: no fictitious measurements.
    ch10=find_body_anchor(body,r'^Chapter\s+10\b')
    if ch10 is not None and ch10.getnext() is not None:
        ch10_first=ch10.getnext()
        append_paragraph(d,ch10_first,'Evidence-status and measurement separation','Heading 3')
        append_paragraph(d,ch10_first,'[Design] The dual-process architecture specifies a reflex, a deliberative evaluator, and an arbiter over one action interface. Their mathematical composition does not establish a feasible or beneficial closed-loop controller. [Measured] The separate licensed PSS/E 33.4 implementation tested steady-state device equivalents and counterfactual selection, and is evaluated only by the quantities and experimental scenarios identified in Chapters 10 and 11. [Future work] Dynamic stability, fault transients, hardware-in-the-loop, and protection-grade timing require independent simulation and measurement campaigns.')
    # Repair only known broken exponent and evidence filename, without destructive global edits.
    fixed=replace_in_runs(d)
    # Replace stale hard-coded table of contents entries and add a truthful note.
    for p in d.paragraphs:
        tx=p.text
        if re.match(r'^Appendix\s+[A-H]\b',tx.strip(),re.I) and re.search(r'\.{8,}',tx):
            p.text=''
    toc=find_body_anchor(body,r'^Table of Contents\s*$')
    if toc is not None:
        append_paragraph(d,toc,'Contents update: regenerate the Word table of contents after final pagination; original static appendix page numbers are intentionally not carried forward.')
    # Explicitly revise appendix wording in prose, but do not overwrite numbered citations and hyperlinks.
    for p in d.paragraphs:
        if re.search(r'\.{8,}',p.text):continue
        for r in p.runs:
            t=r.text
            for letter,target in APP_MAP.items():
                t=re.sub(r'\bAppendix\s+'+letter+r'\b',('Section '+target.split(' ')[0]) if letter in 'ABCDE' else ('the external '+target),t)
            r.text=t
    out=outdir/'CAPSM_Thesis_NoAppendix_Integrated_2026-11-08.docx'
    d.save(out)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
    check=Document(out)
    alltext='\n'.join(p.text for p in check.paragraphs)
    # Exclude remaining TOC references; no chapter named Appendix.
    headings=[p.text for p in check.paragraphs if re.match(r'^Appendix\s+[A-H]\b',p.text,re.I)]
    report={'source':src.name,'output':out.name,'original_appendices':sorted(starts),
            'relocated_full_sections':['D->11.3','E->11.2','A/B/C->14'],
            'archived_only':['F','G','H'],'archived_node_counts':archived,
            'changed_run_count':fixed,'paragraph_count':len(check.paragraphs),
            'table_count':len(check.tables),'residual_appendix_heading_count':len(headings),
            'has_chapter_14':'Chapter 14:' in alltext,
            'target_250_body_pages_verified':False,
            'warning':'Original main-text 250-page requirement is NOT established by this structural integration; page count and substantive additions require a separate expansion gate.'}
    (outdir/'QA_INTEGRATION_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    assert not headings, headings
    assert report['has_chapter_14']
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',default='releases/2026-11-08/CAPSM_PhD_Thesis_Final_313pg_2026-11-08.docx')
    parser.add_argument('--outdir',default='releases/2026-11-08/no_appendix_revision')
    a=parser.parse_args()
    print(json.dumps(build(a.source,Path(a.outdir)),indent=2))