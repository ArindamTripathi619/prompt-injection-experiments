# Experiment Workflow

This document explains how the project orchestrates **11,490 experimental interactions** to validate the defense architecture.

**Infrastructure:**
- **Hardware:** AMD Ryzen 7 8840HS (8 Cores, 16 Threads), 32GB RAM, Samsung PM9B1 NVMe SSD
- **LLM Backend:** `groq/llama-3.3-70b-versatile` via local LiteLLM proxy
- **Evaluator:** Independent LLM-as-a-Judge (`llama-3.1-405b`) — deterministic (T=0.0), binary ASR classification
- **Software:** Python 3.12, `unified_pipeline.py` instrumentation
- **Runtime:** ~3.5 hours for all 11,490 traces (multithreaded)

## Orchestration Logic

The experiment runner is designed for high-performance, multi-threaded validation.

```mermaid
flowchart TD
    Start([Start Experiment Session]) --> Init[Load Configuration & DB]
    Init --> SelectPrompts[Fetch Attack & Benign Prompts]
    
    subgraph "Trial Execution Engine"
    SelectPrompts --> Trials{N Randomized Trials}
    Trials --> Trial1[Trial 1]
    Trials --> Trial2[Trial 2]
    Trials --> TrialN[Trial N]
    
    subgraph "Parallel Requests (Multi-threaded)"
    Trial1 --> R1[Request 1]
    Trial1 --> R2[Request 2]
    end
    end

    R1 --> Collect[Update Execution Trace]
    R2 --> Collect
    Collect --> DB[(SQLite Database)]
    
    DB --> Stats[Statistical Analysis: McNemar's Test]
    Stats --> Reports[JSON Reports & Visualizations]
    Reports --> End([End Session])
```

## Methodology Breakdown

1. **Baseline Campaigns** — Running requests against the unprotected LLM to establish ground truth. Result: **80.8% ASR** (95% CI [75.5%, 85.1%]).
2. **Layer Ablation** — Systematically testing individual and incremental layer combinations to measure contribution:
   - Layer 2 Only (Semantic): **38.5% ASR** — the primary standalone blocker
   - Layer 3 Only (Context Isolation): **80.8% ASR** — **identical to baseline; zero standalone protection** (the "Isolation Illusion")
   - Layer 5 Only (Output Validation): **25.4% ASR**
   - Full Stack (L1–L6): **18.9% aggregate ASR** / **0.0% stealth-subset ASR**
3. **Isolation Illusion Study** — Specifically testing L3 (Context Isolation) against 2,450 stealth attack traces. L3 solo achieves 80.8% ASR — no improvement — proving logical isolation without semantic filtering is completely ineffective.
4. **Utility Stress Testing** — Passing **1,000 diverse benign prompts** across 6 domains through the full defense stack. Result: **0.0% FPR** (95% CI [0.0%, 0.37%]).

## Performance Metrics

| Metric | Definition | Final Value |
|---|---|---|
| **ASR (Attack Success Rate)** | % of injection attempts that successfully bypass all defenses | **18.9%** aggregate / **0.0%** stealth-subset |
| **FPR (False Positive Rate)** | % of legitimate prompts incorrectly blocked | **0.0%** (N=1,000) |
| **Latency Overhead** | Added time per request from the defense stack | **~347ms** total (~310ms L4 guardrail + ~37ms auxiliary) |
| **McNemar's χ²** | Statistical significance of Full Stack vs Baseline | **χ²(1)=173.0, p<0.001** |
| **Cohen's h** | Effect size for Full Stack vs Baseline | **h=1.33** (Large) |
