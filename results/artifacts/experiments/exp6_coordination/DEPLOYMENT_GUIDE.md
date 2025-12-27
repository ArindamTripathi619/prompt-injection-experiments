# Experiment 6: Deployment Guide
## 4-Pod Parallel Execution for Adaptive Coordination Testing

### Quick Deployment Commands

#### Pod 1: Isolated Baseline (No Coordination)
```bash
git clone https://github.com/ArindamTripathi619/exp6_pod1_isolated.git
cd exp6_pod1_isolated
git config --global user.email "arindamtripathi.619@gmail.com"
git config --global user.name "ArindamTripathi619"
BACKGROUND=true bash run_pod1.sh
```

#### Pod 2: Adaptive Layer 3
```bash
git clone https://github.com/ArindamTripathi619/exp6_pod2_adaptive_l3.git
cd exp6_pod2_adaptive_l3
git config --global user.email "arindamtripathi.619@gmail.com"
git config --global user.name "ArindamTripathi619"
BACKGROUND=true bash run_pod2.sh
```

#### Pod 3: Adaptive Layer 4
```bash
git clone https://github.com/ArindamTripathi619/exp6_pod3_adaptive_l4.git
cd exp6_pod3_adaptive_l4
git config --global user.email "arindamtripathi.619@gmail.com"
git config --global user.name "ArindamTripathi619"
BACKGROUND=true bash run_pod3.sh
```

#### Pod 4: Full Adaptive Coordination
```bash
git clone https://github.com/ArindamTripathi619/exp6_pod4_full_adaptive.git
cd exp6_pod4_full_adaptive
git config --global user.email "arindamtripathi.619@gmail.com"
git config --global user.name "ArindamTripathi619"
BACKGROUND=true bash run_pod4.sh
```

### Monitoring All Pods

#### Check progress on each pod:
```bash
# Pod 1
tail -f ~/exp6_pod1_isolated/results/experiment.log

# Pod 2
tail -f ~/exp6_pod2_adaptive_l3/results/experiment.log

# Pod 3
tail -f ~/exp6_pod3_adaptive_l4/results/experiment.log

# Pod 4
tail -f ~/exp6_pod4_full_adaptive/results/experiment.log
```

#### Quick status check (run on each pod):
```bash
# Shows: trace count / expected (210)
sqlite3 results/exp6_*.db "SELECT COUNT(*) as traces FROM execution_traces"

# Shows: successful attacks, blocked attacks, ASR
sqlite3 results/exp6_*.db "SELECT 
    COUNT(*) as total,
    SUM(attack_successful) as succeeded,
    SUM(CASE WHEN attack_successful = 0 THEN 1 ELSE 0 END) as blocked,
    ROUND(100.0 * SUM(attack_successful) / COUNT(*), 2) as ASR
FROM execution_traces"
```

### Expected Timeline

| Time | Event |
|------|-------|
| 0:00 | Start all 4 pods simultaneously |
| 0:30 | Ollama downloads complete |
| 1:00 | Experiments begin |
| 4:00 | First pods start completing |
| 5:00 | All pods complete |

**Total runtime: ~5 minutes** (parallel execution)

### Files to Download (from each pod)

```
results/exp6_isolated.db                    # Pod 1 - 340KB
results/exp6_isolated_summary.json          # Pod 1 - 500B
results/exp6_adaptive_l3.db                 # Pod 2 - 350KB
results/exp6_adaptive_l3_summary.json       # Pod 2 - 600B
results/exp6_adaptive_l4.db                 # Pod 3 - 350KB
results/exp6_adaptive_l4_summary.json       # Pod 3 - 600B
results/exp6_full_adaptive.db               # Pod 4 - 360KB
results/exp6_full_adaptive_summary.json     # Pod 4 - 700B
```

**Total download: ~1.5MB**

### Configuration Matrix

| Pod | Config | Coordination | Layer 3 Adaptive | Layer 4 Enhanced | Layer 5 Adjusted |
|-----|--------|--------------|------------------|------------------|------------------|
| 1 | Isolated | ❌ No | Fixed "good" | Standard | Default thresholds |
| 2 | Adaptive L3 | ✅ Yes | **risk>0.6→strict**, risk>0.4→metadata | Standard | Default |
| 3 | Adaptive L4 | ✅ Yes | Fixed "good" | **risk>0.5→enhanced** | Default |
| 4 | Full Adaptive | ✅ Yes | **Dynamic** | **Enhanced** | **Lowered by 0.2** |

### Expected Results

| Pod | Config | Expected ASR | Expected Blocked | Target Improvement |
|-----|--------|--------------|------------------|---------------------|
| 1 | Isolated | 16-17% | 174-175 | Baseline |
| 2 | Adaptive L3 | 14-15% | 178-180 | +2-3% |
| 3 | Adaptive L4 | 13-14% | 180-182 | +3-4% |
| 4 | Full Adaptive | **10-12%** | **185-189** | **+5-7%** ✅ |

**Success criteria:** Pod 4 ASR ≤ 12% (statistically significant improvement)

### Budget & Cost

- **4 pods** × **$0.44/hr** × **0.08 hrs** = **$0.14**
- **Total experiment cost:** ~$0.15
- **Well under budget!** ($6 available, $0.15 used = 2.5% utilization)

### Post-Experiment Analysis

After all pods complete, download all files and run:

```bash
python3 analyze_exp6_cross_pod.py \
    --pod1 exp6_isolated.db \
    --pod2 exp6_adaptive_l3.db \
    --pod3 exp6_adaptive_l4.db \
    --pod4 exp6_full_adaptive.db
```

This will generate:
- ASR comparison across all 4 configs
- Statistical significance tests (McNemar's)
- Adaptive behavior frequency analysis
- Propagation path visualization
- Trust boundary violation breakdown

### Troubleshooting

**Pod stuck at "Pulling llama3":**
- This is normal first time, takes 2-3 minutes
- Model is 4.7GB, watch disk space

**Experiment not starting:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart if needed
killall ollama
bash run_pod*.sh
```

**Background mode not working:**
```bash
# Check for running process
ps aux | grep run_experiment6

# Check logs
tail -f results/experiment.log

# Kill and restart if hung
kill $(cat results/experiment.pid)
BACKGROUND=true bash run_pod*.sh
```

### Success Verification

Each pod should show:
```
✅ EXPERIMENT COMPLETE - POD X
Total traces: 210
Successful attacks: XX
Blocked attacks: XX
Attack Success Rate: XX.XX%
```

If you see this on all 4 pods, **experiments succeeded!** 🎉

---

**Ready to deploy?** Copy the 4 commands above and paste into each RunPod terminal.

**Estimated total time:** 5 minutes for all 4 pods in parallel  
**Total cost:** ~$0.15  
**Expected impact:** +5-7% ASR reduction, audit score 35→70/100 ✅
