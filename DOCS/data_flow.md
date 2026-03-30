# Data Flow & Pipeline

This document illustrates the journey of a user request through the multi-layer defense pipeline.

## Request Lifecycle

The diagram below shows how a request is processed, with adaptive escalations based on risk levels detected by the initial layers.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryTextColor': '#000', 'noteTextColor': '#000', 'actorTextColor': '#000', 'lineColor': '#000' }}}%%
sequenceDiagram
    participant U as User / Client
    participant P as Unified Pipeline
    participant L1 as L1: Boundary
    participant L2 as L2: Semantic
    participant L3 as L3: Context
    participant L4 as L4: LLM
    participant L5 as L5: Output
    participant L6 as L6: Feedback

    U->>P: Submit Prompt
    P->>L1: Validate Characters
    L1-->>P: Status/Risk Score

    P->>L2: Semantic Similarity Check
    L2-->>P: Risk Score / Flags

    Note over P, L6: Adaptive Escalation (L6)
    alt Risk Score > 0.6
        P->>L3: STRICT Isolation Mode
    else
        P->>L3: STANDARD Role Separation
    end

    P->>L3: Isolate Context
    L3-->>P: Isolated Prompt

    P->>L4: LLM Generation (Guardrails)
    L4-->>P: Raw Content / Response

    P->>L5: Response Filter
    L5-->>P: Pass/Fail (Policy check)

    rect rgb(240, 240, 240)
    Note over P, L6: Update Learning Models
    P->>L6: Execution Trace
    end

    alt No Violation
        P-->>U: Secure Response
    else Violation Blocked
        P-->>U: Error: Request Blocked
    end
```

## Key Orchestration Components

- **UnifiedPipeline**: The central hub that coordinates all layers. It converts raw inputs into a `RequestEnvelope` and manages the `ExecutionTrace`.
- **Adaptive Coordinator**: Monitors the risk scores from L1 and L2 to decide which isolation mode should be used in L3 and whether to apply pre-generation guardrails in L4.
- **Trace Logger**: Captures every decision point, latency metric, and flag for downstream statistical analysis.
