#!/usr/bin/env python3
"""
LifeTree Human Language Translator & Cognitive Friction Reducer
Translates raw mathematical metrics (Dijkstra friction 4.22, Monte Carlo P90 31.8m, VaR $18,508)
into clear, encouraging, plain human executive summaries.
"""

import sys
import json
from typing import Dict, Any

def translate_metrics_to_human_language(raw_engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates mathematical outputs into clear human language:
    - Friction Cost -> Execution Difficulty Rating
    - Monte Carlo P50/P90 -> Target Timeline & Pessimistic Buffer
    - VaR 95% -> Maximum Liquidity Reserve Needed
    """
    mc_results = raw_engine_outputs.get("monte_carlo_results", {})
    path_results = raw_engine_outputs.get("dijkstra_optimal_causal_path", {})

    # 1. Translate Friction Cost
    friction_cost = path_results.get("pathfinding_summary", {}).get("total_path_friction_cost", 3.0)
    difficulty_label = "EASY & DIRECT" if friction_cost < 3.0 else ("MODERATE FRICTION" if friction_cost < 6.0 else "HIGH COMPLEXITY")
    difficulty_explanation = "This route has clear statutory guidelines with minimal bureaucratic friction." if friction_cost < 3.0 else "Requires careful scheduling (embassy interview & statutory deposit)."

    # 2. Translate Monte Carlo Timelines & Costs
    p50_time = mc_results.get("execution_timeline_months", {}).get("P50_median", 24)
    p90_time = mc_results.get("execution_timeline_months", {}).get("P90_pessimistic", 32)
    var_cost = mc_results.get("financial_capital_usd", {}).get("VaR_95_max_cost", 18500.0)

    human_summary = (
        f"🎯 Expected Completion: ~{int(p50_time)} months (most likely scenario).\n"
        f"🛡️ Safety Buffer Timeline: Plan for up to {int(p90_time)} months in case of processing backlogs.\n"
        f"💰 Recommended Financial Buffer: Prepare ${var_cost:,.0f} liquid capital to comfortably cover all statutory deposits and emergency contingencies."
    )

    return {
        "human_readable_summary": human_summary,
        "executive_verdict": {
            "execution_difficulty": difficulty_label,
            "explanation": difficulty_explanation,
            "recommended_target_timeline_months": p50_time,
            "recommended_total_budget_usd": var_cost
        }
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            raw = json.load(f)
    else:
        raw = {
            "dijkstra_optimal_causal_path": {"pathfinding_summary": {"total_path_friction_cost": 4.22}},
            "monte_carlo_results": {
                "execution_timeline_months": {"P50_median": 24.1, "P90_pessimistic": 31.8},
                "financial_capital_usd": {"VaR_95_max_cost": 18508.22}
            }
        }

    res = translate_metrics_to_human_language(raw)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
