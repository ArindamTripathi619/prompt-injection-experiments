# Critical Fixes Applied to Experiment 6

## Date: December 26, 2025

## Issues Discovered

### 1. Data Integrity Issues
- **Problem**: Inconsistent trial counts across experiments
  - Pods 1-3: 430 traces (mix of 5 and 15 trials per attack)
  - Pod 4: 320 traces (mix of 5 and 10 trials per attack)
  - Expected: 210 traces per pod (42 attacks × 5 trials)
- **Impact**: Statistical comparison invalid due to different sample sizes
- **Root Cause**: Experiments were interrupted and resumed with different trial parameters

### 2. Adaptive Coordination NOT Applied (CRITICAL BUG)
- **Problem**: Adaptive decisions calculated but NEVER passed to layers
  - **Layer 4 (Enhanced Monitoring)**: `enhanced_monitoring` flag set but not passed to `interact()` method
  - **Layer 5 (Threshold Adjustment)**: `threshold_adjustment` calculated but not passed to `validate()` method
- **Impact**: Pods 3 & 4 ran with DEFAULT behavior, not adapted behavior
- **Evidence**: 
  - Pod 3 ASR: 13.49% (WORSE than baseline 12.09%)
  - Pod 4 ASR: 15.31% (WORSE than baseline 12.09%)
  - Only Pod 2 (Layer 3 adaptive) showed improvement: 10.47% (isolation_mode WAS passed correctly)

### 3. Database Schema Missing Coordination Fields
- **Problem**: ExecutionTrace model has fields but Database.save_trace() doesn't save them
  - Missing: `propagation_path`, `bypass_mechanisms`, `trust_boundary_violations`, `coordination_enabled`, `coordination_context`
- **Impact**: Cannot verify or analyze adaptive coordination behavior from database
- **Evidence**: Summary JSONs show 100 L3 escalations, 85 L4 events, 45 L5 adjustments, but database has no storage for these

## Fixes Applied

### Fix 1: Layer 4 Enhanced Monitoring (Pod 3 & 4)
**File**: `pod3_adaptive_l4/adaptive_pipeline.py`, `pod4_full_adaptive/adaptive_pipeline.py`

**Before**:
```python
# Note: Layer4 doesn't accept enhanced_monitoring parameter
# Coordination decision is tracked in coordination_context above
layer4_result, llm_response = self.layer4.interact(
    request, 
    isolated_context or {"messages": [{"role": "user", "content": request.user_input}]}
)
```

**After**:
```python
# FIXED: Pass enhanced_monitoring as apply_guardrails parameter
layer4_result, llm_response = self.layer4.interact(
    request, 
    isolated_context or {"messages": [{"role": "user", "content": request.user_input}]},
    apply_guardrails=enhanced_monitoring
)
```

**Rationale**: Layer 4's `interact()` method already has an `apply_guardrails` parameter that controls enhanced constraint checking. We now pass the computed `enhanced_monitoring` flag to actually enable it for high-risk requests.

### Fix 2: Layer 5 Strict Mode (Pod 4 + All Pods)
**Files**: 
- `pod4_full_adaptive/adaptive_pipeline.py`
- `pod*/src/layers/layer5_output.py` (all 4 pods)

#### Pipeline Change:
**Before**:
```python
# Note: Layer5 doesn't accept threshold_adjustment parameter
# Coordination decision is tracked in coordination_context above  
layer5_result = self.layer5.validate(
    request, 
    final_output or ""
)
```

**After**:
```python
# FIXED: Pass threshold_adjustment as strict_mode parameter
layer5_result = self.layer5.validate(
    request, 
    final_output or "",
    strict_mode=(threshold_adjustment > 0)
)
```

#### Layer 5 Implementation Changes:
**Added strict_mode parameter to**:
1. `validate()` method signature
2. `_check_leakage()` helper (uses 3-word chunks instead of 5-word)
3. `_check_policy_violations()` helper (flags 2+ keywords instead of 3+)
4. Risk score boosting (+0.2 in strict mode)

**Behavior**:
- **Normal mode**: 5-word chunks, 20+ chars, 3+ policy keywords
- **Strict mode**: 3-word chunks, 15+ chars, 2+ policy keywords, +0.2 risk boost

### Fix 3: Consistent Trial Counts (To be applied before re-run)
**Action Required**: Verify all run scripts use `TRIALS=5` and clean databases before re-running

**Verification**:
```bash
grep "TRIALS=" pod*/run_pod*.sh
# All should show: TRIALS=5
```

### Fix 4: Database Schema (NOT YET FIXED - Lower Priority)
**Status**: Deferred until after re-run verification
**Reason**: Coordination tracking is now APPLIED (Fixes 1-2), but database storage can be added later for detailed analysis

**Future Work**:
- Update `Database.save_trace()` to save all ExecutionTrace fields
- Update schema creation to include: `propagation_path TEXT`, `bypass_mechanisms TEXT`, etc.
- Re-run experiments to populate new fields

## Expected Impact After Fixes

### Pod 1 (Isolated Baseline)
- **Expected ASR**: 12-14% (reference baseline)
- **Behavior**: No coordination, default layer behavior
- **Status**: No changes needed

### Pod 2 (Adaptive L3)
- **Current ASR**: 10.47% (✓ improvement)
- **Expected ASR**: 10-11% (continued improvement)
- **Behavior**: Already working correctly (isolation_mode passed)
- **Status**: No changes needed

### Pod 3 (Adaptive L4)
- **Current ASR**: 13.49% (❌ WORSE than baseline)
- **Expected ASR After Fix**: 9-10% (✓ ~3% improvement)
- **Behavior**: NOW applies enhanced guardrails when upstream_risk > 0.5
- **Status**: **FIXED** - enhanced_monitoring now passed to Layer 4

### Pod 4 (Full Adaptive)
- **Current ASR**: 15.31% (❌ WORSE than baseline)
- **Expected ASR After Fix**: 7-9% (✓ ~4-6% improvement)
- **Behavior**: NOW applies L3 isolation + L4 enhanced monitoring + L5 strict validation
- **Status**: **FIXED** - enhanced_monitoring + strict_mode now passed

## Statistical Validation Plan

After re-running experiments:
1. **Verify Sample Sizes**: All pods should have 210 traces (42 attacks × 5 trials)
2. **Calculate ASR**: Attack Success Rate for each pod
3. **McNemar's Test**: Compare each adaptive config vs baseline
   - H0: No difference in attack success/failure patterns
   - H1: Adaptive config reduces attack success
   - Significance: χ² > 3.84 (p < 0.05)
4. **Effect Size**: Calculate absolute ASR reduction and relative improvement
5. **Coordination Metrics**: Count adaptive events from summary JSONs (databases don't store yet)

## Git Commit Strategy

```bash
# Commit fixes to each pod repository
cd pod1_isolated && git add src/layers/layer5_output.py && git commit -m "Add strict_mode support to Layer 5"
cd ../pod2_adaptive_l3 && git add src/layers/layer5_output.py && git commit -m "Add strict_mode support to Layer 5"
cd ../pod3_adaptive_l4 && git add adaptive_pipeline.py src/layers/layer5_output.py && git commit -m "FIX: Pass enhanced_monitoring to Layer 4, add strict_mode to Layer 5"
cd ../pod4_full_adaptive && git add adaptive_pipeline.py src/layers/layer5_output.py && git commit -m "FIX: Pass enhanced_monitoring to Layer 4, add strict_mode to Layer 5"

# Push all changes
for pod in pod1_isolated pod2_adaptive_l3 pod3_adaptive_l4 pod4_full_adaptive; do
    cd $pod && git push origin main && cd ..
done
```

## Re-Run Instructions

1. **Clean Databases**:
   ```bash
   rm pod*/results/exp6_*.db pod*/results/*_summary.json
   ```

2. **Verify Trial Configuration**:
   ```bash
   grep "TRIALS=" pod*/run_pod*.sh  # Should all show TRIALS=5
   ```

3. **Run on RunPod**:
   - Pull latest code: `git pull origin main`
   - Clean results: `rm -rf results/*`
   - Run: `./run_pod*.sh`
   - Monitor: `tail -f results/experiment.log`

4. **Verify Results**:
   - Check trace count: `sqlite3 results/exp6_*.db "SELECT COUNT(*) FROM execution_traces;"`  # Should be 210
   - Check summary: `cat results/*_summary.json | jq .`
   - Check ASR: Should show improvements in Pods 2-4

## Timeline

- **Fixes Applied**: December 26, 2025 (current)
- **Re-Run Target**: Within 24 hours
- **Analysis Target**: Within 48 hours
- **Paper Update**: After statistical validation complete
