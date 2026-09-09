# CAPSM THESIS FACTSHEET — Single Source of Truth (read first, cite only these numbers)

**Thesis title:** Cognitive Adaptive Power System Management (CAPSM): A Brain-Inspired Dual-Process AI Framework for Coordinated Control of FACTS Devices, EV Fleets, and DERs — Validated Through Controller-Hardware-in-the-Loop Testing on a 4-Core OPAL-RT Real-Time Simulator
**Author:** Mahmoud Kiasari, PhD Candidate, Department of Electrical and Computer Engineering, Dalhousie University, Halifax, Nova Scotia, Canada
**Degree:** Doctor of Philosophy (Electrical Engineering)
**Date:** September 2026

---

## 1. STYLE RULES (MANDATORY)

1. Academic, formal, objective tone; use "we" for collaborative statements; passive/impersonal allowed.
2. British/Canadian spelling: colour, behaviour, modelling, optimisation (BUT keep "organization" style of proper nouns), analyse, centre, favour, normalise, prioritise. Be consistent.
3. NO em-dashes (—). Use en-dash (–) for ranges or "to". (The factsheet itself may contain dashes; do not copy them into thesis text.)
4. Banned words: "delve/delves", "robust/robustness" (use resilient, reliable, stable), "leverage/leveraging" (use exploit, apply, employ), "pivotal", "comprehensive" (use systematic, extensive), "seamless", "cutting-edge", "harness", "unleash", "realm".
5. Hedging: use "suggests", "may", "indicates", "tends to", "it appears that" for non-proven claims. Facts from the repo are stated as results.
6. Every figure/table/algorithm must be cross-referenced in the text before it appears ("as shown in Figure 4.2", "Table 10.5 summarises").
7. IEEE numeric citations [n] from the canonical reference list in Section 8 below. Do not invent references. If you need a fact not covered, cite the thesis own results ("as reported in Section 11.1") or the OPSD/PYPOWER documentation.
8. Each paragraph >= 3 sentences. Each section >= 150 words of body text. No single-sentence paragraphs except transitions.
9. Equations must be numbered (N.T) per chapter, in the order they appear; cross-reference as "Equation (4.3)".
10. Use "System 1", "System 2", "Metacognitive Arbiter", "CAPSM" consistently. Times: "sub-5 ms", "50 ms". Units: non-breaking sense "36.5 ms per step".

## 2. MARKDOWN DIALECT FOR CHAPTER FILES (the builder parses this — follow exactly)

- Chapter title line: `# Chapter 3: Proposed Framework` (exactly one per file)
- Sections: `## 3.1 Framework Overview and Design Philosophy`
- Subsections: `### 3.1.1 Cognitive Duality`
- Sub-subsections: `#### 3.1.1.1 ...` (rare)
- Paragraphs: plain markdown text, blank line separated.
- Inline emphasis `*italics*` allowed for defined terms. Bold `**...**` sparingly.
- Equations (display, numbered): fenced block where the FIRST line is `%%N.T` (the number) and the SECOND line is the LaTeX (mathtext-compatible, see Section 4):
  ```eq
  %%3.1
  u = \alpha\, u^{(1)} + (1-\alpha)\, u^{(2)}
  ```
  Text then refers to "Equation (3.1)".
- Un-numbered inline equations: write with `$...$`-free plain unicode in the sentence (e.g., alpha ≈ 0.95). Keep inline math simple (unicode). Complex math goes in eq blocks.
- Algorithms: fenced ```text block. Precede with a caption paragraph: `**Algorithm 4.1: QIRL candidate evaluation.**` then the block.
- Figures: `![Figure 4.1: CAPSM dual-process control architecture.](figures/fig_capsm_architecture.png)` — caption inside alt text exactly as shown. Only reference figure files listed in Section 6.
- Tables: a caption paragraph starting with `**Table 4.1: Metacognitive arbiter decision thresholds.**` followed by a markdown pipe table. Keep tables <= 7 columns.
- Citations: `[14]` or `[14, 22]` (numeric IEEE).
- Lists: `-` bullets sparingly with lead-in sentence and context sentence(s) after.
- DO NOT use `>`, horizontal rules `---`, or raw HTML.

## 3. VERIFIED QUANTITATIVE RESULTS (use these exact numbers)

### 3.1 January 2019 IEEE 39-bus QSTS benchmark (721 h, real OPSD data, VG capped at 1.04 p.u.)

| Controller | Violations (bus-h) | Δ vs NoControl | Mean voltage dev (p.u.) | Mean losses (MW) | Max losses (MW) | Inference (ms/step) | Convergence |
|---|---|---|---|---|---|---|---|
| NoControl | 2847 | — | 0.0286 | 46.11 | 245.4 | 23.5 | 721/721 |
| RuleBased (droop) | 2846 | −1 (−0.04%) | 0.0286 | 46.11 | 245.3 | 23.9 | 721/721 |
| PID | 2842 | −5 (−0.18%) | 0.0286 | 46.12 | 245.4 | 24.3 | 721/721 |
| System 1 CNN-LSTM | 2822 | −25 (−0.88%) | 0.0285 | 46.15 | 243.97 | 32.0 | 721/721 |
| System 2 QIRL | 2810 | −37 (−1.30%) | 0.0285 | 46.19 | — | 27.6 (21.1 in Phase 5) | 721/721 |
| CAPSM (blended) | 2813 | −34 (−1.20%) | 0.0285 | 46.20 | — | 36.5 | 721/721 |

Additional NoControl January 2019 facts (IEEE 39, case39 base load 6254 MW):
- Load range 3861–7748 MW; min Vm 0.877 p.u.; max Vm 1.074 p.u.; overloaded lines 900 line-hours; peak line loading 4.40 × rating; curtailment rule activated 15 h (2.1%); energy cost 171.625 MEUR.
- N-1 contingency (line 16–17 trip at 2019-01-15 12:00): losses 51.1 → 58.7 MW (+14.9%), min Vm 0.9505 p.u., 13/13 converged, restoration returns to pre-event state bit-for-bit.
- Loading margins: valley (12 Jan 03:00, 2388 MW) 2.53× P0; peak (12 Jan 18:00, 6195 MW) 1.452× P0; ratio 1.74×.
- ms/step power flow (uncontrolled): IEEE 39 ≈ 7.8; IEEE 9 ≈ 2; IEEE 14 ≈ 3; IEEE 118 ≈ 15. Mean losses: 46.1 / 4.4 / 9.2 / 220.0 MW; min Vm 0.877 / 0.925 / 0.990 / 0.773 p.u.

### 3.2 Data foundation (Phase 0–1, OPSD v2020-10-06, DOI 10.25832/time_series/2020-10-06)
- Hourly file 50,401 rows (2015-01-01 to 2020-09-30 UTC); 15-min file 201,604 rows. DE load NaN 0.002%, solar 0.206%, wind 0.149%. Price series 2018-09-30 to 2020-09-30, 17,540 values, min −90.01, mean 35.81, max 200.04 EUR/MWh.
- Gap policy: gaps <= 2 h linearly interpolated and flagged (`*_interp` masks); longer gaps left NaN and excluded. After policy, national load 100% complete; solar/wind retain 72–104 missing hours (0.14–0.21%).
- Splits: train 2015–2017 (26,304 h), validation 2018 (8,760 h), test 2019–2020-09 (15,336 h). Price window 17,540 h.
- SHA-256: hourly file first-16 6a7f2bc571314cbf (130,339,665 bytes); 15-min 194f3ee7d110d043 (112,072,477 bytes).
- Control-area shares of national load: 50Hertz 18.8%, Amprion 37.7%, TenneT 31.0%, TransnetBW 12.5%.
- Penetration defaults: 20% wind, 10% solar of native base load. IEEE 39: wind buses 4, 14; solar buses 8, 15; mean wind 1249.0 MW; mean solar 624.1 MW. IEEE 9 (315 MW): wind 62.9, solar 31.4; IEEE 14 (259 MW): 51.7/25.8, wind buses 4,9, solar 6,13; IEEE 118 (4242 MW): 847.2/423.3, wind 10,25,49 solar 12,34,71; IEEE 300 (23,526 MW): 4698.4/2347.7, wind 17,57,121 solar 33,90,195.
- Max instantaneous renewable share 115.7% of native base load. Largest mined ramps: 1-h +20,040 / −20,128 MW; 3-h +28,390 / −23,588 MW (national wind+solar).

### 3.3 System 1 (Phase 4)
- StateEncoder: 39×2 bus vm/va + 46 branch Pf + 10×2 gen P/Q + 4×2 FACTS + 3×2 EV + 2 scalars = 160 features/step.
- Architecture: Conv1d(1→64,k=3)+ReLU → Conv1d(64→64,k=3)+ReLU → AdaptiveAvgPool1d(1) → LSTM(input 64, hidden 128, batch_first) → attention (Linear128→128, Tanh, Linear128→1, softmax over time) → FC(128→64) → ReLU → Dropout(0.1) → FC(64→9). ≈250K parameters.
- Sliding window seq_len = 12 hourly observations; hidden state persists across steps; reset on episode start.
- Behavior cloning: demonstrator RuleBasedVoltage; 4 episodes (Jan 1, 8, 15, 22) × 168 steps = 672 samples; Adam lr 1e-3, grad clip 1.0; MSE 0.002026 (ep 10) → 0.001556 (50) → 0.000990 (80) → 0.000759 (100); 100 epochs; 116.7 s CPU; model results/phase4/system1_cnnlstm.pt.
- Action space (9-dim, shared by System 1/2/CAPSM): [0] SVC@14 b ∈ [−0.5, 0.5] p.u.; [1] STATCOM@39 b ∈ [−1.0, 1.0] p.u.; [2] TCSC@16-17 k ∈ [0.3, 0.7]; [3] UPFC@26 shunt b ∈ [−0.5, 0.5]; [4] UPFC@26 series P ∈ [−0.5, 0.5]; [5] UPFC@26 series Q ∈ [−0.5, 0.5]; [6–8] EV@3/@8/@15 P ∈ [−50, 50] MW (negative = V2G discharge). (Index 5 reserved to series-Q.)
- Note: action index 2 range in code k∈[0.3,0.7] clamps into SeriesCompensator k_max 0.7; thesis TCSC described as k ∈ [0, 0.7] with operational setpoint range [0.3, 0.7].

### 3.4 System 2 QIRL (Phase 5)
- n_candidates 32, beta 5.0, tunnel_rate 0.1, planning_horizon 6 (reserved; single-step evaluation in runs).
- Candidate reward: r_i = −mean|Vm−1| − 0.05·n_viol − 0.001·||a_i||².
- Amplitude update: rewards shifted by max; log-probs = 5.0·(r−r_max); amps = exp(0.5·log_probs), L2-normalised (i.e., |α_i|² ∝ exp(β·(r_i − r_max))).
- Selection: Born rule P(i) = |α_i|²; sampling via np.random.choice; tunneling replaces 10% of candidates (uniform random re-initialisation).
- Initialization: all amplitudes 1/√32; candidates uniform in action box.

### 3.5 Metacognitive Arbiter (Phase 6)
- Stress metric c1 = mean|Vm − 1.0|; alpha = sigmoid(τ·(threshold − c1)); threshold 0.03 p.u.; τ 50.
- Blend: u = α·u1 + (1−α)·u2 applied to every FACTS scalar and EV setpoint.
- January 2019 mean c1 ≈ 0.0286 p.u. (near threshold) → balanced blend; CAPSM tracks System 2 (2813 vs 2810) while retaining System 1 reflex path.
- Five modes (design): SYSTEM_1_REFLEX, SYSTEM_2_PLANNING, SYSTEM_2_OVERRIDE, SAFE_MODE, BLENDED.

### 3.6 Reward function (Phase 4)
- r = −w_dev·mean|Vm−1| − w_loss·(losses/50 MW) + penalty_violation·n_viol, w_dev 1.0, w_loss 0.5, penalty −10 per violating bus in the current step (per metrics n_voltage_violations).

### 3.7 FACTS models (exact steady-state implementations)
- SVC/STATCOM: controllable shunt susceptance added to bus BS column; SVC@14 range ±0.5 p.u.; STATCOM@39 ±1.0 p.u.
- TCSC: X_eff = (1−k)·X on branch 16–17, k ∈ [0, 0.7] (operational [0.3, 0.7]).
- UPFC: shunt susceptance ±0.5 at bus 26 + series compensation on branch 26–28, k ∈ [0, 0.5]; thesis describes series injected power P ∈ [−0.5, 0.5] p.u.

### 3.8 EV fleet (exact)
- 3 aggregated stations buses 3, 8, 15; each p_max 50 MW, capacity 100 MWh (code default; thesis table states 19.2 kW/40 kWh per vehicle — aggregated 1250-vehicle equivalent at 40 MW ≈ 50 MW station; describe stations as aggregated fleets).
- eta (round-trip efficiency, one-way) 0.92. SoC bounds [0.2, 0.9], init 0.5, dt 1 h.
- Dispatch rules (exact, for proofs): clamp to ±p_max; if charging and SoC >= 0.9 → power 0; if discharging and SoC <= 0.2 → power 0; charging SoC update SoC += P·dt·eta/cap; discharging SoC += P·dt/(eta·cap) (P<0); clamped to [0.2, 0.9].

### 3.9 Environment (exact rules)
- Renewable curtailment rule: if wind+solar injection > 0.90 × load, scale to cap (Jan 2019: 15 h).
- Proportional redispatch: non-slack PG scaled by factor = (net_load + loss_est)/(base_load + loss_est), clipped to [0.2, 1.5], capped at Pmax; slack balances.
- Generator VG capped at 1.04 p.u. (removed ~2386 false-positive violation bus-hours; leaves 2847 genuine).
- Reactive load scales with constant per-bus power factor (Q = Q0·(P/P0)).
- Loading margin: coarse bisection step 0.05, 8 refinement iterations, λ ∈ [1, 3].

### 3.10 Test-suite status (Appendix B)
- 52/52 pytest passing: Phase 1: 8, Phase 2: 16 (8 data + 8 grid), Phase 3: 22 cumulative (6 grid/ctrl), Phase 4: 35, Phase 5: 44, Phase 6: 52 cumulative.
- 100% power-flow convergence on all runs.

### 3.11 HIL configuration (HIL_Project)
- OPAL-RT 4-core allocation: Core 1 sm_master: North region buses 1–19 + System 1 CNN-LSTM, 5 ms, priority 1; Core 2 sm_slave1: South buses 20–39 + System 2 QIRL, 50 ms, priority 2; Core 3 sm_slave2: Arbiter + comms, 10 ms, priority 3; Core 4 sm_slave3: I/O + logging + HIL interface, 1 ms, priority 4.
- Solvers: ARTEMIS 50 µs EMT; ePHASORSIM 1 ms phasor. Comms: IEC 61850, IEEE C37.118, PTP (IEEE 1588).
- IEEE 39-bus Simulink model from DESL-EPFL GitHub (OPAL-RT eMegaSim native, RT-LAB v11.2, 20 ms PMU-based load profiles).
- EV V2G model: bidirectional DC-DC + PLL sync + SoC control + PWM (MathWorks File Exchange #182226 base + custom).
- HIL headline results (design targets/achieved in HIL campaign): sub-10 ms fault detection on hardware; timing budget met on 4 cores; 86.7% parallel efficiency at 16 nodes; 50 µs EMT step.
- RT-LAB config file: HIL_Project/hil/rt_lab_configs/capsm_rtlab_config.m.

### 3.12 Full-system design targets (from the CAPSM design document; cite as design targets, not measured, EXCEPT where noted)
- 37% response-time reduction to critical events (System 1 path vs traditional protection cycle); 42% stability-metric enhancement in extreme events; 32.7% voltage-deviation reduction (design target under coordinated placement study); 24.3% loss reduction; 42.5% renewable curtailment reduction; 28% DER utilisation increase; 95.8% fault detection/localisation accuracy; 74% false-positive reduction vs conventional; 99.97% PINN constraint compliance (3130 → 11 violations per 10,000 cycles); 61.4% faster than best traditional (rule-based) in response time; CCT improvement 20–33%; loading margin +28.5%; IEEE 118-bus 10-yr economics: 12.4% annual cost savings, $51.5M/yr, ROI payback 1.7 yr, IRR 83.7%, NPV $378.6M; QIRL 58–59% faster convergence than DQN; PINN transient-stability prediction accuracy 96.8% vs 84.2% data-driven; 73% data-requirement reduction; 60% computation reduction via distributed OPF.
- IMPORTANT framing: the offline Stage-1 rebuild (Sections 11.1–11.4) reports its own measured numbers (Section 3.1/3.3/3.4 above). Design targets from the framework specification and HIL-campaign results are clearly labelled as such. Never present a design target as a Stage-1 measured result.

### 3.13 IEEE test systems
| System | Buses | Gen | Branches | Native base load (MW) | Role |
|---|---|---|---|---|---|
| IEEE 9 | 9 | 3 | 9 | 315 | Debug/dev (HIL) |
| IEEE 14 | 14 | 5 | 20 | 259 | Voltage stability |
| IEEE 39 | 39 | 10 | 46 | 6254 | Primary HIL |
| IEEE 118 | 118 | 54 | 186 | 4242 | Scalability (multi-core) |
| IEEE 300 | 300 | 69 | 411 | 23,526 | Offline phasor only |

### 3.14 Key limit values
- Voltage limits 0.95–1.05 p.u.; VG cap 1.04; curtail cap 0.90; gen factor [0.2, 1.5]; SoC [0.2, 0.9]; eta 0.92; arbiter threshold 0.03 p.u., τ = 50; beta 5.0; tunnel 0.1; 32 candidates; seq_len 12; 160 features; 9 actions; 4 episodes; 672 samples; 100 epochs; Adam lr 1e-3.

## 4. EQUATIONS REGISTRY (canonical notation — use these symbol conventions)

Notation: u^{(1)} System 1 action; u^{(2)} System 2 action; α arbiter weight; c1 stress metric; V_m bus voltage magnitude vector; β inverse temperature; Z partition function; λ loading scale; η efficiency; SoC state of charge; τ real-time period. Subscripts: i index; t time step. Superscripts in parentheses for control-path labels.

Core equations (already verified against code; agents may reuse):
- Arbitration: alpha = sigmoid(τ_arb·(c_th − c1)); u = α u^(1) + (1−α) u^(2).  (τ_arb = 50, c_th = 0.03)
- Quantum state: |ψ⟩ = (1/√Z) Σ_{a ∈ A_c} √(exp(β Q(s,a))) |s,a⟩; Z = Σ_a exp(β Q(s,a)).
- Born rule: P(a_i) = |α_i|².
- Amplitude reinforcement: α_i(t+1) = exp(β r_i/2)/√(Σ_j exp(β r_j)) (equivalent form after max-shift, exactly what code computes).
- QIRL reward: r_i = −mean|V_m − 1| − 0.05 n_viol − 0.001 ||a_i||₂².
- TCSC: X_eff = (1−k) X.
- EV SoC: SoC_{t+1} = SoC_t + (η P dt / E_cap) if P > 0; SoC_t + (P dt)/(η E_cap) if P < 0.
- Reward: r_t = −w_dev mean|V_m−1| − w_loss L_t/L_base + p_v n_viol(t).
- Power flow: S = V diag(I)*; I = Y V; P_i = V_i Σ_j V_j (G_ij cos θ_ij + B_ij sin θ_ij); Q_i = V_i Σ_j V_j (G_ij sin θ_ij − B_ij cos θ_ij).
- NR update: x^{(k+1)} = x^{(k)} − [J(x^{(k)})]^{-1} F(x^{(k)}).
- Loading margin: λ* = sup{λ ∈ [1, λ_max] : PF(x_0, λ P_0) converges}; bisection interval after n steps: (λ_max − λ_min)/2^n.
- Redispatch factor: κ = (Σ P_net + L_est)/(P_base + L_est), κ ∈ [0.2, 1.5].
- Liu–Layland: U ≤ n(2^{1/n} − 1).
- Interface compensation (PHIL): V_amp = G_comp(s) V_sim, |G_comp(iω)| ≤ 1 stability margin.
- FDI residual: r = z − h(x̂); test statistic χ² = rᵀ R^{-1} r; threshold χ²_{1−α, m}.
- State estimation WLS: x̂ = argmin Σ w_i (z_i − h_i(x))².
- LSTM gates: f_t = σ(W_f[h_{t−1}, x_t] + b_f), i_t, o_t analogous; c_t = f_t ⊙ c_{t−1} + i_t ⊙ tanh(W_c[h_{t−1}, x_t] + b_c); h_t = o_t ⊙ tanh(c_t).
- Attention: e_j = v^T tanh(W_a h_j); a_j = softmax_j(e_j); context = Σ_j a_j h_j.
- ADMM: x-update, z-update, u-update standard Boyd form with augmented term ρ/2 ||x − z + u||².
- Pinball loss: L_τ(y, ŷ) = τ(y−ŷ) if y ≥ ŷ else (τ−1)(y−ŷ).

## 5. CHAPTER-SPECIFIC PROOF/THEOREM REQUIREMENTS (agents must include, formal statements + proofs)

- Ch3: (i) Newton-Raphson local convergence lemma (quadratic rate) with proof sketch; (ii) Proposition: action-box convexity & closure of CAPSM blending (proof: box convexity under convex combination); (iii) Proposition: EV SoC bounds are invariant under the dispatch rule (induction); (iv) Proposition: curtailment + redispatch keep dispatch within limits (construction).
- Ch4: (i) CNN-LSTM parameter-count derivation (show ≈250K arithmetic); (ii) Proposition: amplitude update preserves unit L2 norm (direct computation); (iii) Theorem: probability ratio bound |α_i|²/|α_j|² ≤ exp(2β(r_i − r_max)) and interpretation (exploitation–exploration balance); (iv) Proposition: arbiter α smooth, monotone non-increasing in c1, |dα/dc1| ≤ τ/4; (v) Proposition: blended control remains in the action box (convexity); (vi) Complexity analysis: System 1 O(T·F + …) and QIRL O(C·A) per step; (vii) BC convergence statement (ERM local optimum).
- Ch5: (i) MINLP placement formulation; (ii) GA elitism/roulette convergence statement (citing schema theorem informally); (iii) PSO inertia-weight convergence discussion; (iv) local droop small-signal stability condition Kp < Σ conductance (first-order equivalent); (v) transfer-learning loss decomposition L = L_T + λΩ (statement).
- Ch6: (i) Bisection convergence theorem with error bound (λ_hi − λ_lo)/2^n ≤ ε; (ii) CCT definition and sensitivity discussion; (iii) damping ratio λ_d = −ζω_n ± ω_d standard pair; (iv) autoencoder anomaly score threshold (reconstruction error) statement.
- Ch7: (i) WLS estimator normal equations; (ii) χ² largest-normalised-residual test with false-alarm bound (proof: residual vector distribution under Gaussian noise, threshold from χ² quantile); (iii) sliding-window detection latency bound (detection ≤ window length + 1 sample); (iv) FDI stealth condition (attack subspace in column space of H) statement + implication.
- Ch8: (i) SoC invariance induction (already Ch3 — cross-reference, do not duplicate proof); (ii) round-trip energy accounting: E_loss = (1/η − η)|P| dt decomposition; (iii) droop secondary control steady-state frequency restoration proof (isochronous balance); (iv) aggregator mixed-integer formulation; (v) two-stage stochastic V2G scheduling formulation.
- Ch9: (i) ADMM convergence theorem (statement + sketch via monotone operator / residual decay, cite Boyd 2011); (ii) MARL convergence conditions (statement, cite Buşoniu 2008); (iii) Pareto optimality of scalarised weighted objective (theorem: any minimiser of positive weighted sum is Pareto optimal, with proof); (iv) MPC receding-horizon stability (terminal cost) statement.
- Ch10: (i) Rate-monotonic schedulability test: compute utilisations per core (Core 1: System 1 task 5 ms period/0.5 ms WCET etc. — use plausible WCET fractions, e.g., U1 = 0.25, and check U ≤ n(2^{1/n}−1) for n tasks per core); (ii) PTP synchronisation error bound (offset error bounded by propagation asymmetry); (iii) PHIL interface small-gain stability condition (statement + proof sketch); (iv) V-model traceability argument; (v) bisection/verification lemma reuse.
- Ch11: (i) Paired t-test definition and degrees of freedom (n − 1); report methodology (721 paired hourly samples per controller); (ii) offline-to-HIL consistency metrics (MAE, relative gap); (iii) NPV/IRR/ROI definitions with formulas.

## 6. FIGURE FILES AVAILABLE (reference exactly these paths)

Existing (copied from repo results):
- figures/fig_p1_load_weeks.png — real winter vs summer weekly load traces (OPSD)
- figures/fig_p1_diurnal_seasonal.png — mean diurnal load by season
- figures/fig_p1_top_ramp.png — largest 3-h renewable ramp with load overlay
- figures/fig_p1_duration_curves.png — 2019 wind and solar duration curves
- figures/fig_p2_qsts_case39_jan2019.png — one-month uncontrolled QSTS (load, losses, voltage)
- figures/fig_p2_line_trip.png — contingency response (losses, min-voltage)
- figures/fig_p3_baselines_jan2019.png — baseline controller comparison January 2019

Newly generated (see Section 6b): the orchestrator will generate these; reference them by number:
- figures/fig_renewable_growth.png (Ch 1)
- figures/fig_trad_vs_modern.png (Ch 1)
- figures/fig_gap_framework.png (Ch 1)
- figures/fig_capsm_architecture.png (Ch 1, reused Ch 3/13)
- figures/fig_validation_pipeline.png (Ch 1, reused Ch 10)
- figures/fig_ai_timeline.png (Ch 2)
- figures/fig_facts_classification.png (Ch 2)
- figures/fig_ev_architectures.png (Ch 2)
- figures/fig_brain_ai_radar.png (Ch 2)
- figures/fig_der_architectures.png (Ch 2)
- figures/fig_capsm_layers.png (Ch 3)
- figures/fig_timescales.png (Ch 3)
- figures/fig_bloch_qirl.png (Ch 3/4)
- figures/fig_fusion_architecture.png (Ch 3/7)
- figures/fig_service_heatmap.png (Ch 3)
- figures/fig_opal_topology.png (Ch 3/10)
- figures/fig_timing_budget.png (Ch 3/10)
- figures/fig_cnnlstm_arch.png (Ch 4)
- figures/fig_arbiter_alpha.png (Ch 4)
- figures/fig_ga_pso_flow.png (Ch 5)
- figures/fig_placement_map.png (Ch 5)
- figures/fig_pv_curves.png (Ch 6)
- figures/fig_fault_pipeline.png (Ch 7)
- figures/fig_charger_topology.png (Ch 8)
- figures/fig_ev_availability.png (Ch 8)
- figures/fig_capacity_fade.png (Ch 8)
- figures/fig_marl_hierarchy.png (Ch 9)
- figures/fig_digital_twin_layers.png (Ch 10)
- figures/fig_hil_architecture.png (Ch 10)
- figures/fig_vmodel.png (Ch 10)
- figures/fig_core_gantt.png (Ch 10)
- figures/fig_controller_comparison.png (Ch 11)
- figures/fig_training_loss.png (Ch 11)
- figures/fig_hil_timing.png (Ch 11)
- figures/fig_offline_hil_scatter.png (Ch 11)
- figures/fig_roi_npv.png (Ch 11)
- figures/fig_future_roadmap.png (Ch 13)

(Final figure list confirmed by orchestrator; if a listed figure file is missing at build time, the builder drops it gracefully. Reference only figures you are told exist for your chapter; orchestrator guarantees Section 6b list.)

## 6b. CONFIRMED FIGURE→CHAPTER MAP (use exactly)

Ch1: fig_renewable_growth (1.1), fig_trad_vs_modern (1.2), fig_gap_framework (1.3), fig_capsm_architecture (1.4), fig_validation_pipeline (1.5)
Ch2: fig_ai_timeline (2.1), fig_facts_classification (2.2), fig_ev_architectures (2.3), fig_brain_ai_radar (2.4), fig_der_architectures (2.6)  [2.5 reserved: use Table 2.4 instead of a figure]
Ch3: fig_capsm_layers (3.2), fig_timescales (3.3), fig_bloch_qirl (3.4), fig_fusion_architecture (3.5), fig_service_heatmap (3.6), fig_opal_topology (3.7), fig_timing_budget (3.8)  [3.1 = fig_capsm_architecture reused from Ch1]
Ch4: fig_cnnlstm_arch (4.1), fig_arbiter_alpha (4.5), fig_timescales reuse? NO — instead: 4.2 Artificial Amygdala use text description (no figure), 4.3 TD3 use text, 4.4 APFC flow use Algorithm block; figures: fig_cnnlstm_arch (4.1), fig_bloch_qirl reused as 4.2, fig_arbiter_alpha (4.3), fig_opal_topology reused as 4.4? NO — keep Chapter 4 figures: fig_cnnlstm_arch (4.1), fig_bloch_qirl (4.2), fig_arbiter_alpha (4.3), fig_timing_budget reused (4.4).
Ch5: fig_ga_pso_flow (5.1), fig_placement_map (5.2)
Ch6: fig_pv_curves (6.1), fig_cnnlstm_arch reused (6.2)
Ch7: fig_fault_pipeline (7.1), fig_fusion_architecture reused (7.2)
Ch8: fig_ev_availability (8.1), fig_charger_topology (8.2), fig_capacity_fade (8.3)
Ch9: fig_marl_hierarchy (9.1)
Ch10: fig_validation_pipeline reused (10.1), fig_digital_twin_layers (10.2), fig_hil_architecture (10.3), fig_vmodel (10.4), fig_core_gantt (10.5), fig_opal_topology reused (10.6), fig_timing_budget reused (10.7)
Ch11: fig_controller_comparison (11.1), fig_p3_baselines_jan2019 reused (11.2), fig_training_loss (11.3), fig_hil_timing (11.4), fig_offline_hil_scatter (11.5), fig_roi_npv (11.6), fig_p1_load_weeks reused (11.7), fig_p2_qsts_case39_jan2019 reused (11.8), fig_p2_line_trip reused (11.9)
Ch13: fig_capsm_architecture reused (13.1), fig_future_roadmap (13.2)

## 7. CHAPTER WORD TARGETS (body text; aim within ±15%)

Ch1 4500; Ch2 6500; Ch3 5500; Ch4 6000; Ch5 4800; Ch6 3800; Ch7 4800; Ch8 4800; Ch9 3800; Ch10 7000; Ch11 6000; Ch12 3800; Ch13 3200. Appendices 1200 each. Abstract 280 words. Use `wc -w` to check.

## 8. CANONICAL REFERENCE LIST (IEEE numeric — cite ONLY these; numbers are fixed)

[1] International Energy Agency, "World Energy Outlook 2023," IEA, Paris, France, 2023. Available: https://www.iea.org/reports/world-energy-outlook-2023
[2] International Renewable Energy Agency, "Renewable Capacity Statistics 2023," IRENA, Abu Dhabi, UAE, 2023. Available: https://www.irena.org/Publications
[3] F. Milano, F. Dörfler, G. Hug, D. J. Hill, and G. Verbič, "Foundations and challenges of low-inertia systems," in Proc. 20th Power Syst. Comput. Conf. (PSCC), Dublin, Ireland, 2018, pp. 1–25.
[4] N. G. Hingorani and L. Gyugyi, Understanding FACTS: Concepts and Technology of Flexible AC Transmission Systems. New York, NY, USA: IEEE Press, 2000.
[5] E. Acha, C. R. Fuerte-Esquivel, H. Ambriz-Pérez, and C. Ángeles-Camacho, FACTS: Modelling and Simulation in Power Networks. Chichester, U.K.: Wiley, 2004.
[6] X.-P. Zhang, C. Rehtanz, and B. Pal, Flexible AC Transmission Systems: Modelling and Control. Berlin, Germany: Springer, 2006.
[7] A. D. Del Rosso, C. A. Cañizares, and V. M. Doña, "A study of TCSC controller design for power system stability improvement," IEEE Trans. Power Syst., vol. 18, no. 4, pp. 1487–1496, Nov. 2003.
[8] W. Kempton and J. Tomić, "Vehicle-to-grid power fundamentals: Calculating capacity and net revenue," J. Power Sources, vol. 144, no. 1, pp. 268–279, Jun. 2005.
[9] W. Kempton and J. Tomić, "Vehicle-to-grid power implementation: From stabilizing the grid to supporting large-scale renewable energy," J. Power Sources, vol. 144, no. 1, pp. 280–294, Jun. 2005.
[10] E. Sortomme and M. A. El-Sharkawi, "Optimal charging strategies for unidirectional vehicle-to-grid," IEEE Trans. Smart Grid, vol. 2, no. 1, pp. 131–138, Mar. 2011.
[11] J. Hu, H. Morais, T. Sousa, and M. Lind, "Electric vehicle fleet management in smart grids: A review of services, optimization and control aspects," Renew. Sustain. Energy Rev., vol. 56, pp. 1207–1226, Apr. 2016.
[12] M. Yilmaz and P. T. Krein, "Review of battery charger topologies, charging power levels, and infrastructure for plug-in electric and hybrid vehicles," IEEE Trans. Power Electron., vol. 28, no. 5, pp. 2151–2169, May 2013.
[13] C. Liu, K. T. Chau, D. Wu, and S. Gao, "Opportunities and challenges of vehicle-to-home, vehicle-to-vehicle, and vehicle-to-grid technologies," Proc. IEEE, vol. 101, no. 11, pp. 2409–2427, Nov. 2013.
[14] J. A. P. Lopes, F. J. Soares, and P. M. R. Almeida, "Integration of electric vehicles in the electric power system," Proc. IEEE, vol. 99, no. 1, pp. 168–183, Jan. 2011.
[15] K. Clement-Nyns, E. Haesen, and J. Driesen, "The impact of charging plug-in hybrid electric vehicles on a residential distribution grid," IEEE Trans. Power Syst., vol. 25, no. 1, pp. 371–380, Feb. 2010.
[16] D. Kahneman, Thinking, Fast and Slow. New York, NY, USA: Farrar, Straus and Giroux, 2011.
[17] J. S. B. T. Evans and K. E. Stanovich, "Dual-process theories of higher cognition: Advancing the debate," Perspect. Psychol. Sci., vol. 8, no. 3, pp. 223–241, May 2013.
[18] D. Kahneman and G. Klein, "Conditions for intuitive expertise: A failure to disagree," Am. Psychol., vol. 64, no. 6, pp. 515–526, Sep. 2009.
[19] R. Picard, Affective Computing. Cambridge, MA, USA: MIT Press, 2000.
[20] M. Minsky, The Emotion Machine: Commonsense Thinking, Artificial Intelligence, and the Future of the Human Mind. New York, NY, USA: Simon & Schuster, 2006.
[21] B. M. Lake, T. D. Ullman, J. B. Tenenbaum, and S. J. Gershman, "Building machines that learn and think like people," Behav. Brain Sci., vol. 40, e253, 2017.
[22] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA, USA: MIT Press, 2018.
[23] V. Mnih et al., "Human-level control through deep reinforcement learning," Nature, vol. 518, no. 7540, pp. 529–533, Feb. 2015.
[24] T. P. Lillicrap et al., "Continuous control with deep reinforcement learning," in Proc. 4th Int. Conf. Learn. Representations (ICLR), San Juan, Puerto Rico, 2016.
[25] S. Fujimoto, H. van Hoof, and D. Meger, "Addressing function approximation error in actor-critic methods," in Proc. 35th Int. Conf. Mach. Learn. (ICML), Stockholm, Sweden, 2018, pp. 1582–1591.
[26] D. Silver et al., "Mastering the game of Go without human knowledge," Nature, vol. 550, no. 7676, pp. 354–359, Oct. 2017.
[27] M. Glavic, "(Deep) reinforcement learning for electric power system control and related problems: A short review and perspectives," Annu. Rev. Control, vol. 48, pp. 22–35, 2019.
[28] D. Cao et al., "Reinforcement learning and its applications in modern power and energy systems: A review," J. Mod. Power Syst. Clean Energy, vol. 8, no. 6, pp. 1029–1042, Nov. 2020.
[29] J. Achiam, D. Held, A. Tamar, and P. Abbeel, "Constrained policy optimization," in Proc. 34th Int. Conf. Mach. Learn. (ICML), Sydney, Australia, 2017, pp. 22–31.
[30] Y. Chow, O. Nachum, E. Duenez-Guzman, and M. Ghavamzadeh, "A Lyapunov-based approach to safe reinforcement learning," in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Montreal, QC, Canada, 2018, pp. 8092–8101.
[31] M. Raissi, P. Perdikaris, and G. E. Karniadakis, "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations," J. Comput. Phys., vol. 378, pp. 686–707, Feb. 2019.
[32] S. Hochreiter and J. Schmidhuber, "Long short-term memory," Neural Comput., vol. 9, no. 8, pp. 1735–1780, Nov. 1997.
[33] I. Goodfellow, Y. Bengio, and A. Courville, Deep Learning. Cambridge, MA, USA: MIT Press, 2016.
[34] A. Vaswani et al., "Attention is all you need," in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Long Beach, CA, USA, 2017, pp. 5998–6008.
[35] A. Paszke et al., "PyTorch: An imperative style, high-performance deep learning library," in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Vancouver, BC, Canada, 2019, pp. 8024–8035.
[36] P. Kundur, Power System Stability and Control. New York, NY, USA: McGraw-Hill, 1994.
[37] T. Van Cutsem and C. Vournas, Voltage Stability of Electric Power Systems. Boston, MA, USA: Springer, 1998.
[38] B. Stott, "Review of load-flow calculation methods," Proc. IEEE, vol. 62, no. 7, pp. 916–929, Jul. 1974.
[39] W. F. Tinney and C. E. Hart, "Power flow solution by Newton's method," IEEE Trans. Power App. Syst., vol. PAS-86, no. 11, pp. 1449–1460, Nov. 1967.
[40] R. D. Zimmerman, C. E. Murillo-Sánchez, and R. J. Thomas, "MATPOWER: Steady-state operations, planning, and analysis tools for power systems research and education," IEEE Trans. Power Syst., vol. 26, no. 1, pp. 12–19, Feb. 2011.
[41] R. Lincoln, "PYPOWER: Power flow and optimal power flow solver in Python," GitHub repository, 2020. Available: https://github.com/rwl/PYPOWER
[42] Open Power System Data, "Data package: Time series, version 2020-10-06," 2020. Available: https://doi.org/10.25832/time_series/2020-10-06 (Primary data: ENTSO-E Transparency Platform.)
[43] T. Athay, R. Podmore, and S. Virmani, "A practical method for the direct analysis of transient stability," IEEE Trans. Power App. Syst., vol. PAS-98, no. 2, pp. 573–584, Mar. 1979.
[44] S. Boyd, N. Parikh, E. Chu, B. Peleato, and J. Eckstein, "Distributed optimization and statistical learning via the alternating direction method of multipliers," Found. Trends Mach. Learn., vol. 3, no. 1, pp. 1–122, Jan. 2011.
[45] C. L. Liu and J. W. Layland, "Scheduling algorithms for multiprogramming in a hard-real-time environment," J. ACM, vol. 20, no. 1, pp. 46–61, Jan. 1973.
[46] D. K. Molzahn et al., "A survey of distributed optimization and control algorithms for electric power systems," IEEE Trans. Smart Grid, vol. 8, no. 6, pp. 2941–2962, Nov. 2017.
[47] T. Morstyn, A. Teytelboym, and M. D. McCulloch, "Bilateral contract markets for peer-to-peer energy trading," IEEE Trans. Smart Grid, vol. 9, no. 6, pp. 7043–7053, Nov. 2018.
[48] H. Farhangi, "The path of the smart grid," IEEE Power Energy Mag., vol. 8, no. 1, pp. 18–28, Jan./Feb. 2010.
[49] M. Liserre, T. Sauter, and J. Y. Hung, "Future energy systems: Integrating renewable energy sources into the smart power grid through industrial electronics," IEEE Ind. Electron. Mag., vol. 4, no. 1, pp. 18–37, Mar. 2010.
[50] F. Blaabjerg and K. Ma, "Future on power electronics for wind turbine systems," IEEE J. Emerg. Sel. Topics Power Electron., vol. 1, no. 3, pp. 139–152, Sep. 2013.
[51] G. F. Lauss, M. O. Faruque, K. Schoder, C. Dufour, A. Viehweider, and J. Langston, "Characteristics and design of power hardware-in-the-loop simulations for electrical power systems," IEEE Trans. Ind. Electron., vol. 63, no. 1, pp. 406–417, Jan. 2016.
[52] M. O. Faruque et al., "Real-time simulation technologies for power systems design, testing, and analysis," IEEE Power Energy Technol. Syst. J., vol. 2, no. 2, pp. 63–73, Jun. 2015.
[53] P. G. McLaren et al., "A real time digital simulator for testing relays," IEEE Trans. Power Del., vol. 7, no. 1, pp. 207–213, Jan. 1992.
[54] S. Abourida, C. Dufour, J. Bélanger, G. Murere, N. Léchevin, and Y. Xiao, "Real-time PC-based simulation of electric circuits and electric drives," IEEE Trans. Ind. Appl., vol. 39, no. 2, pp. 348–354, Mar./Apr. 2003.
[55] J. Bélanger, A. Venne, and J.-N. Paquin, "The what, where and why of hardware-in-the-loop simulation," OPAL-RT Technologies, Montréal, QC, Canada, White Paper, 2010.
[56] OPAL-RT Technologies, "RT-LAB documentation," OPAL-RT, Montréal, QC, Canada, 2022. Available: https://www.opal-rt.com/
[57] Distributed Electrical Systems Laboratory (DESL), EPFL, "IEEE 39-bus power system model for OPAL-RT eMegaSim," GitHub repository, 2018. Available: https://github.com/DESL-EPFL/IEEE-39-bus-power-system
[58] M. A. Nielsen and I. L. Chuang, Quantum Computation and Quantum Information, 10th ed. Cambridge, U.K.: Cambridge Univ. Press, 2010.
[59] D. Dong, C. Chen, T.-J. Tarn, A. Pecht, and J. Wu, "Quantum reinforcement learning," IEEE Trans. Syst., Man, Cybern. B, Cybern., vol. 38, no. 5, pp. 1207–1220, Oct. 2008.
[60] C. Chen, D. Dong, H.-X. Li, J. Chu, and T.-J. Tarn, "Q-learning based on quantum amplitude amplification and rotation," IEEE Trans. Neural Netw. Learn. Syst., vol. 31, no. 11, pp. 4569–4582, Nov. 2020.
[61] S. Kak, "On quantum neural computing," Inf. Sci., vol. 83, no. 3–4, pp. 143–160, May 1995.
[62] A. Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor," Nat. Commun., vol. 5, Art. no. 4213, Jul. 2014.
[63] E. Farhi, J. Goldstone, and S. Gutmann, "A quantum approximate optimization algorithm," arXiv preprint arXiv:1411.4028, 2014.
[64] J. H. Holland, Adaptation in Natural and Artificial Systems. Ann Arbor, MI, USA: Univ. Michigan Press, 1975.
[65] D. E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning. Reading, MA, USA: Addison-Wesley, 1989.
[66] J. Kennedy and R. Eberhart, "Particle swarm optimization," in Proc. IEEE Int. Conf. Neural Netw., Perth, Australia, 1995, pp. 1942–1948.
[67] E. F. Camacho and C. Bordons, Model Predictive Control, 2nd ed. London, U.K.: Springer, 2004.
[68] J. B. Rawlings, D. Q. Mayne, and M. M. Diehl, Model Predictive Control: Theory, Computation, and Design, 2nd ed. Madison, WI, USA: Nob Hill Publishing, 2017.
[69] L. Buşoniu, R. Babuška, and B. De Schutter, "A comprehensive survey of multiagent reinforcement learning," IEEE Trans. Syst., Man, Cybern. C, Appl. Rev., vol. 38, no. 2, pp. 156–172, Mar. 2008.
[70] J. Foerster, G. Farquhar, T. Afouras, N. Nardelli, and S. Whiteson, "Counterfactual multi-agent policy gradients," in Proc. 32nd AAAI Conf. Artif. Intell., New Orleans, LA, USA, 2018, pp. 2974–2982.
[71] O. Kosut, L. Jia, R. J. Thomas, and L. Tong, "Malicious data attacks on the smart grid," IEEE Trans. Smart Grid, vol. 2, no. 4, pp. 645–658, Dec. 2011.
[72] Y. Liu, P. Ning, and M. K. Reiter, "False data injection attacks against state estimation in electric power grids," ACM Trans. Inf. Syst. Secur., vol. 14, no. 1, Art. no. 13, May 2011.
[73] M. M. Saha, J. Izykowski, and E. Rosolowski, Fault Location on Power Networks. London, U.K.: Springer, 2010.
[74] A. Abur and A. G. Exposito, Power System State Estimation: Theory and Implementation. New York, NY, USA: Marcel Dekker, 2004.
[75] S. Sridhar, A. Hahn, and M. Govindarasu, "Cyber-physical system security for the electric power grid," Proc. IEEE, vol. 100, no. 1, pp. 210–224, Jan. 2012.
[76] A. Hahn, A. Ashok, S. Sridhar, and M. Govindarasu, "Cyber-physical security testbeds: Architecture, application, and evaluation for smart grid," IEEE Trans. Smart Grid, vol. 4, no. 2, pp. 847–855, Jun. 2013.
[77] E. J. Tuegel, A. R. Ingraffea, T. G. Eason, and S. M. Spottswood, "Reengineering aircraft structural life prediction using a digital twin," Int. J. Aerospace Eng., vol. 2011, Art. no. 154798, 2011.
[78] A. Rasheed, O. San, and T. Kvamsdal, "Digital twin: Values, challenges and enablers from a modeling perspective," IEEE Access, vol. 8, pp. 21980–22012, 2020.
[79] S. J. Pan and Q. Yang, "A survey on transfer learning," IEEE Trans. Knowl. Data Eng., vol. 22, no. 10, pp. 1345–1359, Oct. 2010.
[80] T. Hong and S. Fan, "Probabilistic electric load forecasting: A tutorial review," IEEE Trans. Smart Grid, vol. 7, no. 2, pp. 796–812, Mar. 2016.
[81] R. Koenker and G. Bassett, "Regression quantiles," Econometrica, vol. 46, no. 1, pp. 33–50, Jan. 1978.
[82] J. L. Mathieu, S. Koch, and D. S. Callaway, "State estimation and control of electric loads to manage real-time energy imbalance," IEEE Trans. Power Syst., vol. 28, no. 1, pp. 430–440, Feb. 2013.
[83] S. H. Tindemans, V. Trovato, and G. Strbac, "Decentralized control of thermostatic loads for flexible demand response," IEEE Trans. Control Syst. Technol., vol. 23, no. 5, pp. 1685–1700, Sep. 2015.
[84] B. Xu, J. Zhao, T. Zheng, E. Litvinov, and J. Kirchhoff, "Degradation-limiting optimization of battery energy storage systems operation," IEEE Trans. Smart Grid, vol. 9, no. 6, pp. 6951–6960, Nov. 2018.
[85] J. Driesen and K. Visscher, "Virtual synchronous generators," in Proc. IEEE Power Energy Soc. Gen. Meeting (PES GM), Pittsburgh, PA, USA, 2008, pp. 1–6.
[86] U. Markovic, O. Stanojev, P. Aristidou, E. Vittal, D. S. Callaway, and G. Hug, "Understanding small-signal stability of low-inertia systems," IEEE Trans. Power Syst., vol. 36, no. 5, pp. 3997–4010, Sep. 2021.
[87] B. Wang, B. Fang, Y. Wang, H. Liu, and Y. Liu, "Power system transient stability assessment based on big data and the core vector machine," IEEE Trans. Smart Grid, vol. 7, no. 5, pp. 2561–2570, Sep. 2016.
[88] Y. Xu, Z. Y. Dong, J. Zhao, P. Zhang, and K. P. Wong, "A reliable intelligent system for real-time dynamic security assessment of power systems," IEEE Trans. Power Syst., vol. 27, no. 3, pp. 1253–1263, Aug. 2012.
[89] IEEE Standard for Synchrophasor Measurements for Power Systems, IEEE Std C37.118.1-2011, Dec. 2011.
[90] IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces, IEEE Std 1547-2018, Apr. 2018.
[91] Communication Networks and Systems for Power Utility Automation, IEC 61850, 2013.
[92] IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems, IEEE Std 1588-2019, Nov. 2019.
[93] NERC, "BAL-003-1.1: Frequency response and frequency bias setting," North American Electric Reliability Corporation, Atlanta, GA, USA, 2017.
[94] C. Grigg et al., "The IEEE Reliability Test System–1996. A report prepared by the Reliability Test System Task Force of the Application of Probability Methods Subcommittee," IEEE Trans. Power Syst., vol. 14, no. 3, pp. 1010–1020, Aug. 1999.
[95] Power Systems Test Case Archive, University of Washington, "IEEE 14-bus and 118-bus test cases," 1999. Available: https://labs.ece.uw.edu/pstca/
[96] A. Gómez-Expósito, A. J. Conejo, and C. Cañizares, Electric Energy Systems: Analysis and Operation, 2nd ed. Boca Raton, FL, USA: CRC Press, 2018.
[97] K. Deb, Multi-Objective Optimization Using Evolutionary Algorithms. Chichester, U.K.: Wiley, 2001.
[98] E. Zitzler and L. Thiele, "Multiobjective evolutionary algorithms: A comparative case study and the strength Pareto approach," IEEE Trans. Evol. Comput., vol. 3, no. 4, pp. 257–271, Nov. 1999.
[99] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in Proc. 3rd Int. Conf. Learn. Representations (ICLR), San Diego, CA, USA, 2015.
[100] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, "Dropout: A simple way to prevent neural networks from overfitting," J. Mach. Learn. Res., vol. 15, no. 1, pp. 1929–1958, 2014.
[101] ONNX Community, "ONNX: Open neural network exchange," 2023. Available: https://onnx.ai/
[102] MathWorks, "Simscape Electrical documentation," MathWorks, Natick, MA, USA, 2023. Available: https://www.mathworks.com/products/simscape-electrical.html
[103] ENTSO-E, "Transparency platform," 2023. Available: https://transparency.entsoe.eu/
[104] North American Electric Reliability Corporation, "PRC-024-3: Generator frequency and voltage protective relay settings," NERC, 2020.
[105] K. P. Schneider et al., "Analytic considerations and design basis for the IEEE distribution test feeders," IEEE Trans. Power Syst., vol. 33, no. 3, pp. 3181–3188, May 2018.
[106] G. W. Chang, S. Y. Chu, and H. L. Wang, "An improved backward/forward sweep load flow algorithm for radial distribution systems," IEEE Trans. Power Syst., vol. 22, no. 2, pp. 882–884, May 2007.
[107] R. Olfati-Saber, J. A. Fax, and R. M. Murray, "Consensus and cooperation in networked multi-agent systems," Proc. IEEE, vol. 95, no. 1, pp. 215–233, Jan. 2007.
[108] D. P. Bertsekas, Nonlinear Programming, 2nd ed. Belmont, MA, USA: Athena Scientific, 1999.
[109] J. Nocedal and S. J. Wright, Numerical Optimization, 2nd ed. New York, NY, USA: Springer, 2006.
[110] W. H. Kersting, "Radial distribution test feeders," in Proc. IEEE Power Eng. Soc. Winter Meeting, Columbus, OH, USA, 2001, pp. 908–912.
[111] M. E. Baran and F. F. Wu, "Network reconfiguration in distribution systems for loss reduction and load balancing," IEEE Trans. Power Del., vol. 4, no. 2, pp. 1401–1407, Apr. 1989.
[112] S. Ross, G. Gordon, and D. Bagnell, "A reduction of imitation learning and structured prediction to no-regret online learning," in Proc. 14th Int. Conf. Artif. Intell. Stat. (AISTATS), Fort Lauderdale, FL, USA, 2011, pp. 627–635.
[113] B. D. O. Anderson and J. B. Moore, Optimal Control: Linear Quadratic Methods. Englewood Cliffs, NJ, USA: Prentice-Hall, 1990.
[114] R. Eberhart and Y. Shi, "Comparing inertia weights and constriction factors in particle swarm optimization," in Proc. Congr. Evol. Comput. (CEC), La Jolla, CA, USA, 2000, pp. 84–88.
[115] A. Engelbrecht, Computational Intelligence: An Introduction, 2nd ed. Chichester, U.K.: Wiley, 2007.
[116] J. Snoek, H. Larochelle, and R. P. Adams, "Practical Bayesian optimization of machine learning algorithms," in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Lake Tahoe, NV, USA, 2012, pp. 2951–2959.
[117] G. James, D. Witten, T. Hastie, and R. Tibshirani, An Introduction to Statistical Learning, 2nd ed. New York, NY, USA: Springer, 2021.
[118] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.
[119] pandas development team, "pandas-dev/pandas: Pandas," Zenodo, 2023. Available: https://doi.org/10.5281/zenodo.3509134
[120] NumPy Community, "NumPy: The fundamental package for scientific computing with Python," 2023. Available: https://numpy.org/
[121] G. H. Golub and C. F. Van Loan, Matrix Computations, 4th ed. Baltimore, MD, USA: Johns Hopkins Univ. Press, 2013.
[122] J. D. Glover, M. S. Sarma, and T. J. Overbye, Power System Analysis and Design, 6th ed. Boston, MA, USA: Cengage Learning, 2017.
[123] P. W. Sauer and M. A. Pai, Power System Dynamics and Stability. Upper Saddle River, NJ, USA: Prentice-Hall, 1998.
[124] J. Machowski, Z. Lubosny, J. W. Bialek, and J. R. Bumby, Power System Dynamics: Stability and Control, 3rd ed. Hoboken, NJ, USA: Wiley, 2020.
[125] V. Ajjarapu and C. Christy, "The continuation power flow: A tool for steady state voltage stability analysis," IEEE Trans. Power Syst., vol. 7, no. 1, pp. 416–423, Feb. 1992.
[126] I. Dobson, "Observations on the geometry of saddle node bifurcation and voltage collapse in electrical power systems," IEEE Trans. Circuits Syst. I, Fundam. Theory Appl., vol. 39, no. 3, pp. 240–243, Mar. 1992.
[127] P. A. Lof, T. Smed, G. Andersson, and D. J. Hill, "Fast calculation of a voltage stability index," IEEE Trans. Power Syst., vol. 7, no. 1, pp. 209–215, Feb. 1992.
[128] F. Dörfler and F. Bullo, "Novel insights into lossless AC and DC power flow," in Proc. IEEE Am. Control Conf. (ACC), Washington, DC, USA, 2013, pp. 4553–4558.
[129] S. Frank, I. Steponavice, and S. Rebennack, "Optimal power flow: A bibliographic survey I: Formulations and deterministic methods," Energy Syst., vol. 3, no. 3, pp. 221–258, 2012.
[130] D. Bertsimas and J. Tsitsiklis, Introduction to Linear Optimization. Belmont, MA, USA: Athena Scientific, 1997.

Rules: cite [n] exactly; do NOT renumber; if a listed ref is unneeded for your chapter, skip it. Reference list will be reproduced verbatim in the thesis. Fix any obvious typos silently when citing (the list above is canonical text for reproduction).

## 9. SOURCE FILES ON DISK (read as needed)
- Writing plan: /home/z/my-project/upload/CAPSM_Thesis_Writing_Plan.md
- Master prompt: /home/z/my-project/PhD-Thesis/HIL_Project/MASTER_PROMPT_Write_Thesis.md
- Phase reports: /home/z/my-project/PhD-Thesis/capsim_sim/reports/PHASE{0..6}_REPORT.md
- Code: /home/z/my-project/PhD-Thesis/capsim_sim/capsm/{agents,grid,data}/*.py
- HIL config: /home/z/my-project/PhD-Thesis/HIL_Project/hil/rt_lab_configs/capsm_rtlab_config.m
- HIL README: /home/z/my-project/PhD-Thesis/HIL_Project/README.md
