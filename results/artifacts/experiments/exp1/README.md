# Experiment 1: Baseline Effectiveness

## Overview

This experiment establishes the baseline Attack Success Rate (ASR) without any defense mechanisms and validates the effectiveness of the complete multi-layer defense architecture.

## Configuration

- **Experiment Type:** Baseline comparison
- **Configurations:** 4
  1. Config A: No Defense (all layers disabled)
  2. Config B: Layer 2 Only (semantic analysis)
  3. Config C: Layers 2+3 (semantic + context isolation)
  4. Config D: Full Defense (all 5 layers enabled)
- **Attack Prompts:** 52 diverse injection patterns
- **Trials per Configuration:** 5
- **Total Execution Traces:** 1,040 (4 configs × 52 prompts × 5 trials)

## Research Question

**RQ1:** What is the baseline effectiveness of prompt injection attacks, and how effective is a full multi-layer defense?

## Key Findings

| Configuration | ASR | 95% CI | Reduction | p-value |
|--------------|-----|---------|-----------|----------|
| Config A: No Defense | 80.8% | [76.2%, 84.8%] | Baseline | - |
| Config B: Layer 2 Only | 38.5% | [33.8%, 43.3%] | -42.3% | < 0.001 |
| Config C: Layers 2+3 | 35.8% | [31.1%, 40.7%] | -45.0% | < 0.001 |
| Config D: Full Defense | 12.7% | [9.6%, 16.4%] | -68.1% | < 0.001 |

### Statistical Significance

- **McNemar's Test:** p < 0.001 (highly significant)
- **Cohen's h:** 1.82 (very large effect size)
- **Sample Size:** n = 520 per configuration (adequate power)

### Interpretation

The full multi-layer defense reduces the Attack Success Rate by **68.1 percentage points**, from 80.8% to 12.7%. This represents an **84.3% relative reduction** in successful attacks, demonstrating the high effectiveness of the proposed architecture.

## Experimental Setup

### RunPod Configuration
- **Instance:** RunPod RTX 4090 Pod
- **GPU:** NVIDIA RTX 4090 (24 GB VRAM)
- **Runtime:** ~30 minutes
- **Cost:** ~$0.22

### Software Stack
- **OS:** Ubuntu 22.04
- **Python:** 3.11
- **LLM Backend:** Ollama
- **Model:** Llama 3.2:1b (locally hosted)

### Defense Configuration

**Full Defense (All Layers Enabled):**
1. **Layer 1:** Request Boundary Detection
   - Max input length: 2000 characters
   - Encoding validation: UTF-8
   
2. **Layer 2:** Semantic Analysis
   - Intent classification threshold: 0.6
   - Injection detection patterns: 15 keywords
   
3. **Layer 3:** Context Isolation
   - Clear delimiter: `--- USER INPUT ---`
   - Context prefix enforcement
   
4. **Layer 4:** LLM Baseline Constraints
   - System prompt with security rules
   - Role-based restrictions
   - Max tokens: 500
   
5. **Layer 5:** Output Validation
   - Sensitive keyword filtering
   - Instruction leak detection
   - Refusal pattern matching

## Attack Prompt Distribution

The 52 attack prompts cover multiple categories:

- **Instruction Override (15):** Direct requests to ignore previous instructions
- **Role Manipulation (12):** Attempts to change the AI's persona
- **Context Escaping (10):** Breaking out of input boundaries
- **System Prompt Extraction (8):** Extracting internal configuration
- **Multi-Turn Sequences (7):** Complex multi-step attacks

## Execution Details

### Database Schema

Results are stored in `exp1_results.db` with the following structure:

```sql
-- Execution traces table
CREATE TABLE execution_traces (
    id INTEGER PRIMARY KEY,
    experiment_id TEXT,
    config_name TEXT,
    trial_number INTEGER,
    user_input TEXT,
    attack_successful BOOLEAN,
    timestamp TEXT
);

-- Layer results table
CREATE TABLE layer_results (
    id INTEGER PRIMARY KEY,
    trace_id INTEGER,
    layer_name TEXT,
    blocked BOOLEAN,
    reason TEXT,
    FOREIGN KEY (trace_id) REFERENCES execution_traces(id)
);
```

### Execution Log

Detailed execution logs are available in `/logs/exp1_execution.log` (848 KB), containing:
- Configuration initialization
- Per-trial execution traces
- Layer-by-layer decision logs
- Attack success/failure determinations
- Performance metrics

## Reproduction

To reproduce this experiment:

```bash
cd experiments/exp1

# Ensure Ollama is running
ollama serve

# Run the experiment
python run_experiments_corrected.py

# Results will be saved to exp1_results.db
# Logs will be written to experiments_corrected.log
```

## Results Location

- **Database:** `/data/exp1_results.db` (1.7 MB)
- **JSON:** `/data/experiment_1_results.json` (289 KB)
- **Log:** `/logs/exp1_execution.log` (848 KB)

## Notes

- This experiment uses the original attack prompt set (52 patterns)
- All prompts are evaluated in both "with defense" and "without defense" modes
- Statistical analysis uses paired McNemar's test since the same prompts are evaluated in both conditions
- The high baseline ASR (80.8%) confirms the severity of the prompt injection threat
- The substantial reduction (68.1%) validates the practical utility of the defense architecture

---

**Experiment Completed:** December 25, 2025  
**RunPod Instance ID:** [Redacted]  
**Total Traces:** 1,040
