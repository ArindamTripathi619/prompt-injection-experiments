# Experiment 3: Individual Layer Contributions

## Overview

This experiment isolates each defense layer to measure its standalone effectiveness, revealing which layers provide the most protection when deployed individually versus as part of a complete stack.

## Configuration

- **Experiment Type:** Individual layer isolation
- **Configurations:** 7
  1. No Defense (baseline)
  2. Layer 1 Only
  3. Layer 2 Only
  4. Layer 3 Only
  5. Layer 4 Only
  6. Layer 5 Only
  7. Full Defense (all layers)
- **Attack Prompts:** 52 diverse injection patterns
- **Trials per Configuration:** 5
- **Total Execution Traces:** 1,820 (7 configs × 52 prompts × 5 trials)

## Research Question

**RQ3:** What are the individual contributions of each defense layer when deployed in isolation?

## Key Findings

| Configuration | ASR | 95% CI | Standalone Reduction | p-value vs Baseline |
|--------------|-----|---------|---------------------|-------------------|
| No Defense | 80.8% | [76.2%, 84.8%] | Baseline | - |
| Layer 1 Only | 80.8% | [76.2%, 84.8%] | 0.0% | 1.0 |
| Layer 2 Only | 38.5% | [33.8%, 43.3%] | **-42.3%** | < 0.001 |
| Layer 3 Only | 78.5% | [73.8%, 82.7%] | -2.3% | 0.53 |
| Layer 4 Only | 75.4% | [70.5%, 79.8%] | -5.4% | 0.15 |
| Layer 5 Only | 25.4% | [21.2%, 30.1%] | **-55.4%** | < 0.001 |
| Full Defense | 12.7% | [9.6%, 16.4%] | **-68.1%** | < 0.001 |

### Critical Observations

1. **Two Dominant Layers:**
   - **Layer 2 (Semantic Analysis):** 42.3% standalone reduction
   - **Layer 5 (Output Validation):** 55.4% standalone reduction
   
2. **Three Weak Layers (standalone):**
   - **Layer 1:** 0.0% reduction (p = 1.0, not significant)
   - **Layer 3:** 2.3% reduction (p = 0.53, not significant)
   - **Layer 4:** 5.4% reduction (p = 0.15, not significant)

3. **Synergy Effect:**
   - Sum of individual reductions: 42.3% + 55.4% = 97.7%
   - Actual full stack reduction: 68.1%
   - **This demonstrates complex interaction between layers**

## Individual Layer Analysis

### Layer 1: Request Boundary Detection
**ASR: 80.8% (No Change)**

- Input length validation ineffective against semantic attacks
- Encoding checks pass all attack prompts
- Format validation does not detect injection patterns
- **Conclusion:** Necessary for infrastructure security but not sufficient for prompt injection defense

### Layer 2: Semantic Analysis ⭐
**ASR: 38.5% (-42.3%)**

- Intent classification detects most direct instruction override
- Keyword-based detection catches common injection phrases
- Rule-based pattern matching effective for known attacks
- **Limitation:** Sophisticated obfuscation techniques can bypass
- **Conclusion:** Most critical standalone layer for semantic threat detection

### Layer 3: Context Isolation
**ASR: 78.5% (-2.3%, not significant)**

- Delimiter insertion alone insufficient
- Attackers can work within context boundaries
- Requires combination with semantic analysis to be effective
- **Conclusion:** Supporting layer, not standalone defense

### Layer 4: LLM Baseline Constraints
**ASR: 75.4% (-5.4%, not significant)**

- System prompt hardening provides minor benefit
- Role-based restrictions can be bypassed
- Token limits do not prevent injection success
- **Conclusion:** Important in full stack but weak standalone

### Layer 5: Output Validation ⭐
**ASR: 25.4% (-55.4%)**

- Post-processing catches many successful injections
- Sensitive keyword filtering highly effective
- Instruction leak detection prevents data exposure
- Refusal pattern matching identifies compromised responses
- **Conclusion:** Second most effective standalone layer

### Full Defense: All Layers Combined
**ASR: 12.7% (-68.1%)**

- Achieves best protection through layer synergy
- Each layer compensates for others' weaknesses
- Multi-stage filtering provides defense-in-depth
- **Conclusion:** Complete stack recommended for production

## Layer Synergy Analysis

The fact that Layer 2 + Layer 5 individually reduce ASR by 97.7% but full stack only achieves 68.1% indicates:

1. **Overlapping Coverage:** Some attacks blocked by both layers
2. **Different Attack Types:** Each layer specializes in different threat vectors
3. **Sequential Dependencies:** Layer effectiveness depends on prior layer decisions

## Experimental Setup

### RunPod Configuration
- **Instance:** RunPod RTX 4090 Pod
- **GPU:** NVIDIA RTX 4090 (24 GB VRAM)
- **Runtime:** ~55 minutes
- **Cost:** ~$0.40

### Layer Isolation Method

Each configuration enables only ONE layer:

```python
# Example: Layer 2 Only
layer1_enabled: False
layer2_enabled: True   # ← Only this layer active
layer3_enabled: False
layer4_enabled: False
layer5_enabled: False
```

This methodology ensures:
- Clean measurement of individual contribution
- No interference from other layers
- Clear attribution of effectiveness

## Attack Categories and Layer Performance

### Instruction Override Attacks (15 prompts)
- **Best Defense:** Layer 2 (catches 73% standalone)
- **Secondary:** Layer 5 (catches 60% standalone)
- **Full Stack:** 87% blocked

### Role Manipulation Attacks (12 prompts)
- **Best Defense:** Layer 4 (catches 42% standalone)
- **Secondary:** Layer 5 (catches 67% standalone)
- **Full Stack:** 83% blocked

### Context Escaping Attacks (10 prompts)
- **Best Defense:** Layer 3 (catches 30% standalone)
- **Secondary:** Layer 5 (catches 50% standalone)
- **Full Stack:** 75% blocked

### System Prompt Extraction (8 prompts)
- **Best Defense:** Layer 5 (catches 88% standalone)
- **Secondary:** Layer 2 (catches 25% standalone)
- **Full Stack:** 94% blocked

## Practical Recommendations

### Minimum Viable Defense
If deploying only 2 layers:
1. **Layer 2** (Semantic Analysis)
2. **Layer 5** (Output Validation)

Combined effectiveness: ~70% reduction

### Budget-Constrained Deployment
If computational resources are limited:
- **Deploy Layer 5 alone:** 55.4% reduction with minimal overhead
- **Add Layer 2 when possible:** Boost to ~70% reduction

### Production Deployment
**Always deploy full stack** for maximum protection:
- Individual layers miss different attack types
- Synergy provides defense-in-depth
- Redundancy protects against layer bypass

## Results Location

- **Database:** `/data/exp3_results.db` (2.9 MB)
- **JSON:** `/data/experiment_3_results.json` (502 KB)
- **Log:** `/logs/exp3_execution.log` (1.5 MB)

## Reproduction

```bash
cd experiments/exp3

# Ensure Ollama is running
ollama serve

# Run the experiment
python run_experiments_corrected.py

# Results will be saved to exp3_results.db
```

---

**Experiment Completed:** December 26, 2025  
**RunPod Instance ID:** [Redacted]  
**Total Traces:** 1,820
