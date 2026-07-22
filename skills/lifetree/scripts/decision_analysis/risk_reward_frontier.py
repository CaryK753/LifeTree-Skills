#!/usr/bin/env python3
"""
LifeTree Pareto Risk-Reward Frontier Calculator
Computes Pareto Efficiency Frontier across candidate decision pathways, isolating non-dominated optimal options.
"""

import sys
import json
from typing import Dict, Any, List

def calculate_pareto_frontier(candidate_pathways: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Identifies Pareto-efficient pathways.
    Objectives:
    1. Maximize Success Probability (Reward)
    2. Minimize Execution Friction/Cost (Risk & Capital)
    A pathway A dominates pathway B if A is no worse than B in all objectives and strictly better in at least one.
    """
    pareto_frontier = []
    dominated_pathways = []

    for i, p1 in enumerate(candidate_pathways):
        reward_1 = p1.get("success_prob", 0.5)
        cost_1 = p1.get("cost_usd", 10000.0)
        time_1 = p1.get("time_months", 12)

        is_dominated = False
        for j, p2 in enumerate(candidate_pathways):
            if i == j:
                continue
            reward_2 = p2.get("success_prob", 0.5)
            cost_2 = p2.get("cost_usd", 10000.0)
            time_2 = p2.get("time_months", 12)

            # Check if p2 dominates p1
            if (reward_2 >= reward_1 and cost_2 <= cost_1 and time_2 <= time_1) and \
               (reward_2 > reward_1 or cost_2 < cost_1 or time_2 < time_1):
                is_dominated = True
                break

        if is_dominated:
            dominated_pathways.append(p1.get("name"))
        else:
            pareto_frontier.append(p1)

    return {
        "frontier_summary": {
            "total_pathways_analyzed": len(candidate_pathways),
            "pareto_efficient_count": len(pareto_frontier),
            "dominated_count": len(dominated_pathways)
        },
        "pareto_frontier_pathways": pareto_frontier,
        "dominated_pathways": dominated_pathways
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            candidates = json.load(f)
    else:
        candidates = [
            {"name": "Option A (Chancenkarte)", "success_prob": 0.88, "cost_usd": 14000.0, "time_months": 24},
            {"name": "Option B (Direct Job Offer)", "success_prob": 0.92, "cost_usd": 8000.0, "time_months": 12},
            {"name": "Option C (High Cost Low Prob)", "success_prob": 0.70, "cost_usd": 25000.0, "time_months": 36}
        ]

    res = calculate_pareto_frontier(candidates)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
