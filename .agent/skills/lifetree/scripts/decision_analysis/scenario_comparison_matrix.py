#!/usr/bin/env python3
"""
LifeTree Multi-Pathway Trade-Off & Comparison Matrix Generator
Renders side-by-side comparative matrices across candidate decision pathways
"""

import sys
import json
from typing import Dict, Any, List

def generate_comparison_matrix(pathway_options: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compares candidate pathways side-by-side across key decision dimensions:
    - Financial Capital Commitment (USD/EUR)
    - Execution Horizon (Months to Goal)
    - Risk & Rejection Level
    - Prerequisite Friction (Language/Qualification)
    - Plan B Hedge Score (0-100)
    """
    matrix_rows = []
    winner_score = -1.0
    top_recommended = None

    for opt in pathway_options:
        p_name = opt.get("name", "Unnamed Pathway")
        cost = opt.get("financial_cost_usd", 0.0)
        horizon_months = opt.get("horizon_months", 12)
        risk_level = opt.get("risk_level", "MEDIUM").upper()
        prereq_friction = opt.get("prereq_friction_level", "MEDIUM").upper()
        plan_b_reliability = opt.get("plan_b_reliability_score", 70.0)

        # Calculate Composite Trade-Off Index (0 to 100, higher is better)
        risk_penalty = {"LOW": 0, "MEDIUM": 15, "HIGH": 35, "CRITICAL": 60}.get(risk_level, 20)
        friction_penalty = {"LOW": 0, "MEDIUM": 10, "HIGH": 25}.get(prereq_friction, 10)
        horizon_penalty = min(30.0, horizon_months * 0.5)

        composite_score = round(max(0.0, 100.0 - risk_penalty - friction_penalty - horizon_penalty + (plan_b_reliability * 0.2)), 1)

        if composite_score > winner_score:
            winner_score = composite_score
            top_recommended = p_name

        matrix_rows.append({
            "pathway_name": p_name,
            "financial_cost_usd": cost,
            "horizon_months": horizon_months,
            "risk_level": risk_level,
            "prerequisite_friction": prereq_friction,
            "plan_b_reliability_score": plan_b_reliability,
            "composite_tradeoff_score": composite_score
        })

    return {
        "comparison_summary": {
            "pathways_compared_count": len(pathway_options),
            "top_recommended_pathway": top_recommended,
            "highest_composite_score": winner_score
        },
        "comparison_matrix": matrix_rows,
        "recommendation": f"Pathway '{top_recommended}' offers the optimal balance of risk, execution time, and Plan B reliability."
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            opts = json.load(f)
    else:
        opts = [
            {
                "name": "Option A: German Chancenkarte -> EU Blue Card",
                "financial_cost_usd": 14000.0,
                "horizon_months": 24,
                "risk_level": "LOW",
                "prereq_friction_level": "MEDIUM",
                "plan_b_reliability_score": 90.0
            },
            {
                "name": "Option B: Canada Express Entry Direct PR",
                "financial_cost_usd": 18000.0,
                "horizon_months": 18,
                "risk_level": "MEDIUM",
                "prereq_friction_level": "HIGH",
                "plan_b_reliability_score": 75.0
            },
            {
                "name": "Option C: Caribbean Golden Visa",
                "financial_cost_usd": 150000.0,
                "horizon_months": 6,
                "risk_level": "LOW",
                "prereq_friction_level": "LOW",
                "plan_b_reliability_score": 85.0
            }
        ]

    res = generate_comparison_matrix(opts)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
