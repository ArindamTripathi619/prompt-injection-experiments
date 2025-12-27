# Experiment 2: Progressive Layer Addition

## Overview

This experiment analyzes how defense effectiveness changes as layers are added incrementally to the defense stack, revealing the cumulative impact of each layer and identifying critical defense thresholds.

## Configuration

- **Experiment Type:** Progressive layering
- **Configurations:** 6
  1. Layer 1 Only
  2. Layers 1-2 (L1 + L2)
  3. Layers 1-3 (L1 + L2 + L3)
  4. Layers 1-4 (L1 + L2 + L3 + L4)
  5. Layers 1-5 (Full Stack)
  6. No Defense (baseline)
- **Attack Prompts:** 52 diverse injection patterns
- **Trials per Configuration:** 5
- **Total Execution Traces:** 1,560 (6 configs × 52 prompts × 5 trials)

## Research Question

**RQ2:** How does defense effectiveness change when layers are added progressively from Layer 1 through Layer 5?

## Key Findings

| Configuration | ASR | 95% CI | Cumulative Reduction | p-value |
|--------------|-----|---------|---------------------|----------|
| No Defense | 80.8% | [76.2%, 84.8%] | Baseline | - |
| Layer 1 Only | 80.8% | [76.2%, 84.8%] | 0.0% | 1.0 |
| Layers 1-2 | 38.5% | [33.8%, 43.3%] | -42.3% | < 0.001 |
| Layers 1-3 | 35.8% | [31.1%, 40.7%] | -45.0% | < 0.001 |
| Layers 1-4 | 22.7% | [18.7%, 27.2%] | -58.1% | < 0.001 |
| Layers 1-5 (Full) | 12.7% | [9.6%, 16.4%] | -68.1% | < 0.001 |

### Critical Observations

1. **Layer 1 Provides No Benefit:** ASR remains at 80.8% (p = 1.0)
   - Input validation alone cannot detect semantic attacks
   
2. **Layer 2 is the Critical Threshold:** Drops ASR by 42.3 percentage points
   - Semantic analysis is essential for meaningful defense
   
3. **Layer 3 Adds Minor Value:** Additional 2.7 percentage point reduction
   - Context isolation provides marginal improvement
   
4. **Layer 4 Provides Significant Boost:** Additional 13.1 percentage point reduction
   - LLM-level constraints are important
   
5. **Layer 5 Completes the Defense:** Final 10.0 percentage point reduction
   - Output validation catches residual attacks

## Incremental Impact Analysis

| Layer Added | ASR Before | ASR After | Incremental Reduction | p-value |
|-------------|-----------|-----------|---------------------|----------|
| L1 | 80.8% | 80.8% | 0.0% | 1.0 |
| L2 | 80.8% | 38.5% | -42.3% | < 0.001 |
| L3 | 38.5% | 35.8% | -2.7% | 0.048 |
| L4 | 35.8% | 22.7% | -13.1% | < 0.001 |
| L5 | 22.7% | 12.7% | -10.0% | < 0.001 |

## Experimental Setup

### RunPod Configuration
- **Instance:** RunPod RTX 4090 Pod
- **GPU:** NVIDIA RTX 4090 (24 GB VRAM)
- **Runtime:** ~45 minutes
- **Cost:** ~$0.33

### Layer Activation Patterns

**Configuration 1: Layer 1 Only**
```python
layer1_enabled: True
layer2_enabled: False
layer3_enabled: False
layer4_enabled: False
layer5_enabled: False
```

**Configuration 2: Layers 1-2**
```python
layer1_enabled: True
layer2_enabled: True
layer3_enabled: False
layer4_enabled: False
layer5_enabled: False
```

And so on through Configuration 5 (all layers enabled).

## Defense Behavior Patterns

### Phase 1: No Semantic Defense (Layer 1 Only)
- Attacks bypass simple input validation
- Semantic injection patterns undetected
- ASR remains at baseline 80.8%

### Phase 2: Semantic Analysis Added (Layers 1-2)
- **Major ASR drop to 38.5%**
- Intent classification detects most obvious injections
- Keyword-based detection catches common patterns
- Remaining attacks use sophisticated obfuscation

### Phase 3: Context Isolation (Layers 1-3)
- Minor improvement to 35.8%
- Delimiter helps separate user input
- Some context-breaking attacks still succeed

### Phase 4: LLM Constraints (Layers 1-4)
- Significant improvement to 22.7%
- System prompt hardening prevents role manipulation
- Instruction following becomes more resistant

### Phase 5: Output Validation (Layers 1-5)
- Final improvement to 12.7%
- Post-processing catches instruction leaks
- Sensitive data exposure prevented

## Statistical Analysis

### Pairwise Comparisons

All adjacent configurations show statistically significant differences (p < 0.001) except:
- L1 vs. No Defense: p = 1.0 (no difference)
- L2 vs. L3: p = 0.048 (marginally significant)

### Effect Sizes (Cohen's h)

- No Defense → L1: 0.00 (no effect)
- L1 → L2: 0.88 (large effect)
- L2 → L3: 0.05 (negligible effect)
- L3 → L4: 0.29 (small-medium effect)
- L4 → L5: 0.23 (small effect)

## Results Location

- **Database:** `/data/exp2_results.db` (2.7 MB)
- **JSON:** `/data/experiment_2_results.json` (432 KB)
- **Log:** `/logs/exp2_execution.log` (1.3 MB)

## Key Insights for Practitioners

1. **Don't rely on input validation alone** - Layer 1 provides no protection against semantic attacks
2. **Semantic analysis is mandatory** - Layer 2 is the foundation of effective defense
3. **Layered defense works** - Each subsequent layer adds incremental protection
4. **Full stack recommended** - Even the final layers contribute meaningful reduction

## Reproduction

```bash
cd experiments/exp2

# Ensure Ollama is running
ollama serve

# Run the experiment
python run_experiments_corrected.py

# Results will be saved to exp2_results.db
```

---

**Experiment Completed:** December 25, 2025  
**RunPod Instance ID:** [Redacted]  
**Total Traces:** 1,560
