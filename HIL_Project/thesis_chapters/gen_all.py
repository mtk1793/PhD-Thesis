import docx
from docx import Document
from docx.shared import Pt
import os

OUT = os.path.dirname(os.path.abspath(__file__))

def setup(title):
    doc = Document()
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(12)
    doc.add_heading(title, 1)
    return doc

def refs(doc, items):
    doc.add_heading("References", 2)
    for i in items:
        doc.add_paragraph(i, "List Bullet")

def save(doc, name):
    p = os.path.join(OUT, name)
    doc.save(p)
    print("Saved: " + p)

def add_list(doc, items):
    for i in items:
        doc.add_paragraph(i, "List Bullet")

def ch2():
    doc = setup("Chapter2: Literature Review")
    doc.add_paragraph("Comprehensive review with new Section 2.8 on real-time HIL validation.")
    secs = [
        ("2.1 Evolution of AI in Power Systems", ["Expert systems","Neural networks","Deep learning","Reinforcement learning"]),
        ("2.2 FACTS Devices", ["SVC","STATCOM","TCSC","UPFC"]),
        ("2.3 AI for Decision-Making", ["Deep RL","Safe RL","MPC","PINNs"]),
        ("2.4 EV V2G/G2V", ["G2V","V2G","V2H/V2X","Bidirectional chargers"]),
        ("2.5 Brain-Inspired AI", ["Dual-process","Artificial amygdala","Artificial prefrontal cortex","Neuromorphic"]),
        ("2.6 DER Integration", ["Centralized","Hierarchical","Distributed","P2P","Transactive"]),
        ("2.7 Gap Analysis", ["Multi-timescale","Uncertainty","Reactive control","T-D coordination","Interpretability","Scalability","Validation"]),
    ]
    for sec, items in secs:
        doc.add_heading(sec, 2)
        add_list(doc, items)
    doc.add_heading("2.8 Real-Time Simulation and HIL Validation [NEW]", 2)
    doc.add_paragraph("New section covering OPAL-RT, ePHASORSIM, and HIL validation gaps.")
    refs(doc, ["[1] OPAL-RT (2024). Power HIL platform.","[2] Golestan et al. (2024). ePHASORSIM. Energies.","[3] DESL-EPFL (2018). IEEE 39-bus.","[4] MathWorks (2024). Simulink.","[5] Chakraborty (2018). RT validation."])
    save(doc, "Chapter2_Literature_Review.docx")

def ch3():
    doc = setup("Chapter3: Proposed AI-Driven Control Framework")
    doc.add_paragraph("CAPSM framework with new Section3.10 on HIL-ready architecture.")
    secs = [
        ("3.1 Framework Overview", ["Cognitive Duality","Hierarchical Coordination","Adaptive Learning"]),
        ("3.2 Dual-Process", ["System1 CNN-LSTM","System2 QIRL","Metacognitive arbitration"]),
        ("3.3 Multi-Layer", ["Device Level","Regional Level","System Level"]),
        ("3.4 Mathematical Modeling", ["FACTS","EV fleet","DER","Power flow"]),
        ("3.5 Quantum-Inspired RL", ["Superposition","Rotation gates","Tunneling"]),
        ("3.6 Multi-Modal Fault Detection", ["Signal/feature/decision fusion","Attention"]),
        ("3.7 Coordinated Control", ["Voltage stability","Congestion","Loss","Frequency"]),
        ("3.8 Practical Implementation", ["Distributed","Communication","EMS/DMS","Scalability"]),
    ]
    for sec, items in secs:
        doc.add_heading(sec, 2)
        add_list(doc, items)
    doc.add_heading("3.9 Summary", 2)
    doc.add_paragraph("Transition to Chapter4 and Chapter10.")
    doc.add_heading("3.10 HIL-Ready Architecture [NEW]", 2)
    doc.add_paragraph("Maps CAPSM onto real-time hardware.")
    refs(doc, ["[1] OPAL-RT eMEGASIM.","[2] MathWorks Simulink Real-Time."])
    save(doc, "Chapter3_Proposed_Framework.docx")

def ch4():
    doc = setup("Chapter4: Advanced AI Control Architecture")
    doc.add_paragraph("Detailed CAPSM implementation with new Section4.7.")
    secs = [
        ("4.1 System Design", ["Temporal","Uncertainty","Control Strategy","System Integration","Interpretability","Knowledge","Scalability","Validation","Implementation","Security"]),
        ("4.2 Brain-Inspired AI", ["Dual-process","Amygdala","Prefrontal cortex","Metacognitive"]),
        ("4.3 Multi-Layer", ["Device","Regional","System"]),
        ("4.4 Data Flow", ["Acquisition","Estimation","Decision support","Execution","Feedback"]),
        ("4.5 Real-Time Adaptation", ["Online learning","Transfer learning","Monitoring","Tuning"]),
    ]
    for sec, items in secs:
        doc.add_heading(sec, 2)
        add_list(doc, items)
    doc.add_heading("4.6 Validation", 2)
    doc.add_paragraph("Multi-layer validation including Controller-HIL.")
    doc.add_heading("4.7 Computational Implementation [NEW]", 2)
    doc.add_paragraph("System1 on FPGA, System2 as RT task, Metacognitive interface.")
    refs(doc, ["[1] OPAL-RT eFPGASIM.","[2] MathWorks Simulink Real-Time."])
    save(doc, "Chapter4_Advanced_AI_Control_Architecture.docx")

def ch5():
    doc = setup("Chapter5: AI-Based Optimal Placement and Parameter Tuning")
    doc.add_paragraph("AI-based placement with new Section5.8.")
    secs = [
        ("5.1 Optimization", ["Power loss","Voltage stability","Investment cost","Load balancing","Carbon emissions"]),
        ("5.2 GA Placement", ["Chromosome","Genetic operators","Fitness","Diversity"]),
        ("5.3 PSO Tuning", ["Adaptive velocity","Swarm intelligence","Multi-swarm"]),
        ("5.4 DRL Controller", ["TD3","Safety-constrained","Adaptive exploration"]),
        ("5.5 Quantum RL for OPF", ["Quantum state","Operators","Hybrid"]),
        ("5.6 Transfer Learning", ["Graph-based","Domain adaptation","Fine-tuning"]),
    ]
    for sec, items in secs:
        doc.add_heading(sec, 2)
        add_list(doc, items)
    doc.add_heading("5.7 Summary", 2)
    doc.add_paragraph("Transition to Chapter6 and Chapter10.")
    doc.add_heading("5.8 HIL-Validated Placement [NEW]", 2)
    doc.add_paragraph("Offline-to-HIL consistency check.")
    refs(doc, ["[1] MATPOWER test cases.","[2] OPAL-RT HIL validation."])
    save(doc, "Chapter5_AI_Based_Optimal_Placement.docx")

def ch7():
    doc = setup("Chapter7: Fault Detection and Localization")
    doc.add_paragraph("CAPSM fault detection with new Section7.6.")
    secs = [
        ("7.1 AI Fault Localization", ["Evolution","CNN/LSTM/Transformer"]),
        ("7.2 Multi-Modal Fusion", ["Signal/feature/decision","Attention"]),
        ("7.3 Anomaly Detection", ["Isolation Forest","Autoencoders","EVT","One-Class"]),
        ("7.4 Classification", ["CNN-LSTM","Feature importance","Transfer learning"]),
        ("7.5 Response Time", ["Compression","Acceleration","Edge","Real-time"]),
    ]
    for sec, items in secs:
        doc.add_heading(sec, 2)
        add_list(doc, items)
    doc.add_heading("7.6 HIL Validation [NEW]", 2)
    doc.add_paragraph("Real-time fault injection, sub-10ms detection.")
    refs(doc, ["[1] OPAL-RT fault injection.","[2] Kezunovic Smart Fault."])
    save(doc, "Chapter7_Fault_Detection_Localization.docx")

def ch8():
    doc = setup("Chapter8: EV Integration and DER Management")
    doc.add_paragraph("EV/DER integration with new Section8.7.")
    secs = [
        ("8.1 EV Fleet Modeling", ["Aggregate","Stochastic","Degradation","SoC","Charging behavior"]),
        ("8.2 V2G/G2V", ["Bidirectional","Power electronics","Transition","Economic"]),
        ("8.3 Frequency Regulation", ["Primary/secondary","Aggregator","Real-time"]),
        ("8.4 Load Forecasting", ["TCN-Transformer","Probabilistic","Ensemble"]),
        ("8.5 DER Coordination", ["Hierarchical","Multi-agent","Market","Grid service"]),
    ]
    for sec, items in secs:
        doc.add_heading(sec, 2)
        add_list(doc, items)
    doc.add_heading("8.6 Summary", 2)
    doc.add_paragraph("Transition to Chapter9.")
    doc.add_heading("8.7 HIL Validation [NEW]", 2)
    doc.add_paragraph("EV V2G with IEEE 39-bus, coordinated on 4-core OPAL-RT.")
    refs(doc, ["[1] OPAL-RT EV V2G.","[2] MathWorks #182226."])
    save(doc, "Chapter8_EV_Integration_DER_Management.docx")

def ch11():
    doc = setup("Chapter11: Results and Performance Analysis")
    doc.add_paragraph("Results across offline + Controller-HIL.")
    doc.add_heading("11.1-11.4 Offline Results", 2)
    add_list(doc, ["37.2% voltage stability","61.4% response","20-33% CCT","28.5% loading","99.6% detection","9.7ms","1.73% localization"])
    doc.add_heading("11.5-11.10 Controller-HIL [NEW]", 2)
    add_list(doc, ["4-core validated","Sub-10ms fault","FACTS 50us","V2G verified","Safe Mode FDI","Offline-to-HIL gap"])
    doc.add_heading("11.11 Summary", 2)
    add_list(doc, ["37% response","42% stability","95.8% accuracy","12.4% cost","4-core HIL"])
    refs(doc, ["[1] IEEE C37.118","[2] OPAL-RT ePHASORSIM","[3] DESL-FL 39-bus","[4] Kroposki","[5] Golestan HIL"])
    save(doc, "Chapter11_Results_Performance_Analysis.docx")

def ch13():
    doc = setup("Chapter13: Conclusions and Future Work")
    doc.add_paragraph("Summary with HIL elevated to contribution.")
    doc.add_heading("13.1 Key Findings", 2)
    add_list(doc, ["37% response","94% convergence","96.8% stability","68% localization","64% voltage","Sub-10ms HIL"])
    doc.add_heading("13.2 Contributions", 2)
    add_list(doc, ["C1-C7","C8 HIL [ELEVATED]","C9 Transfer"])
    doc.add_heading("13.3 Limitations", 2)
    add_list(doc, ["Validation","Test systems","EV/DER","Computational","Communication","Implementation","Regulatory"])
    doc.add_heading("13.4 Future", 2)
    add_list(doc, ["Short-term","Medium-term","Long-term"])
    doc.add_heading("13.5 Industry Roadmap", 2)
    add_list(doc, ["Phase1 advisory","Phase2 limited","Phase3 integrated","Phase4 advanced"])
    doc.add_heading("13.6 Concluding", 2)
    doc.add_paragraph("CAPSM bridges AI to practice via Controller-HIL.")
    refs(doc, ["[1] Kroposki","[2] OPAL-RT HIL","[3] Rudin"])
    save(doc, "Chapter13_Conclusions_Future_Work.docx")

if __name__ == "__main__":
    print("Generating all chapters...")
    for fn in [ch2,ch3,ch4,ch5,ch7,ch8,ch11,ch13]:
        fn()
    print("All chapters generated!")
