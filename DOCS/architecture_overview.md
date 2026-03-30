# Architecture Overview

This document provides a high-level view of the six-layer defense architecture implemented in this project to mitigate prompt injection attacks.

## Defense Stack

The defense strategy follows a "Defense-in-Depth" philosophy, where multiple layers of security are applied to ensure that if one layer fails, others are there to catch the attack.

```mermaid
graph TD
    A[User Request] --> L1[Layer 1: Request Boundary]
    L1 --> L2[Layer 2: Semantic Analysis]
    L2 --> L3[Layer 3: Context Isolation]
    L3 --> L4[Layer 4: LLM Interaction]
    L4 --> L5[Layer 5: Output Validation]
    
    subgraph "Adaptive Feedback Loop"
    L6[Layer 6: Feedback & Monitoring]
    L5 -.-> L6
    L6 -.-> L3
    L6 -.-> L4
    L6 -.-> L5
    end

    L5 --> B[Secure Response]

    style L1 fill:#f9f,stroke:#333,stroke-width:2px,color:#000
    style L2 fill:#bbf,stroke:#333,stroke-width:2px,color:#000
    style L3 fill:#bfb,stroke:#333,stroke-width:2px,color:#000
    style L4 fill:#fbb,stroke:#333,stroke-width:2px,color:#000
    style L5 fill:#fb8,stroke:#333,stroke-width:2px,color:#000
    style L6 fill:#8ff,stroke:#333,stroke-width:2px,color:#000
```

## Layer Responsibilities

| Layer | Name | Primary Responsibility |
|-------|------|------------------------|
| **1** | **Boundary** | Character-level validation, preliminary classification, and basic regex filtering. |
| **2** | **Semantic** | Uses sentence embeddings (`all-MiniLM-L6-v2`) to detect similarity to known attack patterns. |
| **3** | **Context** | Enforces separation between system instructions and user input (Role/Tag isolation). |
| **4** | **LLM** | Orchestrates interaction with the LLM backend (Groq/Llama-3.3) via LiteLLM. |
| **5** | **Output** | Final response filtering for system prompt leakage, policy violations, and semantic consistency. |
| **6** | **Feedback** | Continuously monitors for evasion patterns and adjusts escalation thresholds in real-time. |

## Inter-Layer Coordination

The **Unified Pipeline** and **Adaptive Coordinator** manage the flow of information between layers. If a layer detects a potential risk, it propagates a "Risk Score" which can trigger more stringent isolation modes in Layer 3 or stricter guardrails in Layer 4.
