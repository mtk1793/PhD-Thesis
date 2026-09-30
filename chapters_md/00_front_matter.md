# Front Matter

## Title

**Cognitive Adaptive Power System Management (CAPSM): A Brain-Inspired Dual-Process AI Framework for Coordinated FACTS–EV Control in DER-Rich Power Systems with Controller-Hardware-in-the-Loop Validation**

## Abstract

Power systems are changing faster than the control layer that protects them. As inverter-based wind and solar generation, battery storage, and electric vehicle (EV) fleets displace synchronous plant at high distributed energy resource (DER) penetration, operators face five unresolved control gaps: architectures suited to heterogeneous assets; real-time decision-making under uncertainty; coordination between flexible alternating current transmission system (FACTS) devices and EV fleets; fault detection and localisation in resource-rich environments; and the divide between simulation and deployed hardware. This thesis addresses the five gaps with CAPSM, a brain-inspired dual-process framework in which a reflexive System 1, built on a convolutional neural network with long short-term memory, acts within milliseconds; a deliberative System 2, a quantum-inspired amplitude-based candidate-selection controller, evaluates coordinated candidate actions against the counterfactual network state each step; and a Metacognitive Arbiter blends their actions through a stress-dependent sigmoid weight. Directly controllable assets are the FACTS devices and three aggregated EV stations; renewable DERs provide the variable operating environment. A three-stage pipeline links algorithms to hardware: offline Python simulation with PYPOWER quasi-static time series (QSTS), Simulink model preparation, and Controller-Hardware-in-the-Loop (CHIL) testing on a four-core OPAL-RT real-time simulator. System 1 is trained by behaviour cloning on rule-based demonstrations from 2015–2017 and validated on 2018; the primary unseen test window is January 2019 of the real Open Power System Data on an IEEE 39-bus benchmark. In the Stage-1 build, measured offline results show voltage violations falling from 2847 to 2813 bus-hours under CAPSM (−1.20%) and to 2810 under System 2 alone (−1.30%), with 100% power-flow convergence and 36.5 ms per blended control step; these Stage-1 figures are superseded by the leakage-free retrained pipeline of the final revision and are reported with their evidence class in Chapter 11. Controller-HIL trials achieve sub-10 ms fault detection within per-core timing budgets (HIL-measured). Nine contributions are claimed, spanning the dual-process architecture, quantum-inspired candidate selection with tunnelling, the Metacognitive Arbiter, coordinated FACTS–EV control, multi-modal fault detection, a FACTS and EV placement methodology, a digital twin methodology, the CHIL validation methodology, and a reproducible end-to-end pipeline. The principal limitation is that the headline improvement is bounded by the deployed device placement, and the main unimplemented extension, genuine multi-step planning in the deliberative layer, is reserved for future work.

## Keywords

dual-process control; FACTS devices; electric vehicle integration; quantum-inspired candidate selection; hardware-in-the-loop validation; smart grids

## List of Abbreviations

The thesis uses the following abbreviations. Each term is written in full at first use in the body chapters and abbreviated thereafter. The list is ordered alphabetically for reference during reading.

| Abbreviation | Meaning |
|---|---|
| ADMM | Alternating Direction Method of Multipliers |
| AGC | Automatic Generation Control |
| AI | Artificial Intelligence |
| ARTEMIS | Advanced Real-Time Electromagnetic Transient solver suite (OPAL-RT) |
| BESS | Battery Energy Storage System |
| CAPSM | Cognitive Adaptive Power System Management |
| CCT | Critical Clearing Time |
| CHIL | Controller Hardware-in-the-Loop |
| CNN | Convolutional Neural Network |
| DER | Distributed Energy Resource |
| DMS | Distribution Management System |
| DQN | Deep Q-Network |
| EMT | Electromagnetic Transient |
| EMS | Energy Management System |
| EV | Electric Vehicle |
| FACTS | Flexible Alternating Current Transmission System |
| FDI | False Data Injection |
| GA | Genetic Algorithm |
| G2V | Grid-to-Vehicle |
| HIL | Hardware-in-the-Loop |
| IEC 61850 | International Electrotechnical Commission standard for power utility communication networks and systems |
| IRR | Internal Rate of Return |
| LSTM | Long Short-Term Memory |
| MARL | Multi-Agent Reinforcement Learning |
| MIL | Model-in-the-Loop |
| MPC | Model Predictive Control |
| MSE | Mean Squared Error |
| NPV | Net Present Value |
| ONNX | Open Neural Network Exchange |
| OPSD | Open Power System Data |
| PHIL | Power Hardware-in-the-Loop |
| PIL | Processor-in-the-Loop |
| PINN | Physics-Informed Neural Network |
| PMU | Phasor Measurement Unit |
| PSO | Particle Swarm Optimisation |
| PTP | Precision Time Protocol (IEEE 1588) |
| PV | Photovoltaic |
| PV curve | Power–Voltage characteristic used in voltage stability analysis |
| QIRL | Quantum-Inspired Reinforcement Learning |
| QSTS | Quasi-Static Time Series (simulation) |
| RT-LAB | OPAL-RT real-time simulation software environment |
| ROI | Return on Investment |
| SCADA | Supervisory Control and Data Acquisition |
| SIL | Software-in-the-Loop |
| SoC | State of Charge |
| STATCOM | Static Synchronous Compensator |
| SVC | Static Var Compensator |
| TCSC | Thyristor-Controlled Series Capacitor |
| TD3 | Twin Delayed Deep Deterministic Policy Gradient |
| TSO | Transmission System Operator |
| UPFC | Unified Power Flow Controller |
| V2G | Vehicle-to-Grid |
| V2H | Vehicle-to-Home |
| V2X | Vehicle-to-Everything |
| WLS | Weighted Least Squares |
