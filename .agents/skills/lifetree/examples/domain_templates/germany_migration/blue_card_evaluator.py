#!/usr/bin/env python3
"""
EU Blue Card (Blaue Karte EU) Evaluator for Germany (2024/2025 Revised Rules)
Part of LifeTree Decision Intelligence System MVP
"""

import sys
import json
from typing import Dict, Any

STANDARD_SALARY_THRESHOLD_2024 = 45300.0   # Standard EU Blue Card minimum annual gross salary
SHORTAGE_SALARY_THRESHOLD_2024 = 41041.0   # Shortage occupations & IT specialists minimum annual gross salary

SHORTAGE_OCCUPATION_GROUPS = [
    "IT_SOFTWARE_ENGINEERING",
    "MATHEMATICS",
    "NATURAL_SCIENCES",
    "ENGINEERING",
    "HUMAN_MEDICINE",
    "TEACHING"
]

def evaluate_blue_card_eligibility(job_offer: Dict[str, Any]) -> Dict[str, Any]:
    annual_gross_salary = job_offer.get("annual_gross_salary_eur", 0.0)
    occupation_category = job_offer.get("occupation_category", "OTHER").upper()
    has_university_degree = job_offer.get("has_recognized_university_degree", False)
    it_experience_years = job_offer.get("it_experience_years", 0)
    qualification_matches_role = job_offer.get("qualification_matches_role", True)

    is_shortage = occupation_category in SHORTAGE_OCCUPATION_GROUPS
    required_salary = SHORTAGE_SALARY_THRESHOLD_2024 if is_shortage else STANDARD_SALARY_THRESHOLD_2024

    salary_met = annual_gross_salary >= required_salary

    # Degree / Qualification Check (2024 reform allows 3 years IT experience in lieu of degree for IT roles)
    qualification_ok = False
    qual_reason = ""
    if has_university_degree:
        qualification_ok = True
        qual_reason = "Holds a recognized university degree (or Anabin H+ equivalent)."
    elif occupation_category == "IT_SOFTWARE_ENGINEERING" and it_experience_years >= 3:
        qualification_ok = True
        qual_reason = "Fulfills 2024 IT Specialist provision: Minimum 3 years of professional IT experience in the last 7 years."
    else:
        qual_reason = "Lacks recognized university degree and does not qualify under IT specialist 3-year experience clause."

    rejection_risks = []
    if not salary_met:
        rejection_risks.append({
            "code": "SALARY_BELOW_THRESHOLD",
            "severity": "CRITICAL",
            "message": f"Annual gross salary €{annual_gross_salary:,.2f} is below the required €{required_salary:,.2f} for category '{occupation_category}'."
        })

    if not qualification_ok:
        rejection_risks.append({
            "code": "QUALIFICATION_INSUFFICIENT",
            "severity": "CRITICAL",
            "message": qual_reason
        })

    if not qualification_matches_role:
        rejection_risks.append({
            "code": "DEGREE_ROLE_MISMATCH",
            "severity": "HIGH",
            "message": "Degree field of study does not reasonably align with job duties (Federal Employment Agency / Bundesagentur für Arbeit rejection risk)."
        })

    eligible = (salary_met and qualification_ok and qualification_matches_role)

    return {
        "eligible": eligible,
        "occupation_category": occupation_category,
        "is_shortage_occupation": is_shortage,
        "salary_audit": {
            "offered_annual_gross_eur": annual_gross_salary,
            "required_threshold_eur": required_salary,
            "meets_threshold": salary_met,
            "margin_eur": annual_gross_salary - required_salary
        },
        "qualification_audit": {
            "qualification_ok": qualification_ok,
            "reason": qual_reason,
            "degree_role_matching": qualification_matches_role
        },
        "rejection_risks": rejection_risks,
        "recommendation": "PROCEED_TO_APPLICATION" if eligible else "ADJUST_OFFER_OR_PATHWAY"
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            "annual_gross_salary_eur": 48000.0,
            "occupation_category": "IT_SOFTWARE_ENGINEERING",
            "has_recognized_university_degree": True,
            "it_experience_years": 4,
            "qualification_matches_role": True
        }
    
    res = evaluate_blue_card_eligibility(data)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
