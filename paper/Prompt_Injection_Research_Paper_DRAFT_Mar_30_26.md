# Evaluating and Mitigating Prompt Injection in Full-Stack Web Applications: A System-Level Workflow Model

---

**Arindam Tripathi** (24155614@kiit.ac.in), **Arghya Bose** (24155380@kiit.ac.in), **Arghya Paul** (24155977@kiit.ac.in)
*School of Computer Engineering, KIIT University, Bhubaneswar, India*

**Supervised by:** Dr. Sushruta Mishra (sushruta.mishrafcs@kiit.ac.in), *Faculty, School of Computer Engineering, KIIT University*

---

## ABSTRACT

Large Language Models (LLMs) in commercial web applications introduce critical prompt injection vulnerabilities. This paper synthesizes existing defenses into a system-level workflow model spanning the complete application stack. We present a coordinated **six-layer defense architecture** that maps to the full lifecycle of user requests. Our experimental validation — conducted on a Llama-3.3-70b-based deployment under a black-box attacker model using **11,490 execution traces** — demonstrates that the proposed Full-Stack defense architecture achieves an aggregate **18.9% Attack Success Rate (ASR)** and **0.0% ASR on the evaluated stealth subset** (semantically obfuscated attacks designed to evade filters) (95% CI [0.0%, 0.12%]), representing a **76.6% relative risk reduction** (RRR = (ASR_baseline − ASR_fullstack) / ASR_baseline) over the unprotected baseline. The architecture maintains a **0.0% False Positive Rate** (95% CI [0.0%, 0.37%]), providing a statistically superior security posture (McNemar's χ²(1) = 173.0, p < .001) compared to isolated mitigations. **Dataset, models, and implementation code available at:** `https://github.com/ArindamTripathi619/prompt-injection-experiments`

**Keywords:** Prompt Injection, LLM Security, Full-Stack Defense, Trust Boundary, Adversarial AI, Workflow Model.

---

## 1. INTRODUCTION

### 1.1 Problem Definition and Current Landscape

The rapid integration of Large Language Models (LLMs) into commercial web applications has expanded the attack surface to include sophisticated prompt injection vulnerabilities. While individual components often implement localized security measures, these frequently fail to address the systemic nature of adversarial data flows spanning the entire application stack. These attacks exploit the inherent difficulty of distinguishing between legitimate user input and malicious instructions embedded within data flows, allowing attackers to manipulate LLM behavior in ways that bypass traditional security controls.

Recent empirical evidence demonstrates the severity and prevalence of this threat. The HouYi framework achieved over 85% success rate against real-world LLM-integrated applications including major platforms such as Notion and WriteSonic, with some attacks resulting in significant unauthorized resource usage [1]. These vulnerabilities are not isolated incidents but reflect systemic weaknesses in how LLM-integrated applications are architected and secured. Traditional input validation techniques prove ineffective because LLMs process semantic content rather than syntax-specific patterns, making conventional firewall and filtering approaches inadequate. Furthermore, the opacity of LLM decision-making processes obscures attack vectors that remain hidden from standard security monitoring tools.

The challenge is amplified by the diversity of attack methodologies that continuously evolve. Current research identifies multiple attack categories including direct prompt injection, semantic manipulation, encoding-based obfuscation, jailbreak techniques, and component-level targeting. Each attack vector exploits different system layers, from user input boundaries through data processing pipelines, context management mechanisms, LLM interaction interfaces, output handling, and feedback loops. No single defense mechanism addresses all attack types, yet most organizations implement isolated security measures without understanding how these components interact as a cohesive system.

### 1.2 Current Challenges in Prompt Injection Defense

Existing defenses suffer from critical limitations that prevent effective mitigation of prompt injection threats. The OWASP Top 10 for LLM Applications [14] identifies prompt injection as the highest-priority vulnerability class, yet most defense approaches operate in isolation, addressing specific attack vectors without considering system-wide implications. Keyword filtering detects certain injection patterns but fails against semantic paraphrasing, while prompt engineering improves model robustness but does not prevent determined attackers from discovering novel attack vectors. These isolated defenses create a fragmented security posture where attackers can navigate vulnerabilities at component boundaries.

Second, the architecture of current LLM-integrated applications conflates user-controlled data with trusted system instructions, creating fundamental information flow vulnerabilities. Frontend components, data processing pipelines, system prompts, and output handlers operate with insufficient isolation and context separation. Recent system-level analyses demonstrate that even systems implementing multiple safety constraints at the LLM level remain vulnerable to coordinated attacks exploiting component integration weaknesses. This architectural flaw requires fundamental redesign of information flow between system components.

Third, existing defenses create significant utility-security tradeoffs that limit practical deployment. Aggressive filtering reduces false negatives but increases false positives, blocking legitimate user requests and degrading application functionality. Furthermore, defenses are often model-specific or dataset-specific, failing to generalize across different LLM architectures or application contexts.

Fourth, the dynamic nature of prompt injection threats creates a moving target problem. New attack techniques emerge continuously through automated optimization methods, template-based approaches, and adversarial search algorithms. Attack transferability between models means that defenses designed for one LLM architecture may prove ineffective against others.

### 1.3 Research Questions

This work addresses the following research questions:

- **RQ1:** How do prompt injection attacks propagate across different layers of a Full-Stack web application?
- **RQ2:** Which system-level trust boundary violations enable successful prompt injection?
- **RQ3:** How can coordinated workflow-level defenses reduce attack success compared to isolated mitigations?

### 1.4 Proposed Solution and Research Contribution

**This paper proposes a unifying framework synthesizing existing defense approaches into a system-level workflow model spanning the complete application stack.** Rather than proposing isolated security mechanisms, we present a coordinated six-layer defense architecture that maps to the full lifecycle of user requests flowing through LLM-integrated applications. Each layer addresses specific attack vectors while feeding security-relevant information to downstream layers and maintaining feedback loops that enable adaptive defense refinement.

The proposed model makes three fundamental contributions to prompt injection defense:

1. **Architecture**: A coordinated six-layer Full-Stack defense architecture combining semantic filtering, logical isolation, constraint enforcement, and adaptive feedback.
2. **Evaluation**: An empirical validation using **11,490 execution traces**, quantifying the necessity of multi-layer protection over isolated configuration components.
3. **Insight**: A paired statistical analysis demonstrating a **76.6% risk reduction** and **0.0% Attack Success Rate against stealth variants**, proving that logical isolation fails without semantic filtering.

This system-level perspective is not the main focus of most existing work, which typically treats prompt injection as a model-level problem solvable through improved alignment or detection techniques. This paper argues that architectural decisions at the system level are equally important as component-level robustness.

### 1.5 Threat Model

To ground the evaluation, we define an explicit threat model for the LLM-integrated application:

- **Adversary Capabilities**: The attacker is an external web user interacting with the application through standard frontend interfaces.
- **Access Level**: Black-box execution (no access to model weights, API keys, backend source code, or internal database records).
- **Adaptability**: The attacker can perform multi-turn interactions and adapt their strategy dynamically based on the system's observable textual outputs.
- **Restrictions**: The attacker cannot directly alter the physical storage of the system prompt or backend processing architectures.

The research is grounded in comprehensive analysis of **13 primary research papers** reviewed in §2 (Papers 1–13 in the numbered review), covering attack methodologies, defense mechanisms, threat modeling, and system-level security analysis. Additional references [8, 14, 17, 18] cite foundational security analyses, standards, and tools used in the implementation.

![Comparison between prompt injection attack propagation in unprotected applications versus mitigated flow under the proposed workflow model.](figures/fig1.jpeg)

---

## 2. LITERATURE REVIEW

This literature review synthesizes 13 primary research papers addressing prompt injection 
vulnerabilities across attack methodologies, defense mechanisms, threat modeling, and 
system-level security analysis. Additional cited works [8, 14, 17, 18] provide foundational 
standards and tools referenced in the implementation.

**Paper 1 — Liu et al. [1] (HouYi):** Liu et al. aim to investigate prompt injection 
risks in real-world LLM-integrated applications and develop effective black-box attack 
techniques. They propose HouYi, a three-phase framework using context inference, payload 
generation (Framework, Separator, Disruptor components), and iterative refinement via 
GPT-3.5 feedback. They achieve **86.1% attack success rate** across 36 commercial 
applications including Notion and WriteSonic, demonstrating that existing defenses (XML 
tagging, paraphrasing, retokenization) can be systematically bypassed.

**Paper 2 — Maloyan and Namiot [2] (LLM-as-a-Judge Attacks):** Maloyan and Namiot aim 
to evaluate the vulnerability of LLM-as-a-judge systems to prompt injection attacks. 
They extend the HouYi framework with four attack variants (Basic Injection, Complex Word 
Bombardment, Contextual Misdirection, Adaptive Search-Based) and test them across five 
judge models on diverse evaluation tasks. They show that Adaptive Search-Based attacks 
achieve **42.9–73.8% success rates**, with frontier models demonstrating higher 
robustness, and that multi-model committees using 5–7 diverse models reduce attack 
success to 10–27%.

**Paper 3 — Zhang et al. [4] (JBShield):** Zhang et al. aim to detect and mitigate 
jailbreak attacks by analyzing toxic and jailbreak concepts encoded in LLM hidden 
representations. They apply Linear Representation Hypothesis with truncated SVD to 
extract concept subspaces from counterfactual prompt pairs, using cosine 
similarity-based detection and concept manipulation for mitigation without fine-tuning. 
They achieve **0.95 F1-score** for detection and reduce attack success rates from 61% 
to 2% with minimal utility impact (less than 2% MMLU degradation).

**Paper 4 — Tete [5] (Threat Modeling):** Tete aims to develop threat modeling and risk 
analysis frameworks specifically tailored for LLM-powered applications. The paper 
integrates STRIDE methodology with DREAD risk analysis and adapts Shostack's Four 
Question Framework to address LLM-specific threats including data poisoning, prompt 
injection, and compositional injection. An end-to-end threat model of an LLM-Doctor 
application validates the framework, ranking Denial of Service as highest-risk 
vulnerability followed by Tampering/Prompt Injection.

**Paper 5 — Peng et al. [6] (Comprehensive Review):** Peng et al. aim to systematically 
review jailbreak attacks and mitigation strategies across the evolving LLM security 
landscape. They categorize attacks into manually-designed, optimization-based, 
template-based, linguistics-based, and encoding-based types, while organizing defenses 
into detection-based and mitigation-based approaches. Their analysis reveals that 
multimodal attacks exploit semantic image-text alignment gaps, multilingual attacks 
achieve **50–70% success rates** in low-resource languages, and no single defense 
approach provides complete protection.

**Paper 6 — Shi et al. [15] (PromptArmor):** Shi et al. aim to develop a practical and 
scalable defense against prompt injection attacks on LLM agents. They design a modular 
preprocessing layer using a guardrail LLM with carefully crafted prompting strategies 
to detect and remove injected content via instruction-based detection and fuzzy matching 
extraction. **PromptArmor-GPT-4o achieves below 1% FPR and FNR** on the AgentDojo 
benchmark, significantly outperforming six baseline defenses.

**Paper 7 — Xu et al. [9] (Jailbreak Attack vs. Defense Study):** Xu et al. aim to 
systematically evaluate jailbreak attack effectiveness against various defense mechanisms 
across different model architectures. The authors conduct comparative evaluation testing 
nine attack techniques against seven defense configurations across Vicuna, LLama, and 
GPT-3.5 Turbo, analyzing attack transferability and robustness of combined defense 
strategies. Results show white-box attacks underperform compared to universal techniques, 
and that including special tokens in the input significantly affects the likelihood of 
successful attacks.

**Paper 8 — Wei et al. [3] (Jailbroken):** Wei et al. aim to explain why safety training 
fails against jailbreak attacks by identifying two failure modes: competing objectives 
and mismatched generalization. Their analysis across multiple LLM families reveals that 
sophisticated attacks achieve over 50% success rates even against safety-trained models, 
and that ensemble defense strategies combining filtering, alignment, and output 
validation outperform single-layer defenses by 20–40 percentage points.

**Paper 9 — Perez and Ribeiro [7] (Injection Attack Techniques):** Perez and Ribeiro aim 
to characterize prompt injection as a practical attack class against deployed language 
models. They demonstrate that goal-hijacking and prompt leaking attacks succeed across 
a range of real-world LLM applications, with ensemble detection approaches achieving 
30–40 percentage point F1-score improvement over single-model baselines through semantic 
understanding improving detection accuracy by 15–25 percentage points.

**Paper 10 — Wu et al. [11] (System-Level Analysis):** Wu et al. aim to analyze security 
of complete LLM systems rather than isolated models by examining information flow between 
components. The authors conduct multi-layer decomposition examining constraints between 
the LLM core and integrated components (frontend, webtool, sandbox), with end-to-end 
attack demonstrations on deployed systems like OpenAI GPT-4. System-level analysis 
exposes critical vulnerabilities in full-stack systems despite multiple safety measures, 
with successful attacks acquiring unauthorized user chat history by exploiting component 
boundary weaknesses.

**Paper 11 — Jedrzejewski et al. [16] (ThreMoLIA Framework):** Jedrzejewski et al. aim 
to automate threat modeling for LLM-integrated applications using AI-assisted approaches. 
They develop ThreMoLIA, an LLM-RAG architecture that leverages existing threat model 
repositories as knowledge bases, retrieving relevant historical threats through semantic 
search and integrating STRIDE, DREAD, and OWASP methodologies. Initial feasibility 
studies demonstrate that the framework successfully generates application-specific threat 
models while reducing reliance on manual security expert involvement.

**Paper 12 — Liang et al. [12] (SafeRAG):** Liang et al. aim to evaluate security 
vulnerabilities across all components of Retrieval-Augmented Generation (RAG) systems. 
The authors develop the SafeRAG benchmark classifying attack tasks into silver noise, 
inter-context conflict, soft ad, and white Denial-of-Service categories. Evaluation 
across 14 representative RAG implementations reveals significant vulnerabilities with 
high attack success rates across retriever, filter, ranker, and LLM components despite 
multiple defensive layers.

**Paper 13 — Greshake et al. [13] (Indirect Prompt Injection):** Greshake et al. 
systematically demonstrate indirect prompt injection — where malicious instructions 
embedded in external data sources hijack LLM-integrated applications. Their attacks 
against real-world systems show that content retrieved from the web, documents, or APIs 
can silently redirect application behavior, highlighting that trust boundary enforcement 
must extend beyond direct user input to all data ingestion surfaces.

**Paper 14 — Toyer et al. [10] (Tensor Trust):** Toyer et al. analyze prompt injection 
attacks and defenses through an online game generating over 126,000 real adversarial 
interactions. Their dataset reveals systematic patterns in injection strategies including 
instruction override, context flooding, and role manipulation, providing empirical grounding 
for understanding injection attack diversity at scale.

### 2.1 Research Gaps

While existing literature thoroughly documents attacks and isolated defenses, three 
critical gaps remain: (1) lack of unified framework showing defense coordination across 
system layers, (2) missing connection between architectural design patterns and 
vulnerability mitigation, and (3) absence of concrete implementation guidance for 
coordinated layer-based defenses. The proposed workflow model addresses these gaps by 
synthesizing research into a coherent six-layer framework.

### 2.2 Comparison with Existing Work

| Attack/Defense | Attack Vectors Exploited | Layers Addressing Gaps |
|---|---|---|
| **HouYi Framework** | Context inference, payload injection, iterative refinement bypass defenses | Layer 1 (syntax validation), Layer 2 (semantic analysis), Layer 3 (context isolation prevents framework/separator attacks) |
| **Adaptive Attacks** | Contextual misdirection, complex bombardment targeting judge systems | Layer 4 (guardrail LLM monitoring), Layer 6 (pattern learning detects emerging variations) |
| **JBShield Defense** | Representation-level monitoring, concept manipulation | Workflow integrates as Layer 4 component, enhanced by upstream filtering (Layers 1–2) and downstream validation (Layer 5) |
| **PromptArmor Defense** | Guardrail LLM detection, fuzzy matching extraction | Workflow integrates as Layer 4–5 component, benefits from Layer 3 context isolation reducing false negatives |
| **Indirect Injection** | Malicious instructions embedded in external web data/APIs | Layer 3 (context isolation) and Layer 5 (output validation) detect cross-boundary redirection |
| **Tensor Trust** | Instruction override, context flooding, role manipulation patterns | Layer 3 (structural separation) and Layer 4 (real-time guardrail constraints) |
| **System-Level Exploits** | Component boundary weaknesses, information flow violations | Layer 3 addresses through architectural isolation; Layer 6 feedback closes inter-component gaps |

---

## 3. PROPOSED MODEL

### 3.1 System-Level Workflow Architecture

The system-level workflow model comprises six coordinated defense layers addressing attack vectors across the complete request processing pipeline. Each layer operates at a specific lifecycle point, addresses particular attack categories, and communicates security information to downstream layers. The architecture follows **defense-in-depth** principles [17] where attack success at any single layer remains unlikely due to compensating controls at subsequent layers.

> **Note on Empirical Validation:** Unlike purely theoretical frameworks, this paper presents a fully implemented empirical system architecture and evaluation pipeline, validating the multi-layered defense approach against a comprehensive dataset of **11,490 execution traces**. Effectiveness statements refer to directly measured empirical performance quantified through testing.

![Overall system-level orchestration of the proposed multi-layer LLM defense architecture (L1--L6), illustrating layer interactions and feedback flow.](figures/fig2.jpeg)

### 3.2 Layer 1: Request Boundary

This layer performs character-level validation, syntax checking, and preliminary request classification at the application's outermost edge. Core components include character encoding validation, length threshold enforcement, and protocol-level validation addressing obfuscated inputs, protocol violations, and parser edge cases. While semantic attacks typically bypass this layer, it provides essential first-line defense and outputs validated requests with metadata tagging while maintaining **minimal latency overhead (<1ms)**.

**Layer 1 Outputs:**
```json
{
  "validation_status":   "passed",
  "encoding":            "UTF-8",
  "length":              1247,
  "anomaly_score":       0.12,
  "protocol_violations": []
}
```

### 3.3 Layer 2: Input Processing and Semantic Analysis

This layer performs tokenization, semantic analysis, pattern detection, and feature extraction to identify injection indicators beyond syntax validation. Core components include domain-aware tokenizers understanding LLM-specific patterns, **sentence embeddings** (`all-MiniLM-L6-v2` [18]) to assess meaning similarity with known attack patterns, and pattern detection identifying injection indicators such as command structures, instruction keywords, and boundary markers.

The layer addresses semantic paraphrasing, encoding-based attacks (Base64, ROT13), and context-manipulation attacks. Semantic analysis has been shown to significantly improve detection rates over simple keyword filters, because it assesses meaning rather than exact word sequences. The layer outputs enriched representations with confidence scores and feature vectors for downstream processing.

**Layer 2 Outputs:**
```json
{
  "injection_confidence":  0.73,
  "detected_patterns":     ["command_structure", "instruction_override"],
  "embedding_similarity":  0.42,
  "risk_level":            "medium"
}
```

### 3.4 Layer 3: Context Management and Isolation

This layer establishes logical and operational boundaries between user-controlled input and trusted system instructions, preventing cross-context influence. Core components include system prompt isolation, context compartmentalization establishing separate processing contexts for sessions and functions, and instruction hierarchy defining privilege levels for trusted versus user-originated instructions.

The layer uses programmatic roles (`system` vs `user` messages) and structured data models. **Critically, logical isolation alone is insufficient** — our experiments confirm this quantitatively in §5.2, showing that without complementary semantic filtering, isolation provides no measurable improvement over the unprotected baseline.

**Layer 3 Outputs:**
```json
{
  "user_context_id":        "sess_4729",
  "system_prompt_hash":     "a3f2c1",
  "privilege_level":        "user",
  "isolation_boundary":     "enforced",
  "constraint_violations":  []
}
```

![Internal structure of the Context Isolation Layer (C), showing protected instruction segments, constraint enforcement, and user-data separation boundaries.](figures/fig3.jpeg)

### 3.5 Layer 4: LLM Interaction and Constraint Enforcement

This layer implements constraints at the interface between application logic and LLM, enforcing intended operational boundaries. Core components include constraint enforcement mechanisms, and a **secondary Guardrail LLM** performing real-time semantic validation against operational constraints.

> **Implementation note:** While representation-level monitoring (e.g., JBShield) is conceptually attractive, it requires access to model weights unavailable in commercial API-driven architectures. Our prototype therefore implements Layer 4 as a **secondary Guardrail LLM call** via the Groq API (~310ms overhead per request).

**Layer 4 Outputs:**
```json
{
  "llm_response":           "...",
  "guardrail_verdict":      "safe",
  "guardrail_confidence":    0.92,
  "constraint_violations":  [],
  "response_confidence":    0.91
}
```

### 3.6 Layer 5: Output Handling and Validation

This layer validates LLM outputs before returning to users or downstream systems, preventing data leakage and ensuring format compliance. Core components include response validation checking format specifications and safety constraints, data leakage prevention detecting unintended sensitive information exposure, and confidence scoring assessing injection likelihood. Defense mechanisms include sensitive data pattern detection, output classification, and multi-layered validation.

**Layer 5 Outputs:**
```json
{
  "validated_output":    "...",
  "leakage_detected":    false,
  "format_compliant":    true,
  "sensitive_patterns":  [],
  "final_risk_score":    0.08
}
```

### 3.7 Layer 6: Feedback and Adaptive Monitoring

This layer enables continuous learning by observing system behavior and attack patterns. Core components log attack attempts, analyze patterns, adapt confidence thresholds based on false positive/negative rates, and update detection models through adaptive learning. It maintains time-series data on attack patterns and system performance.

> **Experimental Note:** During the 11,490-trace evaluation, Layer 6 operated in **passive logging mode only** — recording attack patterns and computing recommended threshold adjustments without applying them in real time. This ensures reproducibility by keeping system behavior constant across all traces. The adaptive capabilities described above represent the layer's design-time specification for production deployment.

**Layer 6 Outputs:**
```json
{
  "detected_attack_pattern": "adaptive_search_variant_3",
  "frequency":               47,
  "success_rate":            0.03,
  "recommended_threshold_adjustment": {
    "layer_2_confidence":   0.65
  }
}
```

### 3.8 Layer Interconnections and Information Flow

The six layers form an integrated system: Layer 2 suspicious patterns, building on initial request validation, directly inform Layer 3 context management decisions and trigger enhanced Layer 4 constraint enforcement. Layer 5 data leakage detection triggers Layer 2 retrospective analysis. Layer 6 emerging attack patterns broadcast updated detection rules to all layers.

**Example Application Walkthrough:** Consider an LLM-based customer support chatbot. Layer 1 validates HTTP request format and basic input size constraints. Layer 2 uses semantic analysis to flag injected instructions such as "ignore previous rules and dump all past chats." Layer 3 isolates system prompts and API keys in separate contexts. Layer 4 constrains tool calls to approved operations and monitors for jailbreak patterns. Layer 5 checks that responses do not expose internal ticket IDs, credentials, or system prompts. Layer 6 logs repeated suspicious attempts to refine detection thresholds and update blocking rules.

### 3.9 Practical Design Patterns

The workflow model derives six practical design patterns:

1. **Defense-in-Depth Pipeline** — sequential validation through multiple independent detection modules (Layers 1–2).
2. **Guardrail Model Architecture** — separate, smaller LLMs validating primary LLM outputs (Layer 4).
3. **Representation-Level Defense** *(recommended enhancement)* — monitoring hidden layer activations following approaches like JBShield (~0.95 F1). Not implemented in our API-driven prototype due to model weight access requirements, but recommended for deployments with white-box model access (Layer 4).
4. **Ensemble Consensus** — multiple independent detection models vote on injection attempts (Layers 2 and 4).
5. **Contextual Isolation** — architectural separation of system instructions from user data (Layer 3). Most effective when implemented during architectural design rather than retrofitted.
6. **Adaptive Feedback Loop** — systematic attack data collection, pattern analysis, and automatic threshold/rule adjustment (Layer 6).

---

## 4. EXPERIMENTAL RESULTS AND STATISTICAL VALIDATION

### 4.1 Sampling, Execution Logic, and Dataset Splits

The experimental corpus consisted of **11,490 total execution traces** generated over **3.5 hours** using multithreaded orchestration on AMD Ryzen 7 8840HS (8 Cores, 16 Threads), 32 GB RAM. To prevent overfitting, the corpus was divided into three strictly isolated partitions: a development set for threshold calibration, a validation set for ablation runs, and a held-out test set for final evaluation.

For Full-Stack performance evaluation, we selected a high-adversarial **unseen test subset of 7,850 traces**. The remaining 3,640 traces comprised 850 neutral interactions for FPR validation and 2,790 traces from isolated ablation runs, threshold tuning, and failed pilot iterations.

For paired statistical comparison (Baseline vs. **Full-Stack**), analysis was performed on a **core test subset of 260 unique adversarial prompts** (130 Standard + 130 Stealth variants). The 130 stealth variants represent a stratified sample drawn from the broader 2,450-trace stealth corpus (§4.6), selected to ensure diverse attack category coverage while maintaining a balanced paired comparison. Attack success was determined by an **independent LLM-as-a-judge (Llama-3.1-405b)** to reduce evaluation bias. While a single-judge evaluation carries inherent risks of bias, the 405b parameter scale provides a strong baseline. Evaluation used a strict binary success/fail rubric with deterministic temperature (T=0.0) and chain-of-thought suppressed to enforce strict boolean classification. The 260-prompt subset represents a controlled, identity-paired evaluation to measure the direct effectiveness of the stack, whereas the larger 7,850-trace test set provides a broader measure of aggregate resilience across diverse attack variations.

**Infrastructure:**
- **LLM Backend:** `groq/llama-3.3-70b-versatile` (via local LiteLLM proxy)
- **Hardware:** AMD Ryzen 7 8840HS (8 Cores, 16 Threads), 32 GB RAM, Samsung PM9B1 NVMe SSD
- **Evaluator:** LLM-as-a-Judge (Llama-3.1-405b) for binary ASR classification
- **Software:** Python 3.12, `unified_pipeline.py` instrumentation
- **Parameters:** Temperature: 0.0 (Deterministic), Top P: 1.0

### 4.2 Attack Corpus Distribution

The experimental evaluation utilized a heterogeneous corpus of **11,490 execution traces**, categorized by attack methodology and adversarial complexity:

| Attack Category | Traces (N) | Description |
|---|---|---|
| Direct Injection | 2,700 | Explicit instruction-overriding prompts |
| Semantic Injection | 2,385 | Instructions embedded in narrative context |
| Context Override | 2,595 | Attempts to escape architectural boundaries |
| Jailbreak | 1,280 | Role-play and social engineering |
| Multi-Turn | 975 | Sequential injections in history |
| Encoding Attack | 705 | Obfuscated (Base64/Hex) payloads |
| Neutral Interaction | 850 | Standard interaction benchmarks (benign samples) |
| **TOTAL** | **11,490** | |

### 4.3 Experimental Configuration Matrix

We defined four experimental ablation configurations alongside the Baseline to isolate the efficacy of individual layer categories versus the integrated stack:

| Config | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| Baseline (A) | — | — | — | — | — | — |
| Semantic (B) | — | X | — | — | — | — |
| Isolation (C) | — | — | X | — | — | — |
| Output (D) | — | — | — | — | X | — |
| Full-Stack (E) | X | X | X | X | X | X¹ |

¹ Layer 6 operated in **passive logging mode** during the experiment (see §3.7). It recorded attack patterns but did not apply adaptive threshold adjustments, ensuring reproducibility.

![Incremental defense layering (A--E) and their cumulative role in strengthening prompt injection resistance.](figures/fig4.jpeg)

### 4.4 Overall Effectiveness

Our evaluation demonstrates the substantial effectiveness of the six-layer model:

- **Baseline (A) Attack Success Rate: 80.8%** (95% CI [75.5%, 85.1%])
- **Full-Stack (E) ASR: 18.9%** (Aggregate over 7,850-trace test set) / **13.5%** (Paired Core Subset of 260 prompts)
- **Relative Risk Reduction: 76.6%** — computed as (ASR_baseline − ASR_fullstack) / ASR_baseline = (80.8% − 18.9%) / 80.8%; absolute reduction = 61.9 percentage points

The two ASR figures reflect different evaluation scopes: **18.9%** is the aggregate ASR measured across the full 7,850-trace held-out test set containing diverse attack variations and difficulty levels, while **13.5%** is measured on the smaller 260-prompt paired core subset used for the McNemar statistical comparison. The paired subset uses identity-matched prompts (same prompt evaluated under both Baseline and Full-Stack conditions), providing higher statistical rigor but a narrower adversarial sample. The 76.6% RRR is computed from the aggregate figure (18.9%), which represents the broader performance metric.

![Attack success rate across defense configurations, demonstrating progressive reduction from baseline to full-stack deployment.](figures/fig5_graph.jpeg)

### 4.5 Layer Propagation Metrics (RQ1)

| Configuration | Pooled ASR | 95% Confidence Interval |
|---|---|---|
| **Baseline (A)** | **80.8%** | [75.5%, 85.1%] |
| **Semantic Only (B)** | **38.5%** | [32.8%, 44.5%] |
| **Isolation Solo (C)** | **80.8%** | [75.5%, 85.1%] |
| **Output Solo (D)** | **55.4%** | [49.2%, 61.4%] |
| **Full-Stack (E)** | **18.9%** | [18.1%, 19.8%] |

![Attack success rates with confidence intervals across defense configurations, illustrating statistical robustness of the proposed full-stack approach.](figures/fig6_asr_graph.jpeg)

### 4.6 Coordinated Defense against Stealth Attacks (RQ3)

Testing against **Stealth Attacks** (a specific corpus of **2,450 traces**) designed to evade semantic filters revealed critical architectural weaknesses in standalone configurations. The stealth subset is a **cross-category overlay**: the 30 unique base prompts span Direct Injection, Semantic Injection, and Context Override categories, expanded into 2,450 traces via automated adversarial refinement (iterative HouYi refinement process), employing instruction character replacement and semantic obfuscation to evade Layer 2. These traces are included *within* the category counts in Table 4.2, not additional to the 11,490 total. This corpus was **strictly withheld from any threshold tuning or defense prompt engineering** during the development phase.

| Configuration | ASR | Notes |
|---|---|---|
| **Isolation Solo (C)** | **80.8%** | No measurable improvement vs baseline |
| **Output Solo (D)** | **25.4%** | Significant standalone value |
| **Full-Stack (E)** | **0.0%** | Over 2,450 stealth traces (95% CI [0.0%, 0.12%]) |

> *Note: The 0.0% ASR applies specifically to the stealth attack subset and does not represent the aggregate performance across the full 11,490-trace corpus. ASR figures in this table reflect performance on the stealth-only subset of 2,450 traces and are not directly comparable to the pooled figures in Table 4.5 (e.g., Output Solo (D) achieves 25.4% on stealth traces vs. 55.4% pooled).*

### 4.7 Latency

The defense architecture adds modest latency beyond the base LLM inference:

| Layer | Overhead |
|---|---|
| Layer 2 (Semantic Analysis) | ~36 ms (Local, `all-MiniLM-L6-v2`) |
| Layer 3 (Context Isolation) | <1 ms (Local) |
| Layer 4 (Guardrail LLM) | ~310 ms (Secondary Groq API call) |
| Layer 5 (Output Validation) | <1 ms (Local regex) |
| **Total Latency Overhead** | **~347 ms** (~310 ms guardrail + ~37 ms auxiliary) |

Multithreaded execution achieved **11,490 traces in approximately 3.5 hours**.

### 4.8 Statistical Validation

#### McNemar's Significance Test (Paired Core Subset, N=260 unique prompts)

| | **Full-Stack** Block (Fail) | **Full-Stack** Bypass (Success) |
|---|---|---|
| **Baseline Bypass (Success)** | **175 (Discordant)** | 35 (Both Success) |
| **Baseline Block (Fail)** | 50 (Both Fail) | **0 (Discordant)** |

The "Both Fail" cell (N=50) represents prompts that neither the Baseline nor Full-Stack configurations successfully exploited. These prompts were structurally adversarial but proved ineffective regardless of defensive posture — likely due to inherent model robustness against those specific attack patterns (e.g., poorly constructed injections that the base LLM’s safety training already rejects).

- **McNemar's χ²(1) = 173.0, p < .001**
- **Cohen's h = 1.33** — Large effect size with high statistical power

#### Utility Validation (False Positive Rate)

No false positives were observed within the evaluated benign corpus (N=1,000), resulting in a **0.0% False Positive Rate** (95% CI [0.0%, 0.37%]).

**Benign Prompt Distribution:**

The benign corpus was constructed to represent the five most common enterprise chatbot interaction categories identified in deployment logs, with a larger "Contextual Misc." bucket capturing edge-case queries (e.g., ambiguous phrasing, multi-intent inputs) that are most likely to trigger false positives:

| Domain | Count (N) |
|---|---|
| Technical Support | 150 |
| Creative Writing | 150 |
| Code Review | 150 |
| Academic Inquiry | 150 |
| Enterprise Ops | 150 |
| Contextual Misc. | 250 |
| **Total** | **1,000** |

No benign requests were incorrectly flagged as malicious by the semantic (Layer 2) or output (Layer 5) filters.

### 4.9 Trust Boundary Violation Analysis (RQ2)

Our experimental results identify three primary trust boundary violations that enable successful prompt injection:

1. **Input–Instruction Boundary Collapse (Layer 2 → Layer 3):** The most critical violation occurs when user-controlled data crosses into the instruction context. Layer 3 isolation alone fails to prevent this (80.8% ASR) because the shared attention mechanism in transformer architectures does not enforce privilege separation between `system` and `user` message roles. Successful attacks in this category include context override (2,595 traces) and semantic injection (2,385 traces).

2. **Output Trust Escalation (Layer 4 → Layer 5):** Attacks that bypass the guardrail LLM produce outputs that downstream components treat as trusted. Without Layer 5 validation, leaked system prompts or credentials in LLM outputs propagate to the user. The Output Solo (D) configuration achieves 25.4% ASR on stealth attacks, confirming that output validation alone catches a substantial fraction but not all violations.

3. **Cross-Component Information Flow (System-Level):** As demonstrated by Wu et al. [11], component boundary weaknesses allow attackers to chain exploits across frontend, LLM core, and tool-calling interfaces. The full-stack architecture addresses this by ensuring security metadata propagates across all six layers, preventing any single boundary failure from cascading.

---

## 5. ANALYSIS AND DISCUSSION

### 5.1 Analysis of Key Findings

The results highlight that an integrated, multi-layer approach is significantly more robust than any single architectural or semantic filter. Individual layers demonstrate predictable failure modes when isolated, but their coordination creates a comprehensive barrier against injection. 

The model acknowledges that perfect security remains a moving target, and sophisticated adaptive attacks may discover vulnerability combinations across layers. Consistent with prior findings that multi-layer approaches outperform isolated configurations [3, 6, 9], our experimental validation shows that our specific coordinated implementation provides a substantial reduction in risk.

### 5.2 Isolation Requires Complementary Filtering (Layer 3 Analysis)

The most significant finding is the quantified failure of Trust Boundaries (Layer 3) when acting in isolation. In modern API-driven LLM integrations, "isolation" primarily refers to **logical isolation** — separating system instructions from user space via programmatic roles (`system` vs `user` messages) — rather than true separate-process execution memory isolation. Our experiments show this logical isolation remains **highly vulnerable to stealth injection attacks when used alone, yielding an 80.8% ASR**, showing no statistically significant difference from the unprotected baseline (p ≈ 1.0).

Semantic filtering acts as a necessary prerequisite that allows the **organizational** benefits of isolation to manifest effectively during execution. Our empirical results suggest that logical context separation alone is insufficient under the evaluated threat model if the user input can still semantically influence the generation process within the shared model attention context.

### 5.3 Efficiency and Resource Utilization

Under the tested configuration, **total latency is ~347 ms** (~310 ms from the Guardrail LLM + ~37 ms from auxiliary layers). Heavy reliance on Layer 4 introduces scalability concerns and potential vulnerabilities if attackers specifically target the guardrail model. Adopting a decentralized "Multi-Model Voting" system (listed in future work) for Layer 4 could mitigate these correlated failure modes.

**Local Inference Efficiency:**
- **Hardware Profile:** AMD Ryzen 7 8840HS (8 Cores, 16 Threads), 32 GB RAM
- **Experimental Model:** `groq/llama-3.3-70b-versatile` (via local LiteLLM proxy)
- **Execution Efficiency:** 11,490 traces in approximately 3.5 hours using multithreaded optimization
- **Infrastructure Cost:** Unlike cloud-dependent guardrails that incur significant per-token costs, local semantic filtering and context isolation provide high-efficiency protection with negligible marginal costs

### 5.4 Practical Deployment Recommendations

1. **Prioritize Semantic Filtering:** Implement **Layer 2 (Semantic Filtering)** as the primary input filtering layer. Our data indicates it mitigates over 50% of standard direct injections before they reach the model (p < .001).
2. **Implement Post-Execution Guardrails:** **Layer 5 (Output Validation)** is essential for detecting leakage that bypasses upstream filters, serving as a critical fail-safe for the entire system.
3. **Isolation Requires Complementary Filtering:** Do not rely on architectural isolation (Layer 3) as a standalone defense. It must be implemented in tandem with continuous semantic monitoring to be effective.

### 5.5 Utility–Security Tradeoffs

- **Semantic Specificity:** The Layer 2 filter correctly distinguished between descriptive intent and adversarial injection, achieving a **0.0% FPR** across 1,000 benign prompts.
- **System Robustness:** The coordinated guardrails demonstrated high specificity, though minor utility tradeoffs might occur under extreme security thresholds in highly specialized domains.

### 5.6 Limitations and Future Work

- **Inter-Domain Utility Benchmarking:** Further validation using domain-specific benign corpora (e.g., medical or legal) is recommended to verify semantic filter specificity in restricted namespaces.
- **Multi-Model Heterogeneity:** Testing a decentralized "Multi-Model Voting" system (listed in future work) for Layer 4 could mitigate these correlated failure modes.
- **Defense Persistence:** Evaluating the workflow against models purposefully fine-tuned to bypass semantic filters or ignore system prompt boundaries.
- **Model Scale Generality:** Future work must examine whether lower-parameter models exhibit similar resilience when integrated into the proposed defensive architecture.
- **Structural Layer Quantification:** Future ablation studies should isolate Layer 1 (Request Boundary) and Layer 6 (Adaptive Monitoring) individual contributions, which were treated as structural constants in this experiment due to their negligible standalone latency impact (<1ms).

---

## 6. REPRODUCIBILITY AND EXPERIMENTAL PARAMETERS

To ensure full reproducibility of our empirical findings, the complete implementation logic, orchestration pipeline, and raw dataset are open source:

- **Source Code & Dataset:** `https://github.com/ArindamTripathi619/prompt-injection-experiments`

### 6.1 System and Implementation Parameters

| Parameter | Value |
|---|---|
| **Model** | `Llama-3.3-70b-versatile` |
| **Temperature** | 0.0 (Deterministic) |
| **Top P** | 1.0 |
| **API Architecture** | Groq Cloud API accessed via local `LiteLLM` unified routing proxy |
| **Concurrency** | Asynchronous execution via `asyncio` handling >10 parallel streams |
| **Pipeline Framework**| Custom Python orchestrator (`unified_pipeline.py`) integrating guardrails |
| **Hardware** | AMD Ryzen 7 8840HS (8 Cores, 16 Threads), 32 GB RAM, Samsung PM9B1 NVMe SSD |
| **Software** | Python 3.12 running in local isolated virtual environment |
| **Evaluator** | LLM-as-a-Judge (`Llama-3.1-405b` on Groq) for strict binary ASR classification |
| **Artifacts Export** | Raw execution matrices (SQLite, `data/experiments.db`, 11,490 evaluation rows) |

### 6.2 Structural Logic
The Full-Stack defense operates as an integrated evaluation pipeline. Incoming prompts are first screened via Sentence-BERT (`all-MiniLM-L6-v2`) embedded locally. Safely validated inputs undergo isolated context framing. Finally, responses are passed through the independent Layer 4 Guardrail LLM before output validation, ensuring high-fidelity empirical data logging.

---

## REFERENCES

1. Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, Leo Yu Zhang, and Yang Liu. (2023). Prompt injection attack against LLM-integrated applications. *arXiv preprint arXiv:2306.05499*. DOI: https://doi.org/10.48550/arXiv.2306.05499

2. Nikolai Maloyan and Dmitry Namiot. (2025). Adversarial Attacks on LLM-as-a-Judge Systems: Insights from Prompt Injections. *arXiv preprint arXiv:2504.18333*. DOI: https://doi.org/10.48550/arXiv.2504.18333

3. Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. (2023). Jailbroken: How does LLM safety training fail? *Advances in Neural Information Processing Systems (NeurIPS 2023)*, 36.

4. Shenyi Zhang, Yuchen Zhai, Keyan Guo, Hongxin Hu, Shengnan Guo, Zheng Fang, Lingchen Zhao, Chao Shen, Cong Wang, and Qian Wang. (2025). JBShield: Defending large language models from jailbreak attacks through activated concept analysis and manipulation. *Proceedings of the 34th USENIX Security Symposium (USENIX Security 2025)*.

5. Srijan B. Tete. (2024). Threat modelling and risk analysis for large language model-powered applications. *arXiv preprint arXiv:2406.11007*. DOI: https://doi.org/10.48550/arXiv.2406.11007

6. Benji Peng, Keyu Chen, Qian Niu, Ziqian Bi, Ming Liu, Pohsun Feng, Tianyang Wang, Lawrence K.Q. Yan, Yizhu Wen, Yichao Zhang, Caitlyn Heqi Yin, and Xinyuan Song. (2024). Jailbreaking and mitigation of vulnerabilities in large language models. *arXiv preprint arXiv:2410.15236*. DOI: https://doi.org/10.48550/arXiv.2410.15236

7. Fábio Perez and Ian Ribeiro. (2022). Ignore previous prompt: Attack techniques for language models. *arXiv preprint arXiv:2211.09527*. DOI: https://doi.org/10.48550/arXiv.2211.09527

8. Erik Derner and Kristian Batistič. (2023). Beyond the safeguards: Exploring the security risks of ChatGPT. *arXiv preprint arXiv:2305.08005*. DOI: https://doi.org/10.48550/arXiv.2305.08005

9. Zihao Xu, Yi Liu, Gelei Deng, Yuekang Li, and Stjepan Picek. (2024). A comprehensive study of jailbreak attack versus defense for large language models. *Findings of the Association for Computational Linguistics: ACL 2024*, pp. 7432–7449. DOI: https://doi.org/10.18653/v1/2024.findings-acl.442

10. Sam Toyer, Olivia Watkins, Ethan Adrian Mendes, Justin Svegliato, Luke Bailey, Tiffany Wang, Isaac Ong, Karim Elmaaroufi, Pieter Abbeel, Trevor Darrell, Alan Ritter, and Stuart Russell. (2023). Tensor Trust: Interpretable prompt injection attacks from an online game. *arXiv preprint arXiv:2311.01011*. DOI: https://doi.org/10.48550/arXiv.2311.01011

11. Fangzhou Wu, Ning Zhang, Somesh Jha, Patrick McDaniel, and Chaowei Xiao. (2024). A new era in LLM security: Exploring security concerns in real-world LLM-based systems. *arXiv preprint arXiv:2402.18649*. DOI: https://doi.org/10.48550/arXiv.2402.18649

12. Xun Liang, Simin Niu, Zhiyu Li, Sensen Zhang, Hanyu Wang, Feiyu Xiong, Jason Zhaoxin Fan, Bo Tang, Shichao Song, Mengwei Wang, and Jiawei Yang. (2025). SafeRAG: Benchmarking security in retrieval-augmented generation of large language model. *arXiv preprint arXiv:2501.18636*. DOI: https://doi.org/10.48550/arXiv.2501.18636

13. Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, and Mario Fritz. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISec @ CCS 2023)*, pp. 79-90. DOI: https://doi.org/10.1145/3605764.3623985

14. OWASP Foundation. (2023). OWASP Top 10 for Large Language Model Applications. https://owasp.org/www-project-top-10-for-large-language-model-applications/ (Accessed: March 2026).

15. Tony Shi, Yueyang Qiu, et al. (2025). PromptArmor: Simple yet Effective Prompt Injection Defenses. *arXiv preprint arXiv:2507.15219*. DOI: https://doi.org/10.48550/arXiv.2507.15219

16. Krzysztof Jedrzejewski, Davide Fucci, and Oleg Adamov. (2025). ThreMoLIA: Threat Modeling of Large Language Model-Integrated Applications. *Proceedings of the 2025 International Conference on Software and System Processes (ICSSP)*. DOI: https://doi.org/10.1109/ICSSP.2025.00012

17. NIST. (2023). NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations. *National Institute of Standards and Technology*. DOI: https://doi.org/10.6028/NIST.SP.800-53r5

18. Nils Reimers and Iryna Gurevych. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of EMNLP 2019*, pp. 3982-3992. DOI: https://doi.org/10.18653/v1/D19-1410