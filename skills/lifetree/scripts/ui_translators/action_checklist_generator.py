#!/usr/bin/env python3
"""
LifeTree Immediate Action Checklist Generator
Converts decision paths and top ROI recommendations into an actionable Weekly To-Do Checklist.
"""

import sys
import json
from typing import Dict, Any, List

def generate_action_checklist(path_nodes: List[Dict[str, Any]], top_roi_action: str) -> Dict[str, Any]:
    """
    Generates a prioritized Weekly Action Checklist for the user.
    """
    checklist = [
        {
            "priority": "HIGH",
            "task_title": "Top ROI Personal Action",
            "action_details": top_roi_action,
            "target_deadline": "Within 7 Days",
            "status": "PENDING"
        }
    ]

    for node in path_nodes:
        etype = node.get("entity_type", "").upper()
        label = node.get("label", "Task Step")
        if etype == "CAPITAL_ASSET":
            checklist.append({
                "priority": "HIGH",
                "task_title": f"Fund Statutory Capital ({label})",
                "action_details": f"Open statutory account and deposit funds for '{label}'.",
                "target_deadline": "Within 14 Days",
                "status": "PENDING"
            })
        elif etype == "INSTITUTION_AGENCY":
            checklist.append({
                "priority": "MEDIUM",
                "task_title": f"Book Appointment at {label}",
                "action_details": f"Schedule document submission appointment with {label}.",
                "target_deadline": "Within 30 Days",
                "status": "PENDING"
            })

    return {
        "checklist_summary": {
            "total_action_items": len(checklist),
            "high_priority_count": sum(1 for c in checklist if c["priority"] == "HIGH")
        },
        "weekly_action_checklist": checklist
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            nodes = data.get("nodes", [])
            top_act = data.get("top_roi_action", "Upgrade German Language Level")
    else:
        nodes = [
            {"label": "€12,000 Blocked Account", "entity_type": "CAPITAL_ASSET"},
            {"label": "German Federal Embassy", "entity_type": "INSTITUTION_AGENCY"}
        ]
        top_act = "Upgrade German from A2 to B1"

    res = generate_action_checklist(nodes, top_act)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
