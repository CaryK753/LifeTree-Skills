#!/usr/bin/env python3
"""
LifeTree Universal Domain Rule Evaluator Engine
Domain-Agnostic Rule Processing Module for LifeTree Decision Intelligence System
"""

import sys
import json
from typing import Dict, Any, List

def evaluate_domain_rules(profile: Dict[str, Any], rule_pack: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates a user profile against a domain-agnostic rule pack JSON.
    Rule Pack structure:
    - domain_id: e.g. "IMMIGRATION_DE", "ASSET_ALLOCATION_US", "CAREER_PIVOT_TECH"
    - prerequisites: list of boolean or threshold conditions
    - point_scoring: list of point rules (category, points, condition)
    - threshold_checks: list of numeric checks (field, min/max, error_code)
    - timeline_milestones: list of time-based progressions
    """
    domain_id = rule_pack.get("domain_id", "GENERAL_DOMAIN")
    domain_title = rule_pack.get("domain_title", "General Decision Domain")
    
    # 1. Prerequisite Checks
    prerequisites_met = True
    prereq_audit = []
    for prereq in rule_pack.get("prerequisites", []):
        field_name = prereq.get("field")
        expected_val = prereq.get("expected")
        actual_val = profile.get(field_name)
        
        passed = False
        if prereq.get("operator") == "EQUALS":
            passed = (actual_val == expected_val)
        elif prereq.get("operator") == "IN":
            passed = (actual_val in expected_val) if isinstance(expected_val, list) else False
        elif prereq.get("operator") == "GTE":
            passed = (actual_val is not None and actual_val >= expected_val)
            
        if not passed:
            prerequisites_met = False
            prereq_audit.append({
                "field": field_name,
                "message": prereq.get("failure_message", f"Prerequisite {field_name} failed."),
                "actual": actual_val,
                "expected": expected_val
            })

    # 2. Point Grid Scoring
    total_points = 0
    min_points_required = rule_pack.get("min_points_required", 0)
    point_breakdown = []

    for point_rule in rule_pack.get("point_scoring", []):
        field_name = point_rule.get("field")
        actual_val = profile.get(field_name)
        condition_type = point_rule.get("type")
        
        earned = False
        pts = point_rule.get("points", 0)
        
        if condition_type == "BOOLEAN" and actual_val is True:
            earned = True
        elif condition_type == "RANGE" and actual_val is not None:
            min_v = point_rule.get("min", -sys.maxsize)
            max_v = point_rule.get("max", sys.maxsize)
            if min_v <= actual_val <= max_v:
                earned = True
        elif condition_type == "IN_SET" and actual_val in point_rule.get("values", []):
            earned = True

        if earned:
            total_points += pts
            point_breakdown.append({
                "category": point_rule.get("category", "General"),
                "points": pts,
                "description": point_rule.get("description", "")
            })

    # 3. Threshold Checks (e.g. liquid funds, salary, debt ratio)
    threshold_audit = []
    thresholds_passed = True
    for t_check in rule_pack.get("threshold_checks", []):
        field_name = t_check.get("field")
        actual_val = profile.get(field_name, 0.0)
        req_val = t_check.get("required_value", 0.0)
        operator = t_check.get("operator", "GTE")
        
        ok = False
        if operator == "GTE":
            ok = (actual_val >= req_val)
        elif operator == "LTE":
            ok = (actual_val <= req_val)

        if not ok:
            thresholds_passed = False
            threshold_audit.append({
                "code": t_check.get("error_code", "THRESHOLD_FAILED"),
                "severity": t_check.get("severity", "CRITICAL"),
                "message": t_check.get("message", f"{field_name} requirement failed."),
                "actual": actual_val,
                "required": req_val
            })

    # Overall Verdict
    points_ok = (total_points >= min_points_required) if min_points_required > 0 else True
    overall_eligible = prerequisites_met and points_ok and thresholds_passed

    return {
        "domain_id": domain_id,
        "domain_title": domain_title,
        "eligible": overall_eligible,
        "prerequisites_audit": {
            "all_met": prerequisites_met,
            "failures": prereq_audit
        },
        "points_audit": {
            "total_points": total_points,
            "min_required": min_points_required,
            "points_met": points_ok,
            "breakdown": point_breakdown
        },
        "thresholds_audit": {
            "all_passed": thresholds_passed,
            "failures": threshold_audit
        },
        "status": "APPROVED" if overall_eligible else "REJECTED_OR_BLOCKED"
    }

def main():
    if len(sys.argv) > 2:
        with open(sys.argv[1], 'r', encoding='utf-8') as f1, open(sys.argv[2], 'r', encoding='utf-8') as f2:
            profile = json.load(f1)
            rule_pack = json.load(f2)
    else:
        # Generic synthetic example
        profile = {
            "has_degree": True,
            "years_exp": 5,
            "liquid_capital_usd": 50000.0,
            "risk_score": 3
        }
        rule_pack = {
            "domain_id": "EXAMPLE_DOMAIN",
            "domain_title": "Example Investment Decision",
            "min_points_required": 5,
            "prerequisites": [
                {"field": "has_degree", "operator": "EQUALS", "expected": True, "failure_message": "Degree required"}
            ],
            "point_scoring": [
                {"field": "years_exp", "type": "RANGE", "min": 3, "max": 10, "points": 5, "category": "Experience", "description": "3-10 years experience"}
            ],
            "threshold_checks": [
                {"field": "liquid_capital_usd", "operator": "GTE", "required_value": 30000.0, "severity": "CRITICAL", "message": "Insufficient capital"}
            ]
        }

    res = evaluate_domain_rules(profile, rule_pack)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
