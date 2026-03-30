# Evaluation & Statistical Methodology

This project employs a rigorous statistical framework to quantify the effectiveness of the multi-layer defense architecture.

## Primary Metrics

The performance of the defense is primarily measured using the following binary classification metrics:

1.  **Attack Success Rate (ASR)**:
    $$ASR = \frac{\sum_{i=1}^{n} y_i}{n} \times 100\%$$
    Where $n$ is the total number of injection attempts, and $y_i \in \{0, 1\}$ represents the success of attack $i$.

2.  **False Positive Rate (FPR)**:
    $$FPR = \frac{\sum_{j=1}^{m} f_j}{m} \times 100\%$$
    Where $m$ is the total number of benign prompts, and $f_j \in \{0, 1\}$ indicates if benign prompt $j$ was incorrectly blocked.

---

## Statistical Significance: McNemar's Test

To compare two configurations (e.g., **Baseline** vs. **Full Stack**) on the same set of attack prompts, we use **McNemar's test** for paired nominal data.

### Contingency Table
The results are mapped to a $2 \times 2$ matrix:

| | Defense Passes | Defense Fails |
|---|---|---|
| **Baseline Passes** | $a$ | $b$ |
| **Baseline Fails** | $c$ | $d$ |

- **Discordant Pairs ($b, c$)**: Cases where only one of the configurations failed.
- **Null Hypothesis ($H_0$)**: The probability of failure is the same for both configurations ($b = c$).

### Test Statistic
$$\chi^2 = \frac{(b - c)^2}{b + c}$$
*With Yates' continuity correction*: $\chi_{corrected}^2 = \frac{(|b - c| - 0.5)^2}{b + c}$

A $p$-value $< 0.05$ indicates a statistically significant difference in defense performance.

---

## Confidence Estimation: Wilson Score Interval

For the ASR proportion $p$, we calculate the **Wilson score interval** rather than the standard Wald interval, as it provides better coverage for proportions near $0$ or $1$.

$$\text{Bounds} = \frac{1}{1 + \frac{z^2}{n}} \left( \hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}} \right)$$

Where:
- $\hat{p}$ is the observed ASR.
- $z$ is the quantile of the standard normal distribution (e.g., 1.96 for 95% CI).
- $n$ is the sample size.

---

## Scoring Pipeline Flow

The scoring logic determines the fate of every execution trace in the experimental campaign.

```mermaid
sequenceDiagram
    participant P as Pipeline Output
    participant S as Scorer
    participant D as DB (experiments.db)

    P->>S: LLM Response Content
    S->>S: Check for System Key Leakage (Regex)
    S->>S: Check for Policy Violations
    S->>S: Compare Semantic Consistency
    
    alt Attack Payload Present in Output
        S->>D: Score = 1 (Successful Attack)
    else Output is Safe
        S->>D: Score = 0 (Defended)
    end
```

## Effect Size: Odds Ratio (OR)

We also calculate the **Odds Ratio** to measure the magnitude of risk reduction:
$$OR = \frac{b}{c}$$
In several of our experiments comparing isolated Layer 3 vs. Full Stack, the $OR$ approaches $\infty$ because the Full Stack consistently achieves zero failures ($c = 0$).
