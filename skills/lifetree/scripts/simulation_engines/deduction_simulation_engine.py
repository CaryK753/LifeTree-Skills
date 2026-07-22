#!/usr/bin/env python3
"""
LifeTree Multi-Step Temporal Deduction & Simulation Engine
Simulates multi-year decision pathways, step-by-step state transitions, path probabilities, and UI control contracts.
"""

import sys
import json
from typing import Dict, Any, List

def run_temporal_deduction(user_profile: Dict[str, Any], simulation_timeline_years: int = 5, hypothetical_shocks: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executes a multi-step temporal deduction over N years.
    Simulates year-by-year state transitions, probability curves, constraint propagation, and Plan B triggers.
    """
    if hypothetical_shocks is None:
        hypothetical_shocks = []

    shock_map = {s.get("year", 1): s for s in hypothetical_shocks}

    timeline_steps = []
    current_state = dict(user_profile)
    accumulated_risk_score = 0.0

    for year in range(1, simulation_timeline_years + 1):
        step_events = []
        state_changes = {}
        path_probability = max(0.1, 0.95 - (year * 0.08)) # Baseline probability decay over time

        # Apply hypothetical shocks for this year
        if year in shock_map:
            shock = shock_map[year]
            shock_name = shock.get("name", "Unforeseen Event")
            shock_impact = shock.get("impact", "NEUTRAL")
            step_events.append(f"HYPOTHETICAL SHOCK: {shock_name} ({shock_impact})")
            
            if shock_impact == "NEGATIVE":
                accumulated_risk_score += 2.5
                path_probability *= 0.7
                state_changes["risk_alert"] = f"Plan B side bud activated for {shock_name}!"
            elif shock_impact == "POSITIVE":
                path_probability = min(0.99, path_probability * 1.2)

        # Standard Milestone Progression
        if year == 1:
            step_events.append("Entry & Compliance Verification completed.")
        elif year == 3:
            step_events.append("3-Year Accelerated Milestone Reached (Fast-track criteria check).")
        elif year == 5:
            step_events.append("5-Year Permanent Status Milestone Reached.")

        timeline_steps.append({
            "year": year,
            "simulated_date_offset": f"+{year}Y",
            "path_success_probability": round(path_probability, 2),
            "accumulated_risk_score": round(accumulated_risk_score, 1),
            "step_events": step_events,
            "state_snapshot": dict(current_state, **state_changes),
            "ui_step_contract": {
                "step_number": year,
                "label": f"Year {year} Milestone",
                "status": "STABLE" if accumulated_risk_score < 3.0 else "WARNING",
                "recommended_ui_badge": "OPTIMAL_PROGRESSION" if path_probability >= 0.7 else "PLAN_B_ACTIVATED"
            }
        })

    return {
        "deduction_summary": {
            "simulation_horizon_years": simulation_timeline_years,
            "applied_shocks_count": len(hypothetical_shocks),
            "final_path_probability": timeline_steps[-1]["path_success_probability"],
            "overall_risk_level": "LOW" if accumulated_risk_score < 3.0 else ("MEDIUM" if accumulated_risk_score < 6.0 else "HIGH"),
            "plan_b_triggered": accumulated_risk_score >= 3.0
        },
        "timeline_steps": timeline_steps
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            prof = data.get("profile", {})
            horizon = data.get("years", 5)
            shocks = data.get("shocks", [])
    else:
        prof = {"user_id": "usr_sim_01", "current_age": 30, "liquid_funds_usd": 40000.0}
        horizon = 5
        shocks = [
            {"year": 2, "name": "Global CPI Inflation Surge (+10%)", "impact": "NEGATIVE"},
            {"year": 4, "name": "Language C1 Certification Attained", "impact": "POSITIVE"}
        ]

    res = run_temporal_deduction(prof, horizon, shocks)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
