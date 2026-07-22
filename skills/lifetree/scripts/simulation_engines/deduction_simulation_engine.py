#!/usr/bin/env python3
"""
LifeTree Multi-Branch Temporal Deduction & Simulation Engine
Simulates multi-year future state trajectories across competing decision branches (Choice A vs Choice B),
calculating annual probability curves, capital accumulation, risk exposure, and Plan B triggers.
"""

import sys
import json
from typing import Dict, Any, List

def run_temporal_deduction(user_profile: Dict[str, Any], simulation_timeline_years: int = 5, hypothetical_shocks: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executes multi-step temporal deduction over 1-10 years.
    Returns year-by-year trajectory for Choice A (Chancenkarte -> Blue Card) vs Choice B (Direct Employer Sponsorship).
    """
    shocks = hypothetical_shocks or []
    
    # Base parameters
    initial_funds = user_profile.get("financial_assets", {}).get("liquid_funds_usd", 40000.0)
    current_de = user_profile.get("languages", {}).get("secondary", "A2")

    pathway_a_steps = []
    pathway_b_steps = []

    prob_a = 0.85
    prob_b = 0.70
    funds_a = initial_funds
    funds_b = initial_funds

    for yr in range(1, simulation_timeline_years + 1):
        # 1. Check for year shocks
        yr_shocks = [s for s in shocks if s.get("year") == yr]
        yr_events_a = [f"Year {yr} Standard Progression"]
        yr_events_b = [f"Year {yr} Direct Employment Progression"]

        for s in yr_shocks:
            s_name = s.get("name", "Macro Event")
            s_impact = s.get("impact", "NEGATIVE")
            yr_events_a.append(f"SHOCK: {s_name} ({s_impact})")
            yr_events_b.append(f"SHOCK: {s_name} ({s_impact})")
            if s_impact == "NEGATIVE":
                prob_a = max(0.20, prob_a - 0.12)
                prob_b = max(0.10, prob_b - 0.20)
                funds_a -= 2000.0
                funds_b -= 4000.0

        # State updates
        if yr == 1:
            funds_a -= 14000.0 # Sperrkonto deposit
            funds_b -= 5000.0  # Relocation
        elif yr == 2:
            prob_a = min(0.95, prob_a + 0.05) # Transition to Blue Card
            funds_a += 20000.0 # Salary income
            funds_b += 25000.0
        elif yr == 3:
            if current_de == "B1" or yr >= 3:
                prob_a = 0.98 # PR eligibility
                yr_events_a.append("Statutory Settlement PR (§ 18g) Unlocked!")
            prob_b = min(0.92, prob_b + 0.10)
            funds_a += 30000.0
            funds_b += 35000.0

        plan_b_active_a = prob_a < 0.60
        plan_b_active_b = prob_b < 0.60

        pathway_a_steps.append({
            "year": yr,
            "success_probability": round(prob_a, 2),
            "capital_balance_usd": round(funds_a, 2),
            "events": yr_events_a,
            "plan_b_active": plan_b_active_a,
            "badge": "PLAN_B_ACTIVATED" if plan_b_active_a else ("PR_ELIGIBLE" if prob_a >= 0.95 else "OPTIMAL_PROGRESSION")
        })

        pathway_b_steps.append({
            "year": yr,
            "success_probability": round(prob_b, 2),
            "capital_balance_usd": round(funds_b, 2),
            "events": yr_events_b,
            "plan_b_active": plan_b_active_b,
            "badge": "PLAN_B_ACTIVATED" if plan_b_active_b else ("PR_ELIGIBLE" if prob_b >= 0.95 else "HIGH_FRICTION_PROGRESSION")
        })

    return {
        "deduction_summary": {
            "timeline_horizon_years": simulation_timeline_years,
            "final_year_prob_pathway_a": pathway_a_steps[-1]["success_probability"],
            "final_year_prob_pathway_b": pathway_b_steps[-1]["success_probability"],
            "recommended_branch": "Pathway A (Chancenkarte -> Blue Card)" if pathway_a_steps[-1]["success_probability"] >= pathway_b_steps[-1]["success_probability"] else "Pathway B"
        },
        "pathway_a_trajectory": pathway_a_steps,
        "pathway_b_trajectory": pathway_b_steps
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            prof = data.get("profile", {})
            yrs = data.get("years", 5)
            shocks = data.get("shocks", [])
    else:
        prof = {"financial_assets": {"liquid_funds_usd": 40000.0}, "languages": {"secondary": "A2"}}
        yrs = 5
        shocks = [{"year": 2, "name": "Statutory Sperrkonto Increase", "impact": "NEGATIVE"}]

    res = run_temporal_deduction(prof, yrs, shocks)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
