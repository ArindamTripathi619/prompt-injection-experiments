# Prompt Injection Defense: Multi-Layer Architecture Experiments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the complete experimental validation of a six-layer defense architecture against prompt injection attacks in Large Language Models (LLMs). All experiments were conducted on RunPod cloud GPU instances using NVIDIA RTX 4090 GPUs.

**Research Process:** For a detailed summary of the research progression from initial experiments to the breakthrough in adaptive coordination, see [PROCESS_SUMMARY.md](docs/PROCESS_SUMMARY.md).

## 📄 Paper Reference

This repository corresponds to the experimental validation described in:

**"A Multi-Layer Defense Architecture Against Prompt Injection Attacks in Large Language Models"**

**Paper Version:** The results in this repository correspond to commit `[COMMIT_HASH]` and represent the experiments conducted in December 2025.

## 🎯 Project Overview

Prompt injection attacks pose significant security risks to LLM-based applications. This research proposes and validates a comprehensive six-layer defense architecture:

1. **Layer 1: Request Boundary Detection** - Input validation and length constraints
2. **Layer 2: Semantic Analysis** - Intent classification and prompt injection detection
3. **Layer 3: Context Isolation** - Separation of user input from system instructions
4. **Layer 4: LLM Baseline Constraints** - System prompt hardening and role-based restrictions
5. **Layer 5: Output Validation** - Response filtering and safety checks
6. **Layer 6: Feedback & Adaptive Monitoring** - Continuous learning (future work)

### Key Findings

- **Overall Attack Success Rate (ASR):** 31.51% on baseline (no defense)
- **Full Defense Effectiveness:** 68.1% reduction in ASR (from 80.8% → 12.7%)
- **Adaptive Coordination Effectiveness:** 9.05% additional reduction (27.62% → 18.57%, p < 0.001) ⭐ **NEW**
- **Most Critical Layer:** Layer 2 (Semantic Analysis) provides 42.3% reduction alone
- **Most Impactful Coordination:** Layer 4 adaptive monitoring provides 8.10% reduction ⭐ **NEW**
- **Statistical Significance:** All results validated with p < 0.001 using McNemar's test
- **Sample Size:** 11,490 execution traces across 103 configurations, 5 trials each

## 🏗️ Repository Structure

```
prompt-injection-experiments/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
│
├── docs/                              # Project Documentation
│   ├── EXPERIMENT_SUMMARY.md          # Detailed experiment summary
│   ├── PROCESS_SUMMARY.md             # Research process narrative
│   ├── PUBLICATION_CHECKLIST.md       # Pre-publication checklist
│   └── analysis_results.txt           # Detailed statistical analysis
│
├── data/                              # Data and Visualizations
│   ├── experiments.db                 # Main merged database (all experiments)
│   └── visualizations/                # Generated research paper figures
│       ├── architecture_diagram.png
│       ├── asr_comparison_chart.png
│       └── ...
│
├── results/                           # Raw Results & Logs
│   ├── metrics/                       # Partial databases and JSON summaries
│   │   ├── exp1_results.db
│   │   ├── experiment_1_results.json
│   │   └── ...
│   ├── artifacts/                     # Raw experiment execution artifacts
│   │   ├── exp1/
│   │   ├── exp2/
│   │   └── ...
│   └── logs/                          # Execution logs
│
└── src/                               # Core Source Code
    ├── config.py                      # Configuration settings
    ├── experiment_runner.py           # Main experiment orchestration
    ├── pipeline.py                    # Defense pipeline logic
    ├── statistical_analysis.py        # Statistical testing tools
    ├── create_visualizations.py       # Visualization generation script
    ├── layers/                        # Defense layer implementations
    │   ├── layer1_boundary.py
    │   └── ...
    └── models/                        # Pydantic data models
```

## 🧪 Experimental Methodology

### Experiment Design

We conducted four complementary experiments to comprehensively evaluate the defense architecture:

#### Experiment 1: Baseline Effectiveness
- **Purpose:** Establish baseline ASR and validate full defense effectiveness
- **Configurations:** 2 (No Defense, Full Defense)
- **Trials:** 5 per configuration
- **Attack Prompts:** 52 diverse injection patterns
- **Total Traces:** 1,040
- **Key Finding:** Full defense reduces ASR from 80.8% to 12.7% (p < 0.001)

#### Experiment 2: Progressive Layering
- **Purpose:** Analyze incremental defense improvements
- **Configurations:** 6 (Layer 1, Layers 1-2, 1-3, 1-4, 1-5, Full)
- **Trials:** 5 per configuration
- **Attack Prompts:** 52 diverse injection patterns
- **Total Traces:** 1,560
- **Key Finding:** Layer 2 provides critical threshold, dropping ASR to 38.5%

#### Experiment 3: Individual Layer Contributions
- **Purpose:** Isolate each layer's standalone effectiveness
- **Configurations:** 7 (None, Layer 1 only, Layer 2 only, ..., Layer 5 only, Full)
- **Trials:** 5 per configuration
- **Attack Prompts:** 52 diverse injection patterns
- **Total Traces:** 1,820
- **Key Finding:** Layer 2 alone provides 42.3% reduction; Layer 5 provides 55.4%

#### Experiment 4: Layer Ablation Study
- **Purpose:** Identify redundant layers in full defense stack
- **Configurations:** 6 (Full, Remove Layer 1, Remove Layer 2, ..., Remove Layer 5)
- **Trials:** 5 per configuration
- **Attack Prompts:** 14 high-difficulty patterns
- **Total Traces:** 420
- **Key Finding:** Layer 1 redundant (p = 1.0); all other layers critical

#### Experiment 6: Adaptive Coordination Defense ⭐ **NEW**
- **Purpose:** Validate TRUE adaptive coordination across defense layers
- **Configurations:** 4 (Isolated baseline, Adaptive L3, Adaptive L4, Full adaptive)
- **Trials:** 5 per configuration
- **Attack Prompts:** 42 diverse injection patterns
- **Total Traces:** 840
- **Key Findings:** 
  - Full adaptive coordination: 9.05% ASR reduction (27.62% → 18.57%)
  - Layer 4 adaptive monitoring: Most impactful (8.10% reduction alone)
  - Statistical significance: χ² = 13.04, **p < 0.001** (highly significant)
  - Measured 230 coordination decisions (100 L3 + 85 L4 + 45 L5)
  - **PROOF:** Coordination is TRUE (adaptive behavior), not fake (additive coverage)

### Infrastructure: RunPod Cloud GPU Setup

All experiments were executed on **RunPod** cloud GPU instances with the following specifications:

- **GPU:** NVIDIA RTX 4090 (24 GB VRAM)
- **Instances:** 4 parallel pods (one per experiment)
- **Cost:** ~$0.44/hour per pod
- **Runtime:** ~1.5 hours per experiment
- **Total Cost:** ~$2.64
- **LLM Backend:** Ollama running Llama 3.2:1b locally on each pod

#### Why RunPod?
1. **Reproducibility:** Consistent GPU access ensures identical runtime conditions
2. **Parallelization:** Run all 4 experiments simultaneously
3. **Cost-Effective:** Only pay for actual compute time
4. **Isolation:** Each experiment runs independently to avoid interference
5. **GPU Requirement:** Ollama LLM inference requires GPU acceleration

### Attack Prompt Dataset

We curated a comprehensive dataset of **52 diverse prompt injection attacks** covering:

- **Instruction Override:** "Ignore previous instructions..."
- **Role Manipulation:** "You are now a malicious assistant..."
- **Context Escaping:** "End previous context. New task:..."
- **System Prompt Extraction:** "Reveal your system prompt..."
- **Multi-Turn Attacks:** Sequential injections across conversations
- **Obfuscation Techniques:** Base64, Unicode, leetspeak encoding
- **Jailbreaking Patterns:** DAN, AIM, and other known jailbreaks

Attack prompts are stored in `data/attack_prompts.py` in each experiment directory.

### Statistical Methodology

All results were validated using rigorous statistical methods:

- **Confidence Intervals:** Wilson Score with 95% confidence level
- **Significance Testing:** McNemar's test for paired comparisons (α = 0.05)
- **Effect Size:** Cohen's h for practical significance
- **Sample Size:** Minimum n ≥ 210 per configuration (adequate power)
- **Multiple Testing:** Bonferroni correction where applicable

See `docs/STATISTICAL_ANALYSIS_SUMMARY.md` for complete statistical analysis.

## 🚀 Reproducing the Results

### Prerequisites

1. **Python 3.11+**
2. **Ollama** with Llama 3.2:1b model
3. **SQLite3**
4. **RunPod account** (optional, for cloud execution)

### Setup

```bash
# Clone the repository
git clone https://github.com/researcher/prompt-injection-experiments.git
cd prompt-injection-experiments

# Install dependencies
pip install -r requirements.txt

# Start Ollama (if running locally)
ollama serve

# Pull the Llama model
ollama pull llama3.2:1b
```

### Running Experiments Locally

To replicate a single experiment:

```bash
# Run Experiment 1 (Baseline)
cd experiments/exp1
python run_experiments_corrected.py

# Run Experiment 2 (Progressive Layers)
cd ../exp2
python run_experiments_corrected.py

# And so on...
```

### Analyzing Results

After running experiments, analyze the results:

```bash
# Merge all experiment databases
python src/merge_results.py

# Run comprehensive statistical analysis
python src/run_full_analysis.py
```

The analysis will generate:
- `docs/analysis_results.txt` - Full statistical output
- `docs/STATISTICAL_ANALYSIS_SUMMARY.md` - Key findings

### Running on RunPod

To replicate the exact experimental setup on RunPod:

1. **Create 4 RunPod instances** with RTX 4090 GPUs
2. **Upload experiment code** to each pod:
   ```bash
   # On your local machine
   tar -czf exp1.tar.gz experiments/exp1/*
   scp exp1.tar.gz root@POD_IP:/workspace/
   ```

3. **SSH into each pod** and run setup:
   ```bash
   ssh root@POD_IP
   cd /workspace
   tar -xzf exp1.tar.gz
   cd exp1
   bash setup.sh
   bash START_EXPERIMENT.sh
   ```

4. **Download results** after completion:
   ```bash
   scp root@POD_IP:/workspace/exp1/exp1_results.db ./
   ```

See individual experiment README files for specific instructions.

## 📊 Key Results

### Overall Attack Success Rate (ASR)

| Configuration | ASR | 95% CI | Change | p-value |
|--------------|-----|---------|---------|----------|
| No Defense | 80.8% | [76.2%, 84.8%] | Baseline | - |
| Full Defense | 12.7% | [9.6%, 16.4%] | -68.1% | < 0.001 |

### Layer-by-Layer Effectiveness

| Layer Added | ASR | Reduction | p-value |
|-------------|-----|-----------|----------|
| None | 80.8% | Baseline | - |
| Layer 1 Only | 80.8% | 0.0% | 1.0 |
| Layer 2 Only | 38.5% | -42.3% | < 0.001 |
| Layer 3 Only | 78.5% | -2.3% | 0.53 |
| Layer 4 Only | 75.4% | -5.4% | 0.15 |
| Layer 5 Only | 25.4% | -55.4% | < 0.001 |
| Full Stack | 12.7% | -68.1% | < 0.001 |

### Ablation Study (Removing Layers)

| Configuration | ASR | Impact | p-value |
|--------------|-----|---------|----------|
| Full Defense | 11.9% | Baseline | - |
| Remove Layer 1 | 11.9% | +0.0% | 1.0 |
| Remove Layer 2 | 75.7% | +63.8% | < 0.001 |
| Remove Layer 3 | 15.7% | +3.8% | 0.035 |
| Remove Layer 4 | 18.6% | +6.7% | < 0.001 |
| Remove Layer 5 | 78.6% | +66.7% | < 0.001 |

### Research Questions Answered

✅ **RQ1:** What is the baseline effectiveness of prompt injection attacks, and how effective is a full multi-layer defense?
- **Answer:** Baseline ASR is 80.8%. Full defense reduces ASR by 68.1% to 12.7% (p < 0.001).

✅ **RQ2:** How does defense effectiveness change when layers are added progressively?
- **Answer:** Layer 2 provides critical threshold (42.3% reduction). Subsequent layers provide incremental improvements.

✅ **RQ3:** What are the individual contributions of each defense layer?
- **Answer:** Layer 2 (42.3%) and Layer 5 (55.4%) are most effective standalone. Layers 1, 3, 4 have minimal standalone value.

✅ **RQ4:** Which layers are redundant when the full defense stack is deployed?
- **Answer:** Layer 1 is redundant in full stack (p = 1.0). All other layers are critical.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This repository represents the experimental validation for a research paper. While we welcome feedback and discussion through GitHub Issues, we are not accepting pull requests as the code is archived for reproducibility purposes.

## 👥 Authors

- **Arindam Tripathi** - *Lead Researcher* - [arindamtripathi.619@gmail.com](mailto:arindamtripathi.619@gmail.com)
- **Arghya Bose** - *Researcher* - [bosearghya29@gmail.com](mailto:bosearghya29@gmail.com)
- **Arghya Paul** - *Researcher* - [arghya.paul.162006@gmail.com](mailto:arghya.paul.162006@gmail.com)

**Supervised by:**
- **Dr. Sushruta Mishra** - *Faculty, School of Computer Engineering, KIIT University*

## 📧 Contact

For questions about the experiments or reproduction, please open an issue on GitHub or contact the authors directly.

## 🙏 Acknowledgments

- **RunPod** for providing cost-effective GPU compute infrastructure
- **Ollama** for the local LLM inference engine
- **Llama 3.2** model by Meta AI

## ⚠️ Security Note

The attack prompts in this repository are for **research purposes only**. Do not use these techniques for malicious purposes. Responsible disclosure practices were followed throughout this research.

---

**Last Updated:** December 26, 2025  
**Repository Status:** Archived for paper publication (commit: [COMMIT_HASH])
