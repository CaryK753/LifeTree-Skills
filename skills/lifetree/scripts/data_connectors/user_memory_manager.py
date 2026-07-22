#!/usr/bin/env python3
"""
LifeTree User Memory & Decision Journal Manager
Manages global shared user profile, background assets, explicit requirements, and decision journal history across all topics
"""

import sys
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

DEFAULT_MEMORY_FILE = "resources/user_global_memory_store.json"

def initialize_empty_memory(user_id: str = "usr_global_default") -> Dict[str, Any]:
    now_iso = datetime.now(timezone.utc).isoformat()
    return {
        "user_id": user_id,
        "created_at": now_iso,
        "last_updated": now_iso,
        "global_profile": {
            "demographics": {
                "age": 30,
                "nationality": "UNSPECIFIED",
                "current_residence": "UNSPECIFIED"
            },
            "education": {
                "highest_degree": "BACHELOR",
                "field_of_study": "GENERAL",
                "is_recognized": True
            },
            "languages": {
                "primary": "ENGLISH_C1",
                "secondary": "NONE"
            },
            "work_experience": {
                "years": 5,
                "current_role": "Professional",
                "industry_category": "GENERAL"
            },
            "financial_assets": {
                "liquid_funds_usd": 30000.0,
                "annual_income_usd": 50000.0,
                "risk_tolerance": "MODERATE"
            }
        },
        "explicit_requirements_and_goals": [
            {
                "goal_id": "goal_01",
                "title": "Achieve Global Mobility & Strategic Residency",
                "priority": "HIGH",
                "target_horizon_years": 3
            }
        ],
        "active_topics": [],
        "decision_journal": []
    }

def update_user_memory(current_memory: Dict[str, Any], profile_updates: Dict[str, Any] = None, new_decision: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Updates the shared user memory with profile updates and appends decisions to the Decision Journal.
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    updated_mem = dict(current_memory)
    updated_mem["last_updated"] = now_iso

    # Update Global Profile parameters
    if profile_updates:
        for section, values in profile_updates.items():
            if section in updated_mem["global_profile"] and isinstance(values, dict):
                updated_mem["global_profile"][section].update(values)
            else:
                updated_mem["global_profile"][section] = values

    # Append to Decision Journal
    if new_decision:
        journal = updated_mem.get("decision_journal", [])
        decision_entry = {
            "entry_id": f"dec_{len(journal) + 1}_{now_iso[:10]}",
            "timestamp": now_iso,
            "topic_id": new_decision.get("topic_id", "GENERAL"),
            "decision_title": new_decision.get("title", "User Decision"),
            "chosen_pathway": new_decision.get("chosen_pathway"),
            "user_rationale": new_decision.get("rationale"),
            "plan_b_status": new_decision.get("plan_b_status", "INACTIVE")
        }
        journal.append(decision_entry)
        updated_mem["decision_journal"] = journal

    return updated_mem

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            mem = json.load(f)
    else:
        mem = initialize_empty_memory()

    # Sample update
    updated = update_user_memory(
        mem,
        profile_updates={"languages": {"secondary": "GERMAN_B1"}},
        new_decision={
            "topic_id": "tpc_germany_immigration",
            "title": "Selected Opportunity Card Entry Route",
            "chosen_pathway": "Chancenkarte § 20a",
            "rationale": "Meets 6-point requirement with B1 German and C1 English.",
            "plan_b_status": "READY"
        }
    )

    print(json.dumps(updated, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
