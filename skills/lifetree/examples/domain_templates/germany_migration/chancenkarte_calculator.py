#!/usr/bin/env python3
"""
Chancenkarte (Opportunity Card) Calculator for Germany (2024/2025 Rules)
Part of LifeTree Decision Intelligence System MVP
"""

import sys
import json
from typing import Dict, Any

BLOCKED_ACCOUNT_REQUIREMENT_EUR = 12000.0  # Statutory minimum proof of financial funds per year

def calculate_chancenkarte_points(applicant: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates Chancenkarte points based on German Residence Act § 20a / 20b rules.
    Minimum total required: 6 points (provided basic prerequisites are met).
    
    Basic Prerequisites:
    1. Fully recognized foreign degree OR vocational training of at least 2 years.
    2. German language at A1 level OR English language at B2 level.
    """
    points = 0
    breakdown = []
    prerequisites_met = True
    prereq_failures = []

    # Basic Prerequisites Check
    has_recognized_degree = applicant.get("has_recognized_degree_or_2yr_vocational", False)
    if not has_recognized_degree:
        prerequisites_met = False
        prereq_failures.append("Lacks minimum 2-year recognized vocational qualification or university degree.")

    german_level = applicant.get("german_level", "None").upper() # None, A1, A2, B1, B2, C1, C2
    english_level = applicant.get("english_level", "None").upper() # None, A1, A2, B1, B2, C1, C2

    valid_german_prereq = german_level in ["A1", "A2", "B1", "B2", "C1", "C2"]
    valid_english_prereq = english_level in ["B2", "C1", "C2"]
    
    if not (valid_german_prereq or valid_english_prereq):
        prerequisites_met = False
        prereq_failures.append("Language prerequisite failed: Requires at least German A1 OR English B2.")

    # Blocked Account Check
    liquid_funds = applicant.get("liquid_funds_eur", 0.0)
    blocked_account_ok = liquid_funds >= BLOCKED_ACCOUNT_REQUIREMENT_EUR
    blocked_account_warning = None
    if not blocked_account_ok:
        blocked_account_warning = f"Liquid funds (€{liquid_funds:,.2f}) fall below required Sperrkonto threshold (€{BLOCKED_ACCOUNT_REQUIREMENT_EUR:,.2f}). High risk of visa refusal."

    # Point Scoring
    # 1. Partial Recognition of Foreign Qualification (4 Points)
    if applicant.get("partial_recognition_germany", False):
        points += 4
        breakdown.append({"category": "Partial Recognition", "points": 4, "desc": "Partial recognition of professional qualification in Germany"})

    # 2. Shortage Occupation + Professional Experience (3 Points)
    work_exp_years = applicant.get("work_experience_years", 0)
    is_shortage_occupation = applicant.get("is_shortage_occupation", False)
    
    if is_shortage_occupation and work_exp_years >= 5:
        points += 3
        breakdown.append({"category": "Work Experience & Shortage Role", "points": 3, "desc": "5+ years work experience in shortage occupation within last 7 years"})
    elif work_exp_years >= 2 and applicant.get("exp_matches_qualification", True):
        # 2 Points for 2 years experience matching qualification
        points += 2
        breakdown.append({"category": "Work Experience", "points": 2, "desc": "2+ years professional experience matching qualification within last 5 years"})

    # 3. Language Skills
    if german_level in ["B2", "C1", "C2"]:
        points += 3
        breakdown.append({"category": "German Language", "points": 3, "desc": f"German language proficiency {german_level} (B2+)"})
    elif german_level == "B1":
        points += 2
        breakdown.append({"category": "German Language", "points": 2, "desc": "German language proficiency B1"})
    elif german_level == "A2":
        points += 1
        breakdown.append({"category": "German Language", "points": 1, "desc": "German language proficiency A2"})

    if english_level in ["C1", "C2"] or applicant.get("is_native_english", False):
        points += 1
        breakdown.append({"category": "English Language", "points": 1, "desc": "English C1 level or Native speaker"})

    # 4. Age Criteria
    age = applicant.get("age", 99)
    if age < 35:
        points += 2
        breakdown.append({"category": "Age", "points": 2, "desc": f"Applicant age ({age}) is under 35"})
    elif 35 <= age <= 40:
        points += 1
        breakdown.append({"category": "Age", "points": 1, "desc": f"Applicant age ({age}) is between 35 and 40"})

    # 5. Connection to Germany
    if applicant.get("previous_stay_germany_6months", False):
        points += 1
        breakdown.append({"category": "Connection to Germany", "points": 1, "desc": "Legal stay in Germany for at least 6 consecutive months in the last 5 years"})

    # 6. Joint Application with Spouse
    if applicant.get("spouse_meets_chancenkarte", False):
        points += 1
        breakdown.append({"category": "Spouse Bonus", "points": 1, "desc": "Spouse meets Chancenkarte requirements and applies jointly"})

    eligible = prerequisites_met and (points >= 6) and blocked_account_ok

    return {
        "eligible": eligible,
        "prerequisites_met": prerequisites_met,
        "prereq_failures": prereq_failures,
        "total_points": points,
        "points_required": 6,
        "points_breakdown": breakdown,
        "financial_audit": {
            "liquid_funds_eur": liquid_funds,
            "required_eur": BLOCKED_ACCOUNT_REQUIREMENT_EUR,
            "sufficient": blocked_account_ok,
            "warning": blocked_account_warning
        },
        "risk_level": "LOW" if eligible else ("MEDIUM" if points >= 6 and not blocked_account_ok else "HIGH")
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            applicant_data = json.load(f)
    else:
        # Sample fallback test data
        applicant_data = {
            "has_recognized_degree_or_2yr_vocational": True,
            "german_level": "A2",
            "english_level": "C1",
            "age": 31,
            "work_experience_years": 4,
            "exp_matches_qualification": True,
            "is_shortage_occupation": True,
            "partial_recognition_germany": False,
            "previous_stay_germany_6months": False,
            "spouse_meets_chancenkarte": False,
            "liquid_funds_eur": 13500.0
        }
    
    res = calculate_chancenkarte_points(applicant_data)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
