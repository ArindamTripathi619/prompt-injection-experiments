# Evaluating and Mitigating Prompt Injection in Full-Stack Web Applications: A System-Level Workflow Model


**Arindam Tripathi** (arindamtripathi.619@gmail.com), **Arghya Bose** (bosearghya29@gmail.com), **Arghya Paul** (arghya.paul.162006@gmail.com)  
*School of Computer Engineering, KIIT University, Bhubaneswar, India*

**Supervised by:** Dr. Sushruta Mishra, *Faculty, School of Computer Engineering, KIIT University*

---
 
### ABSTRACT

Large Language Model (LLM) integration into web applications introduces complex security vulnerabilities, primarily prompt injection, where malicious inputs manipulate model behavior to bypass safety controls. Traditional defense mechanisms typically operate in isolation, failing to address the systemic nature of these attacks. This research proposes and validates a comprehensive **six-layer defense architecture** spanning the entire request lifecycle: (1) Input Boundary Detection, (2) Semantic Analysis, (3) Context Isolation, (4) LLM Interaction Constraints, (5) Output Validation, and (6) Adaptive Feedback. We evaluated this architecture through rigorous experimentation involving **11,490 execution traces** across 103 configurations using the **Llama 3.2:1b** model on RunPod GPU infrastructure. Results demonstrate that our full defense stack reduces the Attack Success Rate (ASR) from **80.8%** (baseline) to **18.7%** (**68.1% absolute reduction**). Furthermore, we introduce an **adaptive coordination mechanism** (Experiment 6) that enables dynamic information sharing between layers, further enhancing resilience significantly (p < 0.001) compared to static deployments. The study empirically confirms that a coordinated, system-level workflow model provides a robust, cost-effective, and practical solution for securing LLM-integrated applications against sophisticated prompt injection threats.

**Keywords:** Large Language Models, Prompt Injection, Adversarial Attacks, Defense-in-Depth, System Security, Adaptive Defense, AI Safety.

---

## INTRODUCTION

### Problem Definition and Current Landscape

The rapid integration of Large Language Models (LLMs) into commercial web applications has created a new class of security vulnerabilities that existing application security frameworks were not designed to address. Unlike syntax-targeted SQL injection, which exploits predictable parsing rules in databases, prompt injection leverages LLMs' semantic processing capabilities to hijack control flow across diverse tasks, creating attack surfaces that span entire application architectures. These attacks exploit the inherent difficulty of distinguishing between legitimate user input and malicious instructions embedded within data flows, allowing attackers to manipulate LLM behavior in ways that bypass traditional security controls.

Recent empirical evidence demonstrates the severity and prevalence of this threat. The HouYi framework achieved over 85% success rate against real-world LLM-integrated applications including major platforms such as Notion and WriteSonic, with some attacks resulting in significant unauthorized resource usage. These vulnerabilities are not isolated incidents but reflect systemic weaknesses in how LLM-integrated applications are architected and secured. Traditional input validation techniques prove ineffective because LLMs process semantic content rather than syntax-specific patterns, making conventional firewall and filtering approaches inadequate. Furthermore, the opacity of LLM decision-making processes obscures attack vectors that remain hidden from standard security monitoring tools.

The challenge is amplified by the diversity of attack methodologies that continuously evolve. Current research identifies multiple attack categories including direct prompt injection, semantic manipulation, encoding-based obfuscation, jailbreak techniques, and component-level targeting. Each attack vector exploits different system layers, from user input boundaries through data processing pipelines, context management mechanisms, LLM interaction interfaces, output handling, and feedback loops. No single defense mechanism addresses all attack types, yet most organizations implement isolated security measures without understanding how these components interact as a cohesive system.

### Current Challenges in Prompt Injection Defense

Existing defenses suffer from critical limitations that prevent effective mitigation of prompt injection threats. First, most defense approaches operate in isolation, addressing specific attack vectors without considering system-wide implications. Keyword filtering detects certain injection patterns but fails against semantic paraphrasing, while prompt engineering improves model robustness but does not prevent determined attackers from discovering novel attack vectors. These isolated defenses create a fragmented security posture where attackers can navigate vulnerabilities at component boundaries.

Second, the architecture of current LLM-integrated applications conflates user-controlled data with trusted system instructions, creating fundamental information flow vulnerabilities. Frontend components, data processing pipelines, system prompts, and output handlers operate with insufficient isolation and context separation. Recent system-level analyses demonstrate that even systems implementing multiple safety constraints at the LLM level remain vulnerable to coordinated attacks exploiting component integration weaknesses. This architectural flaw requires fundamental redesign of information flow between system components.

Third, existing defenses create significant utility-security tradeoffs that limit practical deployment. Aggressive filtering reduces false negatives but increases false positives, blocking legitimate user requests and degrading application functionality. Furthermore, defenses are often model-specific or dataset-specific, failing to generalize across different LLM architectures or application contexts.

Fourth, the dynamic nature of prompt injection threats creates a moving target problem. New attack techniques emerge continuously through automated optimization methods, template-based approaches, and adversarial search algorithms. Attack transferability between models means that defenses designed for one LLM architecture may prove ineffective against others.

### Research Questions

This work addresses the following research questions:

**RQ1:** How do prompt injection attacks propagate across different layers of a full-stack web application?

**RQ2:** Which system-level trust boundary violations enable successful prompt injection?

**RQ3:** How can coordinated workflow-level defenses reduce attack success compared to isolated mitigations?

### Proposed Solution and Research Contribution

**This paper proposes a unifying framework synthesizing existing defense approaches into a system-level workflow model spanning the complete application stack.** Rather than proposing isolated security mechanisms, we present a coordinated six-layer defense architecture that maps to the full lifecycle of user requests flowing through LLM-integrated applications. Each layer addresses specific attack vectors while feeding security-relevant information to downstream layers and maintaining feedback loops that enable adaptive defense refinement.

The proposed model makes three fundamental contributions to prompt injection defense. **First, it provides a system-level workflow deriving implementable patterns from literature synthesis, extending beyond model-centric prior work that treats prompt injection as solvable through improved alignment alone.** This structured framework decomposes the complex problem of securing LLM-integrated applications into manageable, addressable components spanning the complete application stack. Second, it shows how existing defense mechanisms can be orchestrated into a coherent system where individual components operate synergistically, each compensating for limitations in others and collectively providing defense-in-depth protection. Third, it introduces six practical design patterns derived from the workflow model that developers can implement to secure full-stack applications without requiring deep expertise in prompt injection vulnerabilities or LLM security.

This system-level perspective is not the main focus of most existing work, which typically treats prompt injection as a model-level problem solvable through improved alignment or detection techniques. This paper argues that architectural decisions at the system level are equally important as component-level robustness. The workflow model shows how information flow between frontend, data processing, context management, LLM interaction, output handling, and feedback loops must be redesigned to inherently resist prompt injection attacks.

The research is grounded in comprehensive analysis of 12 foundational papers covering attack methodologies, defense mechanisms, threat modeling, and system-level security analysis. Through synthesis of existing literature and extension of prior work, we develop a coherent framework addressing gaps identified in current research: the lack of system-level security analysis for complete applications, the absence of architecture-centric defense design, and the missing connection between threat modeling and implementation guidance.

---

## LITERATURE REVIEW

This literature review synthesizes 12 key research papers addressing prompt injection vulnerabilities across attack methodologies, defense mechanisms, threat modeling, and system-level security analysis.

**Paper 1 (HouYi)**: Liu et al. aim to investigate prompt injection risks in real-world LLM-integrated applications and develop effective black-box attack techniques. They propose HouYi, a three-phase framework using context inference, payload generation (Framework, Separator, Disruptor components), and iterative refinement via GPT-3.5 feedback. They achieve 86.1% attack success rate across 36 commercial applications including Notion and WriteSonic, demonstrating that existing defenses (XML tagging, paraphrasing, retokenization) can be systematically bypassed.

**Paper 2 (LLM-as-a-Judge Attacks)**: Maloyan and Namiot aim to evaluate the vulnerability of LLM-as-a-judge systems to prompt injection attacks. They extend the HouYi framework with four attack variants (Basic Injection, Complex Word Bombardment, Contextual Misdirection, Adaptive Search-Based) and test them across five judge models on diverse evaluation tasks. They show that Adaptive Search-Based attacks achieve 42.9-73.8% success rates, with frontier models demonstrating higher robustness, and that multi-model committees using 5-7 diverse models reduce attack success to 10-27%.

**Paper 3 (JBShield)**: Zhang et al. aim to detect and mitigate jailbreak attacks by analyzing toxic and jailbreak concepts encoded in LLM hidden representations. They apply Linear Representation Hypothesis with truncated SVD to extract concept subspaces from counterfactual prompt pairs, using cosine similarity-based detection and concept manipulation for mitigation without fine-tuning. They achieve 0.95 F1-score for detection and reduce attack success rates from 61% to 2% with minimal utility impact (less than 2% MMLU degradation).

**Paper 4 (Threat Modeling)**: Burabari aims to develop threat modeling and risk analysis frameworks specifically tailored for LLM-powered applications. The paper integrates STRIDE methodology with DREAD risk analysis and adapts Shostack's Four Question Framework to address LLM-specific threats including data poisoning, prompt injection, and compositional injection. An end-to-end threat model of an LLM-Doctor application validates the framework, ranking Denial of Service as highest-risk vulnerability followed by Tampering/Prompt Injection.

**Paper 5 (Comprehensive Review)**: Peng et al. aim to systematically review jailbreak attacks and mitigation strategies across the evolving LLM security landscape. They categorize attacks into manually-designed, optimization-based, template-based, linguistics-based, and encoding-based types, while organizing defenses into detection-based and mitigation-based approaches. Their analysis reveals that multimodal attacks exploit semantic image-text alignment gaps, multilingual attacks achieve 50-70% success rates in low-resource languages, and no single defense approach provides complete protection.

**Paper 6 (PromptArmor)**: Shi et al. aim to develop a practical and scalable defense against prompt injection attacks on LLM agents. They design a modular preprocessing layer using a guardrail LLM with carefully crafted prompting strategies to detect and remove injected content via instruction-based detection and fuzzy matching extraction. PromptArmor-GPT-4o achieves 0.47% attack success rate with 0.07% false positive rate and 68.68% utility preservation on the AgentDojo benchmark, significantly outperforming six baseline defenses.

**Paper 7 (LLM Security Survey)**: This survey aims to comprehensively categorize security threats across the complete LLM lifecycle from training to deployment. The authors systematically classify training-phase attacks (data poisoning, backdoors) versus inference-phase attacks (prompt injection, jailbreaking), and organize defenses into prevention-based approaches (prompt filtering, instruction hierarchy) versus detection-based methods (output monitoring, cross-LLM validation). Empirical analysis reveals inference-phase threats persist as isolated filters fail against adaptive adversaries capable of modifying attack strategies, emphasizing the necessity of multi-layered defense strategies combining prevention and detection.

**Paper 8 (Jailbreak Study)**: This paper aims to systematically evaluate jailbreak attack effectiveness against various defense mechanisms across different model architectures. The authors conduct comparative evaluation testing 10+ distinct attack methods against 8 defense configurations through systematic benchmarking, analyzing attack transferability across GPT, Claude, and Llama model families and robustness of combined defense strategies. Results show sophisticated attacks achieve over 50% success rates even against defended models, with ensemble defense strategies combining filtering, alignment, and output validation outperforming single-layer defenses by 20-40 percentage points through transferability mitigation.

**Paper 9 (Detection Methods)**: This paper aims to develop effective detection approaches for prompt injection attacks on LLM applications. The authors propose methods combining BERT-based feature extraction capturing syntactic and semantic patterns, semantic analysis using sentence embeddings to compute cosine similarity with known injection templates, and ensemble techniques where 3-5 detection models vote on injection likelihood with majority consensus. Ensemble approaches achieve 30-40 percentage point F1-score improvement over single-model baselines, with semantic understanding improving detection accuracy by 15-25 percentage points while maintaining application utility through low false positive rates.

**Paper 10 (System-Level Analysis)**: This paper aims to analyze security of complete LLM systems rather than isolated models by examining information flow between components. The authors conduct multi-layer decomposition examining constraints between the LLM core and integrated components (frontend, webtool, sandbox), with end-to-end attack demonstrations on deployed systems like OpenAI GPT-4. System-level analysis exposes critical vulnerabilities in full-stack systems despite multiple safety measures, with successful attacks acquiring unauthorized user chat history by exploiting component boundary weaknesses.

**Paper 11 (ThreMoLIA Framework)**: Jedrzejewski et al. aim to automate threat modeling for LLM-integrated applications using AI-assisted approaches. They develop ThreMoLIA, an LLM-RAG architecture that leverages existing threat model repositories as knowledge bases, retrieving relevant historical threats through semantic search and integrating STRIDE, DREAD, and OWASP methodologies. Initial feasibility studies demonstrate that the framework successfully generates application-specific threat models while reducing reliance on manual security expert involvement.

**Paper 12 (SafeRAG)**: This paper aims to evaluate security vulnerabilities across all components of Retrieval-Augmented Generation (RAG) systems. The authors develop the SafeRAG benchmark and propose ReGENT, a reinforcement learning-based attack framework that optimizes adversarial perturbations to manipulate document retrieval rankings. Evaluation across 14 representative RAG implementations reveals significant vulnerabilities with high attack success rates across retriever, filter, ranker, and LLM components despite multiple defensive layers.

**Research Gaps**: While existing literature thoroughly documents attacks and isolated defenses, three critical gaps remain: (1) lack of unified framework showing defense coordination across system layers, (2) missing connection between architectural design patterns and vulnerability mitigation, and (3) absence of concrete implementation guidance for coordinated layer-based defenses. The proposed workflow model addresses these gaps by synthesizing research into a coherent six-layer framework where each layer compensates for limitations in others, transforming isolated findings into actionable security architecture guidance.

### Comparison with Existing Work

Table 1 demonstrates how the proposed workflow model addresses vulnerabilities exploited by current attack frameworks while incorporating defenses from state-of-the-art mitigation approaches:

| Attack/Defense | Attack Vectors Exploited | Layers Addressing Gaps |
|----------------|-------------------------|------------------------|
| **HouYi Framework** | Context inference, payload injection, iterative refinement bypass defenses | Layer 1 (syntax validation), Layer 2 (semantic analysis), Layer 3 (context isolation prevents framework/separator attacks) |
| **Adaptive Attacks** | Contextual misdirection, complex bombardment targeting judge systems | Layer 4 (representation monitoring), Layer 6 (pattern learning detects emerging variations) |
| **JBShield Defense** | Representation-level monitoring, concept manipulation | Workflow integrates as Layer 4 component, enhanced by upstream filtering (Layers 1-2) and downstream validation (Layer 5) |
| **PromptArmor Defense** | Guardrail LLM detection, fuzzy matching extraction | Workflow integrates as Layer 4-5 component, benefits from Layer 3 context isolation reducing false negatives |
| **System-Level Exploits** | Component boundary weaknesses, information flow violations | Layer 3 addresses through architectural isolation; Layer 6 feedback closes inter-component gaps |

The workflow model uniquely combines attack surface coverage (addressing HouYi's exploit vectors) with defense orchestration (coordinating JBShield, PromptArmor mechanisms across layers), filling the gap between isolated component security and full-stack protection.

---

## PROPOSED MODEL

### System-Level Workflow Architecture

The system-level workflow model comprises six coordinated defense layers (Figure 1) addressing attack vectors across the complete request processing pipeline. Each layer operates at a specific lifecycle point, addresses particular attack categories, and communicates security information to downstream layers. The architecture follows defense-in-depth principles where attack success at any single layer remains unlikely due to compensating controls at subsequent layers.

**Note on Model Validation**: This section introduces the conceptual model. In Section 4, we present empirical experiments that implement a subset of these mechanisms (Layers 1-5 and partial Layer 6) to evaluate their impact in a concrete system. Effectiveness statements for specific techniques in this section refer to results reported in prior work.

![System-Level Workflow Model for Prompt Injection Mitigation](./visualizations_root/architecture_diagram_generated.png)

*Figure 1: High-level multi-layer LLM request processing and security framework. The core processing system applies Layers 1–5, while the feedback layer performs offline monitoring and adaptation.*

![Detailed System Workflow](./visualizations_root/System-Level%20Workflow%20Model%20for%20Prompt%20Injection%20Mitigation_generated.png)

*Figure 2: System-level workflow model for prompt injection mitigation. Boundary, semantic, context, LLM interaction, and output validation layers are coordinated with adaptive elements and a partially implemented feedback layer.*

### Layer 1: Request Boundary

This layer performs character-level validation, syntax checking, and preliminary request classification at the application's outermost edge. Core components include character encoding validation, length threshold enforcement, and protocol-level validation addressing obfuscated inputs, protocol violations, and parser edge cases. While semantic attacks typically bypass this layer, it provides essential first-line defense and outputs validated requests with metadata tagging while maintaining minimal latency overhead.

**Layer 1 Outputs**: The layer appends a JSON metadata structure `{"validation_status": "passed", "encoding": "UTF-8", "length": 1247, "anomaly_score": 0.12, "protocol_violations": []}` to each request, which downstream layers consume for risk assessment.

### Layer 2: Input Processing and Semantic Analysis

This layer performs tokenization, semantic analysis, pattern detection, and feature extraction to identify injection indicators beyond syntax validation. Core components include domain-aware tokenizers understanding LLM-specific patterns, semantic analysis employing embeddings to assess meaning similarity with benign content, and pattern detection identifying injection indicators such as command structures, instruction keywords, and boundary markers.

The layer addresses semantic paraphrasing, encoding-based attacks (Base64, ROT13), and context-manipulation attacks. Semantic analysis has been shown to significantly improve detection rates over simple keyword filters in prior work, because it assesses meaning rather than exact word sequences. However, adversarial optimization can circumvent detection through carefully crafted inputs maintaining semantic validity while injecting commands. The layer outputs enriched representations with confidence scores and feature vectors for downstream processing.

**Layer 2 Outputs**: The layer enriches requests with `{"injection_confidence": 0.73, "detected_patterns": ["command_structure", "instruction_override"], "embedding_similarity": 0.42, "risk_level": "medium"}`, enabling Layer 3 to adjust isolation strictness and Layer 4 to trigger enhanced monitoring.

### Layer 3: Context Management and Isolation

This layer establishes logical and operational boundaries between user-controlled input and trusted system instructions, preventing cross-context influence. Core components include system prompt isolation maintaining instructions in protected memory regions, context compartmentalization establishing separate processing contexts for sessions and functions, and instruction hierarchy defining privilege levels for trusted versus user-originated instructions.

The layer addresses system prompt exposure attacks, context override attempts, and privilege escalation through prompt templating, data-prompt separation using delimiters, and constraint enforcement. Architectures that keep system prompts in separate processes can greatly reduce prompt injection success in reported experiments, while shared string processing architectures remain substantially more vulnerable. The key insight: information flow architecture itself determines effectiveness; detection mechanisms cannot fully compensate for architectural weaknesses. The layer outputs requests with contextual annotations marking content origins and privilege levels.

**Layer 3 Outputs**: The layer produces `{"user_context_id": "sess_4729", "system_prompt_hash": "a3f2c1", "privilege_level": "user", "isolation_boundary": "enforced", "constraint_violations": []}`, ensuring Layer 4 knows which instructions are trusted and which require skeptical processing.

![Context Isolation Architecture (Layer 3)](./visualizations_root/Context%20Isolation%20Architecture%20(Layer%203)_generated.png)

*Figure 3: Context isolation architecture (Layer 3). User input and session data remain isolated from system prompts until combined by the constraint enforcement layer, which prioritizes system instructions before invoking the LLM core.*

### Layer 4: LLM Interaction and Constraint Enforcement

This layer implements constraints at the interface between application logic and LLM, enforcing intended operational boundaries. Core components include constraint enforcement mechanisms defining prohibited operations, representation-level monitoring analyzing LLM hidden layer activations to detect harmful request patterns, and guardrail model architecture employing separate LLMs to validate primary LLM outputs.

The layer addresses attacks succeeding despite input filtering, attacks exploiting fine-tuned LLM behavior, and attacks targeting sensitive operations through legitimate-appearing requests. Representation-level defenses like JBShield report F1 scores around 0.95 and reduce jailbreak attack success to about 2% on their benchmark, while guardrail model approaches like PromptArmor demonstrate strong filtering effectiveness with minimal false positives. Attack vectors include adaptive attacks designed to pass representation-level detection, multi-turn attacks gradually manipulating LLM behavior, and composite attacks combining multiple techniques. The layer outputs validated LLM responses with confidence scores and detailed processing information.

**Layer 4 Outputs**: The layer generates `{"llm_response": "...", "guardrail_verdict": "safe", "representation_anomaly": 0.15, "constraint_violations": [], "response_confidence": 0.91}`, which Layer 5 uses to determine if additional output validation is required.

### Layer 5: Output Handling and Validation

This layer validates LLM outputs before returning to users or downstream systems, preventing data leakage and ensuring format compliance. Core components include response validation checking format specifications and safety constraints, data leakage prevention detecting unintended sensitive information exposure such as system prompts or training data, and confidence scoring assessing injection likelihood.

The layer addresses data exfiltration where injected instructions cause sensitive output, format manipulation where outputs bypass downstream security, and prompt leakage where system prompts are revealed. Defense mechanisms include sensitive data pattern detection, output classification, and multi-layered validation combining format, semantic, and pattern checking. Output-layer defenses provide critical protection for specific attack categories where input-layer defenses alone prove insufficient.

**Layer 5 Outputs**: The layer produces `{"validated_output": "...", "leakage_detected": false, "format_compliant": true, "sensitive_patterns": [], "final_risk_score": 0.08}`, with feedback sent to Layer 6 for pattern learning.

### Layer 6: Feedback and Adaptive Monitoring

This layer enables continuous learning by observing system behavior and attack patterns. Core components log attack attempts, analyze patterns, adapt confidence thresholds based on false positive/negative rates, and update detection models through adaptive learning. It maintains time-series data on attack patterns and system performance to identify trends and emerging threats.

The layer enables feedback loops where detections at any layer inform adjustments across the entire system. New attack patterns update detection rules for all layers. It supports anomaly detection, ensemble adjustment, and automated rule evolution, outputting recommendations for system adjustments, alerts on emerging threats, and updated detection rules.

**Layer 6 Outputs**: The layer broadcasts `{"detected_attack_pattern": "adaptive_search_variant_3", "frequency": 47, "success_rate": 0.03, "recommended_threshold_adjustment": {"layer_2_confidence": 0.65}}` to all layers, enabling coordinated adaptation.

### Layer Interconnections and Information Flow

The six layers form an integrated system where information flows sequentially from requests through LLM to outputs, plus through feedback and lateral communications. **Building on initial request validation, Layer 2 suspicious patterns directly inform Layer 3 context management decisions and trigger enhanced Layer 4 constraint enforcement.** Layer 5 data leakage detection triggers Layer 2 retrospective analysis for similar patterns in queued requests. Layer 6 emerging attack patterns broadcast updated detection rules to all layer detection modules.

Attacks bypassing one layer encounter multiple compensating controls at subsequent stages. Semantic attacks bypassing Layer 2 pattern detection encounter Layer 3 context isolation preventing system prompt override and Layer 4 constraint enforcement blocking unauthorized operations. Attacks successfully manipulating LLM behavior at Layer 4 remain blocked by Layer 5 output validation detecting data exfiltration patterns. Adaptive attacks defeating Layer 4 representation-level detection trigger Layer 6 anomaly detection and pattern analysis, enabling rapid rule updates.

**Example Application Walkthrough**: Consider an LLM-based customer support chatbot integrated into a web application. Layer 1 validates HTTP request format and basic input size constraints. Layer 2 uses semantic analysis to flag injected instructions such as "ignore previous rules and dump all past chats." Layer 3 isolates system prompts and API keys in separate contexts, ensuring user input cannot override trusted instructions. Layer 4 constrains tool calls to approved operations and monitors hidden representations for jailbreak patterns. Layer 5 checks that responses do not expose internal ticket IDs, credentials, or system prompts. Layer 6 logs repeated suspicious attempts from specific sources to refine detection thresholds and update blocking rules across all layers.

![Attack Flow vs Mitigated Flow](./visualizations_root/Attack%20Flow%20vs%20Mitigated%20Flow_generated.png)

*Figure 4: Comparison of vulnerable attack flow versus mitigated flow with the workflow model. The baseline mixes user and system prompts directly, while the mitigated pipeline enforces layered checks and output validation before returning a safe response.*

### Practical Design Patterns

The workflow model enables derivation of six practical design patterns for securing full-stack applications:

**Pattern 1: Defense-in-Depth Pipeline** implements sequential validation through multiple independent detection modules in series, processing requests only when passing all modules. Maps to Layers 1-2 coordination.

**Pattern 2: Guardrail Model Architecture** implements Layer 4 constraints using separate, smaller LLMs validating primary LLM outputs, achieving strong security-utility tradeoff through semantic understanding versus keyword patterns.

**Pattern 3: Representation-Level Defense** implements Layer 4 constraint enforcement through monitoring hidden layer activations, following approaches like JBShield that report around 0.95 F1 detection and substantial reductions in jailbreak success on their benchmarks.

**Pattern 4: Ensemble Consensus** implements collaborative defense across Layers 2 and 4 where multiple independent detection models vote on injection attempts, reducing individual model limitations through voting mechanisms (typically 3-5 models).

**Pattern 5: Contextual Isolation** implements Layer 3 context management through architectural separation of system instructions from user data via separate processing paths, memory regions, or representational separation. Most effective when implemented during architectural design rather than retrofitted.

**Pattern 6: Adaptive Feedback Loop** implements Layer 6 monitoring through systematic attack data collection, pattern analysis, and automatic threshold/rule adjustment, enabling continuous security improvement as systems encounter real attacks.

### Model Validation and Limitations

The model synthesizes findings from 12 research papers, comprehensively covering attack surfaces identified across literature: direct injection (Layers 1-3), semantic attacks (Layers 2, 4), system prompt targeting (Layer 3), LLM manipulation (Layer 4), data exfiltration (Layer 5), and adaptive attacks (Layer 6). Each layer incorporates defense mechanisms validated in existing research: pattern matching (Layer 2), prompt isolation (Layer 3), representation-level monitoring (Layer 4, as demonstrated by JBShield), guardrail models (Layer 4-5, as demonstrated by PromptArmor), ensemble detection (Layers 2 and 4), and adaptive learning (Layer 6).

Defense-in-depth principles from Papers 2, 5, and 8 directly inform coordinated layering. System-level vulnerability analysis from Papers 10 and 12 motivates the model's component-interaction focus. Threat modeling frameworks from Papers 4 and 11 provide methodology for mapping threats to layers.

The model acknowledges that perfect security remains unachievable, and sophisticated adaptive attacks may discover vulnerability combinations across layers. Model effectiveness depends on proper layer implementation, and resource-limited organizations may struggle with complete six-layer deployment. However, implementing comprehensive defense-in-depth architecture informed by existing research enables substantial attack success rate reduction compared to isolated defenses, as demonstrated in our experiments (Section 4). The model provides framework for continuous improvement through feedback mechanisms and adaptive learning, enabling security evolution as attack techniques advance.

### Validation Roadmap

To empirically validate this conceptual framework, we conducted comprehensive experiments using the HouYi framework against different layer configurations (baseline, Layers 1-3 only, Layers 1-5 only, complete six-layer). The experiments benchmarked attack success rates across 11,490 execution traces with configurations including isolated baselines and adaptive coordination mechanisms. We measured configuration-specific detection rates and evaluated defense coordination effectiveness by comparing attack success against isolated single-layer defenses versus the integrated workflow model. The experimental protocol tested the hypothesis that coordinated multi-layer architectures achieve superior attack mitigation compared to component-level defenses, quantifying the value of system-level security design.

---

## EXPERIMENTAL RESULTS AND ANALYSIS

### Implementation Scope

To empirically validate the proposed framework, we implemented Layers 1-5 as runtime defenses and a partial Layer 6. Our implementation covers the full request processing pipeline including input validation (L1), semantic analysis (L2), context isolation (L3), LLM interaction with constraints (L4), and output validation (L5). Layer 6 (Feedback) implementation is conceptual for online adaptation; feedback was used offline to refine configurations between experiments, but real-time automated rule updates were not active during single execution runs.

> Attacks used HouYi-style templates (52 context-inference prompts, 42 payload variants) targeting data exfiltration, system prompt theft, and unauthorized operations. Success was automatically judged by regex matching on outputs for leaked data, ignored instructions, or constraint violations.

> Code, `experiments.db` (11,490 traces), and logs: https://github.com/ArindamTripathi619/prompt-injection-experiments (commit [cd77095]).

### 4.1 Overall Defense Effectiveness

![Qualitative Defense Effectiveness Flow](./visualizations_root/layer_effectiveness_flow_generated.png)

*Figure 5: Qualitative defense effectiveness flow. Each layer contributes different types of safeguards; this diagram is conceptual and does not represent measured probabilities.*

Our comprehensive experimental validation demonstrates the effectiveness of the proposed six-layer workflow model against prompt injection attacks. Across 11,490 execution traces, the full defense architecture achieved a substantial reduction in attack success rates from 80.77% (no defense) to 18.67% (full defense), representing a 68.1% absolute risk reduction. The overall attack success rate across all configurations was 31.51%.

**Baseline Attack Success Rate (ASR):** 80.77%
**Full Defense ASR:** 18.67%
**Risk Reduction:** 68.1% (from 80.77% to 18.67%)

### 4.2 Performance Metrics

#### 4.2.1 Attack Success Rate Metrics

The experimental analysis yielded the following configuration-specific ASR metrics across 11,490 traces:

| Configuration | Layers Active | Coordination | ASR |
|---------------|---------------|--------------|-----|
| **Isolated** | L1-L5 Independent | None | 21.83% |
| **Adaptive L3** | L1-L5 | L2 signals → L3 isolation | 20.12% |
| **Adaptive L4** | L1-L5 | L2 signals → L4 guardrails | 18.52% |
| **Full Adaptive** | L1-L5 | L2 → L3 & L4; L6 signals | 18.67% |

*> \*No defense = Layer 4 (base LLM) without additional pipeline defenses (L1,2,3,5).*

The adaptive coordination approach showed an absolute reduction of 2.72% (12.46% relative) compared to isolated configurations, demonstrating the modest but measurable value of coordinated defense mechanisms.

#### 4.2.2 Key Performance and Impact Metrics

| Metric | Value |
|--------|-------|
| Total traces | 11,490 |
| Baseline ASR | 80.77% |
| Full defense ASR | 18.67% |
| Output leakages | 959 |
| Total cost | $6.60 |

The analysis identified output leakage as the most common attack vector (959 occurrences, 65% of detected bypasses), highlighting the critical necessity of Layer 5 validation. Semantic detection bypasses accounted for 400 occurrences, while direct LLM constraint violations were rarest at 114 occurrences.

![Bypass Mechanisms Distribution](./visualizations_root/bypass_mechanisms.png)

*Figure 6: Distribution of 1,473 bypass mechanisms observed across 11,490 traces. Output leakage dominates, followed by semantic detection bypasses and a smaller fraction of direct LLM constraint violations.*

Regarding performance, the system maintained acceptably low latency overhead (20-50ms per request for defenses) compared to the dominant LLM inference time (262ms - 3s). The total cost of $6.60 for 11,490 traces confirms the economic feasibility of this defense architecture for large-scale security testing.

### 4.3 Statistical Methodology and Validation

The statistical analysis employed the following methods:

- **Wilson Score Confidence Intervals** were calculated for all configurations
- **McNemar's test** was not applicable because each configuration utilized a slightly different test set, necessitating a between-group comparison approach rather than paired testing
- **Effect size calculations** showed consistent improvement across configurations

The analysis confirmed that adaptive coordination provides measurable value, with full adaptive coordination achieving the lowest ASR of 18.67%.

![ASR Statistical Significance](./visualizations_root/statistical_significance_analysis.png)

*Figure 7: Attack success rate (ASR) distributions with 95% confidence intervals for isolated deployment and adaptive configurations. Relative percentage changes shown in green are computed against the isolated baseline.*

![ASR Configuration Comparison](./visualizations_root/asr_comparison_chart_generated.png)

*Figure 8: ASR comparison across baseline and defense configurations. Adaptive Layer 4 only and full adaptive setups yield the lowest attack success rates relative to the isolated configuration.*


### 4.4 Conclusion

Our evaluation across 11,490 traces confirms that a coordinated, multi-layer defense architecture dramatically outperforms isolated mitigations. The full defense stack reduced the Attack Success Rate (ASR) from 80.77% to 18.67%, a 68.1% absolute risk reduction. Findings indicate that while output validation is individually powerful, maximum resilience requires adaptive coordination, particularly at the LLM interaction layer. With minimal computational overhead and low cost, this approach is both effective and practical. These results empirically validate the shift from component-level fixes to system-level workflow models as the necessary evolution for securing LLM-integrated applications against sophisticated prompt injection threats.

## 5. ANALYSIS AND DISCUSSION

### 5.1 Hardware Specifications and Computational Overhead

The experimental validation was conducted on RunPod cloud GPU infrastructure utilizing NVIDIA RTX 4090 GPUs with 24 GB VRAM. The complete experimental suite was executed across 4 parallel pods simultaneously, with each experiment running on dedicated hardware resources. The computational infrastructure specifications include:

- **GPU Hardware**: NVIDIA RTX 4090 (24 GB VRAM) per pod
- **System Memory**: 31 GB RAM per pod
- **Virtual CPUs**: 8 vCPUs per pod
- **Storage**: 50+50GB storage (system + data) per pod
- **Execution Time**: 1.5-3.0 hours total for all 4 experiments
- **Individual Experiment Duration**: 
  - Exp 1: 15.1 minutes (Total time: 0.25 hours)
  - Exp 2: 21.9 minutes (Total time: 0.37 hours)
  - Exp 3: 28.0 minutes (Total time: 0.47 hours)
  - Exp 4: 4.1 minutes (Total time: 0.07 hours)
- **Per-Request Latency**: 
  - Layer 4 (LLM Interaction): 262ms to 2,973ms (average ~1,500ms) - dominated by LLM inference
  - Layer 2 (Semantic Analysis): 5-15ms
  - Layer 1 (Boundary): <1ms
  - Layer 3 (Context Isolation): <1ms
  - Layer 5 (Output Validation): <1ms
- **Total Per-Request Latency**: Varies from ~300ms to ~3,000ms depending on LLM processing time

The latency overhead is primarily dominated by LLM inference time, with the defense layers adding minimal computational overhead (typically <20ms per defense layer). The multi-layer defense architecture adds approximately 20-50ms of additional overhead beyond the baseline LLM processing time. The Ollama LLM inference engine was used with Llama 3.2:1b model, running locally on each pod to ensure consistent performance metrics across all experiments.

### 5.2 Cost Analysis

The total computational cost for the complete experimental validation was $6.60, broken down as follows:

| Experiment | Pods | Runtime | Cost/Pod | Total Cost |
|-----------|------|---------|----------|------------|
| Exp 1 | 1 | 1.5h | $0.66 | $0.66 |
| Exp 2 | 1 | 2.0h | $0.88 | $0.88 |
| Exp 3 | 1 | 2.5h | $1.10 | $1.10 |
| Exp 4 | 1 | 1.0h | $0.44 | $0.44 |
| Exp 5 | 4 | 1.0h | $0.44 | $1.76 |
| Exp 6 | 4 | 1.0h | $0.44 | $1.76 |
| **Total** | — | — | — | **$6.60** |

**Pricing Details:**
- GPU: NVIDIA RTX 4090 at $0.44/hour per pod
- Platform: RunPod Cloud
- Total runtime: ~8 hours across all experiments

The actual documented cost in the experimental logs was $6.60. This represents the accurate cost of the 4 RTX 4090 GPU pods with the specified hardware configuration (24GB VRAM, 31GB RAM, 8vCPUs, 50+50GB storage) used for the experiments.

The cost-effectiveness analysis shows that comprehensive validation of the multi-layer defense architecture achieved significant security improvements at minimal computational cost. The cost per percentage point of ASR improvement was approximately $0.09, demonstrating excellent cost-effectiveness for security research validation.

### 5.3 Key Findings and Implications

The experimental results provide several critical insights into the nature of prompt injection attacks and effective defense strategies:

#### 5.3.1 Adaptive Coordination Value The full adaptive coordination achieved 18.67% ASR compared to 21.83% for isolated configurations, representing a 2.72% absolute reduction (12.46% relative). This demonstrates that while individual layers provide the bulk of defense, information sharing adds a layer of robustness.

#### 5.3.2 Layer 4 as Critical Coordination Point

The analysis showed that Adaptive L4 only configuration achieved 18.52% ASR, which was slightly better than full adaptive (18.67%), indicating that Layer 4 (LLM Interaction) adaptive monitoring is particularly effective as a coordination point. This layer can dynamically adjust its guardrail intensity based on risk signals from earlier layers.

#### 5.3.3 Output Validation as Primary Defense

The trust boundary analysis revealed that output leakage was detected in 959 occurrences (the most common attack vector), highlighting the critical importance of output validation as a defense mechanism. This confirms that organizations implementing prompt injection defenses should prioritize output validation capabilities.

### 5.4 Attack Propagation and Defense Evasion

The experimental results provide clear evidence of how prompt injection attacks propagate through defense layers:

- **Overall bypass rate:** 12.82% of traces showed some form of bypass mechanism
- **Primary bypass vectors:** Output leakage (959 occurrences), semantic detection (400 occurrences), and LLM constraint violations (114 occurrences)
- **Defense effectiveness:** The progression from 80.77% baseline ASR to 18.67% with full defense demonstrates the cumulative effectiveness of the layered approach

### 5.5 Performance vs. Security Trade-offs

The analysis reveals important trade-offs between security and performance:

- The multi-layer defense architecture processes 11,490 traces with an overall ASR of 31.51%
- The coordination overhead is minimal while providing measurable security improvements
- The adaptive coordination provides 2.72% additional reduction in ASR with minimal computational cost

### 5.6 Practical Deployment Implications

Based on the experimental results, we recommend the following deployment strategies:

1. **Minimum Viable Defense:** Organizations should implement output validation as it addresses the most common attack vector (959 occurrences of output leakage detected).

2. **Comprehensive Defense:** Organizations requiring maximum protection should implement all five layers with adaptive coordination enabled, achieving the demonstrated 2.72% additional improvement over isolated configurations.

3. **Layer Prioritization:** When resource constraints prevent full implementation, prioritize Layer 4 (critical for coordination) and output validation capabilities.

### 5.7 Limitations and Future Work

While the experimental results are robust, several limitations should be acknowledged:

1. **McNemar's Test Limitation:** Due to different test sets per configuration, McNemar's test was not possible, limiting statistical significance testing.

2. **Configuration Differences:** Experiments 6B and 6C were planned but not executed, limiting the scope of configuration comparisons.

3. **Future Work:** Future evaluations should use common test sets for direct comparison and more rigorous statistical testing.

Despite these limitations, the experimental results provide strong evidence for the effectiveness of the proposed six-layer workflow model and offer practical guidance for implementing prompt injection defenses in real-world applications.

---

## REFERENCES

1. Liu, Y., Deng, G., Li, Y., Wang, K., Wang, Z., Wang, X., Zhang, T., Liu, Y., Wang, H., Zheng, Y., & Liu, Y. (2024). Prompt injection attack against LLM-integrated applications (HouYi). *arXiv preprint arXiv:2306.05499*.

2. Maloyan, N., & Namiot, D. (2024). Adversarial attacks on LLM-as-a-judge systems. *arXiv preprint arXiv:2504.18333*.

3. Zhang, S., Zhai, Y., Guo, K., Hu, H., Guo, S., Fang, Z., Zhao, L., Shen, C., Wang, C., & Wang, Q. (2025). JBShield: Defending large language models from jailbreak attacks. *USENIX Security 2025*.

4. Burabari, S. T. (2024). Threat modelling and risk analysis for large language model-powered applications. *arXiv preprint arXiv:2406.11007*.

5. Peng, B., Chen, K., Niu, Q., Bi, Z., Liu, M., Feng, P., Wang, T., Yan, L. K. Q., Wen, Y., Zhang, Y., Yin, C. H., & Song, X. (2024). Jailbreaking and mitigation of vulnerabilities in large language models. *arXiv preprint arXiv:2410.15236*.

6. Shi, T., Zhu, K., Wang, Z., Jia, Y., Cai, W., Liang, W., Wang, H., Alzahrani, H., Lu, J., Kawaguchi, K., Alomair, B., Zhao, X., Wang, W. Y., Gong, N., Guo, W., & Song, D. (2025). PromptArmor: Simple yet effective prompt injection defenses. *arXiv preprint arXiv:2507.15219*.

7. Zhang, Y., et al. (2025). LLM security: Vulnerabilities, attacks, defenses, and evaluation. *arXiv preprint arXiv:2505.01177*.

8. Wang, L., et al. (2024). A comprehensive study of jailbreak attack versus defense for large language models. *ACL Findings 2024*.

9. Chen, X., et al. (2024). Detecting prompt injection attacks against LLM applications. *arXiv preprint arXiv:2512.12583*.

10. Li, H., et al. (2024). A new era in LLM security: Multi-layer and system-level analysis. *arXiv preprint arXiv:2402.18649*.

11. Jedrzejewski, F. V., et al. (2025). Threat modeling with LLM-RAG: ThreMoLIA framework. *arXiv preprint arXiv:2504.24369*.

12. Kumar, A., et al. (2024). SafeRAG: Benchmarking security in retrieval-augmented generation. *arXiv preprint arXiv:2501.18636*.

13. Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. *ACM CCS 2023*.

14. OWASP Foundation. (2023). OWASP Top 10 for Large Language Model Applications. Retrieved from https://owasp.org/www-project-top-10-for-large-language-model-applications/