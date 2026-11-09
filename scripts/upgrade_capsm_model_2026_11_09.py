#!/usr/bin/env python3
"""Evidence-aware CAPSM thesis augmentation: diagrams, audited equations and comparative tables.
Usage: python upgrade_capsm_model.py input.docx output.docx [figure_dir]
Designed to run locally or in GitHub Actions against the checked-in integrated thesis.
Only uses measurements already reported in the source thesis; all new figures are labelled.
"""
from pathlib import Path
import sys, math, re, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC=Path(sys.argv[1]) if len(sys.argv)>1 else Path('releases/2026-11-08/no_appendix_revision/CAPSM_Thesis_NoAppendix_Integrated_2026-11-08.docx')
OUT=Path(sys.argv[2]) if len(sys.argv)>2 else Path('releases/2026-11-09/CAPSM_PhD_Thesis_Model_Enhanced_2026-11-09.docx')
FIGDIR=Path(sys.argv[3]) if len(sys.argv)>3 else OUT.parent/'model_figures'
FIGDIR.mkdir(parents=True, exist_ok=True)
OUT.parent.mkdir(parents=True, exist_ok=True)
D=Document(str(SRC))
BLUE='#11345C'; TEAL='#087A87'; GREY='#5D6977'; ORANGE='#C77933'; LIGHT='#EAF2F7'; RED='#B4493E'

# Insert objects in the main document stream immediately before the next section heading.
def anchor(section):
    paragraphs=D.paragraphs
    i=next((i for i,p in enumerate(paragraphs) if p.text.strip()==section),None)
    if i is None: raise ValueError('Missing thesis section: '+section)
    para=paragraphs[i]
    level=1 if para.style.name=='Heading 1' else 2
    for p in D.paragraphs[i+1:]:
        if p.style.name in ('Heading 1','Heading 2') and (p.style.name=='Heading 1' or level==2):
            return p
    raise ValueError('No later section boundary for '+section)

def put_para(before, txt='',style=None,boldlead=None):
    p=D.add_paragraph(style=style or 'Normal'); before._p.addprevious(p._p)
    if boldlead and txt.startswith(boldlead):p.add_run(boldlead).bold=True;p.add_run(txt[len(boldlead):])
    else:p.add_run(txt)
    return p

def heading(before,title):return put_para(before,title,'Heading 3')
def caption(before,title):
    p=put_para(before,title,'Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    return p

def keep_rows(t):
    for r in t.rows:
        trPr=r._tr.get_or_add_trPr();e=OxmlElement('w:cantSplit');trPr.append(e)
    if t.rows:
        trPr=t.rows[0]._tr.get_or_add_trPr();e=OxmlElement('w:tblHeader');e.set(qn('w:val'),'true');trPr.append(e)

def shade(cell,color):
    tcPr=cell._tc.get_or_add_tcPr();shd=OxmlElement('w:shd');shd.set(qn('w:fill'),color);tcPr.append(shd)

def table(before,name,headers,rows,note=None):
    caption(before,name)
    t=D.add_table(rows=1, cols=len(headers))
    t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=True
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i];c.text=str(h);shade(c,'DDE9F2')
        for run in c.paragraphs[0].runs:run.bold=True;run.font.size=Pt(8)
    for j,row in enumerate(rows):
        cells=t.add_row().cells
        for i,value in enumerate(row):
            cells[i].text=str(value)
            if j%2:shade(cells[i],'F6F9FB')
            cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in cells[i].paragraphs:
                for run in p.runs:run.font.size=Pt(8)
    keep_rows(t);before._p.addprevious(t._tbl)
    if note:put_para(before,'Note. '+note)
    return t

def image(before,number,description,path,width=6.25):
    p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True
    r=p.add_run();shape=r.add_picture(str(path),width=Inches(width));before._p.addprevious(p._p)
    shape._inline.docPr.set('descr',description)
    caption(before,number+': '+description)

def eq(before,formula,desc,key):
    fig,ax=plt.subplots(figsize=(9.5,0.75));ax.axis('off');ax.text(0.5,0.52,formula,fontsize=17,ha='center',va='center',color='#20364E')
    pth=FIGDIR/(key+'.png');fig.savefig(pth,dpi=180,transparent=False,bbox_inches='tight',pad_inches=.12);plt.close(fig)
    p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run();sh=r.add_picture(str(pth),width=Inches(5.8));sh._inline.docPr.set('descr',desc)
    before._p.addprevious(p._p)

def base_fig(w=10,h=4.5):
    fig,ax=plt.subplots(figsize=(w,h));ax.set_xlim(0,10);ax.set_ylim(0,5);ax.axis('off');return fig,ax

def node(ax,x,y,w,h,txt,color=BLUE,fs=10):
    patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.035,rounding_size=0.13',facecolor=color,edgecolor='#25394A',linewidth=0.5)
    ax.add_patch(patch);ax.text(x+w/2,y+h/2,txt,ha='center',va='center',color='white',fontsize=fs,weight='bold',wrap=True)

def arrow(ax,x1,y1,x2,y2,color=GREY):ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=13,linewidth=1.8,color=color))

def draw_arch():
    fig,ax=base_fig(11,4.7)
    node(ax,.15,2.05,1.45,.84,'Measured\nstate',TEAL)
    node(ax,2.05,3.25,1.8,.85,'System 1\nCNN-LSTM',BLUE)
    node(ax,2.05,1.05,1.8,.85,'System 2\nQIRL',BLUE)
    node(ax,4.4,2.05,1.62,.84,'Metacognitive\narbiter',ORANGE)
    node(ax,6.52,2.05,1.35,.84,'Projection\n& limits',TEAL)
    node(ax,8.35,2.05,1.48,.84,'AC model\n& actuators',BLUE)
    for a,b,c,d in [(1.6,2.52,2.05,3.68),(1.6,2.48,2.05,1.45),(3.85,3.68,4.4,2.7),(3.85,1.48,4.4,2.25),(6.02,2.47,6.52,2.47),(7.87,2.47,8.35,2.47)]:arrow(ax,a,b,c,d)
    ax.annotate('Stress, confidence, deadlines',xy=(5.25,3.1),ha='center',fontsize=11,color=GREY)
    ax.annotate('Shared 9-dimensional action; projection is not a power-flow feasibility proof',xy=(5.0,.22),ha='center',fontsize=10,color=GREY)
    path=FIGDIR/'capsm_control_contract.png';fig.savefig(path,dpi=210,bbox_inches='tight');plt.close(fig);return path

def draw_action():
    fig,ax=plt.subplots(figsize=(11,3.7));ax.set_xlim(-.4,9.4);ax.set_ylim(0,2.5);ax.axis('off')
    labels=['SVC B','STATCOM B','TCSC k','UPFC shunt','UPFC series 1','UPFC series 2','EV3 MW','EV8 MW','EV15 MW']
    for i,lab in enumerate(labels):
        col=TEAL if i<6 else ORANGE
        node(ax,i+.04,.9,.88,.8,lab,col,7.1)
        ax.text(i+.48,.55,'u'+str(i+1),ha='center',fontsize=9,color=GREY)
    ax.text(4.5,2.15,'A common action vector does not imply a common physical response model',ha='center',fontsize=12,color=BLUE,weight='bold')
    path=FIGDIR/'capsm_action_vector.png';fig.savefig(path,dpi=215,bbox_inches='tight');plt.close(fig);return path

def draw_schema():
    fig,ax=plt.subplots(figsize=(9,3));ax.axis('off');ax.set_xlim(0,10);ax.set_ylim(0,3)
    node(ax,.4,1.35,3.2,.9,'Design encoder: 160 features',BLUE,12)
    node(ax,6.3,1.35,3.2,.9,'Measured learning: 159 features',TEAL,11)
    arrow(ax,3.7,1.8,6.2,1.8,RED)
    ax.text(5.0,2.3,'Schema reconciliation required',ha='center',fontsize=11,color=RED,weight='bold')
    ax.text(5.0,.53,'No one-to-one mapping or drop-column justification is established by this figure.',ha='center',fontsize=10,color=GREY)
    path=FIGDIR/'capsm_feature_schema.png';fig.savefig(path,dpi=200,bbox_inches='tight');plt.close(fig);return path

def draw_soc():
    fig,ax=plt.subplots(figsize=(8,4))
    xs=[0,1,2]; ys=[.50,.50+.92*25/100,.50-25/(.92*100)]
    ax.bar(xs,ys,color=[BLUE,TEAL,ORANGE],width=.55)
    ax.set_xticks(xs,['Initial','1h charging\n25 MW AC','1h discharge\n25 MW AC']);ax.set_ylabel('Battery state of charge (p.u.)');ax.set_ylim(0,.82)
    for x,y in zip(xs,ys):ax.text(x,y+.025,f'{y:.4f}',ha='center',fontsize=12,fontweight='bold')
    ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    ax.set_title('Illustrative energy balance: E = 100 MWh, efficiency = 0.92')
    fig.tight_layout();path=FIGDIR/'capsm_soc_examples.png';fig.savefig(path,dpi=220,bbox_inches='tight');plt.close(fig);return path

def draw_evidence():
    fig,ax=base_fig(11,4.1)
    node(ax,.25,2.8,2.6,.82,'Stage 1: offline / QSTS',BLUE)
    node(ax,3.55,2.8,2.6,.82,'PSS/E 33.4 campaign',TEAL)
    node(ax,6.9,2.8,2.8,.82,'HIL / EMT / PINN / HMARL',ORANGE)
    ax.text(1.55,2.14,'Implementation and\nprofile-specific checks',ha='center',fontsize=10,color=GREY)
    ax.text(4.85,2.14,'AC power flow, N-1,\nlearning and timings',ha='center',fontsize=10,color=GREY)
    ax.text(8.3,2.14,'Proposed or separate;\nnot demonstrated here',ha='center',fontsize=10,color=GREY)
    for x in [2.95,6.25]:ax.plot([x,x],[1.0,3.95],ls=':',lw=2,color=RED)
    ax.text(5.0,.4,'Dashed boundaries prohibit transferring evidence across campaigns',ha='center',fontsize=11,color=RED)
    path=FIGDIR/'capsm_evidence_boundaries.png';fig.savefig(path,dpi=215,bbox_inches='tight');plt.close(fig);return path

def draw_week():
    days=['Jan 19','Jan 20','Jan 21','Jan 22','Jan 23','Jan 24','Jan 25'];vals=[24,24,20,24,11,10,19]
    fig,ax=plt.subplots(figsize=(10,3.8));bars=ax.bar(days,vals,color=[TEAL if n==24 else ORANGE for n in vals],width=.63)
    ax.set_ylim(0,27);ax.set_ylabel('Convergent hours (out of 24)');ax.axhline(24,linestyle='--',color=GREY,linewidth=1)
    for b,n in zip(bars,vals):ax.text(b.get_x()+b.get_width()/2,n+.45,str(n)+'/24',ha='center',fontsize=10)
    ax.set_title('Measured held-out January week: 132/168 converged [E-C]')
    fig.tight_layout();path=FIGDIR/'capsm_week_convergence.png';fig.savefig(path,dpi=215,bbox_inches='tight');plt.close(fig);return path

def draw_n1():
    fig,ax=plt.subplots(figsize=(9,3.7));labels=['Convergent','Non-convergent'];vals=[840,264]
    bars=ax.barh(labels,vals,color=[TEAL,RED],height=.55);ax.set_xlim(0,1150);ax.invert_yaxis();ax.set_xlabel('Outage solves (per policy; 1104 total)')
    for bar,v in zip(bars,vals):ax.text(v+13,bar.get_y()+bar.get_height()/2,f'{v:,} ({v/1104:.1%})',va='center',fontsize=11)
    ax.set_title('Measured N-1 numerical convergence [E-G]');fig.tight_layout();path=FIGDIR/'capsm_n1_accounting.png';fig.savefig(path,dpi=220,bbox_inches='tight');plt.close(fig);return path

def draw_loss():
    fig,ax=plt.subplots(figsize=(8.7,3.9));names=['No control','Droop'];vals=[48.4315,48.5170];bars=ax.bar(names,vals,color=[BLUE,ORANGE],width=.53)
    ax.set_ylim(48.1,48.72);ax.set_ylabel('Mean active-power losses (MW)');ax.set_title('Measured 24-hour baseline: droop did not reduce losses [E-C]')
    for bar,v in zip(bars,vals):ax.text(bar.get_x()+bar.get_width()/2,v+.018,f'{v:.4f} MW',ha='center',fontsize=11)
    ax.text(.5,.94,'Difference: +0.0855 MW (droop minus no control)',ha='center',fontsize=10,color=RED,transform=ax.transAxes)
    fig.tight_layout();path=FIGDIR/'capsm_loss_comparison.png';fig.savefig(path,dpi=215,bbox_inches='tight');plt.close(fig);return path

def draw_timing():
    fig,ax=plt.subplots(figsize=(9,4));names=['Deliberative design target','One recorded Stage E solve','32 Stage E solves (serial)'];vals=[50,180.6,5779.2]
    ax.barh(names,vals,color=[BLUE,ORANGE,RED]);ax.set_xscale('log');ax.set_xlim(20,12000);ax.invert_yaxis();ax.set_xlabel('Elapsed time (ms), logarithmic axis')
    for y,v in enumerate(vals):ax.text(v*1.08,y,f'{v:,.1f} ms',va='center',fontsize=10)
    ax.set_title('Design deadline versus measured host-side computation [E-E]')
    fig.tight_layout();path=FIGDIR/'capsm_timing_comparison.png';fig.savefig(path,dpi=215,bbox_inches='tight');plt.close(fig);return path

def draw_readiness():
    fig,ax=base_fig(10,3.7)
    titles=[('1','Numerical parity','Measured'),('2','Policy efficacy','Not established'),('3','Dynamic stability','Not established'),('4','Real-time HIL','Not established')]
    for i,(k,t,s) in enumerate(titles):
        x=.2+i*2.5;node(ax,x,2.15,2.18,.82,k+' '+t,TEAL if i==0 else GREY,9)
        ax.text(x+1.09,1.67,s,ha='center',fontsize=10,color=BLUE if i==0 else RED)
        if i<3:arrow(ax,x+2.22,2.55,x+2.46,2.55)
    ax.text(5,.55,'Progression requires new evidence; passing an earlier gate never implies a later one.',ha='center',fontsize=10.5,color=GREY)
    path=FIGDIR/'capsm_deployment_gates.png';fig.savefig(path,dpi=215,bbox_inches='tight');plt.close(fig);return path

# -- Chapter 3: model consistency --
a=anchor('3.4 Mathematical Modelling of Integrated Components')
heading(a,'3.4.5 Action-space, units and feasibility contract')
put_para(a,'The controller shares a nine-component command vector, but individual components act on different electrical equivalents. The source implementation uses fixed susceptance, fixed reactance and fixed active-power edits. Consequently, satisfying a command bound is only a necessary input-domain condition: the next AC power-flow solution may still fail, and voltage or branch-loading limits may remain violated. This distinction applies to every controller path and is preserved in the following interface contract.')
image(a,'Figure 3.9','Nine-dimensional CAPSM command vector grouped by physical proxy; conceptual encoding, not converter-level validation.',draw_action())
table(a,'Table 3.3: Action-model interface and physical interpretation',['Command group','Control coordinates','Simulation proxy','Required additional check'],[
 ('Shunt FACTS','u1, u2, u4–u6','Fixed-bus shunt susceptance / equivalent channels','Bus Q balance; generator Q limits; actual converter capability'),
 ('Series FACTS','u3','Fixed branch reactance or compensation multiplier','Thermal rating, series limits, line topology'),
 ('Aggregated EV','u7, u8, u9','Signed fixed-P exchange at buses 3, 8, 15','Availability; SoC; energy balance; P bounds; network feasibility')], 'The command count follows Table 4.2; several UPFC channels are reduced-order proxies, not a full converter model.')
table(a,'Table 3.4: Feasibility checks at the action-to-network boundary',['Order','Check','Pass condition','Failure response'],[
 ('1','Syntax, units, dimensions','Nine finite values in explicit engineering units','Reject candidate and record malformed action'),
 ('2','Equipment command bounds','lo_i <= u_i <= hi_i for each i','Project or reject with projection flag'),
 ('3','EV energy and availability','Battery energy and connection limits respected','Clip charge/discharge or mark infeasible'),
 ('4','Network model integrity','Device endpoints and elements exist','Record missing-element action error'),
 ('5','AC load flow','Solution converges under stated tolerances','Log failure separately; do not infer instability'),
 ('6','Operational security','Voltage / thermal / reactive margins meet criteria','Report violation counts and severity; do not declare safe')])
put_para(a,'A convex blend of individually bounded System 1 and System 2 outputs remains inside the same box. It does not imply preservation of AC feasibility because nonlinear network constraints define a generally nonconvex subset of that box. In deployment, the arbitration output must therefore pass a separate feasibility and fallback layer before a field command is released.')

# -- Chapter 4: learned controllers and schema audit --
a=anchor('4.2 Development of the Brain-Inspired AI Framework')
heading(a,'4.2.4 Explicit controller contract and arbitration audit')
put_para(a,'Both cognitive paths may produce candidate actions concurrently; the metacognitive controller chooses a blend according to the observed operating stress and confidence in each path. The decision layer is distinct from the Markov decision process used for sequential policy learning: the MDP formalizes state, action, transition and reward, while the arbiter chooses how a reflexive and deliberative output is consumed at the current decision instant.')
image(a,'Figure 4.4','CAPSM signal contract and projection boundary; conceptual architecture, not measured end-to-end hardware execution.',draw_arch())
eq(a,r'$u_t=\Pi_{\mathcal{A}}\!\left[\alpha_t u_t^{(1)}+(1-\alpha_t)u_t^{(2)}\right]$','Bounded dual-process blending with projection into the command box','equation_arbitration')
put_para(a,'Here alpha is constrained between zero and one; u(1) and u(2) are candidate setpoint vectors in identical units; and the projection operator enforces box limits only. Runtime fallback must retain the most recent accepted safe action or a verified conventional controller if a fresh candidate fails validation. This is an implementation requirement, not a measured result of the PSS/E 33.4 campaign.')
eq(a,r'$\frac{p_i^{+}}{p_j^{+}}=\frac{p_i}{p_j}\exp\{2\beta(A_i-A_j)\}$','Probability-ratio update following an exponentiated amplitude transformation','equation_qirl')
put_para(a,'For an amplitude update proportional to exp(beta A), probability is amplitude squared after normalization; the corresponding relative probability exponent is 2 beta, not beta. The formula is a mathematical consistency correction and does not establish improved exploration or convergence in the measured campaign.')
table(a,'Table 4.7: Controller-design interface and empirical scope',['Component','Design-level function','Evidence currently available','Not established'],[
 ('System 1 CNN–LSTM','Rapid nine-action proposal from temporal features','159-feature realized imitation implementation; 137,418 parameters; normalized error 0.00311','Closed-loop protection grade response; certified real-time execution'),
 ('System 2 QIRL','Deliberation and candidate ranking','PSS/E candidate exploration with 32 trial actions','Quantum hardware advantage; optimal candidate guarantee'),
 ('Metacognitive arbiter','Stress-adaptive combination of both action paths','Conceptual architecture and selected offline tests','Fail-safe system-level switching in field conditions'),
 ('Projection and safety layer','Command bounds, network constraints and fallback','Command-box argument; numerical AC outcomes','Formal guarantee of secure post-contingency operation')], 'Evidence boundaries distinguish design architecture from the PSS/E AC campaign [E-E, E-F].')
image(a,'Figure 4.5','Design-versus-implementation feature count; a one-feature discrepancy requiring explicit schema reconciliation.',draw_schema())
table(a,'Table 4.8: State-interface reconciliation checkpoint',['Source layer','Recorded size','Interpretation','Acceptance criterion'],[
 ('Architecture description (Table 4.3)','160 features per time step','Design state encoder specification','Publish ordered feature map and scaling'),
 ('Measured CNN–LSTM learning bridge [E-F]','159 features per time step','Realized training/inference schema','Explain every added, dropped, transformed feature'),
 ('Cross-domain deployment','Unresolved 160 versus 159 mapping','Potential silent feature misalignment','Unit tests prove exact column order and units before inference')])

# -- Chapter 8: energy-consistent V2G --
a=anchor('8.2 Bidirectional Power Flow Management (V2G/G2V)')
heading(a,'8.2.1 EV energy accounting, direction conventions and headroom')
put_para(a,'For this section the signed grid-side power is decomposed into nonnegative charging power P_ch and nonnegative discharge power P_dis. Power charging the battery is reduced by charging efficiency; exporting active power to the AC grid requires more battery-side energy than the delivered AC energy. An SoC recurrence that divides the export by discharge efficiency therefore avoids overstating V2G availability.')
eq(a,r'$\mathrm{SoC}_{t+1}=\mathrm{SoC}_{t}+\frac{\eta_{\rm ch}P_{\rm ch}\Delta t}{E}-\frac{P_{\rm dis}\Delta t}{\eta_{\rm dis}E}$','Direction-consistent EV battery energy recurrence','equation_soc')
image(a,'Figure 8.4','Illustrative one-hour EV SoC example; values calculated from the stated assumptions, not an experimental trace.',draw_soc())
table(a,'Table 8.6: Worked SoC balance for one aggregated station',['Operation','AC energy exchange (MWh)','Battery energy change (MWh)','Final SoC'],[
 ('Initial condition','0','0','0.5000'),
 ('Charge at 25 MW for 1 h','25 imported','+23.0000','0.7300'),
 ('Discharge at 25 MW for 1 h','25 exported','−27.1739','0.2283')], 'Illustration assumes E = 100 MWh, eta_ch = eta_dis = 0.92, no other losses, and no ancillary-service activation.')
put_para(a,'These are algebraic examples rather than observations from PSS/E. A deployable controller must additionally check SoC minimum/maximum bounds, connected-vehicle availability, charger P/Q capability, fleet participation uncertainty and the terminal SoC requirement. A stationary power-flow injection alone does not verify those conditions.')

# -- Chapter 10: validated versus proposed evidence --
a=anchor('10.11 Domain-transfer and model-representation controls')
heading(a,'10.12 Measured, derived and proposed evidence separation')
put_para(a,'A single numerical agreement metric cannot support every layer of the CAPSM architecture. The validation record is therefore partitioned by simulator, model fidelity, controllable assets and observable outputs. The comparisons in Chapter 11 are evidence of selected AC model behavior and algorithm execution, whereas the HIL, EMT, PINN and hierarchical multi-agent claims require distinct campaigns and test equipment.')
image(a,'Figure 10.1','Evidence boundaries across offline simulation, licensed PSS/E AC validation, and unexecuted or separate higher-fidelity claims.',draw_evidence())
table(a,'Table 10.1: Evidence provenance and permitted inference',['Evidence tier','Representative records','Supports','Does not support'],[
 ('E-B baseline','39-bus PSS/E and MATPOWER solved base','Input transfer, solver cross-check, base-limit audit','Compliance; transient/dynamic stability'),
 ('E-C trajectories','24-hour baseline; 168-hour January holdout','Hourly AC losses, voltages and non-convergence counts','Unseen contingency performance'),
 ('E-D actuators','41 isolated fixed-B/fixed-X/fixed-P cases','Proxy-model parity','Detailed converter validation'),
 ('E-E candidate policies','32-action selection on 24-hour cases','Candidate ranking and host-compute burden','Sub-50 ms online control'),
 ('E-F imitation bridge','159-feature CNN–LSTM tests','Normalized imitation error on specified split','Closed-loop savings or security'),
 ('E-G N-1 campaign','1,104 outages per policy','Preventive AC contingency screening','Cascading, protection, transient survival'),
 ('HIL, EMT, PINN, HMARL','Design and research agenda','Engineering requirements / hypotheses','Measured PSS/E campaign outcomes')])
table(a,'Table 10.2: Validation acceptance gates for future CAPSM campaigns',['Gate','Minimum artifact','Measurement and pass rule'],[
 ('Network data','RAW snapshot; bus and branch mapping','Hash input and verify all controlled endpoints'),
 ('Interface integrity','Feature order, transforms and controller version','Exact 159/160 schema reconciliation and reproducible feature hashes'),
 ('Candidate transaction','One baseline, trials, and commitment per time step','Count calls and restore state between trials'),
 ('Statistical fairness','Matched feasible timestamps and contingency cases','Report both paired comparison and full non-convergence denominator'),
 ('Model fidelity','Dynamic converter, actuator and protection parameters','Compare phasor/EMT behavior independently of fixed proxies'),
 ('Real-time performance','Hardware timestamps across sensor-to-actuator path','Bound worst-case latency and deadline misses under load')])

# -- Chapter 11: quantitative dashboard --
a=anchor('11.9 Findings supported by the campaign')
heading(a,'11.9.1 Quantitative comparison and negative-result accounting')
put_para(a,'The measurement ledger below fixes denominators before comparing policies. The measured records establish accurate cross-solver transfer on convergent solutions, but the baseline has pre-existing limit violations and the droop comparison increases average losses. These negative and conditional findings are essential to the interpretation of the current CAPSM implementation.')
image(a,'Figure 11.4','Measured held-out January 19–25, 2019 AC convergence by day; exact daily totals from the thesis [E-C].',draw_week())
table(a,'Table 11.1: Held-out daily solver-convergence ledger',['Date in 2019','Converged hours','Failed hours','Daily convergence'],[(f'Jan {day}',n,24-n,f'{n/24*100:.1f}%') for day,n in zip(range(19,26),[24,24,20,24,11,10,19])]+[('Total',132,36,'78.6%')], 'The 36 failed hours must not be silently omitted when describing scenario coverage [E-C].')
image(a,'Figure 11.5','Per-policy N-1 outage convergence; non-convergent cases are not classified as physical instability [E-G].',draw_n1())
table(a,'Table 11.2: Preventive N-1 accounting and interpretation',['Quantity','Observed count / value','Interpretation'],[
 ('Hourly operating points','24','Matched preventive screen, not automatic post-fault recovery'),
 ('Outages at each hour','46','Lines and transformers under the adopted topology'),
 ('Outage AC attempts per policy','1,104','24 × 46'),
 ('Convergent outage solves','840 (76.1%)','Subset on which electrical metrics can be compared'),
 ('Non-convergent outage solves','264 (23.9%)','240 recurring transformer cases plus 24 line 16–19 cases'),
 ('Base solves per policy','24','Separate from the 1,104 outage attempts'),
 ('Total attempted solves per policy','1,128','24 base + 1,104 outage'),
 ('Successful contingency rescues by droop','0','No failed outage was recovered in tested cases')], 'Numbers follow Section 11.7 and the Chapter 10 screening protocol [E-G].')
image(a,'Figure 11.6','Measured loss comparison for 24 matched hours; axis intentionally zoomed and numeric labels shown [E-C].',draw_loss())
table(a,'Table 11.3: Distinguishing solver agreement, control benefit and security',['Question','Reported measurement','Defensible conclusion'],[
 ('Did source systems agree numerically?','Base loss 43.63 MW vs 43.64 MW; held-out max loss discrepancy 0.00636 MW','Agreement on selected mutually convergent AC solutions'),
 ('Did droop reduce mean hourly losses?','48.4315 MW no control vs 48.5170 MW droop','No: +0.0855 MW for the reported 24-hour window'),
 ('Was the reference base secure?','7 voltage magnitudes outside 0.95–1.05 p.u.','No compliance claim for adopted base mapping'),
 ('Was the N-1 set fully solvable?','840/1,104 converged per policy','No; 264 solver failures remain'),
 ('Was HIL timing demonstrated?','Host-side Stage E approx. 180.6 ms per solve','No sensor-to-actuator or deterministic HIL result')])
image(a,'Figure 11.7','Controller-time comparison; 32 serial candidate solves at Stage E mean imply about 5.78 s before other overhead [E-E].',draw_timing())
put_para(a,'The 32-solve product is a derived serial-execution estimate, not an observed end-to-end decision time. Parallelization can change the wall-clock total, but requires a measured worker schedule, contention profile and aggregation overhead. An earlier 50 ms design budget and the recorded 180.6 ms mean single solve are not interchangeable quantities.')

# -- Chapter 12: qualification before deployment --
a=anchor('12.8 Lessons for the metacognitive design')
heading(a,'12.9 Engineering acceptance criteria for field-oriented transfer')
put_para(a,'A real-world CAPSM deployment requires separation between mathematical command admissibility, simulated steady-state feasibility, dynamic security and hard real-time execution. The evidence ladder in Figure 12.1 is intentionally one-way: successfully transferring a base case between software tools does not certify the next stage.')
image(a,'Figure 12.1','Evidence-gated progression from numerical parity to operational deployment; only the first gate has current support.',draw_readiness())
table(a,'Table 12.1: Deployment gate, failure consequence and required new evidence',['Gate','Open engineering issue','Required future experiment'],[
 ('Safety enforcement','Bounded command can still violate AC limits','Feasibility filter, feasibility-rate metric, safe fallback tests'),
 ('Physics representation','Fixed-B/X/P proxies omit converter controls','Dynamic model verification under comparable setpoint changes'),
 ('Feature integration','160-feature design vs 159-feature realized model','Schema unit tests, missing-data behavior and out-of-distribution alarm'),
 ('Contingency validity','Known baseline violations and 264 failed N-1 cases','Screen secure reference envelope; classify topology versus solver failures'),
 ('Efficacy','Droop mean losses increase in matched day','Matched secure scenarios; uncertainty; multiobjective Pareto audit'),
 ('Timing','Approx. 180.6 ms per Stage E solve','Full pipeline on target hardware with deadline-miss histogram'),
 ('Resilience','HIL and cyber failure not part of measured campaign','Independent SIL/CHIL fault injections, event logs and recovery time')])

# -- Chapter 14: final claim registry --
a=anchor('14.6 Mathematical corrections to the expansion blueprint')
heading(a,'14.7 Compact claim integrity and consistency register')
table(a,'Table 14.1: Claims and provenance accepted in this edition',['Claim','Status','Evidence / restriction'],[
 ('IEEE 39-bus PSS/E↔MATPOWER base numerical parity','Measured, qualified','E-B; only converged AC snapshots'),
 ('Held-out hourly scenario coverage 132/168','Measured','E-C; 36 numerical failures unfilled'),
 ('Isolated-device proxy parity for 41 cases','Measured, proxy-limited','E-D; not dynamic converter testing'),
 ('Nine-dimensional shared actuator command','Documented design','Command bounds do not prove nonlinear feasibility'),
 ('CNN–LSTM 159-feature measured input','Measured implementation','E-F; differs from 160-feature design specification'),
 ('32-candidate deliberative search','Implemented in offline campaign','E-E; bounded search, not global optimization'),
 ('Sub-50 ms deliberative execution','Design target, unverified','Conflicts with present host-side solve measurements'),
 ('N-1 preventive screening 840/1104 convergence','Measured','E-G; not corrective action or physical fault-stability proof'),
 ('PINN compliance / HMARL scale / real-time HIL','Unverified in this campaign','Require independent artifacts before empirical use')])
put_para(a,'No new experiment was executed for this model-enhanced edition. New numerical values in Figures 8.4 and 11.7 are calculated examples or transparent arithmetic derived from stated assumptions. All other plotted empirical values are transcribed from the measured thesis text identified in their captions. The bibliography and original measured tables remain in place.')

# Final metadata and structural check.
D.core_properties.title='CAPSM: Cognitive Adaptive Power System Management — Model-Enhanced Thesis'
D.core_properties.subject='Evidence-aware mathematical model, diagrams, and validation tables'
D.save(str(OUT))
reloaded=Document(str(OUT))
figs=list(FIGDIR.glob('*.png'))
report={
 'input':str(SRC),'output':str(OUT),'paragraphs':len(reloaded.paragraphs),
 'tables':len(reloaded.tables),'inline_shapes':len(reloaded.inline_shapes),
 'new_figure_files':sorted(x.name for x in figs),'new_table_captions':[p.text for p in reloaded.paragraphs if re.match(r'Table (3\.3|3\.4|4\.7|4\.8|8\.6|10\.1|10\.2|11\.1|11\.2|11\.3|12\.1|14\.1):',p.text)],
 'has_references':any(p.text.strip()=='References' for p in reloaded.paragraphs),
 'has_14_chapters':sum(1 for p in reloaded.paragraphs if p.style.name=='Heading 1' and p.text.startswith('Chapter '))==14,
 'notes':'No new simulations executed; measured figures use existing thesis evidence, other figures conceptual/derived.'}
(OUT.parent/'CAPSM_MODEL_UPDATE_QA.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))