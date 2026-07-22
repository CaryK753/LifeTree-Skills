# 23. Decision Science & Behavioral Utility Modeling Architecture Framework

## 1. Executive Summary & Vision

LifeTree is designed specifically for **high-stakes, irreversible personal decision-making** (e.g., cross-border relocation, career pivots, asset liquidations, global tax structuring). In traditional software architectures, AI agents frequently rely on naive weighted sums or LLM text hallucinations, yielding a "toy demo" feeling with false precision.

To solve this core paradigm gap, LifeTree implements a rigorous suite of **Code-Driven Mathematical Decision Frameworks** grounded in behavioral economics, multi-attribute utility theory, tail-risk management, Bayesian probability updating, dynamic game theory, and intertemporal discounting.

---

## 2. Multi-Attribute Utility Theory (MAUT) & AHP Weight Elicitation

### 2.1 Multi-Dimensional Attribute Definitions & Normalization
Human personal decisions cannot be reduced to monetary net worth alone. LifeTree models 6 core non-monetary and monetary life attributes $x_i \in [0, 100]$:

1. **Income & Wealth ($x_{\text{income}}$)**:
   Normalized from annual income and liquid capital:
   $$u_{\text{income}}(\mathbf{x}) = \min \left(100, \frac{\text{annual\_income}}{100,000} \times 100 \times 0.6 + \frac{\text{liquid\_funds}}{200,000} \times 100 \times 0.4 \right)$$

2. **Health ($x_{\text{health}}$)**:
   Subjective physical and mental health rating $u_{\text{health}} \in [0, 100]$.

3. **Inverted Time Cost ($x_{\text{time\_inv}}$)**:
   Captures free personal time availability. Higher work experience or demanding roles reduce time freedom:
   $$u_{\text{time\_inv}}(\mathbf{x}) = \max \left(30, 100 - \text{years} \times 5 \right)$$

4. **Freedom ($x_{\text{freedom}}$)**:
   Visa mobility, global citizenship rights, and legal autonomy score $u_{\text{freedom}} \in [0, 100]$.

5. **Family Stability ($x_{\text{family}}$)**:
   Dependent care obligations and family security:
   $$u_{\text{family}}(\mathbf{x}) = \max \left(50, 85 - \text{dependents} \times 5 \right)$$

6. **Inverted Stress ($x_{\text{stress\_inv}}$)**:
   Workload stress and psychological pressure:
   $$u_{\text{stress\_inv}}(\mathbf{x}) = \max \left(20, 100 - \text{work\_hours\_per\_week} \times 0.875 \right)$$

### 2.2 Standardized MAUT Aggregation Function
The overall multi-attribute utility $U_{\text{MAUT}}(\mathbf{x})$ is computed as the weighted sum of individual normalized utility functions:

$$U_{\text{MAUT}}(\mathbf{x}) = \sum_{i=1}^K w_i \cdot u_i(x_i), \quad \text{subject to } \sum_{i=1}^K w_i = 1.0, \quad w_i \ge 0$$

### 2.3 Analytic Hierarchy Process (AHP) Pairwise Weight Elicitation
To assist users in eliciting mathematically consistent attribute weights $w_i$, LifeTree implements the Saaty Analytic Hierarchy Process (AHP) Pairwise Comparison Matrix $\mathbf{A} = (a_{ij})_{n \times n}$, where $a_{ij}$ represents the relative importance of attribute $i$ over attribute $j$ on a scale of 1 to 9:

$$\mathbf{A} = \begin{bmatrix} 1 & a_{12} & \cdots & a_{1n} \\ 1/a_{12} & 1 & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ 1/a_{1n} & 1/a_{2n} & \cdots & 1 \end{bmatrix}$$

#### Eigenvector Computation ($\mathbf{A} w = \lambda_{\max} w$)
The principal priority weight vector $w$ is derived by solving the eigenvalue problem:

$$\mathbf{A} w = \lambda_{\max} w$$

#### Consistency Check ($\text{CR} < 0.10$)
To ensure the user's pairwise comparisons are not contradictory (e.g., $A > B$ and $B > C$ but $C > A$), the Consistency Index ($\text{CI}$) and Consistency Ratio ($\text{CR}$) are calculated:

$$\text{CI} = \frac{\lambda_{\max} - n}{n - 1}, \quad \text{CR} = \frac{\text{CI}}{\text{RI}_n}$$

Where $\text{RI}_n$ is the Random Index for $n$ attributes (for $n=6$, $\text{RI}_6 = 1.24$). If $\text{CR} < 0.10$, the weight matrix is verified as mathematically consistent. Executed via [maut_utility_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/decision_models/maut_utility_engine.py).

---

## 3. Kahneman-Tversky Prospect Theory & Loss Aversion

### 3.1 Empirical Background & Rationale
Classical Expected Utility Theory (EUT) assumes decision-makers are rational economic agents with risk-neutral or risk-averse utility functions. However, behavioral economics (Kahneman & Tversky, 1979) proves that humans evaluate outcomes as gains or losses relative to a subjective reference point, exhibiting severe **loss aversion** ($\text{Losses loom larger than gains}$) and non-linear **probability distortion**.

### 3.2 Asymmetric Value Function $v(x)$
LifeTree models psychological utility via the Kahneman-Tversky value function:

$$v(x) = \begin{cases} x^\alpha & \text{if } x \ge 0 \quad (\text{Gains}) \\ -\lambda (-x)^\beta & \text{if } x < 0 \quad (\text{Losses}) \end{cases}$$

#### Recommended Parameter Values & Justification:
- **Loss Aversion Multiplier $\lambda = 2.25$**: Empirical studies demonstrate that a loss of $\$10,000$ creates approximately $2.25$ times more psychological pain than the pleasure of gaining $\$10,000$.
- **Diminishing Sensitivity Exponents $\alpha = \beta = 0.88$**: Reflects diminishing marginal sensitivity for larger gains and losses.

### 3.3 Non-Linear Probability Weighting $w(p)$
Humans consistently overweight small tail-risk probabilities (e.g., $1\%$ probability of deportation or total bankruptcy) while underweighting moderate probabilities:

$$w(p) = \frac{p^\gamma}{\left(p^\gamma + (1-p)^\gamma\right)^{1/\gamma}}$$

Where $\gamma = 0.61$ is the empirical probability weighting parameter. Executed via [prospect_theory_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/decision_models/prospect_theory_engine.py).

---

## 4. Tail Risk Management: VaR vs. CVaR Expected Shortfall ($ES_{0.95}$)

### 4.1 Limitations of Traditional Value at Risk (VaR)
Standard 95% Value at Risk ($\text{VaR}_{0.95}$) measures the maximum threshold loss expected at a $95\%$ confidence level over a given horizon. However, VaR suffers from a fatal flaw: **it completely ignores the magnitude of losses beyond the 95th percentile cutoff**. In fat-tailed personal decisions, the tail losses can mean total financial bankruptcy or legal deportation.

### 4.2 Conditional Value at Risk ($\text{CVaR}_{0.95}$ / Expected Shortfall)
LifeTree extends Monte Carlo simulations to compute $\text{CVaR}_{0.95}$, defined as the expected conditional loss given that the loss exceeds the $\text{VaR}_{0.95}$ threshold:

$$\text{CVaR}_{\alpha}(X) = \mathbb{E} \left[ X \mid X \ge \text{VaR}_{\alpha}(X) \right] = \frac{1}{1 - \alpha} \int_{\alpha}^1 \text{VaR}_u(X) \, du$$

$$\text{Tail Severity Ratio} = \frac{\text{CVaR}_{0.95}}{\text{VaR}_{0.95}}$$

If $\text{Tail Severity Ratio} > 1.25$, LifeTree flags a **Fat-Tail Disaster Alert** warning the user of potential irreversible insolvency. Executed via [cvar_risk_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/decision_models/cvar_risk_engine.py).

---

## 5. Summary of Utility & Decision Engine Mapping

| Engine Component | Script Location | Theoretical Foundation | Input Parameters | Output Indicators |
| :--- | :--- | :--- | :--- | :--- |
| **MAUT Utility** | `maut_utility_engine.py` | Multi-Attribute Utility & AHP | 6 Life Attributes, Pairwise Matrix | MAUT Score (0-100), CR Ratio |
| **Prospect Theory** | `prospect_theory_engine.py` | Kahneman-Tversky CPT | Payoffs, Probabilities ($\lambda=2.25$) | CPT Score, Human vs Rational |
| **CVaR Expected Shortfall**| `cvar_risk_engine.py` | Extreme Value Tail Risk | Monte Carlo Costs ($\alpha=0.95$) | VaR_95, CVaR_95, Tail Ratio |
| **Influence Diagram** | `influence_diagram_layer.py` | Decision Analysis & Causal Maps| Knowledge Graph Nodes & Edges | Node Types ($\square, \bigcirc, \diamondsuit$), Causal Edges |
