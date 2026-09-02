"""
Generate Chapter10 Word document - HIL Testing and Validation Framework.
MAJOR EXPANSION (3x length) - this is the HIL core chapter.
"""
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
import os

def create_chapter10():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    doc.add_heading('Chapter10: Testing and Validation Framework', level=1)

    doc.add_paragraph(
        'This chapter addresses the critical gap between theoretical advances in AI-driven power '
        'system control and their practical implementation. Building upon the CAPSM framework '
        'presented in Chapter3 and the various control methodologies outlined in preceding chapters, '
        'this chapter develops a comprehensive testing and validation framework that encompasses '
        'three progressive stages: offline Python simulation, Simulink model preparation, '
        'and Controller-Hardware-in-the-loop (HIL) testing on a 4-core OPAL-RT real-time simulator. '
        'The framework ensures that the theoretical advances developed in previous chapters can be '
        'translated into practical technologies with quantifiable benefits for modern power systems.'
    )

    # 10.1
    doc.add_heading('10.1 Three-Stage Validation Methodology', level=2)
    doc.add_paragraph(
        'The validation framework employs a three-stage progressive approach that systematically '
        'validates the CAPSM system from concept to real-time deployment. Each stage '
        'introduces increasing realism and computational constraints, ensuring that issues '
        'are identified at the earliest possible stage.'
    )

    doc.add_heading('Stage 1: Offline Python Simulation', level=3)
    doc.add_paragraph(
        'The first stage uses PYPOWER as the primary power flow solver, wrapped in a '
        'Quasi-Static Time Series (QSTS) simulation environment with OpenAI Gym-like interfaces. '
        'This stage enables rapid iteration of CAPSM control algorithms (System-1 CNN-LSTM and '
        'System-2 QIRL) without real-time constraints. Real-world load and renewable '
        'generation profiles from Open Power System Data (OPSD) provide realistic variability. '
        'The GridEnvironment class encapsulates the QSTS loop, loading time-series data, '
        'applying control actions, and solving AC power flow at each time step.'
    )
    doc.add_paragraph(
        'Key deliverables from Stage1 include: trained CAPSM System-1 and System-2 policies, '
        'baseline performance metrics across all IEEE test systems (9, 14, 39, 118, 300 bus), '
        'and a comprehensive scenario database covering normal operation, faults, '
        'renewable intermittency, and cyber-attacks.'
    )

    doc.add_heading('Stage 2: Simulink Model Preparation', level=3)
    doc.add_paragraph(
        'The second stage transitions from the Python offline environment to high-fidelity '
        'Simulink models that can be deployed on real-time simulators. This stage '
        'involves acquiring and adapting IEEE standard test system models, integrating '
        'FACTS device subsystems and EV V2G/G2V charger models, and configuring '
        'the models for the target real-time platform.'
    )
    doc.add_paragraph(
        'The primary IEEE 39-bus Simulink model was acquired from the DESL-EPFL GitHub '
        'repository, which was specifically built for the OPAL-RT eMegaSim real-time simulation '
        'platform. This model includes dynamic load profiles (20ms resolution) and conventional '
        'generation dynamics, making it directly suitable for HIL deployment.'
    )
    doc.add_heading('Simulink Model Integration', level=3)
    for item in [
        'IEEE 9-bus: MathWorks Simscape Electrical built-in example, configured for RT-LAB',
        'IEEE 39-bus: DESL-EPFL model (OPAL-RT eMegaSim native), updated for current MATLAB version',
        'IEEE 118-bus: Built programmatically via Simulink API from MATPOWER case data',
        'FACTS devices: SVC at Bus 14, STATCOM at Bus 39, TCSC on Line 16-17, UPFC at Bus 26',
        'EV V2G fleet: 3 bidirectional charging stations at Buses 3, 8, 15',
    ]:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('Stage 3: Controller-HIL on 4-Core OPAL-RT', level=3)
    doc.add_paragraph(
        'The third and final stage deploys the CAPSM controllers on real-time hardware. '
        'The 4-core OPAL-RT simulator (OP5700 or OP4510) runs the IEEE grid model in '
        'real-time while the CAPSM System-1 (CNN-LSTM) and System-2 (QIRL) algorithms '
        'execute as real-time software tasks on the simulator CPUs. The Metacognitive '
        'Arbitration layer coordinates between the two systems and the I/O interface.'
    )
    doc.add_paragraph(
        'This stage reveals timing constraints, communication latencies, and computational '
        'limitations that are invisible in offline simulation, providing the critical '
        'evidence that HIL validation is essential for translating AI control into practice.'
    )

    # 10.2
    doc.add_heading('10.2 Simulation Platform Development', level=2)
    doc.add_paragraph(
        'The first step in validating the CAPSM framework is the development of a comprehensive '
        'simulation platform that accurately represents the behavior of modern power systems '
        'with high penetration of FACTS devices, EV fleets, and DERs.'
    )

    doc.add_heading('Power System Simulation Tools', level=3)
    for tool in [
        'Power Flow and Transient Stability: PYPOWER (Python) for offline, MATPOWER/Simulink for HIL',
        'FACTS Device Models: Simscape Electrical with EMT models of SVC, STATCOM, TCSC, UPFC',
        'EV and DER Simulation: Custom bidirectional DC-DC converter models with PLL synchronization',
        'Communication Network: NS-3 for offline, IEC 61850 for HIL',
        'AI Framework: PyTorch (offline), TensorFlow/PyTorch on OPAL-RT FPGA (HIL)',
    ]:
        doc.add_paragraph(tool, style='List Bullet')

    doc.add_paragraph(
        'These components are integrated through a custom middleware layer that synchronizes '
        'data exchange and temporal progression across the different simulation environments.'
    )

    # 10.3
    doc.add_heading('10.3 Digital Twin Creation Methodology', level=2)
    doc.add_paragraph(
        'Digital twins provide a bridge between simulation and physical implementation by '
        'creating high-fidelity virtual replicas of physical assets that can operate in '
        'parallel with real assets. The digital twin implementation for CAPSM follows '
        'a layered architecture with varying fidelity levels.'
    )

    doc.add_heading('Fidelity Levels', level=3)
    for level in [
        'Level 1 - Functional: Black-box models capturing input-output relationships for non-critical components',
        'Level 2 - Behavioral: Grey-box models capturing dynamic behavior for secondary control loops',
        'Level 3 - Detailed: White-box models with comprehensive physical representations for critical FACTS devices',
        'Level4 - High-Precision: Circuit-level models including parasitics and nonlinearities for power electronics',
    ]:
        doc.add_paragraph(level, style='List Number')

    # 10.4
    doc.add_heading('10.4 Hardware-in-the-Loop Testing Architecture', level=2)
    doc.add_paragraph(
        'Hardware-in-the-Loop (HIL) testing represents a critical step in validating the CAPSM '
        'framework by integrating the real-time simulator with the CAPSM control algorithms. '
        'Since the target platform is a 4-core OPAL-RT simulator without separate controller '
        'boards, the CAPSM System-1 and System-2 run as real-time software tasks on the '
        'simulator CPUs themselves.'
    )

    doc.add_heading('4-CPU Core Allocation', level=3)
    doc.add_paragraph(
        'The 4 CPUs are allocated as follows to balance computational load with '
        'real-time constraints:'
    )

    cores = [
        'Core 1 (sm_master): North region (Buses 1-19) + System-1 CNN-LSTM - 5ms task time, highest priority (protection-level)',
        'Core 2 (sm_slave1): South region (Buses 20-39) + System-2 QIRL - 50ms task time, medium priority',
        'Core 3 (sm_slave2): CAPSM Arbitration + Communication - 10ms task time, coordination priority',
        'Core 4 (sm_slave3): I/O + Logging + HIL Interface - 1ms task time, lowest priority',
    ]
    for core in cores:
        doc.add_paragraph(core, style='List Bullet')

    doc.add_heading('Solver Configuration', level=3)
    doc.add_paragraph(
        'The ARTEMIS solver is configured for electromagnetic transient (EMT) simulation '
        'with a 50 microsecond time step for the grid model. For larger systems '
        '(118-bus and above), a hybrid approach uses ePHASORSIM (1ms phasor domain) for '
        'the bulk of the network while reserving EMT for sub-networks containing FACTS '
        'devices and critical control interfaces.'
    )

    doc.add_heading('Communication Infrastructure', level=3)
    for comm in [
        'Field level: IEC 61850 (4ms latency) for device-level communication',
        'Regional level: IEEE C37.118 (20ms latency) for PMU data',
        'System level: Secure TCP/IP (100ms latency) for system-wide coordination',
        'Synchronization: IEEE 1588 PTP providing sub-microsecond timing accuracy',
        'Cybersecurity: TLS encryption, authentication, intrusion detection for all HIL communication',
    ]:
        doc.add_paragraph(comm, style='List Bullet')

    # 10.5
    doc.add_heading('10.5 Real-Time Task Scheduling', level=2)
    doc.add_paragraph(
        'The real-time implementation follows a task scheduling approach that ensures '
        'critical control functions meet their timing constraints. The scheduling '
        'uses a rate-monotonic priority assignment where shorter period tasks receive higher priority.'
    )
    doc.add_paragraph(
        'The worst-case response time for each task is computed using the rate-monotonic '
        'analysis, accounting for interference from higher-priority tasks. The analysis '
        'ensures that the System-1 inference (5ms target), System-2 optimization (50ms target), '
        'and Arbitration decisions (10ms target) all meet their deadlines on the 4-core OPAL-RT.'
    )

    # 10.6
    doc.add_heading('10.6 Scenario Design for HIL', level=2)
    doc.add_paragraph(
        'A comprehensive set of HIL test scenarios has been developed to evaluate the '
        'CAPSM framework under diverse real-time conditions. These scenarios '
        'are derived from the offline scenario database and adapted for real-time execution.'
    )

    doc.add_heading('Test Scenarios', level=3)
    scenarios = [
        ('Normal Operation', '3600s duration, daily load variations, renewable fluctuations, EV charging patterns'),
        ('Fault Test', '60s duration, three-phase fault at Bus 14, verifies sub-10ms detection time on HIL'),
        ('Renewable Intermitency', '120s duration, 60% wind generation drop, verifies System-1 fast response on HIL'),
        ('Cyber Attack (FDI)', '60s duration, false data injection at Buses 5,10, verifies Safe Mode activation on HIL'),
        ('EV V2G Coordination', '300s duration, V2G/G2V mode switching, verifies coordinated frequency regulation on HIL'),
    ]
    for name, desc in scenarios:
        doc.add_paragraph(f'{name}: {desc}', style='List Bullet')

    # 10.7
    doc.add_heading('10.7 Progressive Validation: MIL to SIL to PIL to CHIL', level=2)
    doc.add_paragraph(
        'The progressive validation process implements a V-model approach that matches '
        'verification activities to development stages. Each stage builds upon previous '
        'results and introduces additional complexity and realism:'
    )
    stages = [
        'Model-in-the-Loop (MIL): Pure Python/PYPOWER simulation with idealized interfaces - validates algorithms',
        'Software-in-the-Loop (SIL): Simulink model with realistic computational constraints but simplified interfaces',
        'Processor-in-the-Loop (PIL): CAPSM software deployed to OPAL-RT CPU targets with emulated I/O',
        'Hardware-in-the-Loop (HIL): Full real-time simulation on 4-core OPAL-RT with actual I/O hardware',
        'Field Testing: Final validation on real system testbed with all physical components (future work)',
    ]
    for stage in stages:
        doc.add_paragraph(stage, style='List Number')

    # 10.8
    doc.add_heading('10.8 Automated Regression Testing', level=2)
    doc.add_paragraph(
        'To ensure consistency and efficiency, the validation framework implements automated '
        'regression testing across all platforms. Test automation scripts '
        'execute test cases across all stages with minimal manual intervention. '
        'Continuous integration validates code changes against core test cases to identify regressions early.'
    )

    # 10.9
    doc.add_heading('10.9 Comprehensive Validation Metrics and Reporting', level=2)
    doc.add_paragraph(
        'The validation metrics are organized in a hierarchical framework that links detailed '
        'technical measurements to higher-level performance indicators relevant '
        'to business and operational objectives.'
    )

    doc.add_heading('Metric Levels', level=3)
    metrics = [
        'Level1 - Technical Detail: Control loop response times, stability margins, state estimation errors',
        'Level 2 - Functional Performance: Voltage regulation effectiveness, congestion management success',
        'Level3 - Operational Impact: Reliability improvements, reduced curtailment, increased DER utilization',
        'Level4 - Business Value: Cost savings, deferred infrastructure investment, improved service quality',
    ]
    for level in metrics:
        doc.add_paragraph(level, style='List Number')

    # 10.10 Summary
    doc.add_heading('10.10 Summary', level=2)
    doc.add_paragraph(
        'This chapter has presented a comprehensive three-stage testing and validation '
        'framework for the CAPSM system, addressing the critical gap between theoretical '
        'advances and practical implementation. The key contributions include:'
    )
    for contrib in [
        'Development of an integrated offline Python simulation platform using PYPOWER with OPSD real-world data',
        'Establishment of a digital twin methodology with multi-fidelity models for parallel operation',
        'Design of a 4-core Controller-HIL architecture on OPAL-RT with ARTEMIS solver (50us EMT)',
        'Implementation of real-time task scheduling with rate-monotonic priority assignment',
        'Creation of five HIL test scenarios covering normal, fault, renewable, cyber, and EV V2G conditions',
        'Integration of progressive MIL-SIL-PIL-CHIL validation with automated regression testing',
    ]:
        doc.add_paragraph(contrib, style='List Bullet')

    doc.add_paragraph(
        'The next chapter will present the comprehensive results obtained through the '
        'application of this testing and validation framework, demonstrating the '
        'performance of the CAPSM system across both offline simulation and Controller-HIL '
        'on the 4-core OPAL-RT real-time simulator.'
    )

    # References
    doc.add_heading('References', level=2)
    refs = [
        '[1] Palmintier, B., et al. (2017). HELICS: High-performance transmission-distribution-communication-market co-simulation framework.',
        '[2] DESL-EPFL (2018). IEEE 39-bus power system Simulink model for OPAL-RT eMegaSim.',
        '[3] OPAL-RT Technologies (2024). ePHASORSIM: Real-time phasor-based simulation. Documentation.',
        '[4] MathWorks (2024). Power Systems Studies with Simulink and Simscape Electrical. Webinar.',
        '[5] Golestan, S., et al. (2024). Real-Time Simulation and HIL Testing Based on OPAL-RT ePHASORSIM. Energies, 17(19), 4893.',
    ]
    for r in refs:
        doc.add_paragraph(r, style='List Bullet')

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Chapter10_Testing_Validation_Framework.docx')
    doc.save(out_path)
    print(f'Saved: {out_path}')
    return out_path

if __name__ == '__main__':
    create_chapter10()
