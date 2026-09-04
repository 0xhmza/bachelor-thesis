import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "RUB Cybersecurity Theses"

# Styling
header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
hot_fill_5 = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')  # green - sehr hot
hot_fill_4 = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')  # yellow - hot
hot_fill_3 = PatternFill(start_color='F4B4C2', end_color='F4B4C2', fill_type='solid')  # light red - medium
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
wrap_alignment = Alignment(wrap_text=True, vertical='top')

headers = [
    "Nr.",
    "Chair / Professor",
    "Title / Topic (Original Language)",
    "Type (BA/MA)",
    "Cybersecurity Field",
    "Subfield",
    "Hotness (1-5)",
    "Language",
    "Full Description / Motivation & Research Problem",
    "Requirements / Prerequisites",
    "Supervisor / Contact",
    "Status",
    "Source URL"
]

for col_idx, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    cell.border = thin_border

# Column widths
col_widths = [5, 28, 55, 10, 28, 28, 10, 8, 65, 50, 35, 15, 45]
for i, w in enumerate(col_widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Freeze header
ws.freeze_panes = 'A2'

# Auto-filter
ws.auto_filter.ref = f"A1:M1"

# ---- DATA ----
thesis_data = [
    # ============================================
    # Security Engineering (Tim Güneysu)
    # ============================================
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Automated and Formal Hardware Security Verification",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Formal Verification / Hardware Security",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Automated hardware security verification has become essential for building trust in cryptographic designs and embedded systems. However, most tools struggle with complex real-world designs and advanced security notions.\n\nRESEARCH PROBLEM: Existing approaches (SMT/SAT-based analyses, BDDs/MTBDDs) often require simplifying assumptions or hit scalability limits. Need for modular, automated verification techniques that handle complex architectures and support advanced security models.",
        "reqs": "Strong interest in cryptography, implementation security (SCA/FIA), and formal methods. Solid background in discrete math, logic, probability, and programming (C/C++/Rust/Python/Sage). Familiarity with automated reasoning (SMT/SAT, model checking) or proof assistants (Coq/Isabelle/F*) beneficial.",
        "contact": "Dr.-Ing. Pascal Sasdrich (pascal.sasdrich@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Automated and Security-Aware Design Space Exploration in Hardware",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Cryptographic Engineering / Design Automation",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: With increasing complexity of modern cryptography (especially PQC) and physical implementation attacks, the design space of efficient hardware instances often grows exorbitantly.\n\nYOUR TASK: Extend the HADES-framework by adding templates (e.g., for symmetric cryptography like PRESENT) or implementing new features in the backend. Possible tasks: new templates for symmetric cryptography (LED, Skinny, Speedy), designing templates for PQC (Dilithium, MAYO), adding performance metrics, optimizing randomness usage for side-channel protection.",
        "reqs": "Tool is written in Scala and SpinalHDL. Experience with hardware implementations (VHDL/Verilog/SpinalHDL) and object-oriented programming (Scala/Java/C++).",
        "contact": "Fabian Buschkowski (fabian.buschkowski@rub.de) or Niklas Höher (niklas.hoeher@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Combined Physical Implementation Security",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Side-Channel Analysis / Fault Injection",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Combined Analysis (CA) exploits information leakage (SCA) and induced faults (FIA) simultaneously to bypass defenses that protect against either class in isolation.\n\nRESEARCH PROBLEM: Many countermeasures either provide leakage resilience or fault tolerance, while their security guarantees rarely compose cleanly. Need for novel models and implementations of countermeasures that simultaneously address leakage and faults.",
        "reqs": "Interest in applied cryptography and cryptographic engineering. Solid programming (C/C++/Rust/Python) or hardware design (Verilog/VHDL/HCL/HLS) skills beneficial. Exposure to physical implementation attacks (SCA/FIA) beneficial.",
        "contact": "Dr.-Ing. Pascal Sasdrich (pascal.sasdrich@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Implementation and Side-Channel Security of Multivariate Quadratic Signature Schemes",
        "type": "BA/MA",
        "field": "Post-Quantum Cryptography",
        "subfield": "Implementation Security / Side-Channel",
        "hotness": 5,
        "lang": "EN",
        "desc": "MOTIVATION: NIST has announced several PQC schemes to be standardized. A fourth round will open for signature schemes that are not based on lattice assumptions, including several based on multivariate quadratic assumptions.\n\nYOUR TASK: Work on embedded software implementations, hardware implementations, and/or side-channel attacks and countermeasures for multivariate quadratic signature schemes.",
        "reqs": "VHDL, embedded C and Assembly, and/or side-channel analysis (depending on direction).",
        "contact": "Georg Land (georg.land@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Hardware Implementation of Combined Secure Block Ciphers using Code-Based Masking",
        "type": "MA",
        "field": "Hardware Security",
        "subfield": "Side-Channel & Fault Countermeasures",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Physical attacks (SCA and FIA) are major threats to cryptographic hardware. Protecting against both simultaneously is a new field. First attempts combine masking and replication at high area cost.\n\nYOUR TASK: Develop a strategy to secure linear functions of block ciphers against combined attacks using masking and error-correcting codes. Implement one or more full block ciphers (AES, PRESENT) in hardware and evaluate their performance and security.",
        "reqs": "First hardware design experiences, knowledge of physical attacks, general programming skills.",
        "contact": "Elisabeth Krahmer or Fabian Buschkowski",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Hardware Implementation of HAETAE",
        "type": "MA",
        "field": "Post-Quantum Cryptography",
        "subfield": "Hardware Implementation / Lattice-Based Crypto",
        "hotness": 5,
        "lang": "EN",
        "desc": "MOTIVATION: HAETAE was selected as the final algorithm of the Korean PQC competition (KpqC) in January 2025. Like Dilithium, it is a post-quantum digital signature scheme based on lattice problems. No hardware implementation of HAETAE exists yet.\n\nYOUR TASK: Develop a hardware implementation of HAETAE, starting with smaller sub-functions (following Dilithium hardware design where applicable), finishing with the sampling process for hyperball uniform distributions.",
        "reqs": "Experience in hardware design (Verilog) beneficial. Familiarity with lattice-based PQC schemes advantageous.",
        "contact": "Dina Hesse (dina.hesse@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Implementation of a Randomized Cache in Hardware on the RISC-V Rocket Core",
        "type": "MA",
        "field": "Hardware Security",
        "subfield": "Microarchitectural Security / Cache Attacks",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Microarchitectural attacks, particularly cache timing attacks (Spectre, Meltdown) have emerged as significant threats. Randomized caches like ScatterCache have been proposed as countermeasures but no good usable implementations exist.\n\nYOUR TASK: Implement a randomized cache design (e.g., ScatterCache) on the open-source RISC-V Rocket Core using the ChipYard framework. Evaluate speed and area consumption. Ensure reusability.",
        "reqs": "First hardware design experience, general programming skills (Chisel/Scala for hardware design), basic Linux/command line knowledge, basic understanding of CPU designs.",
        "contact": "Moritz Peters (moritz.peters-v41@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Microarchitectural Side Channel Attacks and Countermeasures",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Microarchitectural Attacks / CPU Security",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: The internal hardware of modern CPUs (microarchitecture) was long considered a trust anchor. Recent attacks including Spectre and Meltdown changed this. Aspects range from cache side channel attacks over Rowhammer to speculative execution attacks.\n\nRESEARCH PROBLEM: Design and/or evaluation of attacks and countermeasures. May use the gem5 simulator for evaluation.",
        "reqs": "C/C++ programming skills, basics of x86 assembly, basic understanding of CPU designs (pipeline, caches, etc.).",
        "contact": "Moritz Peters (moritz.peters-v41@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Noise-Robust Deep Learning for Side-Channel Analysis",
        "type": "BA/MA",
        "field": "Side-Channel Analysis",
        "subfield": "Deep Learning / ML for SCA",
        "hotness": 5,
        "lang": "EN",
        "desc": "MOTIVATION: Deep-learning-based side-channel analysis (DL-SCA) has set new benchmarks for extracting secrets from physical leakage. Real-world devices introduce diverse noise sources.\n\nRESEARCH PROBLEM: No systematic, quantitative evaluation of noise effects in DL-SCA. Which noise types most interfere with DL-SCA? How do pre-processing and training strategies trade off accuracy and generalization? This thesis will model and inject controlled noise and analyze its impact on DL-SCA performance.",
        "reqs": "Interest in applied cryptography and machine learning. Solid programming skills in Python beneficial.",
        "contact": "Dina Hesse",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Optimizing a Custom Intermediate Representation (IR) for Attribute-Based Encryption (ABE) Schemes",
        "type": "BA",
        "field": "Cryptographic Engineering",
        "subfield": "Compiler Optimization / ABE",
        "hotness": 3,
        "lang": "EN",
        "desc": "MOTIVATION: At the chair we are developing a compiler for Attribute-based Encryption. This compiler emits a custom IR which models operations typically required in ABE implementations. Currently, generated code is not optimized, resulting in lengthy implementations. Specialized instructions may offer performance boosts.\n\nYOUR TASK: Research existing optimization strategies from literature and conceptually apply them to the custom IR. Implement algorithms as a plugin in Python and evaluate correctness. Evaluate based on code size reduction and performance gains.",
        "reqs": "Familiarity with abstract modeling of programming languages (ASTs, IRs). Experience with Python development. Good foundation in discrete math.",
        "contact": "Sven Argo (sven.argo@ruhr-uni-bochum.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Optimizing Associative Containers by Exploiting Domain-Specific Knowledge",
        "type": "BA/MA",
        "field": "Cryptographic Engineering",
        "subfield": "Data Structures / ABE Performance",
        "hotness": 3,
        "lang": "EN",
        "desc": "MOTIVATION: ABE requires associative containers to handle dynamically sized keys and ciphertexts. Domain-specific knowledge (key format, distribution) can be exploited for speed-ups.\n\nYOUR TASK: Implement (at least two) custom associative containers in Rust which outperform the built-in HashMap by exploiting known key formats and distributions. Evaluate runtime and memory performance.",
        "reqs": "Solid foundation in data structures and performance characteristics. Extensive experience with Rust and memory management. Understanding of discrete math and basic cryptography.",
        "contact": "Sven Argo (sven.argo@ruhr-uni-bochum.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Secure Computation (TLB Countermeasures / ISA Extensions / Fault-Free ISA Designs)",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Processor Security / Secure Architectures",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Many new attacks target both desktop and embedded hardware. Caches can leak information, SPECTRE/MELTDOWN exploit speculative execution, and IoT devices face increasing threats.\n\nRESEARCH: Implement TLB countermeasure into a softcore OOO-CPU, implement an ISA extension against faults in a softcore embedded-grade CPU (with compiler support), or research fault-free ISA designs. Open for student proposals.",
        "reqs": "Experience with hardware description languages, high-level languages for compiler support (depending on direction).",
        "contact": "M.Sc. Florian Stolz (florian.stolz@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Theoretical Adversary Models for Physical Implementation Attacks",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Formal Models / SCA / FIA",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Physical implementation attacks (SCA, FIA) are practical and cost-effective. Security claims often rely on unrealistic assumptions.\n\nRESEARCH PROBLEM: Current models (probing, noisy-leakage for SCA; zeta-/k-injection for FIA; emerging CA models) vary in complexity and rarely compose cleanly. Need parameterized, formal adversary models with well-defined relations between models. Includes proving implications/separations, defining simulation-/game-based security notions, and establishing composability results.",
        "reqs": "Strong interest in cryptography, implementation security (SCA/FIA), and formal reasoning. Solid background in discrete math, logic, probability, and programming (Python/Sage). Experience with formal methods or proof assistants is a plus.",
        "contact": "Dr.-Ing. Pascal Sasdrich (pascal.sasdrich@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Security Engineering (Prof. Tim Güneysu)",
        "title": "Tooling for Physical Implementation Security",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Design Automation / SCA/FIA Countermeasures",
        "hotness": 4,
        "lang": "EN",
        "desc": "MOTIVATION: Rising complexity of modern embedded systems, combined with manual integration of countermeasures, creates vulnerability to physical attacks. Current manual design methods are time-consuming, error-prone, and unable to scale.\n\nRESEARCH PROBLEM: Lack of constructive tooling for physical implementation security. Goal is to develop automated tooling that enables creation of secure embedded systems by automatically integrating SCA/FIA and/or CA countermeasures.",
        "reqs": "Strong interest in embedded security, computer architecture, and design automation. Solid programming (C/C++/Rust/Python) or hardware design (Verilog/VHDL/HCL/HLS) skills beneficial. Exposure to physical implementation attacks beneficial.",
        "contact": "Dr.-Ing. Pascal Sasdrich (pascal.sasdrich@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/seceng/lehre/abschlussarbeiten/"
    },

    # ============================================
    # System Security (Katharina Kohls)
    # ============================================
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Controlling a Robotic Arm with 5G",
        "type": "BA/MA",
        "field": "Mobile Network Security",
        "subfield": "5G Campus Networks / Industrial Security",
        "hotness": 4,
        "lang": "EN",
        "desc": "Industrial facilities use 5G campus networks to control production units. Compared to WiFi, 5G campus networks benefit from security and performance capabilities. However, series of attacks enable adversaries to interfere with 5G network components.\n\nBuild a demonstrator setup with a robotic arm and a 5G network component. 3D-print a suitable model, assemble it, connect to 5G lab network. Setup a toy example to control the robotic arm through 5G. Conduct security analysis and reflect on requirements in an industrial 5G campus network.",
        "reqs": "(Not explicitly stated - inquire with chair)",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Location Verification in Car2X Communication",
        "type": "MA",
        "field": "Mobile Network Security",
        "subfield": "V2X / Location Security / 5G",
        "hotness": 4,
        "lang": "EN",
        "desc": "Cars exchange information with vehicles, roadside units, or pedestrians via 5G. Communication is decentralized (no infrastructure needed). Correctness of exchanged location information is crucial - manipulation can affect safety of traffic participants.\n\nImplement a simulation model imitating information exchange between mobile participants in traffic. As evaluation, implement a verification mechanism that validates location information of vehicles.",
        "reqs": "(Not explicitly stated - inquire with chair)",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Biased Overlay Networks",
        "type": "BA/MA",
        "field": "Privacy / Anonymity",
        "subfield": "Overlay Networks / Tor / Internet Infrastructure",
        "hotness": 4,
        "lang": "EN",
        "desc": "Overlay networks (e.g., Tor) provide additional security and privacy for online connections. Protection level depends on the infrastructure of the underlying network. If traffic is routed through countries that monitor/censor Tor, transmissions are more likely targeted by attacks.\n\nAnalyze the bias that Internet infrastructure introduces for overlay networks using empirical information of the Internet. Implement a simulation model and analyze how the Internet influences security and privacy of connections.",
        "reqs": "(Not explicitly stated - inquire with chair)",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "AI-based Network Planning for Secure 6G Campus Networks",
        "type": "MA",
        "field": "Mobile Network Security",
        "subfield": "6G Security / AI for Network Planning",
        "hotness": 5,
        "lang": "EN",
        "desc": "Network planning strongly impacts both performance and security of mobile networks. Poor placement of base stations may enable attacks such as IMSI-Catchers or rogue base stations. AI-based optimization can help design topologies that minimize risks while maintaining performance.\n\nTasks: Literature study on network planning and security metrics; build a simulation model of campus networks; design and train an ML algorithm for secure cell placement; evaluate against realistic attack and usage scenarios.",
        "reqs": "ns-3, Python (TensorFlow/PyTorch), cellular networks knowledge (5G/6G), machine learning.",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Deep Learning for Anomaly Detection in the 6G Core",
        "type": "MA",
        "field": "Mobile Network Security",
        "subfield": "6G Core Security / ML Anomaly Detection",
        "hotness": 5,
        "lang": "EN",
        "desc": "The 6G core network is a critical target for attacks such as denial-of-service or rogue functions. Classical intrusion detection systems struggle with scalability. Deep learning-based anomaly detection promises more robust protection.\n\nTasks: Analyze 6G core functions and attack vectors; collect or generate relevant network traffic data; implement and train DL-based anomaly detection models (Autoencoder, RNN, CNN); benchmark performance against classical IDS methods.",
        "reqs": "Python, TensorFlow/Keras, Mininet/Open5GS, network security.",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Simulation and Analysis of Attack Scenarios in 6G Network Structures",
        "type": "MA",
        "field": "Mobile Network Security",
        "subfield": "6G Attack Simulation / Threat Modeling",
        "hotness": 5,
        "lang": "EN",
        "desc": "6G networks will be highly complex, making realistic attack simulations (IMSI-Catcher, rogue base stations, traffic injection) essential for evaluating countermeasures. Systematic simulation of such scenarios provides valuable data for AI-driven defense mechanisms.\n\nTasks: Model different 6G attack vectors; implement scenarios in a simulator or testbed; analyze impact on confidentiality, integrity, and availability; prepare datasets for ML-based defense methods.",
        "reqs": "ns-3, OpenAirInterface, USRP (SDR), cellular security basics.",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Centralized vs. Decentralized AI Approaches for Network Security",
        "type": "MA",
        "field": "AI for Security",
        "subfield": "Edge AI / 6G / Distributed AI",
        "hotness": 5,
        "lang": "EN",
        "desc": "Deciding whether AI for network security runs centrally (cloud) or decentrally (edge) affects performance, latency, and resilience. The trade-off between cloud-based and edge AI is a hot research topic in 6G with direct implications for secure infrastructures.\n\nTasks: Compare centralized vs. decentralized AI security models; build proof-of-concepts (edge training vs. cloud training); evaluate performance, latency, and energy efficiency; derive architectural recommendations.",
        "reqs": "TensorFlow Lite, Docker/Kubernetes, edge computing basics, distributed systems.",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Implementation and Benchmarking of Classical Traffic Morphing Techniques",
        "type": "BA",
        "field": "Privacy / Anonymity",
        "subfield": "Traffic Analysis / Traffic Morphing",
        "hotness": 3,
        "lang": "EN",
        "desc": "Classical traffic morphing techniques remain foundational for traffic privacy. Their performance and limits need to be understood before integrating quantum-inspired ideas.\n\nImplement traffic morphing strategies (e.g., dummy traffic, timing shifts), run benchmark experiments, and evaluate effectiveness under known traffic analysis attacks.",
        "reqs": "(Not explicitly stated - inquire with chair)",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Frontend for Visualizing Simulated Traffic Traces",
        "type": "BA",
        "field": "Privacy / Anonymity",
        "subfield": "Visualization / Traffic Analysis",
        "hotness": 2,
        "lang": "EN",
        "desc": "Traffic simulations often generate abstract trace files that are hard to interpret. A visual frontend helps researchers understand how protocols affect observable traffic.\n\nDevelop a simple web-based interface for viewing packet timelines, flow diagrams, and adversarial trace reconstructions based on simulation output files.",
        "reqs": "(Not explicitly stated - inquire with chair)",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },
    {
        "chair": "System Security (Prof. Katharina Kohls)",
        "title": "Integration of Adversarial Correlation Attacks into Simulation Testbed",
        "type": "MA",
        "field": "Privacy / Anonymity",
        "subfield": "Traffic Analysis / Correlation Attacks",
        "hotness": 4,
        "lang": "EN",
        "desc": "To evaluate metadata leakage, simulation environments must include realistic adversarial models capable of timing and flow analysis.\n\nImplement correlation-based traffic analysis attacks (e.g., flow linking, burst timing) as modular components in the simulation framework, and provide evaluation scenarios comparing defenses from the SQUID project.",
        "reqs": "(Not explicitly stated - inquire with chair)",
        "contact": "Chair for System Security (syssec)",
        "status": "Offen",
        "url": "https://informatik.rub.de/en/syssec/teaching/"
    },

    # ============================================
    # Information Security (Ghassan Karame)
    # ============================================
    {
        "chair": "Information Security (Prof. Ghassan Karame)",
        "title": "Decentralized Systems Security (Various Topics)",
        "type": "BA/MA",
        "field": "Decentralized Systems / Blockchain",
        "subfield": "Decentralized Security Primitives",
        "hotness": 3,
        "lang": "EN",
        "desc": "Decentralized systems security is receiving considerable attention due to applicability in the financial sector, IoT sector, among others. Tasks: Survey of existing decentralized security technologies, analyze and implement selected technologies, evaluate performance.\n\nPAST TOPICS include: Solana Smart Contract Security, Blockchain-based E-Voting, Front-running attacks on Smart Contracts, BLS Signatures in Blockchain, Selfish Mining Strategies, XRP Ledger Consensus Protocol, LLM-based Smart Contract Security analysis, Anonymity in PoW Blockchain Transactions.",
        "reqs": "Registration in Moodle course required. General background in security/crypto/programming.",
        "contact": "Register to Moodle course (link on website)",
        "status": "Offen",
        "url": "https://informatik.rub.de/infsec/teaching/theses/"
    },
    {
        "chair": "Information Security (Prof. Ghassan Karame)",
        "title": "Machine Learning Security (Various Topics)",
        "type": "BA/MA",
        "field": "AI/ML Security",
        "subfield": "Adversarial ML / ML Vulnerabilities",
        "hotness": 5,
        "lang": "EN",
        "desc": "Advances in machine learning have enabled widespread adoption of AI in critical decision-making. Massive use of ML opens door to unprecedented risks. Goal: Explore and address vulnerabilities of ML in adversarial settings, with focus on security and privacy.\n\nTasks: Survey existing vulnerabilities of ML algorithms from a security/privacy viewpoint; analyze and implement selected technologies to mitigate ML vulnerabilities; evaluate performance.\n\nPAST TOPICS: Adversarial Attacks in Federated Learning, Universal Adversarial Perturbations for CNNs, Backdoor Attacks on Diffusion Models, Adversarial Examples for Autonomous Vehicles, Fingerprinting Libraries for Adversarial Example Attacks, Backdoor Attacks against Personalized FL in NLP.",
        "reqs": "Intermediate familiarity with (adversarial) machine learning. Intermediate programming experience in Python. Optional: PyTorch / TensorFlow.",
        "contact": "Register to Moodle course (link on website)",
        "status": "Offen",
        "url": "https://informatik.rub.de/infsec/teaching/theses/"
    },
    {
        "chair": "Information Security (Prof. Ghassan Karame)",
        "title": "Platform Security (Various Topics - TEEs)",
        "type": "BA/MA",
        "field": "Platform Security / TEE",
        "subfield": "Trusted Execution Environments",
        "hotness": 4,
        "lang": "EN",
        "desc": "Digital platforms bring innovation opportunities by connecting physical and digital objects with the cloud. This opens up new adversarial opportunities. Trusted Execution Environments (TEEs) may mitigate such threats, but they require careful design to meet performance, flexibility and security.\n\nFocus on implementing and evaluating TEE-based solutions for platforms.\n\nPAST TOPICS: TEE-based Smart Contracts, Remote Attestation of Distributed Workloads, Confidential HPC (RDMA for CVMs), AMD SEV Security, TEEs in presence of malicious peripherals, Extending Attestation Primitives for Keystone, TEE-based ML for PPFL.",
        "reqs": "Registration in Moodle course required.",
        "contact": "Register to Moodle course (link on website)",
        "status": "Offen",
        "url": "https://informatik.rub.de/infsec/teaching/theses/"
    },

    # ============================================
    # Software Security (Kevin Borgolte)
    # ============================================
    {
        "chair": "Software Security (Prof. Kevin Borgolte)",
        "title": "Individual Thesis Topics (No Pre-Listed Topics)",
        "type": "BA/MA",
        "field": "Software Security",
        "subfield": "Program Analysis / Fuzzing / Vulnerability Discovery",
        "hotness": 4,
        "lang": "EN",
        "desc": "The chair does not list specific topics. Instead, topics are discussed after application to match student expertise and interests. Past topics include: Analyzing Impact of Software Patches through Symbolic Path Constraints, Detecting TLS Interception in the Wild, Enhancing Fuzzbench for Multi-Core Fuzzing, Fuzzing Online Multiplayer Games, Fuzzing Stateful Systems, Optimization of Resources in Fuzzing Clusters, Signed Certificate Timestamps, Static Binary Analysis for Network Protocol Synthesis.",
        "reqs": "Programming experience in Python, C, C++, or Rust. Experience with Git, LaTeX, and Linux. Background in at least one: static program analysis, dynamic analysis (fuzzing), vulnerability discovery/exploitation, network measurements/protocol analysis, network protocols (TLS, DNS, BGP, IPv6). Preferably taken relevant courses: Software Security 1/2, Internet Security, Network and Data Security, etc.",
        "contact": "applications@softsec.ruhr-uni-bochum.de",
        "status": "Offen (Apply with transcript, motivation, skills)",
        "url": "https://softsec.eu/teaching/theses/"
    },

    # ============================================
    # Embedded Security (Christof Paar)
    # ============================================
    {
        "chair": "Embedded Security (Prof. Christof Paar)",
        "title": "FPGA Security: Security Analysis of AMD Spartan UltraScale+ FPGAs",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "FPGA Security / Bitstream Security",
        "hotness": 4,
        "lang": "EN/DE",
        "desc": "Project 1 - AMD recently released first devices in the Spartan UltraScale+ family with substantially overhauled configuration process. Aim to explore differences from older FPGA families and improve automated security analysis. Develop tooling for meaningful security research: reverse engineer new configuration process, support custom FPGA configuration via OpenOCD (JTAG) and Python. Integrate tools into ConFuzz fuzzing framework, improve using state-of-the-art fuzzing techniques including LLM-assisted approaches.",
        "reqs": "Interest in FPGA security. Hardware/software skills depending on the project.",
        "contact": "Felix Hahn / emsec+BA_MA@rub.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/emsec/teaching/theses/"
    },
    {
        "chair": "Embedded Security (Prof. Christof Paar)",
        "title": "FPGA Security: Hardware Fuzzing with Side Channels",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Side-Channel / FPGA Fuzzing",
        "hotness": 4,
        "lang": "EN/DE",
        "desc": "Project 2 - Combines power side-channel analysis with hardware fuzzing. Power traces captured during configuration reveal information about the configuration engine's internal state, guiding ConFuzz toward security-relevant inputs. Goal: Complete hardware and software integration of custom JTAG controller with ConFuzz and side-channel measurement setup, then perform targeted fuzzing campaigns.",
        "reqs": "Interest in FPGA security, side-channel analysis. Hardware/software skills.",
        "contact": "Felix Hahn / emsec+BA_MA@rub.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/emsec/teaching/theses/"
    },
    {
        "chair": "Embedded Security (Prof. Christof Paar)",
        "title": "FPGA Security: Power Glitching with Custom PCB",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Fault Injection / Power Glitching / FPGA",
        "hotness": 4,
        "lang": "EN/DE",
        "desc": "Project 3 - Power glitching attacks deliberately disturb a chip's power supply at precisely timed moments to cause faults (e.g., skipping authentication checks, bypassing memory clears). Custom PCB has been designed/fabricated exposing individual power rails of AMD 7-Series FPGA. Goal: Develop software tooling to automate glitching campaigns and attack several security-relevant operations on the FPGA.",
        "reqs": "Interest in FPGA security, fault injection. Hardware/software skills.",
        "contact": "Felix Hahn / emsec+BA_MA@rub.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/emsec/teaching/theses/"
    },
    {
        "chair": "Embedded Security (Prof. Christof Paar)",
        "title": "Wireless Physical-Layer Security (Multiple Topics)",
        "type": "BA/MA",
        "field": "Wireless Security",
        "subfield": "Physical-Layer Security / RF Sensing",
        "hotness": 4,
        "lang": "EN/DE",
        "desc": "Radio waves interact with their propagation environment, allowing extraction of detailed information about the physical environment. Physical-layer information not protected by current cryptographic primitives. Research areas: Security/privacy of wireless systems with RIS (Reconfigurable Intelligent Surfaces), Wi-Fi sensing (CSI/BFI), UWB and phase-based ranging security, mmWave radar sensing, physical tamper detection, ML on physical-layer information, channel reciprocity-based key generation, wireless jamming, emission security.",
        "reqs": "Interest in wireless security / RF. Contact Paul Staat.",
        "contact": "Paul Staat / emsec+BA_MA@rub.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/emsec/teaching/theses/"
    },

    # ============================================
    # Ubisys (Veelasha Moonsamy)
    # ============================================
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Exploring the Potential of In-App Safety Guidance in Social Media Platforms",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Social Media Safety / In-App Guidance",
        "hotness": 4,
        "lang": "EN",
        "desc": "Explores an in-platform social media safety companion that helps users interpret suspicious content, profiles, messages, or interactions. Instead of leaving the platform, users could click 'Help me understand this' feature, select a concern category (scam, phishing, impersonation, fake advertisement, harassment, privacy risk), and receive an AI-generated explanation, confidence cues, and actionable next steps. Prototype the interface and evaluate usability, or implement a proof-of-concept detection-and-explanation pipeline.",
        "reqs": "(Inquire with chair)",
        "contact": "ubisys+thesis@ruhr-uni-bochum.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "A Tool for Assessing Accessibility-Related Harms of Dark Patterns in Security-Critical User Flows",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Dark Patterns / Accessibility / Privacy",
        "hotness": 4,
        "lang": "EN",
        "desc": "Studies how dark patterns in security- and privacy-critical user interfaces can lead to accessibility-related harms. Involves designing and evaluating a practical tool supporting structured analysis of dark pattern mechanisms, interface accessibility, and impact on user decisions in flows such as login, consent, or account recovery. Artifact-centered project focusing on building and applying the tool to realistic interface examples.",
        "reqs": "(Inquire with chair)",
        "contact": "Agata Stanczyk (agata.stanczyk@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Exploring User Interfaces to Support Secure Chatbot Interactions",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "HCI / Chatbot Privacy / LLM Security",
        "hotness": 5,
        "lang": "EN",
        "desc": "Explores Human-Centered Design to propose interventions supporting secure human-chatbot interactions. With increasing lack of awareness of privacy mechanisms in chatbots and risks in human-chatbot interactions, there is a need for users to have more control and transparency. Explore design and development of visual prototypes in a conversational UI context supporting users with improving awareness and agency of privacy mechanisms. Bridges gap between HCD and privacy mechanisms.",
        "reqs": "(Inquire with chair)",
        "contact": "Ramya Kandula (ramya.kandula@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Analyzing and Enhancing Traffic Watermarking Attacks Against Anonymity Systems",
        "type": "BA/MA",
        "field": "Privacy / Anonymity",
        "subfield": "Traffic Watermarking / Tor / Deanonymization",
        "hotness": 4,
        "lang": "EN",
        "desc": "Traffic watermarking is a network traffic analysis technique to evaluate resistance of anonymity systems (e.g., Tor) to deanonymization attacks. A watermark is a unique pattern embedded in encrypted traffic flows to link traffic at different points in the network. Watermarking attacks are highly effective, but assessing their impact remains challenging due to variable network conditions, different anonymity systems, and new features. Goal: Explore and evaluate existing watermarking techniques, develop new ideas, and show how to effectively deploy them.",
        "reqs": "(Inquire with chair)",
        "contact": "Dimitri Mankowski (dimitri.mankowski@rub.de)",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "From Regulation to Code: Enforcing the GDPR via Compile-Time Checks and Live Monitoring",
        "type": "BA/MA",
        "field": "Privacy / Compliance",
        "subfield": "GDPR / Static Analysis / Runtime Enforcement",
        "hotness": 4,
        "lang": "EN",
        "desc": "Compliance to the GDPR is often seen as a legal/organizational task, but many GDPR principles can be translated into technical policies and checks (e.g., 'data protection by design and by default', Article 25). Instead of treating this as legal guideline, enforce it in software.\n\nTasks: Identify and categorize GDPR rules that can be technically enforced; distinguish static analysis from runtime enforcement; design and implement prototypes demonstrating enforcement via static analysis and runtime monitoring; test tools on sample applications to validate ability to catch violations.",
        "reqs": "(Inquire with chair)",
        "contact": "ubisys+thesis@ruhr-uni-bochum.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Embedded Security (Firmware and Hardware Security)",
        "type": "BA/MA",
        "field": "Embedded Security",
        "subfield": "Firmware / Hardware Security",
        "hotness": 4,
        "lang": "EN",
        "desc": "Broad research area covering firmware and hardware security topics. Contact the chair for specific available projects.",
        "reqs": "(Inquire with chair)",
        "contact": "ubisys+thesis@ruhr-uni-bochum.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Security and Privacy of Large Language Models (SENTIMENT Project)",
        "type": "BA/MA",
        "field": "AI/ML Security",
        "subfield": "LLM Security & Privacy",
        "hotness": 5,
        "lang": "EN",
        "desc": "Research on security and privacy aspects of Large Language Models, part of the SENTIMENT project. Specific topics to be discussed with the chair.",
        "reqs": "(Inquire with chair)",
        "contact": "ubisys+thesis@ruhr-uni-bochum.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Tools and Techniques for Privacy Compliance",
        "type": "BA/MA",
        "field": "Privacy / Compliance",
        "subfield": "Privacy Tools / Compliance Automation",
        "hotness": 4,
        "lang": "EN",
        "desc": "Development and analysis of tools and techniques supporting privacy compliance. See related publications from the chair.",
        "reqs": "(Inquire with chair)",
        "contact": "ubisys+thesis@ruhr-uni-bochum.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Social Engineering and Mobile Accessibility (Dark Patterns, Inclusive Security)",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Social Engineering / Accessibility / Dark Patterns",
        "hotness": 3,
        "lang": "EN",
        "desc": "Research on social engineering, mobile accessibility, dark patterns, and inclusive security & privacy for people with disabilities, including assistive tools.",
        "reqs": "(Inquire with chair)",
        "contact": "Agata Stanczyk",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Secure Self-Disclosure in Human-AI Interactions",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Human-AI Interaction / Self-Disclosure",
        "hotness": 4,
        "lang": "EN",
        "desc": "Research on secure self-disclosure in the context of human-AI interactions.",
        "reqs": "(Inquire with chair)",
        "contact": "Ramya Kandula",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },
    {
        "chair": "Security & Privacy of Ubiquitous Systems (Prof. Veelasha Moonsamy)",
        "title": "Traffic Analysis (Network Traffic Watermarking Attacks against Anonymity Systems)",
        "type": "BA/MA",
        "field": "Privacy / Anonymity",
        "subfield": "Traffic Analysis / Watermarking",
        "hotness": 3,
        "lang": "EN",
        "desc": "Research on network traffic watermarking attacks targeting anonymity systems.",
        "reqs": "(Inquire with chair)",
        "contact": "Dimitri Mankowski",
        "status": "Offen",
        "url": "https://informatik.rub.de/ubisys/teaching/theses/"
    },

    # ============================================
    # Secure Mobile Networking (Christian Zenger)
    # ============================================
    {
        "chair": "Secure Mobile Networking (Jun.-Prof. Christian Zenger)",
        "title": "RADAR from Inside: Advanced Tamper Detection for Critical Infrastructures",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Tamper Detection / Electromagnetic Analysis",
        "hotness": 4,
        "lang": "EN",
        "desc": "Focus on using electromagnetic waves to detect unauthorized interference with electronic devices for critical infrastructures. Investigate advanced signal processing techniques and develop novel detection algorithms to create highly sensitive tamper detection systems protecting against cyber-physical threats. Applications: national security assets, financial and healthcare systems.",
        "reqs": "(Inquire with chair)",
        "contact": "christian.zenger@rub.de",
        "status": "Offen",
        "url": "https://www.christianzenger.de/theses"
    },
    {
        "chair": "Secure Mobile Networking (Jun.-Prof. Christian Zenger)",
        "title": "Security of Neural Implants (Brain-Computer Interfaces)",
        "type": "BA/MA",
        "field": "Embedded Security",
        "subfield": "Neural Implant Security / BCI Security",
        "hotness": 5,
        "lang": "EN",
        "desc": "Neural implants and brain-computer interfaces (BCIs) represent the cutting edge of human-machine integration, introducing new and complex security challenges. Delve into critical issues surrounding protection of these sensitive devices from potential cyber threats. As these technologies become more widespread in medical/consumer applications, ensuring their security is paramount to preventing unauthorized access to neural data. One of the most ethically and technically demanding fields in cybersecurity today.",
        "reqs": "(Inquire with chair)",
        "contact": "christian.zenger@rub.de",
        "status": "Offen",
        "url": "https://www.christianzenger.de/theses"
    },
    {
        "chair": "Secure Mobile Networking (Jun.-Prof. Christian Zenger)",
        "title": "Radiofrequency Machine Learning: Transforming Wireless Security with AI",
        "type": "BA/MA",
        "field": "Wireless Security",
        "subfield": "RF Machine Learning / AI for Wireless",
        "hotness": 5,
        "lang": "EN",
        "desc": "Convergence of machine learning and radiofrequency analysis offers unprecedented opportunities to revolutionize wireless security. Explore how AI can be applied to analyze wireless signals, detect anomalies, and predict security breaches with high precision. Develop models that learn from vast amounts of data, aiming to create intelligent systems capable of real-time threat detection and response. Enhance resilience of wireless networks, making them more adaptive to emerging threats.",
        "reqs": "(Inquire with chair)",
        "contact": "christian.zenger@rub.de",
        "status": "Offen",
        "url": "https://www.christianzenger.de/theses"
    },
    {
        "chair": "Secure Mobile Networking (Jun.-Prof. Christian Zenger)",
        "title": "LoRaWAN Security: Securing the Future of Low Power Wide Area Networks",
        "type": "BA/MA",
        "field": "IoT Security",
        "subfield": "LoRaWAN / LPWAN Security",
        "hotness": 4,
        "lang": "EN",
        "desc": "LoRaWAN is a key technology for IoT, enabling long-range communication with minimal power consumption. Security remains a significant concern. Focus on identifying and mitigating vulnerabilities within LoRaWAN networks to ensure data confidentiality and protect networks against unauthorized access. Develop new security protocols and frameworks to bolster IoT network defenses. Vital for the future of smart cities, agriculture, and industries.",
        "reqs": "(Inquire with chair)",
        "contact": "christian.zenger@rub.de",
        "status": "Offen",
        "url": "https://www.christianzenger.de/theses"
    },

    # ============================================
    # STOI (Rebekah Overdorf)
    # ============================================
    {
        "chair": "Security & Trustworthiness of Online Information (Prof. Rebekah Overdorf)",
        "title": "Online Information Manipulation: Detection, Analysis & Mitigation",
        "type": "BA/MA",
        "field": "Online Information Security",
        "subfield": "Disinformation / Social Media Manipulation",
        "hotness": 5,
        "lang": "EN",
        "desc": "Research at the intersection of security, privacy and data science. Studies how manipulation shapes what information users see online and how it can be detected, understood, and mitigated. Explores how malicious actors exploit platform mechanisms, often at scale with real societal consequences. Designs novel attacks on systems to inform stronger defenses. Topics span: data collection and analysis, applied ML for detection, and privacy/security of online information.",
        "reqs": "(Inquire with chair)",
        "contact": "rebekah.overdorf@rub.de",
        "status": "Offen",
        "url": "https://informatik.rub.de/stoi/"
    },

    # ============================================
    # Automated Security Analysis (Flavio Toffalini)
    # ============================================
    {
        "chair": "Automated Security Analysis (Prof. Flavio Toffalini)",
        "title": "Automated Software Testing / Fuzzing / System Security",
        "type": "BA/MA",
        "field": "Software Security",
        "subfield": "Automated Testing / Fuzzing / TEE",
        "hotness": 4,
        "lang": "EN",
        "desc": "Research expertise in system security, with focus on automatic software testing, threat mitigation, and trusted computing technologies. Current opportunities include research on browser and interpreter testing, fuzzing, and TEE security (SGX, TrustZone). Open for personal proposals outside automated testing that reach other system security areas.",
        "reqs": "(Inquire with chair)",
        "contact": "flavio.toffalini@rub.de",
        "status": "Offen",
        "url": "https://flaviotoffalini.info/"
    },

    # ============================================
    # Symmetric Cryptography (Gregor Leander)
    # ============================================
    {
        "chair": "Symmetric Cryptography (Prof. Gregor Leander)",
        "title": "Design of Symmetric Primitives / Breaking Symmetric Cryptography / Analysis Tools",
        "type": "BA/MA",
        "field": "Cryptography",
        "subfield": "Symmetric Cryptography / Boolean Functions",
        "hotness": 3,
        "lang": "EN/DE",
        "desc": "Topics: Design of symmetric primitives, breaking symmetric cryptography, tools for the analysis of symmetric cryptography, theory of Boolean functions. Exact topic determined together with the student. Can range from implementation to mathematical experiments and pure theory.",
        "reqs": "Motivated students from ITS, Computer Science, and Math. Contact: gregor.leander@rub.de.",
        "contact": "gregor.leander@rub.de",
        "status": "Offen (topic discussed individually)",
        "url": "https://informatik.rub.de/symcrypt/lehre/abschlussarbeiten/"
    },

    # ============================================
    # Cryptography (Eike Kiltz)
    # ============================================
    {
        "chair": "Cryptography (Prof. Eike Kiltz)",
        "title": "Theoretical Cryptography: Digital Signatures, Encryption, Zero-Knowledge, PQC (Gitter-basiert)",
        "type": "BA/MA",
        "field": "Cryptography",
        "subfield": "Public-Key Crypto / PQC / Zero-Knowledge",
        "hotness": 4,
        "lang": "DE/EN",
        "desc": "Der Lehrstuhl beschäftigt sich mit den theoretischen Grundlagen der Kryptographie. Entwurf neuer Protokolle und formale Sicherheitsanalyse. Fokus auf Digitalen Signaturen, Verschlüsselung, Zero-Knowledge und Authentifizierungsprotokollen. Post-Quantum Kryptographie (insb. Gitter-basierte Verfahren) gewinnt an Bedeutung.\n\nEin Thema baut normalerweise auf einer englischen Originalarbeit auf. Minimalziel: Arbeit bis ins Detail verstehen und in eigenen Worten wiedergeben. Möglichkeit: Bearbeitung eines Themenfeldes mit selbständiger Literatursichtung.",
        "reqs": "Optimalerweise Kryptographie I+II und Spezialvorlesung 'Kryptographische Protokolle' gehört, sowie Seminar in Kryptographie. Allgemeines Interesse an theoretischen Fragestellungen.",
        "contact": "Prof. Eike Kiltz",
        "status": "Offen (topic discussed individually)",
        "url": "https://informatik.rub.de/crypto/abschlussarbeiten/"
    },

    # ============================================
    # Distributed Cryptography (Julian Loss)
    # ============================================
    {
        "chair": "Distributed Cryptography (Prof. Julian Loss)",
        "title": "Cryptography and its Applications to Distributed Algorithms",
        "type": "BA/MA",
        "field": "Cryptography",
        "subfield": "Distributed Cryptography / Consensus",
        "hotness": 4,
        "lang": "EN",
        "desc": "Broadly interested in cryptography and its applications to distributed algorithms. Research supported by an ERC Starting Grant. Contact directly for available thesis topics.",
        "reqs": "(Inquire with chair)",
        "contact": "lossjulian@gmail.com",
        "status": "Offen (contact directly)",
        "url": "https://www.julianloss.com/"
    },

    # ============================================
    # NDS - Network and Data Security (Jörg Schwenk)
    # ============================================
    {
        "chair": "Network and Data Security (Prof. Jörg Schwenk)",
        "title": "SSH Security Analysis and Protocol Security",
        "type": "BA/MA",
        "field": "Network Security",
        "subfield": "SSH Protocol / Cryptographic Protocols",
        "hotness": 3,
        "lang": "DE/EN",
        "desc": "Thesis on security of SSH, network protocols, and cryptographic implementations. Analysis and securing of the SSH protocol.\n\nSTATUS: Aktuell keine Annahme weiterer Bachelor-/Masterarbeiten (currently not accepting).",
        "reqs": "Interest in SSH, network protocols, and cryptographic implementations.",
        "contact": "Chair NDS (see website)",
        "status": "Derzeit keine Annahme",
        "url": "https://informatik.rub.de/nds/teaching/theses/"
    },
    {
        "chair": "Network and Data Security (Prof. Jörg Schwenk)",
        "title": "TLS/DTLS/QUIC Security Analysis using TLS-Attacker Tools",
        "type": "BA/MA",
        "field": "Network Security",
        "subfield": "TLS / DTLS / QUIC Protocol Analysis",
        "hotness": 4,
        "lang": "DE/EN",
        "desc": "The chair develops various tools (https://github.com/tls-attacker) for investigating cryptographic protocols like TLS, DTLS, and QUIC. Thesis on analyzing/improving these protocols or the tools.\n\nSTATUS: Aktuell keine Annahme weiterer Bachelor-/Masterarbeiten (currently not accepting).",
        "reqs": "Interest in cryptographic protocols (TLS/DTLS/QUIC).",
        "contact": "Chair NDS (see website)",
        "status": "Derzeit keine Annahme",
        "url": "https://informatik.rub.de/nds/teaching/theses/"
    },
    {
        "chair": "Network and Data Security (Prof. Jörg Schwenk)",
        "title": "Web Security: Modern Web Applications, Browser Security, Authentication",
        "type": "BA/MA",
        "field": "Web Security",
        "subfield": "Browser Security / WebAuthn / Authentication",
        "hotness": 4,
        "lang": "DE/EN",
        "desc": "Thesis on security of modern web applications, browsers, and authentication procedures. Various areas of Web Security.\n\nSTATUS: Aktuell keine Annahme weiterer Bachelor-/Masterarbeiten (currently not accepting).",
        "reqs": "Interest in web security, browsers, and authentication.",
        "contact": "Chair NDS (see website)",
        "status": "Derzeit keine Annahme",
        "url": "https://informatik.rub.de/nds/teaching/theses/"
    },
    {
        "chair": "Network and Data Security (Prof. Jörg Schwenk)",
        "title": "Eigenes Thema vorschlagen (Propose Your Own Topic)",
        "type": "BA/MA",
        "field": "Network Security",
        "subfield": "Open Topic / Student Proposal",
        "hotness": 3,
        "lang": "DE/EN",
        "desc": "Students can propose their own topics. Requirements: Define your topic, find a suitable supervisor. Topic proposal must include defined scope, methodology, and supervisor agreement.",
        "reqs": "Must define topic and find supervisor within the chair.",
        "contact": "Chair NDS (see website)",
        "status": "Offen",
        "url": "https://informatik.rub.de/nds/teaching/theses/"
    },

    # ============================================
    # Human-Centred Security (Martina Angela Sasse)
    # ============================================
    {
        "chair": "Human-Centred Security (Prof. Martina Angela Sasse)",
        "title": "Physiological Measures in Security (Eye Tracking, Heart Rate)",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Physiological Security Indicators / Behavior",
        "hotness": 3,
        "lang": "EN",
        "desc": "Supervised by Peter Heubl. Security topics that include physiological measures (e.g., eye tracking, heart rate). Goal: Identify signs that people are at risk by analyzing human behavior and physiological responses, and thus better protect them when using technology.\n\nNOTE: Chair currently at full capacity; very limited supervision opportunities.",
        "reqs": "Apply via hcs-theses@ruhr-uni-bochum.de using HCS Email Application Template.",
        "contact": "hcs-theses@ruhr-uni-bochum.de",
        "status": "Begrenzt (Limited capacity)",
        "url": "https://informatik.rub.de/hcs/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Human-Centred Security (Prof. Martina Angela Sasse)",
        "title": "Risk Perception and Changing Security Behaviors/Habits of Citizens",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Risk Perception / Behavior Change / Interventions",
        "hotness": 3,
        "lang": "EN",
        "desc": "Supervised by Jan Nold. Topics on risk perception and changing behaviors or habits of citizens regarding IT security. Focus on potential interventions and security measures that are easy to implement and have lasting impact on users' security posture. Spans improved communication, enhanced training programs, and development of support systems like apps.\n\nNOTE: Chair currently at full capacity.",
        "reqs": "Apply via hcs-theses@ruhr-uni-bochum.de using HCS Email Application Template.",
        "contact": "hcs-theses@ruhr-uni-bochum.de",
        "status": "Begrenzt (Limited capacity)",
        "url": "https://informatik.rub.de/hcs/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Human-Centred Security (Prof. Martina Angela Sasse)",
        "title": "IT Security in Organizations",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Organizational Security / Security Management",
        "hotness": 3,
        "lang": "EN",
        "desc": "Supervised by Jens Opdenbusch. Final theses on the topic of IT security in organizations.\n\nNOTE: Chair currently at full capacity.",
        "reqs": "Apply via hcs-theses@ruhr-uni-bochum.de using HCS Email Application Template.",
        "contact": "hcs-theses@ruhr-uni-bochum.de",
        "status": "Begrenzt (Limited capacity)",
        "url": "https://informatik.rub.de/hcs/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Human-Centred Security (Prof. Martina Angela Sasse)",
        "title": "Software Bills of Materials (SBOM) and Cybersecurity in Organizations",
        "type": "BA/MA",
        "field": "Software Security",
        "subfield": "SBOM / Supply Chain Security",
        "hotness": 5,
        "lang": "EN",
        "desc": "Supervised by Felix Reichmann. Theses on the topic of Software Bills of Materials (SBOM) and Cybersecurity in organizations.\n\nNOTE: Chair currently at full capacity.",
        "reqs": "Apply via hcs-theses@ruhr-uni-bochum.de using HCS Email Application Template.",
        "contact": "hcs-theses@ruhr-uni-bochum.de",
        "status": "Begrenzt (Limited capacity)",
        "url": "https://informatik.rub.de/hcs/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Human-Centred Security (Prof. Martina Angela Sasse)",
        "title": "Game-Based Approaches for IT Security Training (Habit Formation)",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Gamification / Security Training / Education",
        "hotness": 3,
        "lang": "EN",
        "desc": "Supervised by Sangavi Shanthakumar. Game-based approaches for IT security training to form habits and achieve lasting secure behaviour. Includes topics requiring technical implementation.\n\nNOTE: Chair currently at full capacity.",
        "reqs": "Apply via hcs-theses@ruhr-uni-bochum.de using HCS Email Application Template.",
        "contact": "hcs-theses@ruhr-uni-bochum.de",
        "status": "Begrenzt (Limited capacity)",
        "url": "https://informatik.rub.de/hcs/lehre/abschlussarbeiten/"
    },
    {
        "chair": "Human-Centred Security (Prof. Martina Angela Sasse)",
        "title": "Human Factors in Trustworthy AI / Privacy / GDPR & DSA Issues",
        "type": "BA/MA",
        "field": "Usable Security",
        "subfield": "Trustworthy AI / GDPR / DSA / EUDIW",
        "hotness": 5,
        "lang": "EN",
        "desc": "Supervised by Jan Tolsdorf. Human factors in trustworthy Artificial Intelligence (AI), human-centered information privacy and security. Topics include: understanding and measuring human perceptions of trustworthiness in generative AI, interventions related to organizational security and data protection, investigations of GDPR-, DSA-, and EUDIW-related issues.\n\nNOTE: Chair currently at full capacity.",
        "reqs": "Apply via hcs-theses@ruhr-uni-bochum.de using HCS Email Application Template.",
        "contact": "hcs-theses@ruhr-uni-bochum.de",
        "status": "Begrenzt (Limited capacity)",
        "url": "https://informatik.rub.de/hcs/lehre/abschlussarbeiten/"
    },

    # ============================================
    # TrustHLT (Ivan Habernal)
    # ============================================
    {
        "chair": "Fairness and Transparency / TrustHLT (Prof. Ivan Habernal)",
        "title": "Trustworthy AI/ML: Fairness, Transparency, NLP Security",
        "type": "BA/MA",
        "field": "AI/ML Security",
        "subfield": "Trustworthy AI / NLP / Fairness / Transparency",
        "hotness": 5,
        "lang": "EN",
        "desc": "Thesis topics published through TrustHLT Thesis Moodle course. Research on trustworthy human language technology, including fairness, transparency, explainability, and security of AI/NLP systems. Enroll to Moodle to check open projects.\n\nCan also propose own research idea (max 400 word abstract).",
        "reqs": "Enrolled at RUB. Prior experience with Python, AI/ML applications and libraries (PyTorch, TensorFlow, Huggingface).",
        "contact": "Prof. Ivan Habernal (ivan.habernal@ruhr-uni-bochum.de)",
        "status": "Offen (via Moodle)",
        "url": "https://informatik.rub.de/trusthlt/trusthlt-master-thesis/"
    },

    # ============================================
    # DNet (Steffen Bondorf) - Network-related
    # ============================================
    {
        "chair": "Distributed and Networked Systems (Prof. Steffen Bondorf)",
        "title": "A Heuristic for Flow Prolongation (Network Calculus)",
        "type": "BA/MA",
        "field": "Network Security",
        "subfield": "Network Calculus / Performance Analysis",
        "hotness": 2,
        "lang": "EN",
        "desc": "Flow prolongation can improve the quality of performance bounds derived with deterministic network calculus. During analysis it is not possible to know the most beneficial prolongation among all alternatives. An exhaustive enumeration was shown not to scale well. Develop a heuristic approach.",
        "reqs": "Knowledge of network calculus, algorithms, and mathematical modeling.",
        "contact": "dnet-teaching(at)rub.de",
        "status": "Offen",
        "url": "https://dnet.rub.de/teaching/theses/"
    },
    {
        "chair": "Distributed and Networked Systems (Prof. Steffen Bondorf)",
        "title": "Graph Neural Networks in Network Performance Analysis",
        "type": "BA/MA",
        "field": "Network Security",
        "subfield": "GNN / Network Performance / ML",
        "hotness": 3,
        "lang": "EN",
        "desc": "Graph Neural Networks (GNNs) can speed up performance analysis with Deterministic Network Calculus (DNC). Various topics available extending existing literature (DeepTMA, Flow Prolongation with ML).",
        "reqs": "Knowledge of network calculus, machine learning, and GNNs.",
        "contact": "dnet-teaching(at)rub.de",
        "status": "Offen",
        "url": "https://dnet.rub.de/teaching/theses/"
    },

    # ============================================
    # AI and Society (Bilal Zafar)
    # ============================================
    {
        "chair": "AI and Society (Prof. Bilal Zafar)",
        "title": "AI Fairness, Accountability, and Societal Impact",
        "type": "BA/MA",
        "field": "AI/ML Security",
        "subfield": "AI Fairness / Societal Impact",
        "hotness": 5,
        "lang": "EN",
        "desc": "Research on AI and its societal implications, including fairness, accountability, and transparency in AI systems. Contact the chair for specific thesis topics.",
        "reqs": "(Inquire with chair)",
        "contact": "See chair website",
        "status": "Offen",
        "url": "https://informatik.rub.de/aisoc/theses/"
    },

    # ============================================
    # Nils Fleischhacker - Theoretical Cryptography (no URL)
    # ============================================
    {
        "chair": "Theoretical Cryptography (Jun.-Prof. Nils Fleischhacker)",
        "title": "Theoretical Cryptography (Contact directly)",
        "type": "BA/MA",
        "field": "Cryptography",
        "subfield": "Theoretical Cryptography / Foundations",
        "hotness": 3,
        "lang": "EN/DE",
        "desc": "No website with topics listed. Recommended to contact the professor directly via email for available thesis topics.",
        "reqs": "(Contact professor directly)",
        "contact": "Contact Nils Fleischhacker directly",
        "status": "Offen (contact directly)",
        "url": "N/A (no webpage listed)"
    },

    # ============================================
    # Catalin Hritcu - Formally Verified Security (MPI, no URL)
    # ============================================
    {
        "chair": "Formally Verified Security (Apl. Prof. Cătălin Hrițcu, MPI)",
        "title": "Formally Verified Security (Contact directly)",
        "type": "BA/MA",
        "field": "Formal Methods",
        "subfield": "Formal Verification / Security Proofs",
        "hotness": 3,
        "lang": "EN",
        "desc": "No website with topics listed. Research on formally verified security at MPI-SP. Recommended to contact the professor directly via email for available thesis topics.",
        "reqs": "(Contact professor directly)",
        "contact": "Contact Cătălin Hrițcu directly",
        "status": "Offen (contact directly)",
        "url": "N/A (no webpage listed)"
    },

    # ============================================
    # Peter Schwabe - Cryptographic Engineering (MPI, no URL)
    # ============================================
    {
        "chair": "Cryptographic Engineering (Apl. Prof. Peter Schwabe, MPI)",
        "title": "Cryptographic Engineering (Contact directly)",
        "type": "BA/MA",
        "field": "Cryptographic Engineering",
        "subfield": "PQC Implementation / Cryptographic Software",
        "hotness": 5,
        "lang": "EN",
        "desc": "No website with topics listed. Research on cryptographic engineering including high-speed and secure implementations of cryptographic primitives, especially post-quantum cryptography. Recommended to contact the professor directly via email.",
        "reqs": "(Contact professor directly)",
        "contact": "Contact Peter Schwabe directly",
        "status": "Offen (contact directly)",
        "url": "N/A (no webpage listed)"
    },

    # ============================================
    # Yuval Yarom - Computer Security (no URL)
    # ============================================
    {
        "chair": "Computer Security (Prof. Yuval Yarom)",
        "title": "Microarchitectural Security / Side Channels / Hardware Security",
        "type": "BA/MA",
        "field": "Hardware Security",
        "subfield": "Microarchitectural Attacks / Side Channels",
        "hotness": 4,
        "lang": "EN",
        "desc": "No website with topics listed. Prof. Yarom is a leading researcher on microarchitectural side-channel attacks (e.g., FLUSH+RELOAD, Spectre/Meltdown-class attacks). Recommended to contact the professor directly via email for available thesis topics.",
        "reqs": "(Contact professor directly)",
        "contact": "Contact Yuval Yarom directly",
        "status": "Offen (contact directly)",
        "url": "N/A (no webpage listed)"
    },

    # ============================================
    # Alexander May - Cryptanalysis (no URL)
    # ============================================
    {
        "chair": "Cryptanalysis (Prof. Alexander May)",
        "title": "Cryptanalysis (Contact directly)",
        "type": "BA/MA",
        "field": "Cryptography",
        "subfield": "Cryptanalysis / Lattice-Based Attacks",
        "hotness": 3,
        "lang": "EN/DE",
        "desc": "No website with topics listed. Research on cryptanalysis, including lattice-based attacks and analysis of cryptographic primitives. Recommended to contact the professor directly via email for available thesis topics.",
        "reqs": "(Contact professor directly)",
        "contact": "Contact Alexander May directly",
        "status": "Offen (contact directly)",
        "url": "N/A (no webpage listed)"
    },

    # ============================================
    # Gilles Barthe - Principles of Security and Privacy (MPI, no URL)
    # ============================================
    {
        "chair": "Principles of Security and Privacy (Prof. Gilles Barthe, MPI)",
        "title": "Security & Privacy Foundations (Formal Methods, Crypto Proofs)",
        "type": "BA/MA",
        "field": "Formal Methods",
        "subfield": "Security Foundations / Formal Proofs / Privacy",
        "hotness": 3,
        "lang": "EN",
        "desc": "No website with topics listed. Research on principles of security and privacy, including formal verification of cryptographic implementations, side-channel resistance proofs, and differential privacy. Recommended to contact the professor directly via email.",
        "reqs": "(Contact professor directly)",
        "contact": "Contact Gilles Barthe directly",
        "status": "Offen (contact directly)",
        "url": "N/A (no webpage listed)"
    },
]

# ---- Write data ----
for row_idx, thesis in enumerate(thesis_data, 2):
    ws.cell(row=row_idx, column=1, value=row_idx - 1).alignment = Alignment(vertical='top', horizontal='center')
    ws.cell(row=row_idx, column=2, value=thesis["chair"]).alignment = wrap_alignment
    ws.cell(row=row_idx, column=3, value=thesis["title"]).alignment = wrap_alignment
    ws.cell(row=row_idx, column=4, value=thesis["type"]).alignment = Alignment(vertical='top', horizontal='center')
    ws.cell(row=row_idx, column=5, value=thesis["field"]).alignment = wrap_alignment
    ws.cell(row=row_idx, column=6, value=thesis["subfield"]).alignment = wrap_alignment

    hot_val = thesis["hotness"]
    hot_cell = ws.cell(row=row_idx, column=7, value=hot_val)
    hot_cell.alignment = Alignment(vertical='top', horizontal='center')
    if hot_val == 5:
        hot_cell.fill = hot_fill_5
    elif hot_val == 4:
        hot_cell.fill = hot_fill_4
    elif hot_val <= 3:
        hot_cell.fill = hot_fill_3

    ws.cell(row=row_idx, column=8, value=thesis["lang"]).alignment = Alignment(vertical='top', horizontal='center')
    ws.cell(row=row_idx, column=9, value=thesis["desc"]).alignment = wrap_alignment
    ws.cell(row=row_idx, column=10, value=thesis["reqs"]).alignment = wrap_alignment
    ws.cell(row=row_idx, column=11, value=thesis["contact"]).alignment = wrap_alignment
    ws.cell(row=row_idx, column=12, value=thesis["status"]).alignment = Alignment(vertical='top', horizontal='center')
    ws.cell(row=row_idx, column=13, value=thesis["url"]).alignment = wrap_alignment

    # Apply border
    for col in range(1, 14):
        ws.cell(row=row_idx, column=col).border = thin_border

    # Set row height
    ws.row_dimensions[row_idx].height = 120

# ---- Summary / Legend sheet ----
ws2 = wb.create_sheet("Legend & Hotness Scale")
ws2.column_dimensions['A'].width = 30
ws2.column_dimensions['B'].width = 60

legend_data = [
    ("Hotness Scale:", ""),
    ("5 (Green)", "Sehr heiß / Very Hot — Cutting-edge research, strong industry demand, active standardization (e.g., PQC, AI/LLM Security, 6G)"),
    ("4 (Yellow)", "Heiß / Hot — Active research area, relevant industry demand (e.g., Hardware Security, TEE, Privacy, 5G, Side-Channel)"),
    ("3 (Light Red)", "Moderat / Medium — Established field, steady interest (e.g., Classical Cryptanalysis, Usable Security, Blockchain)"),
    ("2", "Niedrig / Low — Niche or declining field"),
    ("1", "Sehr niedrig / Very Low — Outdated or minimal demand"),
    ("", ""),
    ("Cybersecurity Fields Covered:", ""),
    ("Hardware Security", "Physical attacks, side-channel analysis, fault injection, FPGA security, microarchitectural attacks"),
    ("Post-Quantum Cryptography", "PQC implementations, lattice-based crypto, multivariate signatures"),
    ("AI/ML Security", "Adversarial ML, LLM security, AI fairness, trustworthy AI"),
    ("Mobile Network Security", "5G/6G security, V2X, campus networks, mobile protocols"),
    ("Privacy / Anonymity", "Tor, traffic analysis, GDPR compliance, privacy tools"),
    ("Software Security", "Fuzzing, program analysis, vulnerability discovery, SBOM"),
    ("Network Security", "TLS, SSH, web security, protocol analysis"),
    ("Cryptography / Crypto Engineering", "Symmetric crypto, public-key crypto, distributed crypto, implementation"),
    ("Usable Security", "Human-centred security, risk perception, security training, dark patterns"),
    ("Wireless Security", "Physical-layer security, RF ML, LoRaWAN, wireless sensing"),
    ("Embedded / IoT Security", "Firmware security, IoT protocols, embedded systems"),
    ("Platform Security / TEE", "Trusted Execution Environments, SGX, SEV, confidential computing"),
    ("Online Information Security", "Disinformation, social media manipulation detection"),
    ("Formal Methods", "Formal verification, security proofs, protocol verification"),
    ("", ""),
    ("Source:", "Scraped from RUB Informatik Fakultät thesis pages on 2026-07-23"),
    ("", ""),
    ("Note:", "Some chairs do not list specific topics online. These are marked 'contact directly' or 'via Moodle'."),
    ("", ""),
    ("Legend:", "Green = Hotness 5 | Yellow = Hotness 4 | Light Red = Hotness 1-3"),
]

for i, (label, desc) in enumerate(legend_data, 1):
    ws2.cell(row=i, column=1, value=label).font = Font(bold=True)
    ws2.cell(row=i, column=2, value=desc).alignment = Alignment(wrap_text=True)

# ---- Sort by Hotness then Field ----
# We'll also create a sorted version
ws3 = wb.create_sheet("Sorted by Hotness (High to Low)")
for col_idx, header in enumerate(headers, 1):
    cell = ws3.cell(row=1, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    cell.border = thin_border
for i, w in enumerate(col_widths, 1):
    ws3.column_dimensions[get_column_letter(i)].width = w
ws3.freeze_panes = 'A2'
ws3.auto_filter.ref = f"A1:M1"

# Sort data by hotness descending, then by field
sorted_data = sorted(thesis_data, key=lambda x: (-x["hotness"], x["field"], x["chair"]))

for row_idx, thesis in enumerate(sorted_data, 2):
    ws3.cell(row=row_idx, column=1, value=row_idx - 1).alignment = Alignment(vertical='top', horizontal='center')
    ws3.cell(row=row_idx, column=2, value=thesis["chair"]).alignment = wrap_alignment
    ws3.cell(row=row_idx, column=3, value=thesis["title"]).alignment = wrap_alignment
    ws3.cell(row=row_idx, column=4, value=thesis["type"]).alignment = Alignment(vertical='top', horizontal='center')
    ws3.cell(row=row_idx, column=5, value=thesis["field"]).alignment = wrap_alignment
    ws3.cell(row=row_idx, column=6, value=thesis["subfield"]).alignment = wrap_alignment

    hot_val = thesis["hotness"]
    hot_cell = ws3.cell(row=row_idx, column=7, value=hot_val)
    hot_cell.alignment = Alignment(vertical='top', horizontal='center')
    if hot_val == 5:
        hot_cell.fill = hot_fill_5
    elif hot_val == 4:
        hot_cell.fill = hot_fill_4
    else:
        hot_cell.fill = hot_fill_3

    ws3.cell(row=row_idx, column=8, value=thesis["lang"]).alignment = Alignment(vertical='top', horizontal='center')
    ws3.cell(row=row_idx, column=9, value=thesis["desc"]).alignment = wrap_alignment
    ws3.cell(row=row_idx, column=10, value=thesis["reqs"]).alignment = wrap_alignment
    ws3.cell(row=row_idx, column=11, value=thesis["contact"]).alignment = wrap_alignment
    ws3.cell(row=row_idx, column=12, value=thesis["status"]).alignment = Alignment(vertical='top', horizontal='center')
    ws3.cell(row=row_idx, column=13, value=thesis["url"]).alignment = wrap_alignment

    for col in range(1, 14):
        ws3.cell(row=row_idx, column=col).border = thin_border

    ws3.row_dimensions[row_idx].height = 120

# Save
output_path = r"C:\Users\Hamza\Desktop\Share\Uni\#10 WiSe 26 27 - IT Sicherheit und Informationstechnik - Bachelor Arbeit\Bachelor Arbeit\Bewerbung\RUB Topics Scraping\RUB_Cybersecurity_Theses.xlsx"
wb.save(output_path)
print(f"Saved to: {output_path}")
print(f"Total theses: {len(thesis_data)}")
