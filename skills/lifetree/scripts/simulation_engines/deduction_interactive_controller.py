#!/usr/bin/env python3
"""
LifeTree Deduction Mode Interactive Scenario Controller
Handles dynamic user actions (year seeking, shock injection, Plan B toggling) and emits instant delta diffs.
"""

import sys
import json
from typing import Dict, Any, List

def apply_deduction_action(current_timeline: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applies an interactive user action to the deduction timeline:
    Action types:
    - "SEEK_YEAR": Seeks to year N milestone (+1Y, +2Y, +5Y)
    - "INJECT_SHOCK": Injects a hypothetical event into year N
    - "TOGGLE_PLAN_B": Forces Plan B activation/deactivation
    """
    action_type = action.get("action_type", "SEEK_YEAR").upper()
    target_year = action.get("target_year", 1)

    steps = current_timeline.get("timeline_steps", [])
    selected_step = next((s for s in steps if s.get("year") == target_year), None)

    delta_changes = []

    if action_type == "SEEK_YEAR":
        delta_changes.append(f"Seek timeline to Year {target_year} Milestone.")

    elif action_type == "INJECT_SHOCK":
        shock_name = action.get("shock_name", "User Shock Event")
        severity = action.get("severity", "MEDIUM").upper()
        if selected_step:
            selected_step["step_events"].append(f"MANUAL INJECTION: {shock_name} ({severity})")
            if severity == "HIGH":
                selected_step["path_success_probability"] = round(max(0.05, selected_step["path_success_probability"] * 0.75), 2)
                selected_step["accumulated_risk_score"] += 3.0
                selected_step["ui_step_contract"]["recommended_ui_badge"] = "PLAN_B_ACTIVATED"
            delta_changes.append(f"Injected shock '{shock_name}' into Year {target_year}.")

    elif action_type == "TOGGLE_PLAN_B":
        force_active = action.get("activate", True)
        if selected_step:
            selected_step["ui_step_contract"]["recommended_ui_badge"] = "PLAN_B_ACTIVATED" if force_active else "OPTIMAL_PROGRESSION"
            delta_changes.append(f"Plan B status toggled to {'ACTIVE' if force_active else 'INACTIVE'} for Year {target_year}.")

    return {
        "controller_status": "ACTION_APPLIED",
        "action_executed": action,
        "delta_changes": delta_changes,
        "active_year_step": selected_step,
        "updated_timeline": current_timeline
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            tl = data.get("timeline", {})
            act = data.get("action", {})
    else:
        tl = {
            "timeline_steps": [
                {"year": 1, "path_success_probability": 0.85, "accumulated_risk_score": 0.0, "step_events": ["Started"], "ui_step_contract": {"recommended_ui_badge": "OPTIMAL_PROGRESSION"}},
                {"year": 2, "path_success_probability": 0.75, "accumulated_risk_score": 1.0, "step_events": ["In Progress"], "ui_step_contract": {"recommended_ui_badge": "OPTIMAL_PROGRESSION"}}
            ]
        }
        act = {"action_type": "INJECT_SHOCK", "target_year": 2, "shock_name": "Sudden Income Tax Increase", "severity": "HIGH"}

    res = apply_deduction_action(tl, act)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
