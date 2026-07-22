# Advanced Mathematical Algorithms: Monte Carlo, Sensitivity ROI & Game Theory

> [!IMPORTANT]
> **STRICT CODE-DRIVEN MATHEMATICAL ENGINE POLICY**:
> All probabilistic simulations, Value at Risk (VaR) distributions, sensitivity elasticities, and game-theoretic compromises MUST be computed exclusively via Python script execution (`scripts/`). The AI Agent MUST NEVER guess or manually calculate numbers via LLM text generation!

---

## 1. Monte Carlo Stochastic Simulation & Tail Risk Engine (`scripts/monte_carlo_decision_engine.py`)
Rather than relying on static point estimates, LifeTree runs 10,000 stochastic simulation trials over decision pathways:
- **Stochastic Time Delays**: Truncated Gaussian noise model simulating processing backlogs and embassy delays.
- **Stochastic Cost Inflation**: Lognormal distribution model simulating currency fluctuations and statutory deposit hikes.
- **Outcome Metrics**: Computes P10 (optimistic), P50 (median), P90 (pessimistic) confidence intervals, 95% Value at Risk (VaR), and tail risk warnings.

---

## 2. Parameter Sensitivity & Personal ROI Elasticity (`scripts/graph_sensitivity_engine.py`)
Calculates the partial derivative elasticity $\frac{\partial \text{Probability}}{\partial \text{Variable}}$ across user profile parameters:
- Ranks personal actions by Return on Investment (ROI).
- Identifies the single personal parameter change (e.g. language level vs capital deposit) that produces the maximum marginal gain in pathway success.

---

## 3. Game-Theoretic Stakeholder Conflict Solver (`scripts/game_theory_stakeholder_solver.py`)
Analyzes competing regulatory requirements between multi-stakeholder entities (Host Immigration Board vs Origin Tax Board vs Employer):
- Detects physical presence vs worldwide tax residency traps.
- Calculates Pareto-optimal compromise pathways (e.g. DTA Article 4 tie-breaker rules) to achieve non-conflicting compliance.
