# MASTER PROMPT: Write the Complete CAPSM PhD Thesis, 15-Page Presentation, and 80-Minute Podcast

---

## INSTRUCTIONS FOR THE AI

You are tasked with writing the **complete PhD thesis** for Mahmoud Kiasari at Dalhousie University, based on the CAPSM (Cognitive Adaptive Power System Management) framework. This document gives you **everything** you need: full chapter content, figure/table specifications, a 15-page presentation, and an 80-minute podcast script. Follow every section below precisely. Output in Word (.docx) for chapters and Markdown (.md) for presentation and podcast.

### THESIS TITLE
**"Cognitive Adaptive Power System Management (CAPSM): A Brain-Inspired Dual-Process AI Framework for Coordinated Control of FACTS Devices, EV Fleets, and DERs — Validated Through Controller-Hardware-in-the-Loop Testing on a 4-Core OPAL-RT Real-Time Simulator"**

### AUTHOR
Mahmoud Kiasari, PhD Candidate, Department of Electrical and Computer Engineering, Dalhousie University, Halifax, Nova Scotia, Canada.

### OUTPUT REQUIREMENTS
- **Thesis chapters:** Word (.docx), Times New Roman 12pt, heading styles, figure captions, table captions, reference list
- **Presentation:** Markdown (.md), 15 pages of slides
- **Podcast:** Markdown (.md), 80-minute script
- Use **British/Canadian spelling** (colour, organisation, analyse, behaviour, modelling)
- **No em-dashes** (use en-dash – or "to" ranges). No emojis. No "delves into" / "robust" / "leveraging" / AI slop.
- Every figure must have a number and caption (e.g., "Figure 3.1: ...")
- Every table must have a number and caption (e.g., "Table 5.1: ...")
- Cross-reference figures and tables in text (e.g., "as shown in Figure 4.2 ...")

---

## 1. PROJECT CONTEXT (READ THIS FIRST)

### 1.1 What CAPSM Is
CAPSM is a **brain-inspired dual-process AI control architecture** for modern power systems. It maps human cognitive theory (Kahneman's System 1 / System 2) onto grid control:
- **System 1 (Reflexive):** CNN-LSTM neural network for sub-5ms protection responses. Detects faults, instability, oscillations from PMU data. Acts via FACTS devices and inverter-based resources.
- **System 2 (Deliberative):** Quantum-Inspired Reinforcement Learning (QIRL) for 50ms-second optimization. Uses complex-valued probability amplitudes, superposition, tunneling to escape local optima. Handles economic dispatch, V2G scheduling, coordinated control.
- **Metacognitive Arbiter:** Executive layer that decides which system controls the grid at each moment, based on confidence, novelty, urgency, cyber-risk. Modes: SYSTEM_1_REFLEX, SYSTEM_2_PLANNING, SYSTEM_2_OVERRIDE, SAFE_MODE, BLENDED.
- **Physics-Informed Neural Networks (PINNs):** AC power flow equations embedded in the training loss, ensuring every control action respects Kirchhoff's laws and operational limits. Target: >99.8% constraint compliance.

### 1.2 Validation Pipeline (THREE STAGES)
1. **Stage 1 - Offline Python Simulation:** PYPOWER (Python port of MATPOWER) with Quasi-Static Time Series (QSTS) loop. Open Power System Data (OPSD) Germany 2015-2020 time-series for realistic load/renewable profiles. OpenAI Gym-like interface (reset/step/close). IEEE 9/14/39/118/300 bus systems. Trains System 1 (CNN-LSTM) and System 2 (QIRL), runs scenarios (faults, renewable intermittency, cyber-attacks FDI).
2. **Stage 2 - Simulink Model Preparation:** Acquired IEEE 39-bus Simulink model from DESL-EPFL GitHub (OPAL-RT eMegaSim native). Added FACTS device subsystems (SVC at Bus 14, STATCOM at Bus 39, TCSC on Line 16-17, UPFC at Bus 26) and EV V2G chargers (3 stations at Buses 3, 8, 15). Configured for RT-LAB/ARTEMIS solver.
3. **Stage 3 - Controller-HIL on 4-Core OPAL-RT:** IEEE grid model runs in real-time (50us EMT time step) on OPAL-RT. CAPSM System 1 and System 2 execute as real-time software tasks on the simulator CPUs. Metacognitive Arbiter coordinates. Core allocation: Core1=North+System1, Core2=South+System2, Core3=Arbitration+Comms, Core4=I/O. No separate controller board — CAPSM runs ON the OPAL-RT itself.

### 1.3 Key Results to Cite
- 37% reduction in response time to critical events (System 1)
- 42% enhancement in stability metrics during extreme events
- 32.7% reduction in voltage deviation
- 24.3% decrease in system losses
- 42.5% reduction in renewable curtailment
- 28% increase in DER utilisation efficiency
- 95.8% accuracy in fault detection and localization
- 74% reduction in false positives vs conventional methods
- 99.97% constraint compliance via PINNs (3130 violations → 11 in 10,000 cycles)
- 61.4% faster response vs best traditional method (rule-based)
- 20-33% improvement in critical clearing time (transient stability)
- 28.5% loading margin increase (voltage stability)
- 12.4% annual operational cost savings ($51.5M/year on IEEE 118-bus)
- 1.7-year ROI payback, 83.7% IRR, $378.6M NPV (10-year)
- QIRL converges ~58-59% faster than DQN across all optimization problems
- 96.8% transient stability prediction accuracy (PINNs vs 84.2% data-driven)
- 73% reduction in data requirements via physics-informed approach
- Sub-10ms fault detection time on HIL hardware
- 4-core OPAL-RT validates real-time feasibility (50us EMT, 86.7% parallel efficiency at 16 nodes)

### 1.4 IEEE Test Systems
| System | Buses | Generators | Branches | Use |
|---|---|---|---|---|
| IEEE 9-bus | 9 | 3 | 9 | Debug/development (HIL) |
| IEEE 14-bus | 14 | 5 | 20 | Voltage stability tests |
| IEEE 39-bus | 39 | 10 | 46 | **Primary HIL system** |
| IEEE 118-bus | 118 | 54 | 186 | Scalability (multi-core) |
| IEEE 300-bus | 300 | 69 | 411 | Offline only (phasor) |

### 1.5 Core Allocation (4-CPU OPAL-RT)
| Core | Name | Region | Component | Task Time | Priority |
|---|---|---|---|---|---|
| Core 1 | sm_master | North (Buses 1-19) | System 1 CNN-LSTM | 5 ms | 1 (highest - protection) |
| Core 2 | sm_slave1 | South (Buses 20-39) | System 2 QIRL | 50 ms | 2 (medium) |
| Core 3 | sm_slave2 | Global | Metacognitive Arbiter + Comms | 10 ms | 3 (coordination) |
| Core 4 | sm_slave3 | I/O | HIL Interface + Logging | 1 ms | 4 (lowest) |

### 1.6 Software/Hardware Stack
| Layer | Tool | Purpose |
|---|---|---|---|
| Offline simulation | PYPOWER, PyTorch, NumPy, Pandas | QSTS power flow, AI training |
| Simulink models | MATLAB/Simulink, Simscape Electrical, ARTEMIS | IEEE grid models, FACTS, EV |
| Real-time solver | OPAL-RT RT-LAB, ARTEMIS, eFPGASIM, ePHASORSIM | 50us EMT, 1ms phasor |
| Communication | IEC 61850, IEEE C37.118, PTP (IEEE 1588) | Substation, PMU, system-level |
| Data | OPSD Germany 2015-2020 | Real-world load/renewable profiles |
| AI frameworks | PyTorch (offline), TensorFlow/PyTorch (HIL) | CNN-LSTM, QIRL |

### 1.7 FACTS Device Placement (IEEE 39-bus)
| Device | Type | Location | Function |
|---|---|---|---|
| FACTS_1 | SVC | Bus 14 | Voltage support (shunt) |
| FACTS_2 | STATCOM | Bus 39 | Fast voltage support (shunt) |
| FACTS_3 | TCSC | Line 16-17 | Power flow control (series) |
| FACTS_4 | UPFC | Bus 26 | Combined voltage + power flow |

### 1.8 EV V2G Fleet (IEEE 39-bus)
| Fleet | Bus | Power (kW) | Capacity (kWh) | Mode |
|---|---|---|---|---|
| EV_1 | 3 | 19.2 | 40 | V2G/G2V |
| EV_2 | 8 | 19.2 | 40 | V2G/G2V |
| EV_3 | 15 | 19.2 | 40 | V2G/G2V |

---

## 2. COMPLETE CHAPTER-WRITING INSTRUCTIONS

Write each chapter as a Word (.docx) file. Each chapter must be **15-25 pages** (except Ch1 at 10-12 and Ch13 at 8-10). Use the structure and content guidance below. Expand technical detail fully — this is a PhD thesis, not a summary.

### CHAPTER 1: Introduction (10-12 pages)
**Structure:**
1.1 Background on Power System Challenges in the Renewable Energy Era — global energy transformation, IEA statistics (60% capacity increase 2020-2026, 4800 GW), key challenges (intermitency, reduced inertia, bidirectional flows, complexity, cybersecurity, market/regulatory)
1.2 Evolution of FACTS Devices — EPRI 1980s, shunt (SVC/STATCOM), series (TCSC), combined (UPFC), role in renewable integration
1.3 Integration of EVs into Smart Grids (V2G/G2V) — G2V, V2G, V2H, V2X, bidirectional charger requirements, mathematical modelling of EV fleets
1.4 Research Motivation — DER integration trends (132.4 GW → 528.4 GW by 2026, 16.7% CAGR), resilience, technical/economic/environmental imperatives, socio-technical transformation
1.5 Problem Statement — 5 critical control gaps:
   - Gap 1: Inadequate control architectures for heterogeneous systems
   - Gap 2: Limited real-time decision-making under uncertainty
   - Gap 3: Insufficient coordination between FACTS and DERs
   - Gap 4: Insufficient fault detection/localisation in resource-rich environments
   - Gap 5: Integration barriers between theory and practice **(HIL validation is the bridge)**
1.6 Research Objectives — 5 objectives with measurable goals (include the exact metrics from Section1.3 above). Objective 5 must specify the three-stage HIL pipeline.
1.7 Original Contributions — 9 contributions. Contribution 8 is **HIL Validation Methodology on 4-Core OPAL-RT** (explicit, not implicit). Contribution 7 is Digital Twin Methodology.
1.8 Thesis Organization — one paragraph per chapter, highlighting the HIL additions

**Figures required:**
- Figure 1.1: Global renewable energy capacity growth (2010-2023) — **bar chart**, x-axis=year, y-axis=GW, show solar/wind/hydro separately. Caption: "Figure 1.1: Global renewable energy capacity growth (2010-2023)"
- Figure 1.2: Traditional vs modern power system control challenges — **side-by-side diagram**, left=centralized unidirectional, right=distributed bidirectional. Caption: "Figure 1.2: Traditional versus modern power system control challenges"
- Figure 1.3: Research gap identification framework — **flowchart** with 5 gaps as branches leading to CAPSM solutions. Caption: "Figure 1.3: Research gap identification framework"
- Figure 1.4: Overview of proposed AI-driven CAPSM framework — **system architecture diagram** showing System1/System2/Metacognitive/FACTS/EV/DER. Caption: "Figure 1.4: Overview of the proposed AI-driven CAPSM framework"
- Figure 1.5: Three-stage validation pipeline — **block diagram**, Stage1 (Python/PYPOWER) → Stage2 (Simulink) → Stage3 (OPAL-RT HIL). Caption: "Figure 1.5: Three-stage validation pipeline from offline simulation to Controller-HIL"

**Tables required:**
- Table 1.1: Key challenges in modern power systems with high DER penetration — columns: Challenge, Description, Impact. Caption: "Table 1.1: Key challenges in modern power systems with high DER penetration"
- Table 1.2: Comparison of conventional and AI-based control approaches — columns: Aspect, Conventional, AI-Based, Advantage. Caption: "Table 1.2: Comparison of conventional and AI-based control approaches"
- Table 1.3: Research objectives and success metrics — columns: Objective, Measurable Goal, Target Metric. Caption: "Table 1.3: Research objectives and success metrics"

---

### CHAPTER 2: Literature Review (18-22 pages)
**Structure:**
2.1 Evolution of AI Applications in Power Systems — chronological from 1980s expert systems to 2020s deep reinforcement learning. Include key references: Hsu et al. (1990) DELTA expert system, Sobajic & Pao (1989) ANN dynamic security, Tomsovic (1992) fuzzy LP, Glavic et al. (2017) RL survey.
2.2 FACTS Devices and Their Applications — Hingorani (1988, 1993), SVC/STATCOM/TCSC/UPFC evolution, Zhang et al. (2006) STATCOM model, Del Rosso et al. (2003) TCSC, Fujita et al. (1999) UPFC. Comparison table of FACTS characteristics.
2.3 AI Approaches for Decision-Making in Power Grids — DRL (Wang et al. 2020, Hossain et al. 2022), Safe RL (Zhao et al. 2023, Yu et al. 2024), MPC (Ernst et al. 2008), PINNs (Raissi et al. 2019, Kody et al. 2021). Discuss limitations of each.
2.4 EV and V2G/G2V Architectures — Kempton & Tomic (2005) V2G fundamentals, Sortomme & El-Sharkawi (2010) optimal scheduling, Hu et al. (2016) fleet management review, Thompson & Kempton (2021) degradation, Monteiro et al. (2015) modes.
2.5 Brain-Inspired AI Frameworks — Kahneman (2011) Thinking Fast and Slow, Wang & Laird (2019) dual mechanisms, Chen et al. (2021) dual-process for power systems, Liu & Wang (2021) dual-process microgrids, Picard (2000) Affective Computing, Chen & Liu (2022) artificial emotional intelligence, Zhang et al. (2021) risk-sensitive RL. Include Table 2.4 comparing conventional vs brain-inspired AI.
2.6 Assessment of Existing Technologies for DER Integration — Samad et al. (2016) centralized, Liang et al. (2020) hierarchical, Molzahn et al. (2017) distributed, Morstyn et al. (2018) P2P, Kok et al. (2005) PowerMatcher, Widergren et al. (2014) TEC framework. Include Table 2.5 assessing integration approaches for different DER types.
2.7 Gap Analysis and Motivation for Hybrid Frameworks — synthesize 5 gap categories (technical, methodological, implementation). Motivation for hybrid: complementary strengths, multi-timescale, balanced exploration-exploitation, robustness, transitional implementation.
2.8 **[NEW SECTION] Real-Time Simulation and HIL Validation in Power Systems** — review OPAL-RT platforms (eMEGASIM/ePHASORSIM/eFPGASIM), CHIL vs PHIL distinction, Speedgoat Simulink Real-Time, RTDS, cite the EPHCC consortium (GitHub PowerSystemsHIL/EPHCC), Golestan et al. (2024) Energies review of ePHASORSIM advances, DESL-EPFL (2018) IEEE 39-bus model. **This section must argue that most AI power system papers never validate on real-time hardware — this is the literature gap CAPSM fills.**

**Figures required:**
- Figure 2.1: Evolution of AI applications in power systems (1980-present) — **timeline**, x-axis=decade, y-axis=milestone type (expert/NN/fuzzy/EA/RL/DRL/transformer). Caption: "Figure 2.1: Evolution of AI applications in power systems (1980-present)"
- Figure 2.2: Classification of FACTS devices — **tree diagram**, root=FACTS, branches=shunt (SVC/STATCOM)/series (TCSC/SSSC)/combined (UPFC/IPFC). Caption: "Figure 2.2: Classification of FACTS devices and their operating principles"
- Figure 2.3: EV charging technologies and V2G/G2V architectures — **block diagram** showing G2V/V2G/V2H/V2X modes and bidirectional charger. Caption: "Figure 2.3: EV charging technologies and V2G/G2V architectures"
- Figure 2.4: Brain-inspired dual-process AI architecture — **layered diagram**, System1 (amygdala) / System2 (prefrontal cortex) / Metacognitive. Caption: "Figure 2.4: Brain-inspired dual-process AI architecture"
- Figure 2.5: Comparative analysis of brain-inspired vs conventional AI — **radar chart**, axes=features (processing/response/adaptability/uncertainty/efficiency/knowledge), two overlaid polygons. Caption: "Figure 2.5: Comparative analysis of brain-inspired versus conventional AI approaches"
- Figure 2.6: Communication and control architectures for DER integration — **hierarchy diagram**, centralized/hierarchical/distributed/P2P/transactive. Caption: "Figure 2.6: Communication and control architectures for DER integration"

**Tables required:**
- Table 2.1: Chronological evolution of AI techniques in power systems — columns: Era, Key Development, Representative Application, Limitation. Caption: "Table 2.1: Chronological evolution of AI techniques in power systems"
- Table 2.2: Comparison of FACTS devices characteristics and applications — columns: Device, Type, Key Feature, Typical Application, Response Time. Caption: "Table 2.2: Comparison of FACTS devices characteristics and applications"
- Table 2.3: EV fleet charging/discharging characteristics — columns: Parameter, G2V Mode, V2G Mode, V2H Mode. Caption: "Table 2.3: EV fleet charging and discharging characteristics"
- Table 2.4: Comparative analysis of brain-inspired vs conventional AI — columns: Feature, Conventional AI, Brain-Inspired AI, Relevance. Caption: "Table 2.4: Comparative analysis of brain-inspired approaches against traditional AI methods"
- Table 2.5: Assessment of integration approaches for different DER types — columns: DER Type, Key Characteristics, Most Effective Approaches, Remaining Challenges. Caption: "Table 2.5: Assessment of integration approaches for different DER types"

**References:** ~90 references. Use IEEE format. Include the new HIL references (OPAL-RT, ePHASORSIM, DESL-EPFL, EPHCC, Golestan 2024 Energies review, MathWorks webinar, Chakraborty 2018).

---

### CHAPTER 3: Proposed Framework (15-20 pages)
**Structure:**
3.1 Framework Overview and Design Philosophy — CAPSM framework, 3 principles (cognitive duality, hierarchical coordination, adaptive learning). Address the 5 gaps from Ch1.
3.2 Brain-Inspired Dual-Process Control Architecture — System1 (CNN-LSTM, eq u1=f_CNN-LSTM(x,theta_1)), System2 (QIRL, eq u2=argmin...), Metacognitive (eq u=alpha*u1+(1-alpha)*u2, alpha=sigmoid(C1-tau)). **Write out the key equations with proper mathematical notation.**
3.3 Multi-Layer Coordination Architecture — 3-tier (device/regional/system), information flow (5 steps), multi-rate control scheme.
3.4 Mathematical Modeling of Integrated Components — FACTS (dx_F/dt=f(x_F,u_F,V_b)), EV fleet (dSoC/dt=...), DER (P_DER=f(...)), integrated power flow (P_i=V_i*sum...). **Write all equations.**
3.5 Quantum-Inspired Reinforcement Learning — state representation (|psi>=sum alpha_s|s>), Q-value approximation, exploration strategy (P(a|s)=|<phi_a|U|psi>|^2), multi-objective formulation. **Write all equations.**
3.6 Multi-Modal Fault Detection and Localization — data sources (PMU/SCADA/relays/smart meters/weather), 3-level fusion (signal/feature/decision), feature fusion equation (z=sum alpha_i*phi_i(x_i)), deep learning for classification.
3.7 Coordinated Control Strategies — control objectives (voltage/congestion/loss/frequency/renewable/resilience), temporal coordination framework (fast/medium/slow timescales), spatial coordination, ancillary service provision (Table 3.1).
3.8 Practical Implementation Considerations — computational architecture (central/fog/edge/cloud), communication infrastructure (IEC 61850/C37.118/MQTT), EMS/DMS integration, scalability.
3.9 Summary and Transition — key contributions list, transition to Ch4 (implementation) and Ch10 (HIL methodology).
3.10 **[NEW SECTION] HIL-Ready Architecture Design** — specify how System1/System2 map onto real-time hardware. OPAL-RT deployment topology (OP5700 simulator ↔ Ethernet ↔ CAPSM software tasks). I/O interface definition. Real-time constraint formulation (tau_1 < 5ms, tau_2 < 50ms with HIL latency budget). **Include a figure showing the OPAL-RT topology.**

**Figures required:**
- Figure 3.1: High-level CAPSM architecture — **system architecture diagram**, System1/System2/Metacognitive/FACTS/EV/DER layers. Caption: "Figure 3.1: High-level architecture of the CAPSM framework"
- Figure 3.2: Hierarchical control structure — **3-tier pyramid**, device/regional/system levels with bidirectional arrows. Caption: "Figure 3.2: Hierarchical control structure in the CAPSM framework"
- Figure 3.3: Temporal coordination framework — **Gantt chart**, x-axis=time, y-axis=asset type, bars for fast/medium/slow. Caption: "Figure 3.3: Temporal coordination framework showing engagement of assets across timescales"
- Figure 3.4: Quantum-inspired state representation — **Bloch sphere diagram** showing |psi>, basis states, amplitudes. Caption: "Figure 3.4: Quantum-inspired state representation"
- Figure 3.5: Multi-modal data fusion architecture — **3-layer flow**, signal/feature/decision fusion with attention weights. Caption: "Figure 3.5: Multi-modal data fusion architecture"
- Figure 3.6: Ancillary service provision capabilities — **heatmap**, rows=services, columns=FACTS/EV/DER, colour=capability rating. Caption: "Figure 3.6: Ancillary service provision capabilities"
- Figure 3.7: **[NEW]** OPAL-RT deployment topology — **network diagram**, 4 cores with assigned subsystems, I/O interfaces, communication links. Caption: "Figure 3.7: OPAL-RT 4-core deployment topology for Controller-HIL"
- Figure 3.8: **[NEW]** Real-time constraint budget — **timing diagram**, x-axis=control layer, y-axis=time budget (5ms/50ms/10ms/1ms), horizontal lines at deadlines. Caption: "Figure 3.8: Real-time constraint budget across CAPSM control layers"

**Tables required:**
- Table 3.1: Ancillary service provision capabilities — columns: Service, FACTS, EV Fleets, DERs, Rating. Caption: "Table 3.1: Ancillary service provision capabilities"

---

### CHAPTER 4: Advanced AI Control Architecture (18-22 pages)
**Structure:**
4.1 System Design Specifications and Requirements — Table 4.1 mapping requirements to gaps. Table 4.2 hardware/software specs (OPAL-RT OP5700, ARTEMIS, eFPGASIM, IEC 61850, etc.). Table 4.3 performance metrics with target values.
4.2 Development of Brain-Inspired AI Framework — System1 (Algorithm 4.1: CNN-LSTM architecture, write pseudocode), System2 (Algorithm 4.2: QIRL, write pseudocode), Arbitration (Algorithm 4.3). **Include the full algorithms as pseudocode blocks.** Write the CNN-LSTM forward equations (C_t=Pool(...), LSTM gates, attention, FC). Write the quantum state |psi>=(1/sqrt(Z))*sum sqrt(exp(beta*Q))*|s,a>. Write the arbitration weights W1, W2.
4.3 Multi-Layer Control Hierarchy Implementation — device-level (FACTS PID, EV SoC control equations), regional coordination (Algorithm 4.7: ADMM), system-wide optimization. **Include the ADMM algorithm pseudocode.**
4.4 Data Flow Architecture — data acquisition pipeline (Algorithm 4.8), state estimation (minimize sum w_i(z_i-h_i(x))^2), situational awareness, decision support, command execution, feedback. **Write Algorithm 4.8 and 4.9 (online learning) and 4.10 (adaptive tuning) as pseudocode.**
4.5 Real-Time Adaptation Mechanisms — online learning (theta_{t+1}=theta_t+alpha*grad_L), transfer learning (min L_T+lambda*Omega), performance monitoring, adaptive tuning (Algorithm 4.10). **Include all four algorithms as pseudocode.**
4.6 Validation Framework and Methodology — multi-layer validation (component/subsystem/full-system/HIL/field), test scenarios (Table 4.5), test systems (Table 4.6), performance assessment categories.
4.7 **[NEW SECTION] Computational Implementation for Real-Time Deployment** — System1 on FPGA (eFPGASIM for sub-ms inference), System2 as multi-threaded RT task on CPU, Metacognitive coordination interface. Code-to-hardware traceability table mapping each algorithm to its deployment target. **Include this table.**
4.8 Conclusion — summarize implementation, transition to Ch5.

**Figures required:**
- Figure 4.1: CAPSM system architecture — **hierarchy diagram** (cloud/fog/edge) with physical power system at bottom. Caption: "Figure 4.1: CAPSM system architecture"
- Figure 4.2: Artificial Amygdala architecture — **flow diagram**, raw inputs → feature extraction → pattern recognition → urgency assessment → response triggering. Caption: "Figure 4.2: Architecture of the Artificial Amygdala"
- Figure 4.3: Enhanced TD3 architecture — **block diagram**, actor/twin critics/target networks/replay buffer/PINN. Caption: "Figure 4.3: Enhanced TD3 architecture for power system control"
- Figure 4.4: APFC planning and optimization — **flowchart** showing MPC + QIRL loop with quantum state update. Caption: "Figure 4.4: APFC planning and optimisation flow"
- Figure 4.5: Adaptive exploration rate — **line plot**, x-axis=training step, y-axis=exploration sigma, showing decay and adaptation. Caption: "Figure 4.5: Adaptive exploration rate in different operating regions"
- Figure 4.6: **[NEW]** Code-to-hardware traceability — **mapping table** as a figure, left=algorithm, right=hardware target (FPGA/CPU/edge/cloud). Caption: "Figure 4.6: Code-to-hardware traceability for CAPSM real-time deployment"
- Figure 4.7: **[NEW]** Real-time task scheduling — **Gantt chart**, x-axis=time, y-axis=core (1-4), coloured bars for tasks with deadlines. Caption: "Figure 4.7: Real-time task scheduling across 4 OPAL-RT cores"

**Tables required:**
- Table 4.1: System design requirements — columns: Dimension, Requirements, Gap Addressed. Caption: "Table 4.1: System design requirements and gap mapping"
- Table 4.2: Implementation specifications — columns: Component, Specification, Justification. Caption: "Table 4.2: Implementation specifications"
- Table 4.3: Performance metrics — columns: Category, Metric, Target Value, Measurement Method. Caption: "Table 4.3: Key performance indicators"
- Table 4.4: Critical event classification — columns: Event Category, Specific Events, Detection Features. Caption: "Table 4.4: Critical event classification for Artificial Amygdala"
- Table 4.5: Test scenarios — columns: Scenario Category, Specific Scenarios, Test Objectives. Caption: "Table 4.5: Key test scenarios"
- Table 4.6: Test systems — columns: Test System, Description, Key Characteristics. Caption: "Table 4.6: Test systems used for validation"
- Table 4.7: **[NEW]** Code-to-hardware traceability — columns: Algorithm, Deployment Target, Hardware, Timescale, Priority. Caption: "Table 4.7: Code-to-hardware traceability for real-time deployment"

---

### CHAPTER 5: AI-Based Optimal Placement and Parameter Tuning (15-20 pages)
**Structure:**
5.1 Optimization Problem Formulation — general form (min F(x,y,z)=[f1,...,fm]), 5 objective functions (power loss, voltage stability, investment cost, load balancing, carbon emissions) with equations, constraints (power flow, operational, FACTS, EV, DER), decision variables, complexity analysis (Table 5.1).
5.2 Genetic Algorithm Based Placement — chromosome representation, Algorithm 5.1 (multi-segment crossover), Algorithm 5.2 (adaptive mutation), fitness function, diversity maintenance, convergence criteria.
5.3 Particle Swarm Optimization Based Tuning — particle representation, velocity/position update rules, swarm intelligence (cognitive/social adaptation), multi-swarm (Algorithm 5.3), sensitivity analysis (Algorithm 5.4).
5.4 Deep Reinforcement Learning Controller Design — state/action space formulation, reward function (R=w1*R_stability+w2*R_efficiency+w3*R_economics+w4*R_emissions-sum lambda_i*P_i), TD3 architecture, training methodology (Algorithm 5.5: safety-constrained TD3), exploration-exploitation balance.
5.5 Quantum-Enhanced RL for Optimal Power Flow — quantum state representation (amplitude/angle encoding), quantum operators (QFT/Grover/quantum walks), Algorithm 5.6 (hybrid quantum-classical), implementation considerations (Table 5.2 resource requirements), performance comparison (Table 5.3: classical DRL vs QERL).
5.6 Transfer Learning for Cross-Domain Knowledge — graph-based representation learning, domain adaptation (feature alignment/adversarial/meta-learning), Algorithm 5.7 (pre-training and fine-tuning), generalisation assessment (Table 5.4).
5.7 Chapter Summary — 6 key contributions list.
5.8 **[NEW SECTION] HIL-Validated Placement Results** — offline-to-HIL consistency check: placements determined in Python/PYPOWER validated in real-time on OPAL-RT Simulink. Catch modelling errors. Confirm optimal placements work in both environments.

**Figures required:**
- Figure 5.1: GA-based FACTS placement algorithm flowchart — **flowchart**, chromosome encoding → genetic operations → diversity → convergence. Caption: "Figure 5.1: GA-based FACTS placement algorithm"
- Figure 5.2: Multi-swarm PSO architecture — **diagram** showing multiple swarms with local/global balance. Caption: "Figure 5.2: Multi-swarm PSO architecture for parameter tuning"
- Figure 5.3: Enhanced TD3 architecture — **block diagram**, actor/twin critics/targets/replay/PINN. Caption: "Figure 5.3: Enhanced TD3 architecture"
- Figure 5.4: Adaptive exploration strategy — **line plot**, x-axis=step, y-axis=exploration rate, showing decay + system-criticality adaptation. Caption: "Figure 5.4: Adaptive exploration rate"
- Figure 5.5: Classical vs quantum-enhanced RL comparison — **grouped bar chart**, x-axis=test case, y-axis=performance metric, 3 bars (DRL/QERL-sim/QERL-hardware). Caption: "Figure 5.5: Performance comparison between classical and quantum-enhanced methods"
- Figure 5.6: Knowledge transfer between topologies — **network diagram** showing feature space alignment. Caption: "Figure 5.6: Knowledge transfer between power system topologies"
- Figure 5.7: **[NEW]** Offline-to-HIL placement consistency — **side-by-side bar chart**, left=Python/PYPOWER placement, right=OPAL-RT HIL placement, showing matching results. Caption: "Figure 5.7: Offline-to-HIL placement consistency validation"

**Tables required:**
- Table 5.1: Problem complexity factors — columns: System Size, Decision Variables, Constraints, Solution Space, Computational Challenge. Caption: "Table 5.1: Comparison of problem complexity factors"
- Table 5.2: Quantum resource requirements — columns: System Size, Logical Qubits, Circuit Depth, Quantum Ops, Pre/Post-Processing. Caption: "Table 5.2: Quantum resource requirements"
- Table 5.3: Classical vs quantum-enhanced comparison — columns: Metric, Classical DRL, QERL (Simulator), QERL (Hardware), Improvement. Caption: "Table 5.3: Performance comparison"
- Table 5.4: Transfer learning performance — columns: Domain Shift, Performance Ratio, Adaptation Speed, Transfer Efficiency. Caption: "Table 5.4: Transfer learning performance across domain shifts"

---

### CHAPTER 6: Stability Enhancement Using Deep Learning (12-15 pages)
**NOTE:** Chapter6 folder contains Genspark HTML research files (60+ cached web pages). These are research notes, NOT the chapter itself. Write the chapter based on the outline below and the technical content from other chapters.
**Structure:**
6.1 Transient Stability Assessment Approaches — review CCT as primary metric, CNN-LSTM for real-time assessment, SVM/DT alternatives, physics-informed approaches. Reference Moulin et al. (2004) SVM, Diao et al. (2009) DT, Kody et al. (2021) PINNs.
6.2 CNN-LSTM Architecture for Real-Time Stability Assessment — spatial (CNN) + temporal (LSTM) feature extraction, attention mechanism, early warning system, model pruning for edge deployment. Architecture diagram.
6.3 Voltage Stability Enhancement Techniques — continuation power flow (CPF), PV curves, optimal reactive power coordination, FACTS + EV + DER coordinated voltage support.
6.4 Custom ML Models for Grid Stability — hybrid models, transfer learning for cross-system generalisation, uncertainty quantification.
6.5 Generative AI Applications for Control Signal Creation — GANs for synthetic fault scenario generation, diffusion models for control signal generation, LLMs for control strategy recommendation.
6.6 **[NEW]** Integration with CAPSM System1 — how the CNN-LSTM stability model deploys as the System1 reflexive layer, inference pipeline from PMU data → CNN-LSTM → stability assessment → preventive action dispatch. **Include the deployment diagram.**

**Figures required:**
- Figure 6.1: CNN-LSTM architecture for stability assessment — **layered neural network diagram**, input (PMU multi-channel) → CNN (spatial) → LSTM (temporal) → attention → output (stability index). Caption: "Figure 6.1: CNN-LSTM architecture for real-time stability assessment"
- Figure 6.2: PV curves for voltage stability — **line plot**, x-axis=loading (MW), y-axis=voltage (p.u.), multiple curves for different control strategies. Caption: "Figure 6.2: PV curves for critical bus under different control strategies"
- Figure 6.3: **[NEW]** System1 stability deployment pipeline — **data flow diagram**, PMU → preprocessing → CNN-LSTM inference → stability index → action dispatch, with timing annotations. Caption: "Figure 6.3: System1 stability assessment deployment pipeline"

**Tables required:**
- Table 6.1: Performance metrics for stability assessment models — columns: Model, Accuracy, Inference Time, Data Requirement, Generalisation. Caption: "Table 6.1: Performance metrics for stability assessment models"

---

### CHAPTER 7: Fault Detection and Localization (15-20 pages)
**Structure:**
7.1 AI-based Fault Localization Approaches — evolution table (Table 7.1), deep learning architectures (CNN/LSTM/Transformer/GNN).
7.2 Multi-Modal Data Fusion Architecture — 3-level fusion (signal/feature/decision) with equations, information theoretic analysis (mutual information gain), attention mechanism.
7.3 Anomaly Detection Methods — Isolation Forest (anomaly score equation), Deep Autoencoders (reconstruction loss equation), EVT (GPD), One-Class SVM (optimisation problem).
7.4 Classification Algorithms for Fault Type Identification — CNN-LSTM hybrid (Algorithm in section 7.4.1), feature importance (Table 7.2), transfer learning for generalization (domain adaptation equation).
7.5 Response Time Optimization Techniques — model compression (85% reduction), algorithm optimisation, hardware acceleration, distributed vs centralized (Table 7.4), edge computing (Figure 7.3), response time guarantees.
7.6 **[NEW SECTION] HIL Validation of Fault Detection** — inject real faults on OPAL-RT (three-phase short circuit via Ybus mod, line trips via branch status), measure detection latency on CAPSM controller running as RT software task. Compare offline vs HIL detection time. **This is a key results section.**

**Figures required:**
- Figure 7.1: Multi-architecture approach — **flow diagram**, input data sources → signal processing → CNN/LSTM feature extraction → attention fusion → fault analysis (type + location). Caption: "Figure 7.1: Multi-architecture approach for fault detection and localization"
- Figure 7.2: Integration of anomaly detection methods — **flow diagram**, normal profile → ensemble (Isolation Forest/Autoencoder/EVT/OCSVM) → anomaly score → threshold → trigger. Caption: "Figure 7.2: Integration of anomaly detection in CAPSM"
- Figure 7.3: Hierarchical edge-cloud architecture — **network diagram**, cloud (training/advanced analytics) → regional (coordination) → edge (real-time detection/classification) → field sensors. Caption: "Figure 7.3: Hierarchical edge-cloud architecture"
- Figure 7.4: **[NEW]** Offline vs HIL fault detection comparison — **grouped bar chart**, x-axis=metric (accuracy/false positive/detection time), y-axis=method, 3 bars (conventional/single-modal ML/CAPSM HIL). Caption: "Figure 7.4: Offline versus Controller-HIL fault detection performance"
- Figure 7.5: **[NEW]** HIL fault injection and response — **time-series plot**, x-axis=time (s), y-axis=voltage (p.u.) and frequency (Hz), showing fault onset, detection, and recovery on HIL. Caption: "Figure 7.5: HIL fault injection and response timeline"

**Tables required:**
- Table 7.1: Fault localization method comparison — columns: Approach, Method, Accuracy, Computational Complexity, Adaptability. Caption: "Table 7.1: Comparison of traditional and AI-based fault localization methods"
- Table 7.2: Top features for fault classification — columns: Rank, Feature, Importance Score, Description. Caption: "Table 7.2: Top five features for fault classification by importance"
- Table 7.3: Fault classification performance — columns: Test System, Accuracy, Avg Precision, Avg Recall, Avg F1, Latency (ms). Caption: "Table 7.3: Fault classification performance across IEEE test systems"
- Table 7.4: Processing architecture comparison — columns: Criteria, Centralized, Distributed, Hybrid. Caption: "Table 7.4: Comparison of processing architectures"
- Table 7.5: **[NEW]** Offline vs HIL fault detection comparison — columns: Metric, Conventional, Single-Modal ML, CAPSM HIL, Improvement. Caption: "Table 7.5: Offline versus Controller-HIL fault detection comparison"

---

### CHAPTER 8: EV Integration and DER Management (15-20 pages)
**Structure:**
8.1 EV Fleet Modeling Approaches — aggregate vs individual, stochastic availability (non-homogeneous Poisson), battery degradation (semi-empirical capacity fade), SoC dynamics, charging behavior analysis (Table 8.1: 4 clusters).
8.2 Bidirectional Power Flow Management (V2G/G2V) — technologies/standards, power electronics (efficiency equations), V2G/G2V transition control (Algorithm 8.1: mode transition), economic optimization (cost-benefit equation), battery degradation impact.
8.3 Coordinated V2G/G2V Frequency Regulation Strategies — primary/secondary/tertiary control (droop equation, AGC equation), aggregator-based coordination (mixed-integer optimisation), real-time response (RNN prediction), communication requirements (Table 8.3), market integration (two-stage stochastic).
8.4 Load Forecasting with Uncertainty Quantification — deep learning (TCN-Transformer, composite loss), ensemble methods (dynamic weighting), probabilistic forecasting (quantile regression, pinball loss), uncertainty propagation (stochastic/robust optimisation).
8.5 DER Coordination Strategies — hierarchical control (tertiary optimisation), multi-agent (ADMM, consensus equation), market-based (double-sided auction), grid service provision (Table 8.5), stability considerations (synthetic inertia, small-signal), resilience (adaptive islanding equation).
8.6 Summary — key contributions.
8.7 **[NEW SECTION] HIL Validation of V2G Coordination** — EV V2G models integrated with IEEE 39-bus, coordinated charging/discharging verified on 4-core OPAL-RT. OPSD charging profiles. Real-time V2G frequency regulation. **Key results section.**

**Figures required:**
- Figure 8.1: EV availability patterns — **multi-line plot**, x-axis=hour of day, y-axis=availability (%), 3 lines (residential/workplace/public). Caption: "Figure 8.1: Typical EV availability patterns across charging locations"
- Figure 8.2: Bidirectional charger topology — **circuit diagram** showing DC-DC + DC-AC stages with control loops. Caption: "Figure 8.2: Bidirectional charger topology"
- Figure 8.3: Battery capacity fade — **line plot**, x-axis=years, y-axis=capacity (%), multiple curves for different V2G usage scenarios. Caption: "Figure 8.3: Battery capacity fade under different V2G scenarios"
- Figure 8.4: EV fleet response characteristics — **grouped bar chart**, x-axis=characteristic (latency/ramp/precision), y-axis=fleet size. Caption: "Figure 8.4: EV fleet response characteristics for frequency regulation"
- Figure 8.5: V2G implementation case studies — **table-as-figure**, 3 case studies with key indicators. Caption: "Figure 8.5: Case studies of V2G implementation scenarios"
- Figure 8.6: **[NEW]** HIL V2G coordination validation — **time-series plot**, x-axis=time (s), y-axis=power (MW), showing V2G/G2V mode transitions and frequency response on HIL. Caption: "Figure 8.6: HIL validation of coordinated V2G frequency regulation"

**Tables required:**
- Table 8.1: EV charging behavior clusters — columns: Cluster, Charging Pattern, Time of Day, Duration, Price Sensitivity, Flexibility. Caption: "Table 8.1: EV charging behavior clusters"
- Table 8.2: V2G implementation case studies — columns: System, Configuration, Key Indicators, Challenges, Lessons. Caption: "Table 8.2: Case studies of V2G implementation scenarios"
- Table 8.3: Communication requirements — columns: Service Type, Max Latency (ms), Update Rate (Hz), Reliability (%), Bandwidth/Vehicle (kbps), Architecture. Caption: "Table 8.3: Communication requirements for EV-based frequency control"
- Table 8.4: Communication requirements — (same as above if separate, or merge)
- Table 8.5: Grid service provision capabilities — columns: Service, Solar PV, Wind, EV Fleets, Battery Storage, Flexible Loads, Key Metrics. Caption: "Table 8.5: Grid service provision capabilities of different DER types"

---

### CHAPTER 9: Coordinated Control Using Hybrid AI (12-15 pages)
**NOTE:** Chapter9 folder contains Genspark HTML research files. Write the chapter from the outline below.
**Structure:**
9.1 Hierarchical Multi-Agent Reinforcement Learning — multi-agent RL framework, agent coordination, convergence guarantees.
9.2 Coordinated Control of FACTS and EVs — combined FACTS + EV dispatch, response characteristics, model predictive control for anticipation.
9.3 Integration of DERs within the Control Framework — DER coordination, multi-timescale integration.
9.4 Adaptive Control Strategies for Dynamic Conditions — adaptation to renewable variability, load changes, topology reconfiguration.
9.5 Balancing Multiple Control Objectives — multi-objective optimisation, Pareto efficiency, conflict resolution.
9.6 **[NEW]** HIL Validation of Coordinated Control — validate FACTS + EV coordinated control on 4-core OPAL-RT under the renewable intermittency and EV V2G scenarios from Ch10.

**Figures required:**
- Figure 9.1: Hierarchical MARL architecture — **layered diagram**, local/regional/global agents with communication graph. Caption: "Figure 9.1: Hierarchical multi-agent reinforcement learning architecture"
- Figure 9.2: Coordinated FACTS + EV control — **block diagram** showing dispatch logic. Caption: "Figure 9.2: Coordinated control of FACTS and EVs"
- Figure 9.3: **[NEW]** HIL coordinated control validation — **multi-panel time-series**, x-axis=time, showing frequency/voltage/power under coordinated vs independent control on HIL. Caption: "Figure 9.3: HIL validation of coordinated control under renewable intermittency"

---

### CHAPTER 10: Testing and Validation Framework (25-35 pages) **[CORE CHAPTER - 3x EXPANSION]**
**This is the HIL centerpiece. Write it at 3x the length of the current chapter.**
**Structure:**
10.1 Three-Stage Validation Methodology — Stage1 (Python/PYPOWER + OPSD), Stage2 (Simulink model prep), Stage3 (Controller-HIL on 4-core OPAL-RT). Exit criteria between stages. **Include the pipeline diagram.**
10.2 Simulation Platform Development — PYPOWER QSTS, MATPOWER/Simulink, Simscape Electrical (FACTS EMT models), NS-3 (communication), PyTorch (AI). Integration middleware (time sync, data exchange, event recording, fault injection, scenario management, performance monitoring).
10.3 Digital Twin Creation Methodology — layered architecture (physical/communication/control/analytics/visualisation), 4 fidelity levels (functional/behavioural/detailed/high-precision), data sync (state estimation equation), calibration (Algorithm 10.2), applications (controller tuning, what-if, failure mode, operator training, progressive deployment).
10.4 Hardware-in-the-Loop Testing Architecture — OPAL-RT OP5700/OP4510 (50us EMT, 1ms phasor), 4-core allocation (Core1=North+System1, Core2=South+System2, Core3=Arbitration+Comms, Core4=I/O), communication (IEC 61850/C37.118/MQTT, PTP sync), I/O interface (electrical/signal/time sync/interface compensation equation), **write the interface compensation transfer function**.
10.5 Real-Time Task Scheduling — rate-monotonic analysis (worst-case response time equation), Algorithm 10.3 (scheduling), timing validation, deadline-aware resource allocation.
10.6 Scenario Design for HIL — 5 scenarios (normal/fault/renewable/cyber/EV), each with duration, injection parameters, metrics. **Include the full scenario table.**
10.7 Progressive Validation: MIL to SIL to PIL to CHIL — V-model, 5 stages with exit criteria. Algorithm 10.4 (progressive validation). **Include pseudocode.**
10.8 Automated Regression Testing — test automation, CI, version control, results database, regression analysis.
10.9 Comprehensive Validation Metrics and Reporting — 4-level metric hierarchy (technical/functional/operational/business), cross-platform comparison, uncertainty quantification, visualisation tools, structured reporting.
10.10 Summary — key contributions list.
10.11 **[NEW]** OPAL-RT HIL Setup and Configuration — physical setup (simulator/host PC/I/O boards/amplifier/sensors), software configuration (RT-LAB/ARTEMIS/eFPGASIM/ePHASORSIM), model loading and subsystem splitting procedure, build and deployment steps, calibration and timing verification. **This is a practical "how-to" section.**

**Figures required (12+ figures):**
- Figure 10.1: Integrated simulation platform — **architecture diagram**, power system sim + comm sim + AI framework, with middleware. Caption: "Figure 10.1: Integrated simulation platform architecture"
- Figure 10.2: Digital twin layered architecture — **layered diagram**, physical → communication → control → analytics → visualisation. Caption: "Figure 10.2: Digital twin layered architecture"
- Figure 10.3: Digital twin fidelity levels — **table-as-diagram**, 4 levels with descriptions and applications. Caption: "Figure 10.3: Digital twin fidelity levels"
- Figure 10.4: Data synchronization — **block diagram**, physical → acquisition → estimation → calibration → alignment, with equation. Caption: "Figure 10.4: Data synchronization between physical and digital systems"
- Figure 10.5: HIL system architecture — **system diagram**, OPAL-RT + power amplifier + DUT + I/O + sensors, for CHIL configuration. Caption: "Figure 10.5: Controller-HIL system architecture"
- Figure 10.6: Interface compensation — **block diagram** showing V_amp = G_comp * V_sim with feedback. Caption: "Figure 10.6: Interface between physical components and simulated grid"
- Figure 10.7: Real-time task scheduling — **Gantt chart**, cores 1-4, tasks with periods and deadlines. Caption: "Figure 10.7: Real-time task scheduling across 4 OPAL-RT cores"
- Figure 10.8: V-model progressive validation — **V-diagram**, left=development phases, right=validation activities. Caption: "Figure 10.8: V-model of progressive validation process"
- Figure 10.9: **[NEW]** OPAL-RT physical setup — **photograph-style diagram** showing simulator, host PC, I/O boards, amplifier, connections. Caption: "Figure 10.9: OPAL-RT physical setup for Controller-HIL"
- Figure 10.10: **[NEW]** RT-LAB software configuration — **screenshot-style diagram** showing RT-LAB GUI with subsystem assignment, solver settings, communication config. Caption: "Figure 10.10: RT-LAB software configuration for CAPSM deployment"
- Figure 10.11: **[NEW]** Model splitting and core assignment — **flow diagram** showing IEEE 39-bus model → subsystem decomposition → 4-core assignment → build → deploy. Caption: "Figure 10.11: Model splitting and core assignment procedure"
- Figure 10.12: **[NEW]** HIL timing verification — **timing diagram**, x-axis=control layer, y-axis=measured time, showing deadlines vs actuals. Caption: "Figure 10.12: HIL timing verification across CAPSM control layers"

**Tables required (8+ tables):**
- Table 10.1: Implementation control hierarchy — columns: Level, Update Frequency, Key Responsibilities. Caption: "Table 10.1: Implementation control hierarchy"
- Table 10.2: Digital twin fidelity levels — columns: Level, Description, Application. Caption: "Table 10.2: Digital twin fidelity levels"
- Table 10.3: HIL system configurations — columns: Configuration, Hardware Components, Testing Focus. Caption: "Table 10.3: Controller-HIL system configurations"
- Table 10.4: Interface specifications — columns: Interface Type, Bandwidth, Latency, Precision, Protocol. Caption: "Table 10.4: Interface specifications"
- Table 10.5: HIL test scenarios — columns: Scenario, Duration, Injection, Metrics. Caption: "Table 10.5: HIL test scenarios" **(populate fully)**
- Table 10.6: Test systems — columns: System, Buses, Generators, FACTS, EVs, Use. Caption: "Table 10.6: Test systems for HIL validation"
- Table 10.7: **[NEW]** OPAL-RT build and deployment steps — columns: Step, Action, Tool, Output, Verification. Caption: "Table 10.7: OPAL-RT build and deployment procedure"
- Table 10.8: **[NEW]** HIL timing verification results — columns: Component, Target Time, Measured Time, Margin, Status. Caption: "Table 10.8: HIL timing verification results"

---

### CHAPTER 11: Results and Performance Analysis (20-25 pages)
**Split into TWO parts:**
**Structure:**
**Part A: Offline Python Simulation Results (11.1-11.4)**
11.1 Benchmarking Against Traditional Control Methods — methodology, test scenarios, Table 11.1 with all metrics. Statistical significance (paired t-tests, p < 0.01).
11.2 Performance Analysis Across Multiple IEEE Bus Systems — Table 11.2 (normalized to 9-bus), topology impact analysis.
11.3 Stability Analysis Under Varying Conditions — transient (Table 11.3: CCT improvement), voltage (PV curves, loading margin), small-signal (Table 11.4: damping ratios at 0-60% renewable).
11.4 Fault Detection and Response Performance — Table 11.5 (10,000 fault cases), localization error distribution, high-impedance fault detection.

**Part B: Controller-HIL Results (11.5-11.10) [NEW]**
11.5 HIL Setup Verification and Timing Validation — 4-core allocation, ARTEMIS solver, timing budget verification, Table 11.7.
11.6 Real-Time Fault Detection Performance — inject faults on OPAL-RT, measure detection latency on CAPSM controller, Table 11.8 comparing offline vs HIL. **Key result: sub-10ms detection achieved on hardware.**
11.7 Real-Time Stability Enhancement — FACTS coordination under 50us EMT, Table 11.3 results replicated on HIL, transient stability on real-time.
11.8 Real-Time V2G Frequency Regulation — EV fleet coordinated charging/discharging on HIL, Table 11.9 with response characteristics.
11.9 Cyber-Attack Resilience on HIL — FDI injection, Safe Mode activation, Table 11.10 with detection rates and recovery times. **Key result: Safe Mode demonstrated on hardware.**
11.10 Offline-to-HIL Consistency Analysis — quantified simulation-to-reality gap, Table 11.11 comparing offline Python vs HIL metrics. **Critical contribution: proves HIL validation catches issues invisible in simulation.**
11.11 Summary and Conclusions — 8 key findings.

**Figures required:**
- Figure 11.1: Frequency response comparison — **time-series plot**, x-axis=time (s), y-axis=frequency (Hz), 4 curves (PID/rule-based/MPC/CAPSM). Caption: "Figure 11.1: Frequency response comparison during combined contingency"
- Figure 11.2: Performance vs system size — **line plot**, x-axis=system size (buses), y-axis=normalized performance, 5 metrics. Caption: "Figure 11.2: Performance metrics as a function of system size"
- Figure 11.3: PV curves for voltage stability — **line plot**, x-axis=loading, y-axis=voltage, 4 control strategies. Caption: "Figure 11.3: PV curves for critical bus under different control strategies"
- Figure 11.4: Fault localization error distribution — **histogram**, x-axis=error (%), y-axis=frequency, 3 distributions. Caption: "Figure 11.4: Distribution of fault localization errors"
- Figure 11.5: **[NEW]** HIL timing verification — **bar chart**, x-axis=component, y-axis=time (ms), target vs measured, showing margins. Caption: "Figure 11.5: HIL timing verification across CAPSM components"
- Figure 11.6: **[NEW]** Offline vs HIL fault detection — **grouped bar chart**, x-axis=metric, y-axis=method, 3 bars. Caption: "Figure 11.6: Offline versus Controller-HIL fault detection performance"
- Figure 11.7: **[NEW]** HIL fault response timeline — **time-series plot**, x-axis=time, y-axis=voltage + frequency, showing fault onset/detection/recovery on HIL. Caption: "Figure 11.7: HIL fault injection and response timeline"
- Figure 11.8: **[NEW]** HIL V2G frequency regulation — **time-series plot**, x-axis=time, y-axis=power (MW), showing V2G/G2V transitions and grid response. Caption: "Figure 11.8: HIL validation of coordinated V2G frequency regulation"
- Figure 11.9: **[NEW]** HIL cyber-attack resilience — **time-series plot**, x-axis=time, y-axis=voltage, showing FDI injection, detection, Safe Mode activation, recovery. Caption: "Figure 11.9: HIL cyber-attack resilience validation"
- Figure 11.10: **[NEW]** Offline-to-HIL consistency — **scatter plot**, x-axis=offline metric, y-axis=HIL metric, diagonal=perfect agreement, points=actual. Caption: "Figure 11.10: Offline-to-HIL consistency analysis"
- Figure 11.11: ROI analysis — **cumulative line plot**, x-axis=years, y-axis=cumulative cost/benefit, break-even at 1.7 years. Caption: "Figure 11.11: Cumulative costs and benefits of implementing CAPSM"

**Tables required:**
- Table 11.1: Control method comparison — columns: Metric, Traditional PID, Rule-Based, MPC, CAPSM, Improvement. Caption: "Table 11.1: Comparison of control methods across key performance metrics"
- Table 11.2: Performance across IEEE systems — columns: System, Voltage Stability, Frequency Regulation, Congestion Reduction, Response Time, Computation Time. Caption: "Table 11.2: Performance metrics across different IEEE test systems"
- Table 11.3: CCT improvement — columns: Fault Location, No Control, Conventional PSS, Conventional FACTS, CAPSM, Improvement. Caption: "Table 11.3: Critical clearing time improvement"
- Table 11.4: Damping ratio vs renewable — columns: Renewable, No Control, PSS, FACTS, CAPSM. Caption: "Table 11.4: Damping ratio of critical modes under renewable penetration"
- Table 11.5: Fault detection comparison — columns: Metric, Conventional, Single-Modal ML, CAPSM. Caption: "Table 11.5: Fault detection performance comparison"
- Table 11.6: Execution time — columns: Component, IEEE 9, IEEE 39, IEEE 118, IEEE 300. Caption: "Table 11.6: Execution time for different framework components (milliseconds)"
- Table 11.7: Convergence speed — columns: Problem, Conventional Q-Learning, DQN, QIRL, Improvement. Caption: "Table 11.7: Convergence speed comparison"
- Table 11.8: **[NEW]** Offline vs HIL fault detection — columns: Metric, Offline, HIL, Change. Caption: "Table 11.8: Offline versus Controller-HIL fault detection comparison"
- Table 11.9: **[NEW]** HIL V2G response characteristics — columns: Characteristic, HIL Result, Target, Status. Caption: "Table 11.9: HIL V2G fleet response characteristics"
- Table 11.10: **[NEW]** Cyber-physical resilience — columns: Scenario, Detection Rate, Recovery Time, Stability Maintained. Caption: "Table 11.10: Cyber-physical resilience under HIL testing"
- Table 11.11: **[NEW]** Offline-to-HIL consistency — columns: Metric, Offline Value, HIL Value, Gap, Agreement. Caption: "Table 11.11: Offline-to-HIL consistency analysis"
- Table 11.12: Annual operational cost — columns: Cost Component, Traditional, CAPSM, Savings, Percentage. Caption: "Table 11.12: Annual operational cost comparison"

---

### CHAPTER 12: Discussion and Implications (10-12 pages)
**Structure:**
12.1 Analysis of Control System Limitations — computational complexity in very large systems, communication dependency, sensor sensitivity, integration challenges.
12.2 Regulatory and Policy Implications — grid code alignment, certification pathways for AI controllers, responsibility/liability frameworks.
12.3 Implementation Challenges and Solutions — legacy integration, phased deployment, operator trust-building.
12.4 Ethical Considerations — AI decision-making in critical infrastructure, data privacy, algorithmic bias, accountability.
12.5 Comparison with State-of-the-Art Approaches — position CAPSM relative to MPC, DRL, Safe RL, PINN, MARL, transactive energy. **Include a comparison table.**
12.6 **[NEW]** Implications of HIL Validation for Industry Adoption — HIL results de-risk deployment, build operator confidence, accelerate certification, inform regulatory frameworks. **Argue that HIL validation is what makes CAPSM industry-ready.**

**Tables required:**
- Table 12.1: CAPSM vs state-of-the-art — columns: Feature, CAPSM, MPC, DRL, Safe RL, PINN, MARL, Transactive. Caption: "Table 12.1: Comparative analysis of CAPSM with state-of-the-art approaches"

---

### CHAPTER 13: Conclusions and Future Work (8-10 pages)
**Structure:**
13.1 Summary of Key Findings — dual-process (37% response, 18% efficiency), hierarchical MARL (94% convergence, 82% conflict reduction), PINNs (96.8% stability, 73% data reduction), multi-modal fault detection (68% localisation, 43% detection time), EV/DER coordination (64% voltage, 27% cost), **Controller-HIL (sub-10ms fault detection, 50us EMT, 4-core validated)**.
13.2 Review of Contributions — 9 contributions. **Contribution 8 (HIL Validation Methodology) is now explicit and elevated.** Include Table 13.1.
13.3 Acknowledgment of Research Limitations — validation (HIL limited to selected components), test systems, EV/DER models, computational, communication, implementation, regulatory. Table 13.2.
13.4 Future Research Directions — short-term (enhanced PINNs, robust MARL, uncertainty quantification, comprehensive HIL), medium-term (neuro-symbolic, multi-energy, human-AI, market-integrated), long-term (quantum computing, self-designing, cognitive digital twins, autonomous communities).
13.5 Industry Application Roadmap — Phase 1 (Years 1-2, advisory), Phase 2 (Years 2-3, limited closed-loop), Phase 3 (Years 3-5, integrated), Phase 4 (Years 5+, advanced). Include TRL assessment (Table 13.3).
13.6 Concluding Remarks — CAPSM bridges theoretical AI to practical power engineering via Controller-HIL. The journey toward truly intelligent power systems has begun.

**Figures required:**
- Figure 13.1: CAPSM framework summary — **overview diagram** of all components and interactions. Caption: "Figure 13.1: Comprehensive overview of the CAPSM framework"
- Figure 13.2: Future research directions — **concept map**, organised by time horizon (short/medium/long) and research domain. Caption: "Figure 13.2: Conceptual map of future research directions"
- Figure 13.3: Industry implementation timeline — **Gantt chart**, x-axis=year, y-axis=phase, bars for 4 phases with milestones. Caption: "Figure 13.3: Timeline for staged implementation of CAPSM"

**Tables required:**
- Table 13.1: Research contributions — columns: Category, Contribution, Significance. Caption: "Table 13.1: Summary of research contributions"
- Table 13.2: Limitations and mitigations — columns: Limitation, Category, Specific Limitation, Potential Mitigation. Caption: "Table 13.2: Research limitations and mitigation strategies"
- Table 13.3: Technology readiness assessment — columns: Component, TRL, Key Development Needs. Caption: "Table 13.3: Technology readiness assessment of CAPSM components"

---

## 3. PRESENTATION SLIDES (15 pages, Markdown .md)

Write a **15-page presentation** in Markdown (.md) that could be delivered as a PhD defence or conference presentation. Each "page" = 1 slide. Use `---` as slide separators.

### SLIDE STRUCTURE (15 slides total)

**Slide 1: Title Slide**
- Title: "Cognitive Adaptive Power System Management: A Brain-Inspired Dual-Process AI Framework"
- Subtitle: "Validated Through Controller-Hardware-in-the-Loop Testing on a 4-Core OPAL-RT Real-Time Simulator"
- Author: Mahmoud Kiasari
- Affiliation: Dalhousie University, Department of Electrical and Computer Engineering
- Date: 2026

**Slide 2: Motivation - The Energy Transition**
- Global energy transformation: renewable capacity +60% (2020-2026), 4800 GW
- 5 key challenges: intermittency, reduced inertia, bidirectional flows, complexity, cybersecurity
- **Visual:** Bullet list with 5 challenge icons. Caption: "The 5 challenges driving the need for AI-driven grid control"

**Slide 3: Research Gaps**
- Gap 1: Inadequate control architectures
- Gap 2: Limited real-time decision-making under uncertainty
- Gap 3: Insufficient FACTS-DER coordination
- Gap 4: Insufficient fault detection in DER-rich grids
- Gap 5: Theory-to-practice gap **(HIL validation is the bridge)**
- **Visual:** 5-gap flowchart. Caption: "Five critical research gaps in modern power system control"

**Slide 4: CAPSM Concept**
- Brain-inspired dual-process: System 1 (fast/reflexive) + System 2 (slow/deliberative)
- Metacognitive arbitration: confidence × novelty × urgency × cyber-risk
- Physics-informed: PINNs embed Kirchhoff's laws in learning
- **Visual:** CAPSM architecture diagram (System1/System2/Metacognitive). Caption: "CAPSM brain-inspired dual-process architecture"

**Slide 5: System 1 - CNN-LSTM**
- CNN: spatial patterns from PMU bus data
- LSTM: temporal dynamics (oscillations, fault signatures)
- Attention: weights time steps by relevance
- PINN safety filter: enforces 0.94 < V < 1.06
- **Target:** <5 ms inference
- **Visual:** CNN-LSTM layered diagram. Caption: "System 1 CNN-LSTM architecture for reflexive grid protection"

**Slide 6: System 2 - QIRL**
- Quantum-inspired: complex amplitudes (superposition)
- Tunneling: escape local optima
- 58-59% faster convergence than DQN
- Multi-objective: stability + efficiency + cost + emissions
- **Target:** <50 ms optimisation
- **Visual:** Bloch sphere with amplitudes. Caption: "System 2 quantum-inspired reinforcement learning"

**Slide 7: Three-Stage Validation Pipeline**
- Stage 1: Offline Python (PYPOWER + OPSD data)
- Stage2: Simulink model preparation (FACTS + EV integration)
- Stage3: **Controller-HIL on 4-core OPAL-RT**
- **Visual:** 3-stage pipeline flow (Python → Simulink → OPAL-RT). Caption: "Three-stage validation pipeline from simulation to real-time hardware"

**Slide 8: HIL Setup - 4-Core OPAL-RT**
- Core 1: North region + System 1 (5 ms, highest priority)
- Core 2: South region + System 2 (50 ms, medium)
- Core 3: Arbitration + Communication (10 ms)
- Core 4: I/O + Logging (1 ms)
- **Visual:** 4-core allocation Gantt chart. Caption: "4-core OPAL-RT allocation for Controller-HIL"

**Slide 9: IEEE Test Systems**
- 9-bus: debug/development
- 14-bus: voltage stability
- 39-bus: **primary HIL system**
- 118-bus: scalabilities (multi-core)
- 300-bus: offline (phasor)
- **Visual:** Table of 5 systems with single-line diagrams. Caption: "IEEE test systems for CAPSM validation"

**Slide 10: Key Results - Stability**
- 37% voltage stability improvement
- 20-33% critical clearing time increase
- 28.5% loading margin increase
- 60.4% damping improvement at 60% renewable
- **Visual:** Bar chart of stability improvements. Caption: "Stability enhancement results across metrics"

**Slide 11: Key Results - Fault Detection**
- 95.8% detection accuracy
- 9.7 ms detection time (offline), **sub-10 ms on HIL**
- 1.73% localisation error
- 74% false positive reduction
- 96.2% high-impedance fault detection
- **Visual:** Bar chart of fault detection improvements. Caption: "Fault detection and localisation performance"

**Slide 12: Key Results - Economics**
- 12.4% annual cost savings ($51.5M)
- 1.7-year payback, 83.7% IRR
- 42.5% renewable curtailment reduction
- 28% DER utilisation increase
- **Visual:** Cumulative ROI line chart with break-even. Caption: "Economic impact and return on investment"

**Slide 13: HIL Validation Results**
- Sub-10 ms fault detection on real-time hardware
- 50 us EMT time step validated
- Safe Mode activated under FDI on HIL
- V2G frequency regulation verified on 4-core
- Offline-to-HIL gap quantified (catches simulation-invisible issues)
- **Visual:** Side-by-side comparison table offline vs HIL. Caption: "Controller-HIL validation reveals real-time constraints invisible in simulation"

**Slide 14: Contributions**
- C1: Unified mathematical framework
- C2: Brain-inspired dual-process architecture
- C3: Quantum-inspired RL
- C4: CNN-LSTM for real-time stability
- C5: Multi-modal fault detection
- C6: Coordinated FACTS/EV control
- C7: Digital twin methodology
- **C8: HIL validation methodology on 4-core OPAL-RT**
- C9: Transferable knowledge representation
- **Visual:** 9 numbered contribution cards. Caption: "Nine original contributions of the CAPSM framework"

**Slide 15: Conclusions and Future Work**
- CAPSM bridges theoretical AI to practical power engineering
- HIL validation is the key differentiator
- Future: neuro-symbolic AI, multi-energy, quantum computing, cognitive digital twins
- Industry roadmap: 4 phases over 8+ years
- **Visual:** Summary with future directions concept map. Caption: "Conclusions and roadmap for industry application"

---

## 4. PODCAST SCRIPT (80 minutes, Markdown .md)

Write an **80-minute podcast script** in Markdown (.md) for an episode titled "Brain-Inspired AI for the Grid: From Cognitive Theory to Real-Time Hardware Validation."

### PODCAST FORMAT
- Two hosts: **Host A** (expert/researcher voice) and **Host B** (curious learner/questioner voice)
- Aim for a conversational, accessible tone — not a lecture. Think "Radiolab" or "AI Alignment" style.
- Each segment includes: estimated duration, host dialogue, key points to hit, transition notes.
- Include natural pauses, [LAUGHS], [PAUSE], sound-effect notes like [UPBEAT MUSIC].
- Total runtime: **80 minutes** (clearly time-stamped).

### PODCAST STRUCTURE (80 minutes total)

**[0:00 - 2:30] Cold Open + Intro**

*Host B:* So when you say "brain-inspired AI for the grid"... what does that actually mean?

*Host A:* It means we stopped trying to make computers think like computers, and started making them think like **us**. Two systems. One fast, one slow. Like your brain.

*Host B:* And this actually works? For a power grid?

*Host A:* That is exactly what we are about to get into. Welcome to "Brain-Inspired AI for the Grid." I'm your host, [Host A name], and with me is [Host B name]...

*Host B:* ...and over the next 80 minutes we're going to trace this idea from a cognitive theory in a psychology textbook all the way to hardware-in-the-loop validation on a real-time simulator. It is a wild ride.

[UPBEAT MUSIC, FADE]

---

**[2:30 - 8:00] Segment 1: The Problem - Why Grids Need Brains**

*Host A:* Let's start with the problem. The grid is changing. Renewables doubled in a decade. By 2026, we're looking at 4,800 GW of renewable capacity globally.

*Host B:* That is a lot of solar panels.

*Host A:* It is also a lot of **chaos**. Solar drops when a cloud passes. Wind drops when the wind stops. Traditional grids were built for steady, centralised generation. Now generation is distributed, variable, and flows both ways.

*Host B:* So the old control systems...

*Host A:* ...are overwhelmed. There are 5 critical gaps. [PAUSE] First: the control architectures can't scale to thousands of heterogeneous resources. Second: decision-making under uncertainty is too slow. Third: FACTS devices and DERs are controlled independently, missing synergies. Fourth: fault detection struggles with bidirectional flows. And fifth - [PAUSE] - the big one. **Theory never makes it to practice.** Most AI grid control papers stay in simulation. Never validated on real-time hardware.

*Host B:* And that is the gap this thesis fills?

*Host A:* Exactly. Controller-Hardware-in-the-loop. HIL. On an OPAL-RT real-time simulator. That is the bridge.

*Host B:* Okay, I'm sold on the problem. But how does the brain thing work?

[TRANSITION MUSIC]

---

**[8:00 - 18:00] Segment 2: The Idea - Dual-Process Cognition on the Grid**

*Host A:* So in 2011, Daniel Kahneman publishes "Thinking, Fast and Slow." System 1: fast, intuitive, automatic. System 2: slow, deliberative, analytical.

*Host B:* The book everyone read on vacation.

*Host A:* [LAUGHS] Yes, but the insight here is: **map that onto grid control.** System 1 becomes your reflexive protection layer - sub-5 millisecond response to faults. System 2 becomes your deliberative optimizer - 50 milliseconds to seconds, for economic dispatch and coordination.

*Host B:* And the grid just... knows which one to use?

*Host A:* That is the metacognitive layer. It is the executive function. It monitors confidence, novelty, urgency, cyber-risk. And it decides: System 1, you handle this, it is a fault. System 2, you handle this, it needs optimisation. Or if it is a cyber-attack - Safe Mode.

*Host B:* So it is like a brain with a security guard.

*Host A:* That is actually a perfect way to put it.

[PAUSE]

*Host B:* What is actually inside System 1?

---

**[18:00 - 30:00] Segment 3: System 1 - The Reflexive Brain**

*Host A:* System 1 is a CNN-LSTM. Convolutional Neural Network plus Long Short-Term Memory. The CNN looks at all the bus voltages at once - spatial patterns. The LSTM looks at how they evolve over time - temporal patterns.

*Host B:* Like reading the grid's mood from its face and its history simultaneously.

*Host A:* That is a great analogy. And it detects faults, oscillations, instability - all in under 5 milliseconds. Which is protection-level speed.

*Host B:* How fast is 5 milliseconds?

*Host A:* It is... about the time it takes a hummingbird to flap its wings once. [PAUSE] And it does this by recognising patterns in PMU data - phasor measurement units, which sample at 30 to 120 times per second.

*Host B:* And this actually runs on real-time hardware?

*Host A:* On an FPGA. The OPAL-RT has a module called eFPGASIM that runs neural network inference at sub-millisecond. So this is not simulation - this is deployable.

*Host B:* What about the physics? You can't just have a neural net do anything.

*Host A:* Right. That is the PINN - Physics-Informed Neural Network. The AC power flow equations, Kirchhoff's laws, voltage limits - they are embedded **in the training loss**. So every action the network proposes is physically valid. 99.97% constraint compliance.

*Host B:* That is... remarkable. So System 1 is a fast, physically-constrained reflex.

[TRANSITION]

---

**[30:00 - 45:00] Segment 4: System 2 - The Deliberative Brain**

*Host A:* Now System 2 is the slow, thoughtful one. It does economic dispatch, V2G scheduling, coordinated control. And it uses Quantum-Inspired Reinforcement Learning.

*Host B:* Quantum-inspired. That sounds like marketing.

*Host A:* [LAUGHS] It is a fair question. So normal reinforcement learning - DQN, PPO - maintains a table of Q-values. Numbers. Quantum-inspired maintains **complex-valued probability amplitudes**. Like quantum superposition.

*Host B:* Okay, you're going to have to explain that.

*Host A:* In quantum computing, a system can be in a **superposition** of multiple states at once. Instead of picking actions one at a time, the agent evaluates many actions simultaneously. And it has a **tunneling** operator - it can probabilistically tunnel through high-cost barriers to escape local optima.

*Host B:* So it is better at finding the global best solution, not just the nearest decent one.

*Host A:* Exactly. And the results: **58-59% faster convergence** than classical DQN. Across all optimisation problems - OPF, FACTS coordination, EV scheduling, DER dispatch.

*Host B:* And it runs on...?

*Host A:* The OPAL-RT CPU. As a real-time software task. 50 milliseconds target.

[PAUSE]

*Host B:* So we have a fast reflex and a slow optimizer. How do they not step on each other?

---

**[45:00 - 55:00] Segment 5: The Metacognitive Arbitration**

*Host A:* That is the metacognitive layer. It is the executive function. At every time step, it computes: confidence, novelty, urgency, cyber-risk.

*Host B:* And based on those?

*Host A:* It switches modes. High confidence, low urgency - trust the reflex, System 1. High novelty - invoke the deliberative optimizer, System 2. High cyber-risk - **Safe Mode**. Ignore the optimizer, maintain safe setpoints, fall back to conservative voltage support.

*Host B:* So if someone hacks the data...

*Host A:* The system detects it, ignores the potentially poisoned optimiser, and keeps the lights on. That is the "reflex override" - just like a human ducking on instinct when startled.

*Host B:* Does it actually work?

*Host A:* All 4 modes verified in testing. SYSTEM_1_REFLEX, SYSTEM_2_PLANNING, SYSTEM_2_OVERRIDE, SAFE_MODE. And the smooth transitions between them.

[TRANSITION MUSIC]

---

**[55:00 - 65:00] Segment 6: The Three-Stage Validation Pipeline**

*Host B:* Okay, so we have this brain-inspired controller. How do you actually prove it works?

*Host A:* Three stages. Stage 1: offline Python simulation. PYPOWER - a Python port of MATPOWER - with real Open Power System Data from Germany. You train the AI, no real-time constraints.

*Host B:* Fast iteration.

*Host A:* Right. Stage 2: Simulink model preparation. We acquired an IEEE 39-bus model from EPFL that was **already built for OPAL-RT**. We add FACTS devices - SVC, STATCOM, TCSC, UPFC - and EV V2G chargers.

*Host B:* So the model is ready.

*Host A:* Stage 3: **Controller-HIL on the 4-core OPAL-RT.** The grid model runs in real-time at 50 microsecond time steps. The CAPSM controllers run as software tasks on the simulator CPUs.

*Host B:* So the AI is controlling a real-time simulation of the grid.

*Host A:* Exactly. And this is where you find out what simulation **can't show you**. Communication latency, quantisation, sensor noise - things that only appear when energy actually moves through real wires.

*Host B:* And the results?

*Host A:* Sub-10 milliseconds fault detection. On hardware. Not in simulation - **on hardware**. That is the validation that makes this thesis different.

[PAUSE]

---

**[65:00 - 72:00] Segment 7: Key Results**

*Host A:* So what did we actually find? Stability: 37% better voltage stability, 20-33% longer critical clearing time, 28.5% more loading margin.

*Host B:* Those are big numbers.

*Host A:* Fault detection: 95.8% accuracy, 9.7 milliseconds detection time, 74% fewer false positives.

*Host B:* Under 10 milliseconds. On real hardware.

*Host A:* Economics: 12.4% annual cost savings, 1.7-year payback, 83.7% internal rate of return.

*Host B:* So the utility saves $50 million a year and gets its money back in under 2 years.

*Host A:* And the HIL validation: 4-core OPAL-RT, 50 microsecond EMT, sub-10 ms fault detection, Safe Mode under cyber-attack. **This is what makes it real.**

[TRANSITION MUSIC]

---

**[72:00 - 78:00] Segment 8: What This Means for the Grid**

*Host B:* So if I'm a utility operator, why do I care?

*Host A:* Because most AI grid control research **never touches real hardware**. This thesis does. That means the CAPSM framework is not just a simulation result - it is a validated, deployable control system. TRL 6.

*Host B:* Technology Readiness Level 6. That is... actually ready for field testing.

*Host A:* And the roadmap: Phase 1, advisory mode. Phase 2, limited closed-loop. Phase 3, full deployment. Phase 4, advanced capabilities. Over 8+ years.

*Host B:* So we're talking about the next decade of grid control.

*Host A:* Yes. And the future work: quantum computing for real OPF, neuro-symbolic AI for interpretability, cognitive digital twins, autonomous energy communities. This is a foundation, not a finish line.

[PAUSE]

---

**[78:00 - 80:00] Outro + Close**

*Host B:* So the takeaway is: brain-inspired AI, dual-process, validated on real-time hardware, ready for industry deployment.

*Host A:* And the gap it fills - theory to practice - is the gap that has held back AI grid control for decades. CAPSM closes it.

*Host B:* That is a big claim.

*Host A:* It is. And it is backed by sub-10 millisecond fault detection on a 4-core OPAL-RT. Not simulation. Hardware.

*Host B:* Mahmoud Kiasari, Dalhousie University. Thank you for listening to "Brain-Inspired AI for the Grid." Join us next time as we...

[FADE OUT, UPBEAT MUSIC]

---

## 5. STYLE AND QUALITY RULES (APPLY TO ALL OUTPUTS)

1. **Spelling:** British/Canadian English (colour, organisation, behaviour, modelling, analyser, optimise, characterise). No American "ize" endings.
2. **No AI slop:** Never use "delves into," "robust," "leveraging," "in the realm of," "a testament to," "it is worth noting that," "navigating the complexities," "tapestry," "beacon," "underscore," "holistic." If a phrase feels overused by LLMs, rewrite it.
3. **Em-dashes:** Use "to" or en-dash (–) for ranges, never em-dash (—).
4. **Emojis:** None. Anywhere.
5. **Figures/tables:** Every one must have a number and caption. Cross-reference in text.
6. **Tone (thesis):** Academic, precise, confident. Third person. No "we" except in discussion of collaborative work.
7. **Tone (presentation):** Conversational, visual, punchy. Short phrases. One idea per slide.
8. **Tone (podcast):** Conversational, curious, accessible. Two real people talking. Humour where natural.
9. **Citations:** IEEE format throughout. Include DOIs where available.
10. **Math:** Use proper LaTeX-style notation in equations (e.g., u₁(t) = f_{CNN-LSTM}(x_t, θ₁)).
11. **Lengths:** Hit the page targets. Ch10 at 25-35 pages. Ch11 at 20-25. Do not shortchange.
12. **Cross-references:** "as shown in Figure 4.2..." and "as detailed in Table 5.3..." throughout.

---

## 6. REFERENCES TO USE

[1] Hingorani, N.G. (1988). Power electronics in electric utilities. Proc. IEEE, 76(4), 481-482.
[2] Blaabjerg, F., Yang, Y., Yang, D., & Wang, X. (2017). Distributed power-generation systems. Proc. IEEE, 105(7), 1311-1331.
[3] Meng, K., Dong, Z.Y., & Wong, K.P. (2020). Quantum-inspired PSO for power system operations. IEEE Trans. Power Syst., 35(2), 1381-1394.
[4] Wang, W., Yu, N., Gao, Y., & Shi, J. (2019). Safe off-policy DRL for Volt-VAR control. IEEE Trans. Smart Grid, 11(4), 3008-3018.
[5] Liu, Y., Zhang, N., Wang, Y., Yang, J., & Kang, C. (2021). Data-driven power system management. CSEE J. Power Energy Syst., 7(3), 551-565.
[6] Gough, B., Aabrandt, A., & Kempton, W. (2017). V2G power: EVs providing frequency regulation. IET EST, 7(2), 148-154.
[7] Teleke, S., Abdulahovic, T., Thiringer, T., & Svensson, J. (2008). Dynamic performance comparison: Synchronous condenser vs SVC. IEEE Trans. Power Deliv., 23(3), 1606-1612.
[8] Zhang, X.P., Rehtanz, C., & Pal, B. (2012). FACTS: Modelling and control. Springer.
[9] Pavel, M., Vazquez, S., Rodriguez, J., & Wu, B. (2023). Optimal allocation and control of SVCs. IEEE Trans. Power Syst., 38(1), 546-557.
[10] Dash, P.K., Morris, S., & Mishra, S. (2015). Nonlinear variable-gain fuzzy controller for FACTS. IEEE Trans. Control Syst. Technol., 12(3), 428-438.
[11] Karamanakos, P., Liegmann, E., Geyer, T., & Kennel, R. (2020). MPC of power electronic systems. IEEE Open J. Ind. Appl., 1, 95-114.
[12] Shahzad, S., Abbasi, M.A., Chaudhry, M.A., & Hussain, M.M. (2022). MPC strategies in microgrids. IEEE Access, 10, 122211-122225.
[13] Yaghoubi, E., et al. (2025). Systematic review of MPC in microgrids. Processes, 13(7), 2197.
[14] Ghiasi, M., et al. (2023). Cyber-attacks and defense mechanisms for smart grids. Electr. Power Syst. Res., 215, 108975.
[15] Yasin Ghadi, Y., et al. (2024). Security risk models for smart grid attacks. PeerJ Comput. Sci., 10, e1840.
[16] Hossain, R.R., et al. (2022). Efficient learning of voltage control via model-based DRL. arXiv:2212.02715.
[17] Nematshahi, S., et al. (2023). DRL-based voltage control revisited. IET GTD, 17(21), 4826-4835.
[18] Wilk, P., Wang, N., & Li, J. (2024). MARL for smart community energy management. Energies, 17(20), 5211.
[19] Yu, P., Wang, Z., Zhang, H., & Song, Y. (2024). Safe RL for power system control: A review. arXiv:2407.00681.
[20] Raissi, M., Perdikaris, P., & Karniadakis, G.E. (2019). Physics-informed neural networks. J. Comput. Phys., 378, 686-707.
[21] Kody, M., et al. (2021). PINNs for power system state estimation. IEEE PES GM, 1-5.
[22] Rudin, C. (2019). Stop explaining black box ML for high stakes decisions. Nat. Mach. Intell., 1(5), 206-215.
[23] Keren, S., Essayeh, C., Albrecht, S.V., & Morstyn, T. (2024). MARL for energy networks. arXiv:2404.15583.
[24] Kroposki, B., et al. (2017). Achieving a 100% renewable grid. IEEE P&E Mag., 15(2), 61-73.
[25] Botterud, A., & Zhou, Z. (2020). Multi-stage stochastic programming in generation planning. IEEE PES GM, 1-5.
[26] Wang, Q., Guan, Y., & Wang, J. (2012). Chance-constrained stochastic program for unit commitment. IEEE Trans. Power Syst., 27(1), 206-215.
[27] Dall'Anese, E., et al. (2017). Optimal regulation of virtual power plants. IEEE Trans. Power Syst., 33(2), 1868-1881.
[28] Pudjianto, D., Ramsay, C., & Strbac, G. (2007). VPP and system integration of DERs. IET RPG, 1(1), 10-16.
[29] Kok, J.K., et al. (2005). PowerMatcher: Multiagent control in electricity infrastructure. Proc. AAMAS, 75-82.
[30] Widergren, S.E., et al. (2014). AEP Ohio gridSMART demonstration. PNNL Tech. Rep. PNNL-23192.
[31] Mengelkamp, E., et al. (2018). Designing microgrid energy markets: Brooklyn Microgrid. Appl. Energy, 210, 870-880.
[32] Karpunovic, S., et al. (2020). Quantum-inspired RL for complex optimisation. Nat. Mach. Intell., 3(6), 489-498.
[33] Keren, S., et al. (2024). MARL for energy networks: Computational challenges, progress and open problems. arXiv:2404.15583.
[34] Hermans, B.A.L., Walker, S., Ludlage, J.H., & Ozkan, L. (2024). MPC of vehicle charging stations in grid-connected microgrids. Appl. Energy, 368, 123210.
[35] Bevrani, H. (2009). Robust Power System Frequency Control. Springer.
[36] Palmintier, B., et al. (2017). HELICS: High-performance T-D-C-market co-simulation. MSCPES.
[37] Muller, S.C., et al. (2018). Interfacing power system and ICT simulators. IEEE Trans. Smart Grid, 9(1), 14-24.
[38] Vantretti, L., et al. (2016). A Modelica-based dynamic PMU model. IEEE Trans. Smart Grid, 9(3), 1-16.
[39] Faschang, M., Kupzog, F., Widl, E., & Rohjans, S. (2019). Requirements for real-time HW integration into cyber-physical energy system simulation. IEEE Access.
[40] Monti, A., et al. (2018). A global real-time superlab: Enabling high penetration of power electronics. IEEE Power Electron. Mag., 5(3), 35-44.
[41] Caire, R., Sanchez-Jimenez, M., & Hadsaid, N. (2020). PowerShapeGrid: A testbed to address digital twin challenges for future distribution networks. CIGRE Sci. & Eng. J., 17, 15-29.
[42] Steinbrink, C., et al. (2019). MOSAIK: A framework for modular simulation of active components in smart grids. IEEE Trans. Smart Grid, 10(1), 3562-3571.
[43] Podmore, R., & Robinson, M. (2010). The role of simulators for smart grid development. IEEE Trans. Smart Grid, 1(2), 205-212.
[44] Strasser, T., et al. (2015). A review of architectures and concepts for intelligence in future electric energy systems. IEEE Trans. Ind. Electron., 62(4), 2424-2438.
[45] Wang, J., et al. (2012). A review of power electronics based microgrids. J. Power Electron., 12(1), 181-192.
[46] Golestan, S., Golmohamadi, H., Sinha, R., Iov, F., & Bak-Jensen, B. (2024). Real-Time Simulation and HIL Testing Based on OPAL-RT ePHASORSIM. Energies, 17(19), 4893.
[47] OPAL-RT Technologies (2024). Power hardware-in-the-loop. https://www.opal-rt.com/industries-and-applications/simulation-and-testing/power-hardware-in-the-loop/
[48] DESL-EPFL (2018). IEEE-39-bus-power-system. https://github.com/DESL-EPFL/IEEE-39-bus-power-system
[49] MathWorks (2024). Power Systems Studies with Simulink and Simscape Electrical. https://www.mathworks.com/videos/power-systems-studies-with-simulink-and-simscape-electrical-1772205136279.html
[50] All About Circuits (2018). HIL Simulation and Power System Design: An Interview with Dr. Sudipta Chakraaborty. https://www.allaboutcircuits.com/news/engineer-spotlight-sudipta-chakraaborty/
[51] ICSEG (2013). IEEE 39-Bus System. https://icseg.iti.illinois.edu/ieee-39-bus-system
[52] Zenodo (2022). IEEE New England 39-bus test case: Dataset for TSA. https://zenodo.org/records/7350829
[53] Zenodo (2021). Power System TSA Simulations Dataset. https://zenodo.org/records/4521886
[54] IEEE DataPort (2024). Simulation Data of 10-Machine 39-Bus Power System. https://ieee-dataport.org/documents/simulation-data-10-machine-39-bus-power-system
[55] Al-Roomi (2015). 300-Bus System. https://www.al-roomi.org/power-flow/300-bus-system
[56] MATPOWER (2025). MATPOWER 8.1. https://matpower.org/
[57] PYPOWER (2021). PYPOWER: Port of MATPOWER to Python. https://github.com/rwl/PYPOWER
[58] Open Power System Data (2024). Open Power System Data. https://open-power-system-data.org/
[59] MathWorks File Exchange (2026). Bidirectional EV Charger With V2G & G2V Control Model. https://in.mathworks.com/matlabcentral/fileexchange/182226
[60] MathWorks File Exchange (2021). Electric Vehicle bi directional V2G & G2V. https://www.mathworks.com/matlabcentral/fileexchange/98999
[61] OPAL-RT (2024). eFPGASIM: FPGA-based Power Electronics Toolbox. https://opal-rt.atlassian.net/wiki/spaces/PFPET/pages/65278199/
[62] OPAL-RT (2024). ePHASORSIM Documentation. https://opal-rt.atlassian.net/wiki/spaces/PDOCHS/pages/149717752/
[63] Texas A&M University (2023). IEEE 39-Bus System. https://electricgrids.engr.tamu.edu/electric-grid-test-cases/ieee-39-bus-system
[64] Chakraborty, S. (2018). Real-time simulator-based validation of power system controls. IEEE PES GM.
[65] Keren, S., Essayeh, C., Albrecht, S.V., & Morstyn, T. (2024). Multi-Agent RL for Energy Networks. arXiv:2404.15583.

---

## END OF MASTER PROMPT

**Hand this .md file to an AI and it will write:**
1. All 13 thesis chapters as Word (.docx) files with figures, tables, references
2. A 15-page presentation as Markdown (.md)
3. An 80-minute podcast script as Markdown (.md)

**Everything it needs is above. Follow every instruction precisely.**
