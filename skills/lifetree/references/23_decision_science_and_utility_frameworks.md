# 23. Decision Science & Behavioral Utility Modeling Architecture

## 1. Executive Summary
To bridge the paradigm gap between generic numerical graph algorithms and high-stakes personal decision science, LifeTree integrates 6 advanced mathematical decision frameworks:

---

## 2. Prospect Theory & Behavioral Loss Aversion ($v(x)$)
Human personal decision-makers do not maximize linear monetary values; they experience asymmetric subjective utility under loss aversion (Kahneman & Tversky):

$$v(x) = \begin{cases} x^\alpha & \text{if } x \ge 0 \\ -\lambda (-x)^\beta & \text{if } x < 0 \end{cases}$$

Where $\lambda = 2.25$ is the empirical Loss Aversion Coefficient, and $\alpha = \beta = 0.88$.

Probability weighting $w(p)$ overweights small tail probabilities while underweighting moderate probabilities:

$$w(p) = \frac{p^\gamma}{\left(p^\gamma + (1-p)^\gamma\right)^{1/\gamma}}$$

Executed via [utility_theory_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/decision_analysis/utility_theory_engine.py).

---

## 3. Multi-Attribute Utility Theory (MAUT)
Personal choices evaluate multi-dimensional non-monetary attributes (Income, Health, Time Freedom, Family Security, Inverted Stress):

$$U_{\text{MAUT}}(\mathbf{x}) = \sum_{i=1}^K w_i \cdot u_i(x_i), \quad \sum_{i=1}^K w_i = 1.0$$

---

## 4. Tail Risk CVaR & Copula Dependency
Conditional Value at Risk (CVaR / Expected Shortfall) measures average tail loss severity beyond the $\text{VaR}_{0.95}$ threshold:

$$\text{CVaR}_{0.95}(K) = \mathbb{E}\left[ K \mid K \ge \text{VaR}_{0.95}(K) \right]$$

Correlated systemic risk cascades (macro downturn $\rightarrow$ income drop $\rightarrow$ currency depreciation) are modeled using Gaussian Copulas:

$$\mathbf{Z} = \mathbf{L} \cdot \mathbf{\epsilon}, \quad \mathbf{\Sigma} = \mathbf{L} \mathbf{L}^T$$

Executed via [tail_risk_cvar_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/simulation_engines/tail_risk_cvar_engine.py).

---

## 5. Influence Diagram Decision Framework
Replaces passive fact-retrieval graphs with explicit Decision Nodes ($\square$), Chance Nodes ($\bigcirc$), and Value Nodes ($\diamondsuit$), executing backward induction over expected utilities:

$$\text{EU}(d_j) = \sum_{s \in S} P(s \mid d_j) \cdot U(d_j, s)$$

$$\text{Policy}^* = \arg\max_{d_j} \text{EU}(d_j)$$

Executed via [influence_diagram_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/graph_engines/influence_diagram_engine.py).

---

## 6. Recursive Bayesian Belief Updating & Dempster-Shafer Intervals
Updates posterior belief $P(H \mid E)$ upon observing statutory or market evidence $E$:

$$P(H \mid E) = \frac{P(E \mid H) P(H)}{P(E \mid H) P(H) + P(E \mid \neg H) P(\neg H)}$$

Dempster-Shafer evidence theory establishes upper/lower belief bounds $[\text{Bel}(A), \text{Pl}(A)]$. Executed via [bayesian_belief_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/decision_analysis/bayesian_belief_engine.py).

---

## 7. Optimal Stopping & Hyperbolic Discounting
- **37% Optimal Stopping Rule (Snell Envelope)**: Computes optimal timing threshold $k^* = \lfloor n / e \rfloor$ for career pivots or asset liquidations.
- **Hyperbolic Time Discounting**: Models human present bias $U(t) = \frac{V}{1 + k \cdot t}$. Executed via [optimal_stopping_engine.py](file:///Users/cary/Desktop/Fun/LifeTree/.agent/skills/lifetree/scripts/simulation_engines/optimal_stopping_engine.py).
