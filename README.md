# Prompt Injection Defense: Multi-Layer Architecture Experiments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the complete experimental validation of a six-layer defense architecture against prompt injection attacks in Large Language Models (LLMs). All experiments were conducted on a high-performance local environment utilizing **LiteLLM** for adaptive coordination.

## 📄 Paper Reference

This repository corresponds to the experimental validation described in:

**"Evaluating and Mitigating Prompt Injection in Full-Stack Web Applications: A System-Level Workflow Model"**

**Paper Version:** The results in this repository represent the high-precision validation conducted in February 2026.

## 🎯 Project Overview

This research proposes and validates a comprehensive six-layer defense architecture:

1. **Layer 1: Request Boundary** - Character-level validation and preliminary classification
2. **Layer 2: Input Processing & Semantic Analysis** - Intent classification and prompt injection detection
3. **Layer 3: Context Management & Isolation** - Separation of user data from trusted system instructions (L3/L4)
4. **Layer 4: LLM Interaction & Constraint Enforcement** - Representation-level monitoring and guardrails
5. **Layer 5: Output Handling & Validation** - Response filtering and data leakage prevention
6. **Layer 6: Feedback & Adaptive Monitoring** - Continuous learning and pattern adaptation

### Key Findings

- **Baseline Attack Success Rate (ASR):** **80.8%** — the unprotected LLM is highly vulnerable (95% CI [75.5%, 85.1%])
- **Full Stack Aggregate ASR:** **18.9%** — a **76.6% relative risk reduction** over the baseline
- **Full Stack Stealth-Subset ASR:** **0.0%** across 2,450 stealth traces (95% CI [0.0%, 0.12%])
- **Isolation Illusion:** Isolated Layer 3 (Context Isolation) alone yields **80.8% ASR** — statistically identical to no defense (p ≈ 1.0), demonstrating that logical isolation without semantic filtering provides zero standalone protection
- **Utility Validation:** **0.0% False Positive Rate (FPR)** across 1,000 diverse benign prompt tests (95% CI [0.0%, 0.37%])
- **Statistical Significance:** McNemar's $\chi^2(1) = 173.0, p < 0.001$ (paired N=260 core adversarial prompts)
- **Sample Size:** **11,490 execution traces** across 103 configurations, evaluated using an independent LLM-as-a-Judge (Llama-3.1-405b)

## 🖼️ Visual Documentation

For a deeper understanding of the system architecture and experimental results, please refer to the following rich documents:

### Architecture & Flow
- [🏗️ **Architecture Overview**](DOCS/architecture_overview.md) - Detailed view of the 6-layer defense stack.
- [🔄 **Data Flow & Pipeline**](DOCS/data_flow.md) - How requests traverse the defense pipeline.
- [🧠 **Adaptive Defense Logic**](DOCS/adaptive_logic.md) - Deep dive into Layer 6 escalation mechanisms.

### Research & Analysis
- [🧪 **Experiment Workflow**](DOCS/experiment_workflow.md) - Orchestration of the high-precision validation.
- [🔍 **Attack Taxonomy**](DOCS/attack_taxonomy.md) - Categorization of injection patterns tested.
- [📊 **Evaluation & Statistics**](DOCS/evaluation_methodology.md) - Mathematical foundations and scoring logic.
- [🧐 **Result Inferences**](DOCS/inferences.md) - Qualitative analysis and the "Isolation Illusion."

### Performance & Development
- [🛠️ **Developer Guide**](DOCS/developer_guide.md) - Guidelines for extending the defense or adding data.
- [⚡ **Performance Analysis**](DOCS/performance.md) - Latency, memory usage, and utility trade-offs.

## 🏗️ Repository Structure

```
prompt-injection-experiments/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable templates
│
├── data/                              # Data and Visualizations
│   ├── attack_prompts.py              # 52 diverse injection patterns
│   └── benign_prompts_large.py        # 1,000 diverse benign prompts (Utility stress test)
│
├── src/                               # Core Source Code
│   ├── config.py                      # Thread-safe configuration settings
│   ├── experiment_runner.py           # Multithreaded experiment orchestration
│   ├── unified_pipeline.py            # Main coordinated defense pipeline
│   ├── statistical_analysis.py        # McNemar's and Chi-squared testing tools
│   ├── create_visualizations.py       # Premium visualization generation engine
│   └── layers/                        # Defense layer implementations (L1-L6)
```

## 🧪 Experimental Methodology

### Experiment Design

We conducted a high-precision experimental campaign involving **11,490 individual LLM interactions**:

1. **Baseline Campaign**: Evaluated vanilla LLM performance vs. standard layered defenses.
2. **Layer Ablation Study**: Identified the **'Isolation Illusion'** where Layer 3 (Context Isolation) fails catastrophically in isolation (**80.8% ASR — no improvement vs. baseline**) but contributes effectively when coordinated within the full stack, confirming that semantic filtering is a prerequisite for isolation to work.
3. **Utility Stress Test**: Processed 1,000 diverse benign prompts (Professional, Creative, Technical) through the full defense stack to confirm a **0.0% False Positive Rate** (95% CI [0.0%, 0.37%]).

### Infrastructure: High-Performance Setup

The experimental validation was optimized for the following environment:

- **OS/Arch:** Linux x86_64
- **CPU:** AMD Ryzen 7 8840HS (8 Cores, 16 Threads)
- **Memory:** 32GB RAM
- **LLM Backend:** **groq/llama-3.3-70b-versatile** (via local LiteLLM proxy)
- **Performance**: Multithreaded orchestration achieved **11,490 traces in approximately 3.5 hours**.
- **Evaluator**: Independent LLM-as-a-Judge (`Llama-3.1-405b`) for binary ASR classification
- **Parameters**: Temperature: 0.0 (Deterministic), Top P: 1.0

## 🚀 Reproducing the Results

### Prerequisites

1. **Python 3.11+**
2. **Groq API Key** (or compatible OpenAI-format endpoint)
3. **SQLite3**

### Setup

```bash
# Clone the repository
git clone https://github.com/Arindamtripathi619/prompt-injection-experiments.git
cd prompt-injection-experiments

# Create environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY (or local proxy URL)
```

### Running the Validation

To reproduce the final high-precision campaign:

```bash
# Run the full experiment suite (Parallelized)
python src/run_experiments.py

# Run comprehensive statistical analysis
python src/statistical_analysis.py
```

## 📊 Key Results

### Overall Attack Success Rate (ASR)

| Configuration | ASR | 95% CI | Notes |
|---|---|---|---|
| Baseline (No Defense) | **80.8%** | [75.5%, 85.1%] | Unprotected LLM |
| Semantic Only (L2) | 38.5% | [32.8%, 44.5%] | Standalone semantic filter |
| Layer 3 Solo (Isolation Only) | **80.8%** | [75.5%, 85.1%] | No measurable improvement — the "Isolation Illusion" |
| Output Solo (L5) | 25.4% | [20.5%, 31.0%] | Standalone output filter |
| **Full Stack (L1-L6) — Aggregate** | **18.9%** | [18.1%, 19.8%] | **76.6% relative reduction** |
| **Full Stack — Stealth Subset only** | **0.0%** | [0.0%, 0.12%] | Over 2,450 stealth traces |

### McNemar's Significance Test (Paired Core Subset, N=260 prompts)

| Comparison | χ² | p-value |
|---|---|---|
| **Full Stack vs. Baseline** | **χ²(1) = 173.0** | **p < 0.001** |
| **Full Stack vs. L3 Solo** | **χ²(1) = 161.0** | **p < 0.0001** |
| Cohen's h (Full Stack vs. Baseline) | h = 1.33 | Large effect size |

## 🤝 Contributing

This repository represents archived experimental material for a journal publication. While we welcome feedback through GitHub Issues, this branch is finalized for reproducibility purposes.

## 👥 Authors

- **Arindam Tripathi** - *Lead Researcher* - [Arindamtripathi619](https://github.com/Arindamtripathi619)
- **Arghya Bose** - *Researcher* - [officialarghya29](https://github.com/officialarghya29)
- **Arghya Paul** - *Researcher* - 24155977@kiit.ac.in

**Supervised by:**
- **Dr. Sushruta Mishra** - *Faculty, School of Computer Engineering, KIIT University*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated:** March 2026 — README synced with `Research_Paper.tex` (final February 2026 validation)  
**Status:** Final Experimental Validation — 11,490 traces, Groq/Llama-3.3-70b, 0.0% stealth-subset ASR, 18.9% aggregate ASR, 0.0% FPR
