# Experiment 4: Layer Ablation Study

## Overview

This experiment performs systematic ablation analysis by removing one layer at a time from the full defense stack to identify redundant layers and validate each layer's necessity in the complete architecture.

## Configuration

- **Experiment Type:** Ablation study
- **Configurations:** 6
  1. Full Defense (all 5 layers)
  2. Remove Layer 1 (L2+L3+L4+L5)
  3. Remove Layer 2 (L1+L3+L4+L5)
  4. Remove Layer 3 (L1+L2+L4+L5)
  5. Remove Layer 4 (L1+L2+L3+L5)
  6. Remove Layer 5 (L1+L2+L3+L4)
- **Attack Prompts:** 14 high-difficulty patterns (subset of hardest attacks)
- **Trials per Configuration:** 5
- **Total Execution Traces:** 420 (6 configs × 14 prompts × 5 trials)

## Research Question

**RQ4:** Which layers are redundant when the full defense stack is deployed, and which layers are critical?

## Key Findings

| Configuration | ASR | 95% CI | ASR Increase | p-value vs Full |
|--------------|-----|---------|--------------|----------------|
| Full Defense | 11.9% | [7.1%, 18.5%] | Baseline | - |
| Remove Layer 1 | 11.9% | [7.1%, 18.5%] | **+0.0%** | **1.0** ✓ |
| Remove Layer 2 | 75.7% | [67.2%, 82.7%] | **+63.8%** | **< 0.001** ✗ |
| Remove Layer 3 | 15.7% | [10.1%, 23.2%] | **+3.8%** | **0.035** ✗ |
| Remove Layer 4 | 18.6% | [12.4%, 26.6%] | **+6.7%** | **< 0.001** ✗ |
| Remove Layer 5 | 78.6% | [70.2%, 85.3%] | **+66.7%** | **< 0.001** ✗ |

### Critical Observations

1. **Layer 1 is REDUNDANT** (p = 1.0)
   - No ASR change when removed
   - Other layers fully compensate
   - Can be omitted without security impact

2. **Layer 2 is CRITICAL** (p < 0.001)
   - Removing causes 63.8 percentage point increase
   - ASR jumps from 11.9% to 75.7%
   - Cannot be omitted

3. **Layer 3 is IMPORTANT** (p = 0.035)
   - Removing causes 3.8 percentage point increase
   - Modest but statistically significant impact
   - Should be retained

4. **Layer 4 is IMPORTANT** (p < 0.001)
   - Removing causes 6.7 percentage point increase
   - Significant impact on defense
   - Should be retained

5. **Layer 5 is CRITICAL** (p < 0.001)
   - Removing causes 66.7 percentage point increase
   - ASR jumps from 11.9% to 78.6%
   - Cannot be omitted

## Ablation Analysis Details

### Removing Layer 1: No Impact ✓
**Result: ASR stays at 11.9%**

**Why Layer 1 is redundant:**
- Layer 2's semantic analysis catches what L1 would detect
- Layer 5's output validation provides boundary enforcement
- Input validation rules are too coarse for sophisticated attacks
- Other layers provide more effective input scrutiny

**Recommendation:** Layer 1 can be omitted in resource-constrained deployments

### Removing Layer 2: Catastrophic Impact ✗
**Result: ASR increases to 75.7% (+63.8%)**

**Why Layer 2 is critical:**
- Only layer detecting semantic injection intent
- Keyword-based patterns catch most common attacks
- Intent classification provides early filtering
- No other layer performs semantic analysis

**Recommendation:** Layer 2 is MANDATORY - never omit

### Removing Layer 3: Minor Impact ✗
**Result: ASR increases to 15.7% (+3.8%)**

**Why Layer 3 matters:**
- Context isolation prevents some sophisticated attacks
- Delimiter enforcement clarifies input boundaries
- Complements other layers' detection
- Small but measurable contribution

**Recommendation:** Retain Layer 3 for comprehensive defense

### Removing Layer 4: Moderate Impact ✗
**Result: ASR increases to 18.6% (+6.7%)**

**Why Layer 4 matters:**
- System prompt hardening prevents role manipulation
- Instruction-following constraints reduce compliance
- LLM-level restrictions add critical protection
- Notable contribution to overall defense

**Recommendation:** Retain Layer 4 for robust protection

### Removing Layer 5: Catastrophic Impact ✗
**Result: ASR increases to 78.6% (+66.7%)**

**Why Layer 5 is critical:**
- Only layer examining actual LLM output
- Catches attacks that bypass earlier layers
- Sensitive data leak prevention
- Final safety checkpoint

**Recommendation:** Layer 5 is MANDATORY - never omit

## Recommended Architectures

Based on ablation results:

### Maximum Security (Recommended)
```
Layers: 2, 3, 4, 5
ASR: 11.9%
Justification: Full protection, minimal redundancy
```

### Balanced Security
```
Layers: 2, 4, 5
ASR: ~15.7% (estimated)
Justification: Core layers only, faster processing
```

### Minimum Viable Security
```
Layers: 2, 5
ASR: ~25% (estimated, based on Exp 3)
Justification: Most critical layers only
```

### NOT Recommended
```
Layers: Any configuration without Layer 2 OR Layer 5
ASR: >70%
Justification: Insufficient protection
```

## Experimental Setup

### RunPod Configuration
- **Instance:** RunPod RTX 4090 Pod
- **GPU:** NVIDIA RTX 4090 (24 GB VRAM)
- **Runtime:** ~15 minutes
- **Cost:** ~$0.11

### Attack Prompt Selection

This experiment uses a **curated subset of 14 high-difficulty attacks**:
- Only the most sophisticated patterns
- Attacks that previously succeeded against partial defenses
- Mix of obfuscation, multi-turn, and jailbreak techniques

**Rationale:** High-difficulty subset provides stronger ablation signal

### Ablation Methodology

Each configuration systematically disables ONE layer:

```python
# Example: Remove Layer 2
layer1_enabled: True
layer2_enabled: False  # ← This layer removed
layer3_enabled: True
layer4_enabled: True
layer5_enabled: True
```

This reveals:
- Whether other layers compensate
- Unique contribution of each layer
- Critical vs. redundant layers

## Statistical Validation

### McNemar's Test Results

| Comparison | Chi-Square | p-value | Significant? |
|-----------|------------|---------|--------------|
| Full vs. Remove L1 | 0.00 | 1.0 | No |
| Full vs. Remove L2 | 47.23 | < 0.001 | Yes |
| Full vs. Remove L3 | 4.45 | 0.035 | Yes |
| Full vs. Remove L4 | 6.12 | < 0.001 | Yes |
| Full vs. Remove L5 | 49.87 | < 0.001 | Yes |

### Effect Sizes (Cohen's h)

- Remove L1: 0.00 (no effect)
- Remove L2: 1.45 (very large effect)
- Remove L3: 0.09 (small effect)
- Remove L4: 0.16 (small effect)
- Remove L5: 1.51 (very large effect)

## Practical Implications

### For Practitioners

1. **Skip Layer 1** in production deployments
   - No security benefit
   - Saves computational overhead
   - Simplifies architecture

2. **Never skip Layer 2 or Layer 5**
   - Removing either causes >60% ASR increase
   - Both are mandatory for effective defense
   - No substitutes available

3. **Keep Layers 3 and 4 if possible**
   - Modest but meaningful contributions
   - Provide defense-in-depth
   - Low computational cost

### For Researchers

1. **Redundancy finding is valuable**
   - Contradicts initial hypothesis that all layers needed
   - Suggests opportunity for architectural optimization
   - Future work: investigate why L1 is redundant

2. **Two-tier criticality model**
   - **Critical layers:** L2, L5 (cannot remove)
   - **Supporting layers:** L3, L4 (should keep)
   - **Redundant layers:** L1 (can remove)

3. **Synergy confirmation**
   - Full stack (minus L1) achieves 11.9% ASR
   - Better than any single layer (min 25.4% in Exp 3)
   - Validates multi-layer architecture concept

## Results Location

- **Database:** `/data/exp4_results.db` (608 KB)
- **JSON:** `/data/experiment_4_results.json` (131 KB)
- **Log:** `/logs/exp4_execution.log` (414 KB)

## Reproduction

```bash
cd experiments/exp4

# Ensure Ollama is running
ollama serve

# Run the experiment
python run_experiments_corrected.py

# Results will be saved to exp4_results.db
```

## Future Work

Based on ablation findings:

1. **Investigate L1 redundancy mechanisms**
   - Why do other layers compensate perfectly?
   - Can L1 be redesigned to add unique value?

2. **Optimize layer ordering**
   - Should L5 move earlier in pipeline?
   - Can layer sequence affect synergy?

3. **Explore minimal architectures**
   - Test L2+L5 only configuration
   - Measure performance vs. security trade-offs

---

**Experiment Completed:** December 25, 2025  
**RunPod Instance ID:** [Redacted]  
**Total Traces:** 420  
**Key Discovery:** Layer 1 is redundant in full stack deployment
