#!/usr/bin/env python3
"""Conservative CAPSM doctoral-manuscript editorial pass, preserving empirical claims."""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json, re, sys

src=Path(sys.argv[1]);dst=Path(sys.argv[2])
d=Document(src)
normal=d.styles['Normal']; normal.font.name='Times New Roman';normal.font.size=Pt(12);normal.font.color.rgb=RGBColor(0,0,0)
normal.paragraph_format.line_spacing=1.30
normal.paragraph_format.space_after=Pt(5)
for style_name, sz, before, after in [('Heading 1',16,17,11),('Heading 2',13,13,6),('Heading 3',12,10,5)]:
 st=d.styles[style_name];st.font.name='Times New Roman';st.font.size=Pt(sz);st.font.bold=True;st.font.color.rgb=RGBColor(16,31,52)
 st.paragraph_format.space_before=Pt(before);st.paragraph_format.space_after=Pt(after);st.paragraph_format.keep_with_next=True
 st.paragraph_format.widow_control=True
if 'Front Matter Heading' not in d.styles:
 st=d.styles.add_style('Front Matter Heading',WD_STYLE_TYPE.PARAGRAPH)
else: st=d.styles['Front Matter Heading']
st.base_style=normal;st.font.bold=True;st.font.size=Pt(14)
st.paragraph_format.space_before=Pt(14);st.paragraph_format.space_after=Pt(7);st.paragraph_format.keep_with_next=True
cap=d.styles['Caption'];cap.font.name='Times New Roman';cap.font.size=Pt(10);cap.font.italic=False;cap.font.color.rgb=RGBColor(34,46,62)
cap.paragraph_format.space_before=Pt(4);cap.paragraph_format.space_after=Pt(8);cap.paragraph_format.keep_with_next=True
if 'References Body' not in d.styles:
 refs=d.styles.add_style('References Body',WD_STYLE_TYPE.PARAGRAPH)
else: refs=d.styles['References Body']
refs.base_style=normal;refs.font.size=Pt(10);refs.paragraph_format.line_spacing=1.0;refs.paragraph_format.left_indent=Inches(.3);refs.paragraph_format.first_line_indent=Inches(-.3);refs.paragraph_format.space_after=Pt(5)
for section in d.sections:
 section.left_margin=Inches(1.25);section.right_margin=Inches(1.0)
 section.top_margin=Inches(1);section.bottom_margin=Inches(1)
 section.header_distance=Inches(.48);section.footer_distance=Inches(.45)
# Citation and table count remain as in measured edition; do not overwrite references with uncited bibliography.
front_titles={'Abstract','Keywords','List of Abbreviations','Table of Contents','List of Figures','List of Tables'}
para_count=0;captions=0;refs_count=0;abstract_revised=0;front=0
for p in d.paragraphs:
 txt=p.text.strip()
 if not txt:continue
 if p.style.name=='Normal':
  if txt in front_titles:
   p.style=st;front+=1
  elif re.match(r'^(Figure|Table)\s+\d+(?:\.\d+)?\s*[:\.]',txt):
   p.style=cap; captions+=1
  elif re.match(r'^\[\d{1,3}\]\s+',txt):
   p.style=refs;refs_count+=1
  elif len(txt)>110 and not txt.startswith('['):
   p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
   p.paragraph_format.widow_control=True
 if p.style.name=='Heading 1' and txt.startswith(('Chapter ','Appendix ','References')):
  p.paragraph_format.page_break_before=True
 if txt.startswith('This thesis develops Cognitive Adaptive Power System Management (CAPSM)') and len(txt)>550:
  # Maintain original measured outcome and scope while tightening framing and causal claims.
  updated=(
  'This thesis investigates Cognitive Adaptive Power System Management (CAPSM), a dual-process architecture for coordinated control of flexible AC transmission devices and aggregated electric-vehicle resources. It integrates a learned CNN–LSTM proposal path (System 1), a 32-candidate solver-based evaluation path (System 2), and a metacognitive arbiter. The research distinguishes architectural design objectives from results obtained in a licensed PSS/E 33.4 quasi-static IEEE 39-bus study. Baseline and 41 isolated device tests agree with corresponding MATPOWER calculations, with maximum voltage-magnitude discrepancies of 5.26 × 10⁻⁴ and 2.27 × 10⁻⁵ p.u., respectively. A 159-feature, 12-step bridge trains a 137,418-parameter CNN–LSTM on a chronological data split; normalized imitation error is 0.00311 compared with 0.00780 for a constant predictor. Nevertheless, on a 24-hour policy comparison the learned controller increases mean losses by 0.0845 MW relative to no control. Three-seed exploratory results yield mean loss differences of −0.0282 MW for greedy candidates and −0.0653 MW for learned-proposal-seeded selection, with uncertainty intervals that include zero. Contingency screening converges for 840 of 1,104 outages per policy, while the pre-contingency operating envelope already violates voltage or thermal limits. The primary contribution is an auditable, reproducible pathway from controller proposals to AC network evaluation and explicit identification of design and feasibility limitations. The presented evidence does not establish controller superiority, transient security, or hardware-in-the-loop performance.'
  )
  # Preserve paragraph properties and style, replace text.
  if p.runs:
   p.runs[0].text=updated
   for run in p.runs[1:]:run.text=''
  else:p.add_run(updated)
  abstract_revised+=1
 para_count+=1
# Prevent row splitting and repeat table headers in audit tables; avoid wholesale row reflow changes.
for table in d.tables:
 for idx,row in enumerate(table.rows):
  if idx==0:
   trPr=row._tr.get_or_add_trPr()
   if trPr.find(qn('w:tblHeader')) is None: trPr.append(OxmlElement('w:tblHeader'))
  # Avoid applying row keep to long text/appendix tables (may overflow pages).
  for cell in row.cells: cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
# Keep original section headers/footers, but add a consistent document descriptor in CoreProperties.
d.core_properties.title='Cognitive Adaptive Power System Management for Coordinated FACTS and Electric Vehicle Control'
d.core_properties.subject='PhD thesis; measured PSS/E 33 evidence and scientific scope reconciliation'
d.core_properties.keywords='CAPSM, FACTS, electric vehicles, AC power flow, IEEE 39-bus, reproducibility'
# Make revision distinct from approved university submission; not an official submission format certification.
d.save(dst)
print(json.dumps({'input':str(src),'output':str(dst),'paragraphs':len(d.paragraphs),'tables':len(d.tables),'inline_figures':len(d.inline_shapes),'references_formatted':refs_count,'captions_style_adjusted':captions,'abstract_revised':abstract_revised,'front_headings':front,'note':'Original reference list preserved and recent references staged in separate companion library'}))