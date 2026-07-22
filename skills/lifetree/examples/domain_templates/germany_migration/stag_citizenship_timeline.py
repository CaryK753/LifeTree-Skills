#!/usr/bin/env python3
"""
German Citizenship & PR Timeline Projector under 2024 Revised StAG Law
Part of LifeTree Decision Intelligence System MVP
"""

import sys
import json
from typing import Dict, Any, List

def calculate_citizenship_timeline(profile: Dict[str, Any]) -> Dict[str, Any]:
    years_in_germany = profile.get("years_in_germany", 0.0)
    pension_months_paid = profile.get("pension_months_paid", 0)
    german_level = profile.get("german_level", "A1").upper() # A1, A2, B1, B2, C1, C2
    permit_type = profile.get("current_permit_type", "BLUE_CARD") # BLUE_CARD, SKILLED_WORKER, CHANCENKARTE
    special_achievements = profile.get("special_achievements", False) # C1 + exceptional professional/academic integration
    wants_dual_citizenship = profile.get("wants_dual_citizenship", True)

    milestones: List[Dict[str, Any]] = []

    # 1. Permanent Residence (Niederlassungserlaubnis)
    pr_months_needed = 60
    pr_german_needed = "B1"
    
    if permit_type == "BLUE_CARD":
        if german_level in ["B1", "B2", "C1", "C2"]:
            pr_months_needed = 21
            pr_german_needed = "B1"
        else:
            pr_months_needed = 27
            pr_german_needed = "A1"
    elif permit_type == "SKILLED_WORKER":
        if german_level in ["B1", "B2", "C1", "C2"]:
            pr_months_needed = 36
        else:
            pr_months_needed = 48

    pr_eligible = (pension_months_paid >= pr_months_needed)
    months_remaining_for_pr = max(0, pr_months_needed - pension_months_paid)

    milestones.append({
        "milestone": "Niederlassungserlaubnis (Permanent Residency)",
        "legal_basis": "AufenthG § 18g / § 9",
        "pension_months_required": pr_months_needed,
        "pension_months_current": pension_months_paid,
        "required_german_level": pr_german_needed,
        "months_remaining": months_remaining_for_pr,
        "status": "ACHIEVED" if pr_eligible else "IN_PROGRESS"
    })

    # 2. Naturalization (Einbürgerung under 2024 StAG § 10)
    required_years_citizenship = 5.0
    is_fast_track = False
    
    if german_level in ["C1", "C2"] and special_achievements:
        required_years_citizenship = 3.0
        is_fast_track = True

    years_remaining_citizenship = max(0.0, required_years_citizenship - years_in_germany)
    citizenship_eligible = (years_in_germany >= required_years_citizenship) and (german_level in ["B1", "B2", "C1", "C2"])

    milestones.append({
        "milestone": "Einbürgerung (German Citizenship)",
        "legal_basis": "StAG § 10 (2024 Reform)",
        "required_residence_years": required_years_citizenship,
        "current_residence_years": years_in_germany,
        "is_fast_track_3yr": is_fast_track,
        "dual_citizenship_allowed": True,
        "years_remaining": round(years_remaining_citizenship, 2),
        "status": "ACHIEVED" if citizenship_eligible else "IN_PROGRESS"
    })

    return {
        "profile_summary": profile,
        "2024_stag_law_highlights": {
            "dual_citizenship_retained": "YES (No requirement to renounce origin nationality)",
            "standard_residence_requirement": "5 years (reduced from 8 years)",
            "accelerated_residence_requirement": "3 years (requires German C1 + special achievements)"
        },
        "milestones": milestones,
        "actionable_plan_b": [
            "Maintain continuous statutory pension contributions without interruption.",
            "Upgrade German language level to C1 to unlock 3-year fast-track citizenship clause." if german_level not in ["C1", "C2"] else "German C1 requirement fulfilled!"
        ]
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            "years_in_germany": 2.0,
            "pension_months_paid": 22,
            "german_level": "B1",
            "current_permit_type": "BLUE_CARD",
            "special_achievements": False,
            "wants_dual_citizenship": True
        }
    
    res = calculate_citizenship_timeline(data)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
