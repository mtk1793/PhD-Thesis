# CAPSM selected revised thesis passages — editorial draft (2026-11-07)

This file presents replacement prose for selected sections of the CAPSM thesis. It is a **staged editorial draft**, not an automatic replacement for all paragraphs in `chapters_md/`. Original figures, equations, table data and full technical reference numbering remain in the canonical manuscript pending scientific reconciliation. No new findings or citations are introduced.

## Revised abstract

Increasing renewable-generation variability and the growth of flexible electric vehicle (EV) loads create a coordinated-control challenge for transmission networks. Flexible alternating current transmission system (FACTS) devices affect bus voltages and power flows, whereas aggregated EV fleets introduce time-coupled power and energy constraints. These resources operate on different timescales and are commonly represented in separate control formulations. This thesis develops Cognitive Adaptive Power System Management (CAPSM), a brain-inspired dual-process framework for coordinating FACTS and EV actions under a shared representation of the network operating state.

CAPSM combines a convolutional neural network–long short-term memory (CNN–LSTM) System 1 policy, a deliberative System 2 based on quantum-inspired, candidate-specific action evaluation, and a Metacognitive Arbiter that blends their proposed commands according to a voltage-deviation-based stress measure. The architecture uses a nine-position action interface representing FACTS controls and three aggregated EV stations; one UPFC series-reactive position is reserved and inactive in the implemented physical abstraction. Renewable injections provide time-varying operating scenarios rather than directly controlled decision variables. The framework also specifies complementary modules for stability assessment, fault detection, and hierarchical multi-agent coordination, whose implementation status and validation evidence must be distinguished from that of the core controller.

The research methodology separates historical PYPOWER quasi-static time-series studies and the Controller-Hardware-in-the-Loop (CHIL) pathway from a subsequent independent PSS/E and PyTorch validation extension. The latter requires documented IEEE benchmark provenance, physically interpretable FACTS and EV proxies, candidate-specific AC power-flow evaluation, chronological separation of training and testing data, and reproducible controller comparisons. These strands are treated as distinct evidence classes rather than interchangeable demonstrations. The thesis contribution is therefore the explicit formulation of a dual-process control architecture and a traceable programme for assessing its engineering feasibility. Quantitative conclusions from the revised PSS/E campaign are reserved until the relevant experiments have been executed and verified.

## Chapter 1 — Introduction: revised problem statement

This thesis addresses coordinated control of FACTS devices and aggregated EV fleets in transmission systems exposed to variable renewable generation. FACTS device setpoints and EV charging or discharging commands are the directly controlled variables. Wind and solar injections define exogenous operating conditions; the experiments do not assume direct dispatch of those generation sources. The CAPSM framework draws on the distinction between fast and deliberate cognitive processes [16] and uses reinforcement-learning concepts to structure alternative control decisions [22]. Its engineering purpose is to combine rapid action inference with explicit evaluation of candidate network outcomes.

The literature motivates five related research gaps: heterogeneous control architecture; decision-making under uncertainty and computational limits; FACTS–EV coordination; fault awareness using complementary measurements; and the gap between offline simulation and hardware-based validation. CAPSM addresses these through a shared action representation, CNN–LSTM reflexive control, quantum-inspired deliberation and stress-dependent arbitration. Additional perception and hierarchical-coordination modules form separable extensions. The evidence programme must test mathematical consistency, physical-device representations, comparisons with credible baselines, and hardware timing independently.

## Chapter 2 — Literature Review: revised synthesis

The literature identifies complementary strengths and limitations across model-based control, data-driven decision-making, and flexible-resource coordination. FACTS devices offer physically interpretable mechanisms for voltage support and power-flow control, but a locally defined setpoint may have system-wide consequences [4, 6]. EV aggregation studies investigate charging flexibility and vehicle-to-grid services, although their energy-management horizons do not always match transmission-level voltage or thermal constraints [10, 11]. Data-driven methods can learn rapid decisions but introduce challenges associated with training data, generalisation and constraints [27, 28].

These observations motivate hybrid design without establishing that existing methods are universally inadequate. CAPSM's central research question is whether candidate-specific AC evaluation complements a learned reflex sufficiently to justify its additional computational cost. Network-level electrical feasibility must remain distinct from the admissibility of commanded device setpoints.

## Chapter 3 — Framework: revised overview

CAPSM is formulated as a supervisory control architecture for FACTS devices and aggregated EV fleets operating within a transmission network exposed to renewable-generation variability. The dual-process analogy motivates two complementary decision pathways; it is not itself evidence of superior electrical performance. System 1 proposes actions from recent observations, while System 2 evaluates bounded candidate actions against a network model. The arbiter weighs their proposals according to a voltage-based stress measure.

The canonical IEEE 39-bus System 1 interface uses 160 features and a 12-step observation window. System 2 considers 32 **one-step** alternatives rather than quantum-hardware solutions or demonstrated multistep planning. Each alternative must be scored on its own post-action AC state. The shared action interface contains nine positions, of which eight are physically active; the UPFC series-Q position at index 5 is reserved and must remain zero. Renewable injections are scenario inputs, not independently dispatched assets in this model.

## Chapter 4 — Advanced AI Control Architecture: revised arbiter interpretation

Let c₁ represent mean absolute bus-voltage deviation in per unit. The Metacognitive Arbiter uses α(c₁) = σ[50(0.03 − c₁)] and produces the componentwise blended action u = αu⁽¹⁾ + (1 − α)u⁽²⁾. As stress increases, the weighting shifts towards candidate-based deliberation. Smoothness and bounded derivatives describe the arbitration function, not the dynamic stability of the controlled network. Similarly, convex combinations preserve a convex device-action box but do not guarantee satisfaction of AC voltage, thermal or generator constraints. Such constraints require separate physical evaluation.

## Chapter 5 — FACTS and EV Placement: revised opening

Control performance depends on both the selected setpoints and the electrical locations and ratings of available actuators. FACTS and EV placement can be formulated as a mixed-integer nonlinear programme involving discrete siting and continuous device ratings. Genetic algorithms and particle swarm optimisation provide possible computational approaches. The benchmark deployment, however, is a sensitivity-informed engineering configuration and has not been established as a globally optimal placement. The chapter therefore distinguishes its proposed optimisation method from the configuration actually used in the controller experiments.

## Chapter 6 — Stability Enhancement: revised opening

This chapter examines learned stability assessment in relation to the CAPSM reflexive pathway. It distinguishes quasi-static voltage conditions from transient and small-signal stability, which require appropriate dynamic models and reference labels. A CNN–LSTM estimator may produce rapid classification, but classification accuracy alone does not establish enhanced dynamic stability or improved closed-loop control.

## Chapter 7 — Fault Detection: revised opening

Fault detection and localisation involve measurements with different sampling rates, uncertainties and physical interpretations. Within CAPSM, the multi-modal perception pathway combines PMU, SCADA, model-based residuals and learned classifiers. An hourly AC quasi-static simulation cannot substantiate electromagnetic fault behaviour or millisecond detection claims. Reported fault accuracy and response time require independent disturbance definitions, labelled test sets and hardware provenance.

## Chapter 8 — EV Integration: revised opening

Aggregated EV stations provide both controllable charging demand and vehicle-to-grid flexibility, but aggregate models omit individual travel behaviour and distribution-network constraints. The transmission-level CAPSM model therefore requires explicit station power limits, energy capacities, efficiencies and state-of-charge bounds. Counterfactual evaluation must leave the live fleet state unchanged; state of charge advances only when the selected action is admitted and committed.

## Chapter 9 — Hierarchical Coordination: revised opening

Hierarchical multi-agent reinforcement learning addresses the scalability of FACTS–EV coordination as the number of device-level agents increases. This research extension is distinct from the deployed dual-process CAPSM core. The multi-agent formulation and supplementary experiments must therefore remain separate from the main System 1–System 2–Arbiter benchmark and from historical HIL claims.

## Chapter 10 — Validation methodology: revised opening

Algorithmic correctness, AC power-system performance and hardware timing require separate validation procedures. The historical CAPSM pathway comprises PYPOWER quasi-static time-series studies, Simulink model preparation, and Controller-HIL testing on a four-core OPAL-RT platform. Each stage has its own software, model and evidence requirements; successful completion of one stage does not automatically validate another.

The independent PSS/E–PyTorch extension is a separate AC-network validation stream. It requires an audited IEEE benchmark, confirmed solver convergence, physically interpretable FACTS and EV equivalents, candidate-specific AC power-flow evaluation, chronological data splits and matched controller baselines. German OPSD profiles provide measured temporal variability when mapped to the synthetic IEEE benchmark; this does not imply a recreation of the German network or a change in the benchmark's nominal frequency. The new solver and controller experiments must be executed before numerical performance claims can be made.

## Chapter 11 — Results and Performance Analysis

[RESULTS SECTION: UNDER DEVELOPMENT]

## Chapter 12 — Discussion: revised opening

Discussion must identify what each experiment supports and the limits under which its conclusions hold. The original benchmark's actuator placement, simplified renewable injections, aggregated EV dynamics and solver assumptions constrain the interpretation of controller performance. A reduction in quasi-static voltage deviation does not establish improved transient stability, and a fitted real-time deadline does not establish equipment-level security. Historical Stage-1 and HIL evidence must be reconciled independently; no result is transferred to the new PSS/E implementation without a matched experiment.

## Chapter 13 — Conclusions: revised opening

This thesis formulates CAPSM as a dual-process framework for coordinating FACTS and aggregated EV actions under a shared network-state representation. Its principal architectural elements are a learned System 1 policy, a quantum-inspired candidate-evaluation System 2, and stress-dependent metacognitive arbitration. The theoretical formulation, implementation record and experimental evidence must be distinguished. The independent PSS/E–PyTorch extension offers a route to test numerical behaviour and comparative control performance, but final quantitative conclusions remain conditional on verified experiments.

## Required author review

- The UPFC series active-power description and PSS/E branch-reactance proxy are not equivalent models.
- One-step candidate selection must not be represented as multi-step model-predictive planning or proven quantum acceleration.
- Device action-box convexity cannot replace a network-level safety assessment.
- HIL timing, fault and scalability figures require source-data provenance.
- Numbered technical citations in the above excerpts are inherited from the original manuscript. They are **not** represented by the separate university-writing BibTeX entries.
- The complete set of chapter equations, figures and remaining paragraphs still requires section-by-section reconciliation; this file is not a full manuscript replacement.
