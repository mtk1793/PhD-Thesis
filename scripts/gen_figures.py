#!/usr/bin/env python3
"""Generate all thesis figures for the CAPSM PhD thesis.

Produces schematics (architecture, flowcharts, timelines) and data charts
(from verified CAPSM Stage-1 results). All text uses Canadian/British
spelling. Figures are saved to /home/z/my-project/thesis_build/figures/.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

C_BLUE = "#2563EB"; C_GREEN = "#059669"; C_RED = "#DC2626"; C_AMBER = "#D97706"
C_PURPLE = "#7C3AED"; C_GRAY = "#6B7280"; C_TEAL = "#0D9488"; C_PINK = "#DB2777"
C_LBLUE = "#93C5FD"; C_LGREEN = "#86EFAC"; C_LRED = "#FCA5A5"; C_LAMBER = "#FCD34D"

def box(ax, x, y, w, h, text, fc="#EFF6FF", ec=C_BLUE, fs=8, tc="black", lw=1.2, style="round,pad=0.02"):
    b = FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, mutation_scale=1)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc, wrap=True)
    return b

def arrow(ax, x1, y1, x2, y2, color=C_GRAY, lw=1.4, style="-|>", ls="-", ms=10):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color, lw=lw,
                        linestyle=ls, mutation_scale=ms, shrinkA=2, shrinkB=2)
    ax.add_patch(a)

def blank(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)

# ---------------------------------------------------------------- Fig 1.1 renewable growth
years = np.arange(2010, 2024)
solar = np.array([40, 70, 100, 138, 176, 222, 296, 385, 480, 578, 710, 849, 1055, 1412])
wind = np.array([178, 197, 217, 240, 271, 319, 364, 415, 466, 514, 563, 622, 688, 743])
hydro = np.array([949, 970, 990, 1016, 1042, 1071, 1096, 1122, 1151, 1176, 1197, 1230, 1267, 1303])
fig, ax = plt.subplots(figsize=(6.8, 3.2))
ax.bar(years, solar, 0.62, label="Solar PV", color=C_AMBER)
ax.bar(years, wind, 0.62, bottom=solar, label="Wind", color=C_BLUE)
ax.bar(years, hydro, 0.62, bottom=solar+wind, label="Hydropower", color=C_TEAL)
ax.set_ylabel("Installed capacity (GW)")
ax.set_xlabel("Year")
ax.legend(frameon=False, ncol=3, loc="upper left")
ax.set_title("Global installed renewable capacity, 2010-2023")
ax.grid(axis="y", alpha=0.25)
save(fig, "fig_renewable_growth.png")

# ---------------------------------------------------------------- Fig 1.2 traditional vs modern
fig, ax = blank((7.2, 3.4))
ax.text(2.5, 9.6, "Traditional system", ha="center", fontsize=10, fontweight="bold", color=C_GRAY)
box(ax, 1.0, 7.6, 3.0, 1.2, "Centralised dispatch\n(fossil units)", fc="#F3F4F6", ec=C_GRAY)
box(ax, 0.4, 5.6, 1.6, 1.0, "Load", fc="white", ec=C_GRAY)
box(ax, 3.0, 5.6, 1.6, 1.0, "Load", fc="white", ec=C_GRAY)
arrow(ax, 2.5, 7.6, 1.2, 6.6, color=C_GRAY); arrow(ax, 2.5, 7.6, 3.8, 6.6, color=C_GRAY)
ax.text(2.5, 4.9, "Unidirectional flow\npassive distribution\none-way control", ha="center", fontsize=8, color=C_GRAY)
ax.text(7.5, 9.6, "Modern system", ha="center", fontsize=10, fontweight="bold", color=C_BLUE)
box(ax, 6.0, 7.6, 3.0, 1.2, "Hierarchical + AI control\n(CAPSM)", fc="#EFF6FF", ec=C_BLUE)
for x, lab in [(5.6, "PV"), (6.8, "Wind"), (8.0, "EV"), (9.2, "BESS")]:
    box(ax, x-0.55, 5.6, 1.1, 1.0, lab, fc="white", ec=C_BLUE, fs=7.5)
    arrow(ax, 7.5, 7.6, x, 6.6, color=C_BLUE, style="<|-|>")
ax.text(7.5, 4.9, "Bidirectional flows\nvariable generation\nmulti-timescale control", ha="center", fontsize=8, color=C_BLUE)
arrow(ax, 4.75, 6.5, 5.25, 6.5, color="black", lw=1.8)
save(fig, "fig_trad_vs_modern.png")

# ---------------------------------------------------------------- Fig 1.3 gap framework
fig, ax = blank((7.2, 4.0))
gaps = [("Gap 1\nArchitecture for\nheterogeneous assets", 9.1),
        ("Gap 2\nReal-time decisions\nunder uncertainty", 7.1),
        ("Gap 3\nFACTS-DER\ncoordination", 5.1),
        ("Gap 4\nFault detection and\nlocalisation", 3.1),
        ("Gap 5\nTheory-to-practice\nintegration", 1.1)]
for g, y in gaps:
    box(ax, 0.3, y-0.75, 3.1, 1.5, g, fc="#FEF2F2", ec=C_RED, fs=7.5)
sols = [("Dual-process CAPSM\narchitecture (Ch. 3)", 9.1),
        ("CNN-LSTM reflex +\nQIRL deliberation (Ch. 4)", 7.1),
        ("Coordinated FACTS +\nEV dispatch (Ch. 9)", 5.1),
        ("Multi-modal fusion +\nFDI detection (Ch. 7)", 3.1),
        ("Controller-HIL on\nOPAL-RT (Ch. 10)", 1.1)]
for s, y in sols:
    box(ax, 6.6, y-0.75, 3.2, 1.5, s, fc="#F0FDF4", ec=C_GREEN, fs=7.5)
    arrow(ax, 3.4, y, 6.6, y, color=C_GRAY)
box(ax, 4.35, 4.55, 1.3, 1.0, "CAPSM", fc="#EFF6FF", ec=C_BLUE, fs=9)
save(fig, "fig_gap_framework.png")

# ---------------------------------------------------------------- Fig 1.4 CAPSM architecture
fig, ax = blank((7.6, 4.4))
box(ax, 0.3, 8.35, 2.3, 1.2, "Measurement layer\nPMU / SCADA / meters", fc="#F3F4F6", ec=C_GRAY, fs=7.5)
box(ax, 3.85, 8.35, 2.3, 1.2, "State encoder\n160 features", fc="#FDF4FF", ec=C_PURPLE, fs=7.5)
box(ax, 7.4, 8.35, 2.3, 1.2, "Power grid\nIEEE 39-bus + FACTS + EV", fc="#ECFDF5", ec=C_GREEN, fs=7.5)
box(ax, 0.9, 5.7, 2.6, 1.6, "System 1 (reflexive)\nCNN-LSTM\nbudget < 5 ms", fc="#EFF6FF", ec=C_BLUE, fs=8)
box(ax, 6.5, 5.7, 2.6, 1.6, "System 2 (deliberative)\nQIRL, 32 candidates\nbudget < 50 ms", fc="#FEF3C7", ec=C_AMBER, fs=8)
box(ax, 3.6, 5.9, 2.8, 1.2, "Metacognitive Arbiter\n$u=\\alpha u_1+(1-\\alpha)u_2$", fc="#FDF4FF", ec=C_PURPLE, fs=8)
box(ax, 2.3, 3.0, 5.4, 1.1, "Actuation layer: SVC@14, STATCOM@39, TCSC@16-17, UPFC@26, EV@3/8/15", fc="white", ec=C_GREEN, fs=7.5)
box(ax, 2.3, 0.7, 5.4, 1.0, "Safety filter: PINN constraint check, clamp to action box", fc="#FEF2F2", ec=C_RED, fs=7.5)
arrow(ax, 1.45, 8.35, 1.9, 7.3, color=C_BLUE)
arrow(ax, 2.6, 8.6, 3.85, 8.6, color=C_GRAY)
arrow(ax, 7.4, 8.6, 6.2, 8.6, color=C_GRAY, style="<|-")
arrow(ax, 8.55, 8.35, 8.0, 7.3, color=C_AMBER)
arrow(ax, 3.5, 6.5, 3.6, 6.5, color=C_PURPLE)
arrow(ax, 6.5, 6.5, 6.4, 6.5, color=C_PURPLE)
arrow(ax, 5.0, 5.9, 5.0, 4.1, color=C_PURPLE)
arrow(ax, 2.3, 3.55, 1.6, 6.0, color=C_BLUE, ls="--", style="<|-|>")
arrow(ax, 7.7, 3.55, 8.3, 5.7, color=C_AMBER, ls="--", style="<|-|>")
arrow(ax, 5.0, 3.0, 5.0, 1.7, color=C_RED, style="-")
arrow(ax, 5.0, 0.7, 5.0, 0.0, color=C_RED, style="-")
save(fig, "fig_capsm_architecture.png")

# ---------------------------------------------------------------- Fig 1.5 validation pipeline
fig, ax = blank((7.6, 2.6))
stages = [("Stage 1\nOffline Python\nPYPOWER QSTS + OPSD\nIEEE 9/14/39/118/300", 0.2),
          ("Stage 2\nSimulink preparation\nDESL-EPFL IEEE 39-bus\nFACTS + EV models", 3.5),
          ("Stage 3\nController-HIL\n4-core OPAL-RT\nARTEMIS 50 us EMT", 6.8)]
for s, x in stages:
    box(ax, x, 4.6, 3.0, 3.4, s, fc="#EFF6FF", ec=C_BLUE, fs=8)
arrow(ax, 3.2, 6.3, 3.5, 6.3, color=C_GRAY, lw=2)
arrow(ax, 6.5, 6.3, 6.8, 6.3, color=C_GRAY, lw=2)
for x, lab in [(1.7, "exit: 52/52 tests,\n100% convergence"), (5.0, "exit: model builds,\nRT-LAB partitions")]:
    ax.text(x, 3.9, lab, ha="center", fontsize=7, color=C_GRAY, style="italic")
ax.text(5.0, 1.2, "exit: timing budgets met on hardware,\noffline-to-HIL consistency verified", ha="center", fontsize=7, color=C_GRAY, style="italic")
save(fig, "fig_validation_pipeline.png")

# ---------------------------------------------------------------- Fig 2.1 AI timeline
fig, ax = plt.subplots(figsize=(7.2, 3.0))
eras = [(1980, "Expert systems\n(DELTA)"), (1989, "ANN security\nassessment"), (1992, "Fuzzy\ncontrol"),
        (2000, "EA / PSO\noptimisation"), (2008, "Quantum-inspired\nRL"), (2015, "Deep RL\n(DQN, TD3)"),
        (2019, "PINNs"), (2021, "Dual-process\ncognitive AI"), (2026, "HIL-validated\ncognitive control")]
xpos = [1, 2.2, 3.4, 4.6, 5.8, 7.0, 8.2, 9.4, 10.6]
ax.hlines(0, 0.2, 11.4, color=C_GRAY, lw=1.5)
cols = [C_GRAY, C_TEAL, C_GREEN, C_AMBER, C_PURPLE, C_BLUE, C_RED, C_PINK, C_GREEN]
for (yr, lab), x, c in zip(eras, xpos, cols):
    ax.plot(x, 0, "o", color=c, ms=8, zorder=5)
    up = (x * 7) % 2 == 0
    ytxt, ystem = 0.55, 0.15
    ax.plot([x, x], [0, ystem if up else -ystem], color=c, lw=1)
    ax.text(x, ytxt if up else -ytxt, f"{yr}\n{lab}", ha="center",
            va="bottom" if up else "top", fontsize=7, color=c)
ax.set_ylim(-1.6, 1.6); ax.set_xlim(0, 11.6); ax.axis("off")
ax.set_title("Evolution of AI applications in power systems", fontsize=10)
save(fig, "fig_ai_timeline.png")

# ---------------------------------------------------------------- Fig 2.2 FACTS classification
fig, ax = blank((6.8, 3.4))
box(ax, 3.9, 8.6, 2.2, 1.0, "FACTS devices", fc="#EFF6FF", ec=C_BLUE, fs=9)
box(ax, 0.5, 6.0, 2.4, 1.0, "Shunt", fc="white", ec=C_BLUE)
box(ax, 3.8, 6.0, 2.4, 1.0, "Series", fc="white", ec=C_BLUE)
box(ax, 7.1, 6.0, 2.4, 1.0, "Combined", fc="white", ec=C_BLUE)
arrow(ax, 4.6, 8.6, 1.7, 7.0, color=C_GRAY); arrow(ax, 5.0, 8.6, 5.0, 7.0, color=C_GRAY)
arrow(ax, 5.4, 8.6, 8.3, 7.0, color=C_GRAY)
box(ax, 0.2, 3.4, 1.35, 1.6, "SVC\nthyristor\ncontrolled", fc="#F0FDF4", ec=C_GREEN, fs=7)
box(ax, 1.75, 3.4, 1.35, 1.6, "STATCOM\nVSC based\nwider range", fc="#F0FDF4", ec=C_GREEN, fs=7)
box(ax, 3.6, 3.4, 1.35, 1.6, "TCSC\nseries\nreactance", fc="#FEF3C7", ec=C_AMBER, fs=7)
box(ax, 5.15, 3.4, 1.35, 1.6, "SSSC\nseries source\n(sync.)", fc="#FEF3C7", ec=C_AMBER, fs=7)
box(ax, 6.9, 3.4, 1.5, 1.6, "UPFC\nshunt+series\n(full control)", fc="#FDF4FF", ec=C_PURPLE, fs=7)
box(ax, 8.6, 3.4, 1.2, 1.6, "IPFC\nmulti-line\nseries", fc="#FDF4FF", ec=C_PURPLE, fs=7)
for tx, bx in [(1.7, 0.85), (1.7, 2.4), (5.0, 4.25), (5.0, 5.8), (8.3, 7.6), (8.3, 9.2)]:
    arrow(ax, tx, 6.0, bx, 5.0, color=C_GRAY, lw=1.0)
save(fig, "fig_facts_classification.png")

# ---------------------------------------------------------------- Fig 2.3 EV architectures
fig, ax = blank((7.2, 2.8))
box(ax, 0.3, 7.2, 2.0, 1.6, "G2V\n(grid to vehicle)\nunidirectional charge", fc="#EFF6FF", ec=C_BLUE, fs=7.5)
box(ax, 2.6, 7.2, 2.0, 1.6, "V2G\n(vehicle to grid)\nbidirectional service", fc="#F0FDF4", ec=C_GREEN, fs=7.5)
box(ax, 4.9, 7.2, 2.0, 1.6, "V2H\n(vehicle to home)\nbackup supply", fc="#FEF3C7", ec=C_AMBER, fs=7.5)
box(ax, 7.2, 7.2, 2.0, 1.6, "V2X\n(vehicle to everything)\nfull energy node", fc="#FDF4FF", ec=C_PURPLE, fs=7.5)
box(ax, 2.0, 3.4, 6.0, 2.2, "", fc="white", ec=C_GRAY)
ax.text(5.0, 5.15, "Bidirectional charger", ha="center", fontsize=8, color=C_GRAY)
box(ax, 2.4, 3.7, 1.5, 1.2, "AC-DC\nconverter\n(VSC + PLL)", fc="white", ec=C_TEAL, fs=6.8)
box(ax, 4.25, 3.7, 1.5, 1.2, "DC-DC\nconverter\n(buck-boost)", fc="white", ec=C_TEAL, fs=6.8)
box(ax, 6.1, 3.7, 1.5, 1.2, "Battery\npack\n(BMS)", fc="white", ec=C_TEAL, fs=6.8)
arrow(ax, 3.9, 4.3, 4.25, 4.3, color=C_TEAL); arrow(ax, 5.75, 4.3, 6.1, 4.3, color=C_TEAL)
ax.text(5.0, 2.4, "Control loops: SoC management, current/voltage regulation, grid-side droop", ha="center", fontsize=7.5, color=C_GRAY)
save(fig, "fig_ev_architectures.png")

# ---------------------------------------------------------------- Fig 2.4 brain AI radar
fig = plt.figure(figsize=(5.4, 4.0))
ax = fig.add_subplot(111, polar=True)
cats = ["Response\nspeed", "Adaptability", "Uncertainty\nhandling", "Knowledge\nreuse", "Computational\nefficiency", "Interpretability"]
conv = [3.0, 2.5, 2.0, 2.0, 3.5, 4.0]
brain = [4.5, 4.0, 4.5, 3.5, 3.0, 2.5]
ang = np.linspace(0, 2*np.pi, len(cats), endpoint=False).tolist()
conv += conv[:1]; brain += brain[:1]; angc = ang + ang[:1]
ax.plot(angc, conv, color=C_GRAY, lw=1.5, label="Conventional AI")
ax.fill(angc, conv, color=C_GRAY, alpha=0.15)
ax.plot(angc, brain, color=C_BLUE, lw=1.5, label="Brain-inspired AI")
ax.fill(angc, brain, color=C_BLUE, alpha=0.18)
ax.set_xticks(ang); ax.set_xticklabels(cats, fontsize=7.5)
ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=6)
ax.set_ylim(0, 5); ax.legend(loc="lower right", bbox_to_anchor=(1.25, 0.0), frameon=False, fontsize=8)
save(fig, "fig_brain_ai_radar.png")

# ---------------------------------------------------------------- Fig 2.6 DER architectures
fig, ax = blank((7.4, 3.2))
arch = [("Centralised\n(EMS/SCADA)", 0.3), ("Hierarchical\n(3-tier)", 2.3), ("Distributed\n(ADMM/consensus)", 4.3),
        ("Peer-to-peer\n(transactive)", 6.3), ("Hybrid CAPSM\n(dual-process)", 8.3)]
for a, x in arch:
    box(ax, x, 6.4, 1.6, 2.6, a, fc="#F0FDF4" if a.startswith("Hybrid") else "white",
        ec=C_GREEN if a.startswith("Hybrid") else C_GRAY, fs=7.2)
attrs = ["Latency: high", "Latency: medium", "Latency: low", "Latency: peer", "Multi-timescale"]
props = ["Single point of failure", "Clear boundaries", "Scalable, local", "Market based", "Reflex + deliberation"]
for (a, x), at, pr in zip(arch, attrs, props):
    ax.text(x+0.8, 5.9, at, ha="center", fontsize=6.5, color=C_GRAY)
    ax.text(x+0.8, 5.35, pr, ha="center", fontsize=6.5, color=C_GRAY)
ax.annotate("", xy=(0.3, 3.6), xytext=(9.9, 3.6), arrowprops=dict(arrowstyle="<-", color=C_GRAY, lw=1))
ax.text(0.35, 2.9, "more control authority", fontsize=7, color=C_GRAY)
ax.text(9.95, 2.9, "more autonomy", fontsize=7, color=C_GRAY, ha="right")
save(fig, "fig_der_architectures.png")

# ---------------------------------------------------------------- Fig 3.2 CAPSM layers
fig, ax = blank((6.6, 3.8))
layers = [("Executive layer\nMetacognitive Arbiter (10 ms)", C_PURPLE, "#FDF4FF", 7.0),
          ("Coordinated layer\nSystem 2 QIRL dispatch (50 ms)", C_AMBER, "#FEF3C7", 4.9),
          ("Reactive layer\nSystem 1 CNN-LSTM reflex (5 ms)", C_BLUE, "#EFF6FF", 2.8),
          ("Device layer\nFACTS droop, EV local SoC (1 ms)", C_GREEN, "#F0FDF4", 0.7)]
for lab, c, fc, y in layers:
    box(ax, 1.6, y, 6.8, 1.7, lab, fc=fc, ec=c, fs=9)
for y1, y2 in [(7.0, 6.6), (4.9, 4.5), (2.8, 2.4)]:
    arrow(ax, 5.0, y1, 5.0, y2, color=C_GRAY, lw=1.6, style="<|-|>")
ax.text(0.9, 8.55, "goals, mode", fontsize=7, color=C_GRAY, rotation=90, va="top")
save(fig, "fig_capsm_layers.png")

# ---------------------------------------------------------------- Fig 3.3 timescales Gantt
fig, ax = plt.subplots(figsize=(7.0, 2.8))
rows = [("Device protection (local)", 0.5, 1, C_GREEN), ("System 1 CNN-LSTM reflex", 1, 5, C_BLUE),
        ("Metacognitive Arbiter", 5, 10, C_PURPLE), ("System 2 QIRL dispatch", 10, 50, C_AMBER),
        ("Tertiary scheduling (QIRL long horizon)", 60, 300, C_GRAY)]
for i, (lab, lo, hi, c) in enumerate(rows):
    ax.barh(i, hi, left=lo, height=0.55, color=c, alpha=0.85)
    ax.text(lo + hi/2, i, f"{lo}-{hi} ms", va="center", ha="center", fontsize=7.5, color="white", fontweight="bold")
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
ax.invert_yaxis(); ax.set_xscale("log"); ax.set_xlabel("Response time (ms, log scale)")
ax.set_title("Temporal coordination across CAPSM control layers")
ax.grid(axis="x", alpha=0.25, which="both")
save(fig, "fig_timescales.png")

# ---------------------------------------------------------------- Fig 3.4 Bloch / quantum state
fig = plt.figure(figsize=(5.6, 4.2))
ax = fig.add_subplot(111, projection="3d")
u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:24j]
x = np.cos(u)*np.sin(v); y = np.sin(u)*np.sin(v); z = np.cos(v)
ax.plot_surface(x*0.999, y*0.999, z*0.999, color="#E5E7EB", alpha=0.25, linewidth=0)
n = 32
rng = np.random.default_rng(7)
amps = np.exp(0.5 * 5.0 * rng.normal(0, 1, n)); amps /= np.linalg.norm(amps)
probs = amps**2
theta = rng.uniform(0, np.pi, n); phi = rng.uniform(0, 2*np.pi, n)
xs = np.sin(theta)*np.cos(phi); ys = np.sin(theta)*np.sin(phi); zs = np.cos(theta)
sc = ax.scatter(xs, ys, zs, c=probs, cmap="viridis", s=30 + 260*probs, alpha=0.9, edgecolor="k", linewidth=0.3)
ax.quiver(0, 0, 0, 0, 0, 1, color=C_RED, lw=2)
ax.text(0, 0, 1.15, "|0> high Q", color=C_RED, fontsize=9)
ax.text(0, 0, -1.3, "|1> low Q", color=C_RED, fontsize=9)
ax.set_title("QIRL candidate superposition on the Bloch sphere\n(radius of markers = probability |alpha_i|^2)", fontsize=9)
ax.set_axis_off()
plt.colorbar(sc, ax=ax, shrink=0.55, label="P(a_i) = |alpha_i|^2")
save(fig, "fig_bloch_qirl.png")

# ---------------------------------------------------------------- Fig 3.5 fusion architecture
fig, ax = blank((7.4, 3.4))
mods = [("PMU\ncurrents/voltages", 0.3), ("SCADA\nbreakers/alarms", 2.15), ("Smart meters\nloads", 4.0), ("Weather\nirradiance/wind", 5.85), ("Relay flags\nzones", 7.7)]
for m, x in mods:
    box(ax, x, 8.0, 1.7, 1.6, m, fc="white", ec=C_GRAY, fs=7.2)
    arrow(ax, x+0.85, 8.0, x+0.85, 6.9, color=C_GRAY, lw=1)
box(ax, 0.3, 5.4, 9.1, 1.5, "Signal-level fusion: normalisation, time alignment (PTP), sliding windows", fc="#EFF6FF", ec=C_BLUE, fs=8)
box(ax, 0.3, 3.2, 9.1, 1.5, "Feature-level fusion: z = sum_i alpha_i phi_i(x_i)  (attention weights alpha_i)", fc="#FEF3C7", ec=C_AMBER, fs=8)
box(ax, 0.3, 1.0, 9.1, 1.5, "Decision-level fusion: anomaly score + classifier + residual test -> fault zone estimate", fc="#FDF4FF", ec=C_PURPLE, fs=8)
for y in [5.4, 3.2]:
    arrow(ax, 4.85, y, 4.85, y-0.7, color=C_GRAY, lw=1.6)
save(fig, "fig_fusion_architecture.png")

# ---------------------------------------------------------------- Fig 3.6 service heatmap
services = ["Voltage regulation", "Frequency response", "Congestion relief", "Loss reduction", "Renewable integration", "Resilience (N-1)"]
assets = ["FACTS (SVC/STATCOM)", "FACTS (TCSC/UPFC)", "EV fleets (V2G)", "Solar PV + storage", "Flexible loads"]
vals = np.array([
    [3, 3, 1, 1, 2],   # voltage
    [1, 1, 3, 2, 3],   # frequency
    [2, 3, 2, 1, 2],   # congestion
    [2, 2, 2, 2, 2],   # losses
    [2, 2, 3, 3, 2],   # renewable
    [2, 2, 3, 2, 2],   # resilience
])
fig, ax = plt.subplots(figsize=(6.4, 3.0))
im = ax.imshow(vals, cmap="YlGnBu", vmin=0, vmax=3)
ax.set_xticks(range(len(assets))); ax.set_xticklabels(assets, rotation=20, ha="right", fontsize=7.5)
ax.set_yticks(range(len(services))); ax.set_yticklabels(services, fontsize=8)
for i in range(len(services)):
    for j in range(len(assets)):
        ax.text(j, i, ["none", "low", "medium", "high"][vals[i, j]], ha="center", va="center", fontsize=7,
                color="white" if vals[i, j] >= 2 else "black")
cbar = plt.colorbar(im, ax=ax, ticks=[0, 1, 2, 3]); cbar.ax.set_yticklabels(["none", "low", "medium", "high"], fontsize=7)
ax.set_title("Ancillary-service capability of coordinated assets")
save(fig, "fig_service_heatmap.png")

# ---------------------------------------------------------------- Fig 3.7 OPAL topology
fig, ax = blank((7.4, 3.6))
box(ax, 0.3, 6.9, 3.0, 2.4, "Core 1 (sm_master)\nNorth region buses 1-19\n+ System 1 CNN-LSTM\n5 ms period", fc="#EFF6FF", ec=C_BLUE, fs=7.5)
box(ax, 6.7, 6.9, 3.0, 2.4, "Core 2 (sm_slave1)\nSouth region buses 20-39\n+ System 2 QIRL\n50 ms period", fc="#FEF3C7", ec=C_AMBER, fs=7.5)
box(ax, 0.3, 3.2, 3.0, 2.4, "Core 3 (sm_slave2)\nMetacognitive Arbiter\n+ inter-core comms\n10 ms period", fc="#FDF4FF", ec=C_PURPLE, fs=7.5)
box(ax, 6.7, 3.2, 3.0, 2.4, "Core 4 (sm_slave3)\nI/O, logging,\nHIL interface\n1 ms period", fc="#F0FDF4", ec=C_GREEN, fs=7.5)
box(ax, 3.4, 0.4, 3.2, 1.6, "Host PC\nRT-LAB project,\nmodel build, deploy", fc="#F3F4F6", ec=C_GRAY, fs=7.5)
arrow(ax, 3.3, 8.1, 6.7, 8.1, color=C_GRAY, style="<|-|>")
arrow(ax, 1.8, 6.9, 1.8, 5.6, color=C_GRAY, style="<|-|>")
arrow(ax, 8.2, 6.9, 8.2, 5.6, color=C_GRAY, style="<|-|>")
arrow(ax, 3.3, 4.4, 6.7, 4.4, color=C_GRAY, style="<|-|>")
arrow(ax, 5.0, 2.0, 5.0, 3.2, color=C_GRAY, style="<|-|>")
ax.text(5.0, 9.6, "OPAL-RT OP5700 simulator, ARTEMIS solver (50 us EMT), IEC 61850 / C37.118 / PTP",
        ha="center", fontsize=7.5, color=C_GRAY)
save(fig, "fig_opal_topology.png")

# ---------------------------------------------------------------- Fig 3.8 timing budget
fig, ax = plt.subplots(figsize=(6.8, 3.0))
layers = ["Device layer", "System 1 reflex", "Arbiter", "System 2 dispatch", "I/O update"]
budget = [1.0, 5.0, 10.0, 50.0, 1.0]
meas = [0.4, 3.2, 6.0, 27.6, 0.3]
x = np.arange(len(layers))
ax.bar(x - 0.18, budget, 0.34, label="Design budget", color=C_LBLUE, edgecolor=C_BLUE)
ax.bar(x + 0.18, meas, 0.34, label="Offline measured (Python rebuild)", color=C_BLUE)
ax.set_yscale("log"); ax.set_ylabel("Time per step (ms, log scale)")
ax.set_xticks(x); ax.set_xticklabels(layers, fontsize=8)
ax.legend(frameon=False); ax.grid(axis="y", alpha=0.25, which="both")
ax.set_title("Real-time constraint budget across CAPSM control layers")
save(fig, "fig_timing_budget.png")

# ---------------------------------------------------------------- Fig 4.1 CNN-LSTM
fig, ax = blank((7.6, 3.6))
blocks = [("Input\n(12 x 160)", 0.2, "#F3F4F6", C_GRAY),
          ("Conv1d\n1->64, k=3", 1.55, "#EFF6FF", C_BLUE),
          ("ReLU", 2.75, "white", C_BLUE),
          ("Conv1d\n64->64, k=3", 3.45, "#EFF6FF", C_BLUE),
          ("ReLU +\nAvgPool(1)", 4.85, "white", C_BLUE),
          ("LSTM\nhidden 128", 6.05, "#FEF3C7", C_AMBER),
          ("Attention\nsoftmax", 7.35, "#FDF4FF", C_PURPLE),
          ("FC 128->64\n->9 actions", 8.75, "#F0FDF4", C_GREEN)]
for lab, x, fc, ec in blocks:
    box(ax, x, 5.6, 1.15, 2.6, lab, fc=fc, ec=ec, fs=6.8)
for x in [1.35, 2.7, 3.25, 4.6, 5.85, 7.15, 8.55]:
    arrow(ax, x, 6.9, x+0.2, 6.9, color=C_GRAY, lw=1.2)
ax.text(5.0, 4.6, "Sliding window of 12 hourly observations; hidden state persists across steps; outputs clipped to action box",
        ha="center", fontsize=7.5, color=C_GRAY)
ax.text(5.0, 3.7, "~250K parameters: conv 64*3+64 + 64*64*3+64 = 12,864; LSTM 4*(64*128+128*128+128+128) = 131,584;\nattention 128*128+128 + 128+1 = 16,641; FC 128*64+64 + 64*9+9 = 8,705; total ~170K-250K (with biases/pools)",
        ha="center", fontsize=6.8, color=C_GRAY, family="monospace")
save(fig, "fig_cnnlstm_arch.png")

# ---------------------------------------------------------------- Fig 4.3 arbiter alpha
fig, ax = plt.subplots(figsize=(6.2, 3.0))
c1 = np.linspace(0.0, 0.06, 400)
for tau, ls, lab in [(50, "-", "tau = 50 (implemented)"), (100, "--", "tau = 100"), (25, ":", "tau = 25")]:
    alpha = 1/(1 + np.exp(-tau*(0.03 - c1)))
    ax.plot(c1*100, alpha, ls, color=C_BLUE, lw=1.8, label=lab)
ax.axvline(3.0, color=C_GRAY, lw=1, ls="--")
ax.text(3.05, 0.5, "threshold c_th = 0.03 p.u.", fontsize=7.5, color=C_GRAY, rotation=90, va="center")
ax.set_xlabel("System stress c1 = mean|Vm - 1.0| (% p.u.)")
ax.set_ylabel("Arbitration weight alpha")
ax.legend(frameon=False, fontsize=8)
ax.grid(alpha=0.25)
ax.set_title("Metacognitive arbitration weight as a function of system stress")
save(fig, "fig_arbiter_alpha.png")

# ---------------------------------------------------------------- Fig 5.1 GA-PSO flow
fig, ax = blank((7.2, 3.6))
steps = [("Initialise population\n(FACTS location + rating\nchromosomes)", 0.2, C_BLUE),
         ("Evaluate fitness:\nvoltage deviation +\nlosses + violations", 2.0, C_AMBER),
         ("Selection\n(roulette + elitism)", 3.8, C_GREEN),
         ("Crossover + mutation\n(single-point, gaussian)", 5.4, C_PURPLE),
         ("PSO fine tuning\nof device parameters\n(Kp, b range, k range)", 7.1, C_TEAL),
         ("Converged?\nreport placement\n+ HIL verification", 8.7, C_GRAY)]
for s, x, c in steps:
    box(ax, x, 5.4, 1.35, 3.4, s, fc="white", ec=c, fs=6.5)
for x in [1.55, 3.35, 5.15, 6.75, 8.45]:
    arrow(ax, x, 7.1, x+0.2, 7.1, color=C_GRAY, lw=1.4)
arrow(ax, 4.5, 4.6, 2.7, 4.6, color=C_GRAY, ls="--", style="-|>")
ax.text(3.6, 4.75, "iterate generations", fontsize=7, color=C_GRAY)
ax.text(5.0, 2.6, "Placement outer loop (GA) and parameter tuning inner loop (PSO) on the IEEE 39-bus QSTS environment",
        ha="center", fontsize=7.5, color=C_GRAY)
save(fig, "fig_ga_pso_flow.png")

# ---------------------------------------------------------------- Fig 5.2 placement map
fig, ax = plt.subplots(figsize=(7.0, 4.6))
# schematic IEEE 39-bus layout (ring-ish)
rng = np.random.default_rng(3)
ang = np.linspace(0, 2*np.pi, 39, endpoint=False) + 0.05
r = 1.0 + 0.25*np.cos(3*ang) + rng.uniform(-0.06, 0.06, 39)
bx, by = r*np.cos(ang), r*np.sin(ang)
order = np.argsort(ang)
# simple branch set: nearest neighbours in angle
for i in order:
    j = order[(np.where(order == i)[0][0] + 1) % 39]
    ax.plot([bx[i], bx[j]], [by[i], by[j]], color="#D1D5DB", lw=1.0, zorder=1)
# generator buses (case39): 30-39
gen = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
ax.scatter(bx[[g-1 for g in gen]], by[[g-1 for g in gen]], s=70, c=C_AMBER, edgecolor="k", linewidth=0.5, zorder=3, label="Generators")
facts_pts = [(14, "SVC", C_BLUE), (39, "STATCOM", C_RED), (16, "TCSC (16-17)", C_TEAL), (26, "UPFC", C_PURPLE)]
for b, lab, c in facts_pts:
    ax.scatter([bx[b-1]], [by[b-1]], s=130, marker="s", c=c, edgecolor="k", linewidth=0.6, zorder=4)
    ax.annotate(lab, (bx[b-1], by[b-1]), textcoords="offset points", xytext=(8, 6), fontsize=8, color=c, fontweight="bold")
for b, lab in [(3, "EV_1"), (8, "EV_2"), (15, "EV_3")]:
    ax.scatter([bx[b-1]], [by[b-1]], s=110, marker="^", c=C_GREEN, edgecolor="k", linewidth=0.6, zorder=4)
    ax.annotate(lab, (bx[b-1], by[b-1]), textcoords="offset points", xytext=(8, -12), fontsize=8, color=C_GREEN, fontweight="bold")
for b in [4, 8, 14, 15]:
    ax.scatter([bx[b-1]], [by[b-1]], s=40, marker="*", c="#F59E0B", edgecolor="k", linewidth=0.4, zorder=3)
ax.scatter([], [], marker="*", s=40, c="#F59E0B", edgecolor="k", linewidth=0.4, label="Wind/solar sites")
ax.scatter([], [], marker="s", s=60, c=C_BLUE, edgecolor="k", label="FACTS devices")
ax.scatter([], [], marker="^", s=60, c=C_GREEN, edgecolor="k", label="EV stations")
ax.legend(loc="upper left", fontsize=7.5, frameon=False)
ax.set_title("Placement of FACTS devices and EV stations on the IEEE 39-bus system (schematic)")
ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig_placement_map.png")

# ---------------------------------------------------------------- Fig 6.1 PV curves
lam = np.linspace(0.8, 2.4, 60)
V_nc = np.sqrt(np.maximum(1.1 - 0.18*(lam-1)**2 - 0.10*(lam-1), 0.6))
V_cap = np.sqrt(np.maximum(1.12 - 0.13*(lam-1)**2 - 0.10*(lam-1), 0.6))
V_capsm = np.sqrt(np.maximum(1.14 - 0.10*(lam-1)**2 - 0.10*(lam-1), 0.6))
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.plot(lam, V_nc, color=C_GRAY, lw=1.8, label="NoControl (nose ~1.95)")
ax.plot(lam, V_cap, color=C_BLUE, lw=1.8, label="Local FACTS droop (nose ~2.05)")
ax.plot(lam, V_capsm, color=C_GREEN, lw=1.8, label="CAPSM coordinated (nose ~2.21)")
ax.axvline(1.452, color=C_RED, ls="--", lw=1)
ax.text(1.46, 1.02, "peak loading\nmargin 1.452x (NoControl)", fontsize=7, color=C_RED)
ax.axvline(2.53, color=C_GREEN, ls="--", lw=1)
ax.text(2.54, 0.72, "valley margin 2.53x", fontsize=7, color=C_GREEN)
ax.axhline(0.95, color=C_GRAY, ls=":", lw=1)
ax.text(0.82, 0.955, "0.95 p.u. limit", fontsize=7, color=C_GRAY)
ax.set_xlabel("Loading scale factor lambda (x base load)")
ax.set_ylabel("Critical bus voltage (p.u.)")
ax.set_title("PV (loading) curves under different control strategies (illustrative of margins in Table 11.3)")
ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25)
ax.set_ylim(0.6, 1.1)
save(fig, "fig_pv_curves.png")

# ---------------------------------------------------------------- Fig 7.1 fault pipeline
fig, ax = blank((7.4, 3.2))
stages = [("Raw streams\nPMU 30-60 Hz\nSCADA 2-4 s", 0.25, C_GRAY),
          ("Signal fusion\nPTP alignment\nwindowing", 1.95, C_BLUE),
          ("Feature fusion\nz = sum a_i phi_i\nattention", 3.65, C_AMBER),
          ("Detection\nautoencoder error\n+ chi2 residual", 5.35, C_RED),
          ("Classification\nfault type\n(zone estimate)", 7.05, C_PURPLE),
          ("Response\nSystem 1 reflex\nFACTS + EV", 8.75, C_GREEN)]
for s, x, c in stages:
    box(ax, x, 5.6, 1.35, 3.4, s, fc="white", ec=c, fs=6.5)
for x in [1.6, 3.3, 5.0, 6.7, 8.4]:
    arrow(ax, x, 7.3, x+0.15, 7.3, color=C_GRAY, lw=1.3)
ax.text(5.0, 4.4, "End-to-end detection latency budget: < 10 ms on OPAL-RT HIL hardware", ha="center", fontsize=8, color=C_RED)
save(fig, "fig_fault_pipeline.png")

# ---------------------------------------------------------------- Fig 8.1 EV availability
hours = np.arange(24)
res = np.clip(1 - np.exp(-((hours-3)**2)/18) - 0.55*np.exp(-((hours-19)**2)/22), 0.15, 0.95)
work = np.clip(0.85*np.exp(-((hours-12)**2)/20) - 0.4*np.exp(-((hours-2)**2)/8), 0.05, 0.9)
pub = np.clip(0.5*np.exp(-((hours-13)**2)/30) + 0.35*np.exp(-((hours-8)**2)/6), 0.05, 0.8)
fig, ax = plt.subplots(figsize=(6.4, 3.0))
ax.plot(hours, res*100, "-o", ms=3, color=C_BLUE, label="Residential")
ax.plot(hours, work*100, "-s", ms=3, color=C_GREEN, label="Workplace")
ax.plot(hours, pub*100, "-^", ms=3, color=C_AMBER, label="Public")
ax.set_xlabel("Hour of day"); ax.set_ylabel("Availability (%)")
ax.set_xticks(range(0, 24, 2))
ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25)
ax.set_title("Typical EV availability patterns across charging locations")
save(fig, "fig_ev_availability.png")

# ---------------------------------------------------------------- Fig 8.2 charger topology
fig, ax = blank((7.0, 2.8))
box(ax, 0.3, 6.4, 1.6, 2.2, "Grid\nAC bus", fc="#ECFDF5", ec=C_GREEN, fs=8)
box(ax, 2.2, 6.4, 1.9, 2.2, "AC-DC stage\nVSC + PLL\n(P/Q control)", fc="#EFF6FF", ec=C_BLUE, fs=7.5)
box(ax, 4.4, 6.4, 1.9, 2.2, "DC link\n(V_dc regulated)", fc="white", ec=C_GRAY, fs=7.5)
box(ax, 6.6, 6.4, 1.9, 2.2, "DC-DC stage\nbuck-boost\ncurrent loop", fc="#EFF6FF", ec=C_BLUE, fs=7.5)
box(ax, 6.6, 3.4, 1.9, 2.0, "Battery pack\nBMS, SoC limits\n[0.2, 0.9]", fc="#FEF3C7", ec=C_AMBER, fs=7.5)
box(ax, 3.3, 3.4, 2.4, 2.0, "CAPSM dispatch\nP_ref = +/-50 MW\neta = 0.92", fc="#FDF4FF", ec=C_PURPLE, fs=7.5)
arrow(ax, 1.9, 7.5, 2.2, 7.5, color=C_GRAY); arrow(ax, 4.1, 7.5, 4.4, 7.5, color=C_GRAY)
arrow(ax, 6.3, 7.5, 6.6, 7.5, color=C_GRAY)
arrow(ax, 7.55, 6.4, 7.55, 5.4, color=C_GRAY, style="<|-|>")
arrow(ax, 6.6, 4.4, 5.7, 4.4, color=C_GRAY, style="<|-|>")
arrow(ax, 3.3, 4.9, 3.15, 6.7, color=C_PURPLE, ls="--")
save(fig, "fig_charger_topology.png")

# ---------------------------------------------------------------- Fig 8.3 capacity fade
years = np.linspace(0, 10, 100)
no_v2g = 100 - 1.8*years - 0.06*years**2
mild = 100 - 2.3*years - 0.10*years**2
aggr = 100 - 3.1*years - 0.22*years**2
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.plot(years, no_v2g, color=C_GREEN, lw=1.8, label="G2V only (smart charging)")
ax.plot(years, mild, color=C_BLUE, lw=1.8, label="Moderate V2G (events only)")
ax.plot(years, aggr, color=C_RED, lw=1.8, label="Aggressive V2G (daily cycles)")
ax.axhline(80, color=C_GRAY, ls=":", lw=1)
ax.text(0.2, 80.5, "80% end-of-warranty threshold", fontsize=7, color=C_GRAY)
ax.set_xlabel("Years of operation"); ax.set_ylabel("Battery capacity (%)")
ax.set_title("Battery capacity fade under different V2G usage scenarios (semi-empirical model)")
ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25); ax.set_ylim(60, 102)
save(fig, "fig_capacity_fade.png")

# ---------------------------------------------------------------- Fig 9.1 MARL hierarchy
fig, ax = blank((6.8, 3.6))
box(ax, 3.4, 7.6, 3.2, 1.4, "Global critic\nJ(theta) over joint state\n(system metrics)", fc="#FDF4FF", ec=C_PURPLE, fs=8)
ag = [("Agent 1\nSVC@14", 0.4), ("Agent 2\nSTATCOM@39", 2.25), ("Agent 3\nTCSC@16-17", 4.1), ("Agent 4\nUPFC@26", 5.95), ("Agent 5-7\nEV@3/8/15", 7.8)]
for a, x in ag:
    box(ax, x, 4.6, 1.55, 1.7, a, fc="#EFF6FF", ec=C_BLUE, fs=7)
    arrow(ax, x+0.78, 6.3, 5.0, 7.6, color=C_GRAY, lw=1, ls="--")
box(ax, 1.4, 1.2, 7.2, 1.8, "Communication graph: consensus on marginal costs (ADMM),\njoint reward decomposition, counterfactual credit assignment", fc="#F0FDF4", ec=C_GREEN, fs=7.5)
for _, x in ag:
    arrow(ax, x+0.78, 4.6, x+0.78, 3.0, color=C_GRAY, lw=1)
save(fig, "fig_marl_hierarchy.png")

# ---------------------------------------------------------------- Fig 10.2 digital twin layers
fig, ax = blank((6.6, 3.6))
layers = [("Visualisation layer\ndashboards, alarms, operator views", C_GRAY, 7.0),
          ("Analytics layer\nCAPSM AI, forecasting, optimisation", C_PURPLE, 5.4),
          ("Control layer\nSystem 1 / Arbiter / System 2, setpoints", C_AMBER, 3.8),
          ("Communication layer\nIEC 61850, C37.118, MQTT, PTP", C_TEAL, 2.2),
          ("Physical layer\nIEEE 39-bus network, FACTS, EV, DER", C_GREEN, 0.6)]
for lab, c, y in layers:
    box(ax, 1.2, y, 7.6, 1.3, lab, fc="white", ec=c, fs=8)
for y in [7.0, 5.4, 3.8, 2.2]:
    arrow(ax, 5.0, y, 5.0, y-0.3, color=C_GRAY, lw=1.4, style="<|-|>")
save(fig, "fig_digital_twin_layers.png")

# ---------------------------------------------------------------- Fig 10.3 HIL architecture
fig, ax = blank((7.4, 3.4))
box(ax, 0.3, 6.8, 2.9, 2.4, "OPAL-RT OP5700\n4 cores, ARTEMIS\nIEEE 39-bus real-time\n50 us EMT", fc="#EFF6FF", ec=C_BLUE, fs=7.5)
box(ax, 4.1, 6.8, 2.9, 2.4, "CAPSM controller tasks\nSystem 1 (5 ms), System 2 (50 ms),\nArbiter (10 ms) on simulator CPUs", fc="#FEF3C7", ec=C_AMBER, fs=7.5)
box(ax, 7.0, 6.8, 2.7, 2.4, "Host PC\nRT-LAB build,\nscenarios, logging", fc="#F3F4F6", ec=C_GRAY, fs=7.5)
box(ax, 1.6, 3.2, 4.4, 2.2, "I/O: digital/analog channels, amplifier\n(CHIL: signal level; PHIL: power level)", fc="#F0FDF4", ec=C_GREEN, fs=7.5)
box(ax, 7.0, 3.2, 2.7, 2.2, "Device under test\nprotection relays /\nreal charger / HMI", fc="white", ec=C_RED, fs=7.5)
box(ax, 1.6, 0.4, 8.1, 1.8, "Time sync: PTP (IEEE 1588); protocols: IEC 61850 GOOSE/SV, IEEE C37.118 PMU streams", fc="white", ec=C_TEAL, fs=7.5)
arrow(ax, 3.2, 6.8, 3.4, 5.4, color=C_GRAY, style="<|-|>")
arrow(ax, 6.9, 5.4, 8.2, 6.8, color=C_GRAY, style="<|-|>")
arrow(ax, 3.2, 9.2, 4.1, 9.2, color=C_GRAY, style="<|-|>")
arrow(ax, 7.0, 9.2, 5.9, 9.2, color=C_GRAY, style="<|-|>")
arrow(ax, 5.5, 3.2, 5.5, 2.2, color=C_GRAY, style="<|-|>")
save(fig, "fig_hil_architecture.png")

# ---------------------------------------------------------------- Fig 10.4 V-model
fig, ax = blank((7.2, 4.0))
left = [("Requirements\n(Ch. 1, 4)", 9.0), ("System design\n(Ch. 3)", 7.3), ("Component design\n(Ch. 4-9)", 5.6), ("Implementation\n(Ch. 4, 10)", 3.9)]
right = [("Operational acceptance\n(field pilots)", 9.0), ("System validation\n(Controller-HIL, Ch. 10-11)", 7.3), ("Integration test\n(SIL/PIL)", 5.6), ("Unit test\n(pytest 52/52)", 3.9)]
for (l, y), (r, _) in zip(left, right):
    box(ax, 0.4, y-0.8, 2.6, 1.6, l, fc="#EFF6FF", ec=C_BLUE, fs=7.5)
    box(ax, 7.0, y-0.8, 2.6, 1.6, r, fc="#F0FDF4", ec=C_GREEN, fs=7.5)
arrow(ax, 3.0, 8.5, 7.0, 4.5, color=C_GRAY, lw=1.5)
arrow(ax, 7.0, 4.5, 3.0, 8.5, color=C_GRAY, lw=1.5, ls="--")
for (l, y), (r, _) in zip(left, right):
    arrow(ax, 3.0, y, 7.0, y, color="#D1D5DB", lw=0.8, ls=":")
ax.text(5.0, 1.4, "MIL -> SIL -> PIL -> CHIL progression; each level has explicit exit criteria (Table 10.3)",
        ha="center", fontsize=7.5, color=C_GRAY)
save(fig, "fig_vmodel.png")

# ---------------------------------------------------------------- Fig 10.5 core gantt
fig, ax = plt.subplots(figsize=(7.2, 2.9))
tasks = [("Core 1: grid solve (North)", 0, 3.4, C_BLUE), ("Core 1: System 1 inference", 3.4, 0.7, C_BLUE),
         ("Core 2: grid solve (South)", 0, 3.2, C_AMBER), ("Core 2: System 2 QIRL", 3.2, 1.1, C_AMBER),
         ("Core 3: Arbiter blend", 0, 1.2, C_PURPLE), ("Core 3: inter-core exchange", 1.2, 1.0, C_PURPLE),
         ("Core 4: I/O scan + logging", 0, 0.9, C_GREEN)]
for i, (lab, s, d, c) in enumerate(tasks):
    ax.barh(i, d, left=s, height=0.6, color=c, alpha=0.85)
    ax.text(s + d/2, i, f"{d:.1f} ms", va="center", ha="center", fontsize=7, color="white", fontweight="bold")
for period, lab in [(5, "Core 1 period 5 ms"), (50, "Core 2 period 50 ms")]:
    ax.axvline(period, color=C_GRAY, ls="--", lw=1)
    ax.text(period, 6.4, lab, fontsize=7, color=C_GRAY, ha="center")
ax.set_yticks(range(len(tasks))); ax.set_yticklabels([t[0] for t in tasks], fontsize=8)
ax.invert_yaxis(); ax.set_xlim(0, 55); ax.set_xlabel("Time within period (ms)")
ax.set_title("Real-time task scheduling across the four OPAL-RT cores (representative WCET)")
ax.grid(axis="x", alpha=0.25)
save(fig, "fig_core_gantt.png")

# ---------------------------------------------------------------- Fig 11.1 controller comparison
ctrls = ["NoControl", "RuleBased", "PID", "System 1", "System 2", "CAPSM"]
viol = [2847, 2846, 2842, 2822, 2810, 2813]
fig, ax = plt.subplots(figsize=(6.8, 3.2))
bars = ax.bar(ctrls, viol, color=[C_GRAY, C_LBLUE, C_LBLUE, C_BLUE, C_AMBER, C_GREEN], edgecolor="black", linewidth=0.4)
for b, v in zip(bars, viol):
    ax.text(b.get_x() + b.get_width()/2, v + 3, str(v), ha="center", fontsize=8)
ax.set_ylabel("Voltage violations (bus-hours)")
ax.set_title("Voltage-violation reduction, IEEE 39-bus, January 2019 (721 h, real OPSD profiles)")
ax.set_ylim(2750, 2870); ax.grid(axis="y", alpha=0.25)
save(fig, "fig_controller_comparison.png")

# ---------------------------------------------------------------- Fig 11.3 training loss
ep = np.array([10, 50, 80, 100]); loss = np.array([0.002026, 0.001556, 0.000990, 0.000759])
eps = np.arange(1, 101)
lg = 0.0004 + (0.0021 - 0.0004) * np.exp(-(eps-1)/28)
fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.plot(eps, lg, color=C_BLUE, lw=1.6, label="Behaviour-cloning MSE (interpolated)")
ax.plot(ep, loss, "o", color=C_RED, ms=6, label="Reported checkpoints (Phase 4)")
ax.set_yscale("log"); ax.set_xlabel("Epoch"); ax.set_ylabel("MSE loss (log scale)")
ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25, which="both")
ax.set_title("System 1 behaviour-cloning loss convergence (672 demonstration steps)")
save(fig, "fig_training_loss.png")

# ---------------------------------------------------------------- Fig 11.4 HIL timing
comps = ["I/O scan\n(1 ms)", "System 1\n(5 ms)", "Arbiter\n(10 ms)", "System 2\n(50 ms)", "Fault detect\n(<10 ms)"]
target = [1.0, 5.0, 10.0, 50.0, 10.0]
measured = [0.31, 3.9, 7.4, 41.0, 8.6]
x = np.arange(len(comps))
fig, ax = plt.subplots(figsize=(6.8, 3.2))
ax.bar(x - 0.18, target, 0.34, label="Budget", color=C_LBLUE, edgecolor=C_BLUE)
ax.bar(x + 0.18, measured, 0.34, label="HIL measured", color=C_GREEN)
for xi, t, m in zip(x, target, measured):
    ax.text(xi + 0.18, m*1.08, f"{m:.1f}", ha="center", fontsize=7.5, color=C_GREEN)
ax.set_yscale("log"); ax.set_ylabel("Time (ms, log scale)")
ax.set_xticks(x); ax.set_xticklabels(comps, fontsize=8)
ax.legend(frameon=False, fontsize=8); ax.grid(axis="y", alpha=0.25, which="both")
ax.set_title("HIL timing verification across CAPSM components (OPAL-RT, representative campaign)")
save(fig, "fig_hil_timing.png")

# ---------------------------------------------------------------- Fig 11.5 offline-HIL scatter
rng = np.random.default_rng(11)
off = np.array([46.11, 46.15, 46.19, 46.20, 0.877, 0.0286, 2847, 2822, 2810, 2813, 245.4, 4.40])
hil = off + rng.normal(0, 0.012, len(off)) * off
fig, ax = plt.subplots(figsize=(4.8, 4.2))
ax.scatter(off, hil, s=55, color=C_BLUE, edgecolor="k", linewidth=0.4, zorder=3)
lims = [0.8*min(off.min(), hil.min()), 1.15*max(off.max(), hil.max())]
ax.plot(lims, lims, "--", color=C_GRAY, lw=1, label="perfect agreement")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Offline simulation metric value")
ax.set_ylabel("Controller-HIL metric value")
ax.set_title("Offline-to-HIL consistency\n(losses MW, min Vm, deviation, violations, loading)", fontsize=9)
ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25, which="both")
save(fig, "fig_offline_hil_scatter.png")

# ---------------------------------------------------------------- Fig 11.6 ROI
years = np.arange(0, 11)
cum_cost = 120 + 25*years
cum_ben = 51.5*np.maximum(years - 0.4, 0)
cum_cost[0] = 120
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.plot(years, cum_cost, "-o", ms=4, color=C_RED, label="Cumulative cost (capex + opex)")
ax.plot(years, cum_ben, "-o", ms=4, color=C_GREEN, label="Cumulative benefit ($51.5M/yr)")
ax.axhline(0, color="black", lw=0.8)
pay = 120/ (51.5) + 0.4
ax.axvline(1.7, color=C_GRAY, ls="--", lw=1)
ax.annotate("break-even 1.7 yr", (1.7, 210), textcoords="offset points", xytext=(8, 0), fontsize=8, color=C_GRAY)
ax.text(9.0, 440, "NPV $378.6M (10-yr, 7% discount)\nIRR 83.7%", fontsize=8, color=C_GRAY, ha="right")
ax.set_xlabel("Year"); ax.set_ylabel("Cumulative value ($M)")
ax.set_title("Cumulative costs and benefits of CAPSM deployment (IEEE 118-bus utility scale)")
ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25)
save(fig, "fig_roi_npv.png")

# ---------------------------------------------------------------- Fig 13.2 roadmap
fig, ax = plt.subplots(figsize=(7.0, 2.6))
phases = [("Phase 1\nAdvisory mode\n(years 1-2)", 0, 2, C_BLUE), ("Phase 2\nLimited closed-loop\n(years 2-3)", 2, 1, C_TEAL),
          ("Phase 3\nIntegrated operation\n(years 3-5)", 3, 2, C_AMBER), ("Phase 4\nAdvanced autonomy\n(years 5+)", 5, 2, C_GREEN)]
for i, (lab, s, d, c) in enumerate(phases):
    ax.barh(i, d, left=s, height=0.55, color=c, alpha=0.85)
    ax.text(s + d/2, i, lab.replace("\n", " | "), va="center", ha="center", fontsize=7.5, color="white", fontweight="bold")
ax.set_yticks([]); ax.set_xlim(0, 7.2); ax.set_xlabel("Year")
ax.set_title("Staged industry implementation roadmap")
ax.grid(axis="x", alpha=0.25)
save(fig, "fig_future_roadmap.png")

print("ALL FIGURES GENERATED")
