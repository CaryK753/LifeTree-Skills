# Multi-Pathway Comparison & Regret Minimization Framework

## 1. Multi-Pathway Trade-Off Matrix (`scripts/scenario_comparison_matrix.py`)
When evaluating multiple viable options (e.g. Option A: Germany Blue Card vs Option B: Canada Express Entry vs Option C: Golden Visa), the agent constructs a side-by-side comparison matrix (`resources/scenario_comparison_schema.json`):
- **Financial Commitment (USD)**: Capital required for deposits, fees, and liquid reserves.
- **Execution Horizon**: Time (in months) required to reach permanent residency or strategic target.
- **Risk Score**: Rejection probability & legislative volatility penalty.
- **Composite Trade-Off Index (0-100)**: Unified score determining the recommended optimal path.

## 2. Decision Journal Retrospective & Regret Minimization Audit (`scripts/decision_journal_auditor.py`)
Applies Jeff Bezos's **Regret Minimization Framework** to historical decision entries:
- Evaluates decision stability and strategic pivot frequency.
- Computes **Regret Minimization Index (0-100)**: Assesses whether choices align with long-term 80-year-old self perspective.
- Verifies that every strategic pivot maintains an active Plan B reserve to prevent downside risk.
