#!/usr/bin/env python3
"""
LifeTree Cross-Topic Ripple Effect Calculator
Quantifies domino impacts across parallel user research topics
"""

import sys
import json
from typing import Dict, Any, List

def calculate_cross_topic_ripple(primary_topic_event: Dict[str, Any], active_topics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates how an event in a primary topic impacts parallel user topics.
    Example:
    - Primary Event: Capital commitment increase in Topic A (e.g., $20,000 regulatory deposit)
    - Active Parallel Topics: Topic B (Asset Allocation), Topic C (Career Pivot)
    - Computes financial liquidity drain, time shift, and risk escalation.
    """
    primary_id = primary_topic_event.get("topic_id", "TOPIC_PRIMARY")
    event_type = primary_topic_event.get("event_type", "CAPITAL_DRAIN") # CAPITAL_DRAIN, REGULATORY_DELAY, POLICY_SHIFT
    cost_delta = primary_topic_event.get("cost_delta", 0.0)
    time_delay_months = primary_topic_event.get("time_delay_months", 0)

    impacts = []

    for topic in active_topics:
        t_id = topic.get("topic_id")
        if t_id == primary_id:
            continue

        t_name = topic.get("title", t_id)
        t_category = topic.get("category", "GENERAL")

        ripple_severity = "LOW"
        notes = []

        if event_type == "CAPITAL_DRAIN" and cost_delta > 0:
            if t_category in ["ASSET_ALLOCATION", "INVESTMENT", "REAL_ESTATE"]:
                ripple_severity = "HIGH" if cost_delta > 10000 else "MEDIUM"
                notes.append(f"Reduces available liquid reserves for '{t_name}' by ${cost_delta:,.2f}.")
            elif t_category in ["EDUCATION", "CAREER"]:
                ripple_severity = "MEDIUM"
                notes.append(f"May constrain discretionary budget for training/tuition in '{t_name}'.")

        if time_delay_months > 0:
            if t_category in ["IMMIGRATION", "CAREER", "BUSINESS"]:
                ripple_severity = "HIGH" if time_delay_months >= 6 else "MEDIUM"
                notes.append(f"Pushes back key target execution timeline in '{t_name}' by {time_delay_months} months.")

        impacts.append({
            "target_topic_id": t_id,
            "target_topic_name": t_name,
            "category": t_category,
            "ripple_severity": ripple_severity,
            "impact_summary": "; ".join(notes) if notes else "No significant direct friction detected."
        })

    return {
        "primary_event": primary_topic_event,
        "active_topics_count": len(active_topics),
        "ripple_impacts": impacts,
        "system_recommendation": "Rebalance local portfolio or adjust timeline markers for impacted topics."
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            primary = data.get("primary_event", {})
            active = data.get("active_topics", [])
    else:
        primary = {
            "topic_id": "tpc_immigration_path",
            "event_type": "CAPITAL_DRAIN",
            "cost_delta": 15000.0,
            "time_delay_months": 3
        }
        active = [
            {"topic_id": "tpc_immigration_path", "title": "Global Mobility", "category": "IMMIGRATION"},
            {"topic_id": "tpc_investment", "title": "Portfolio Growth", "category": "ASSET_ALLOCATION"},
            {"topic_id": "tpc_career", "title": "Senior Tech Role Transition", "category": "CAREER"}
        ]

    res = calculate_cross_topic_ripple(primary, active)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
