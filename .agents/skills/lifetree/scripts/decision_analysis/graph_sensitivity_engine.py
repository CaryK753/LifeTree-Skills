#!/usr/bin/env python3
"""
LifeTree Dynamic Graph Sensitivity & MAUT Mapping Engine
Maps real user_profile parameters to dynamic MAUT attribute scores and computes dynamic marginal utility gains.
"""

import sys
import os
import json
from typing import Dict, Any, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
DECISION_MODELS_DIR = os.path.join(SKILL_ROOT, "scripts", "decision_models")
if DECISION_MODELS_DIR not in sys.path:
    sys.path.insert(0, DECISION_MODELS_DIR)

try:
    import maut_utility_engine
except ImportError:
    maut_utility_engine = None

def compute_maut_attribute_scores_from_profile(user_profile: Dict[str, Any]) -> Dict[str, float]:
    """
    Maps real user_profile data into normalized 0-100 MAUT attribute scores:
    - income: annual_income (60%) + liquid_funds (40%)
    - health: health_status (default 80)
    - time_cost_inverted: max(30, 100 - years * 5)
    - freedom: nationality/visa (default 70)
    - family_stability: dependents count (default 85)
    - stress_inverted: current_role & work_hours (default 65)
    """
    fin = user_profile.get("financial_assets", {})
    liquid_funds = float(user_profile.get("liquid_funds_usd") or fin.get("liquid_funds_usd", 40000.0))
    annual_income = float(user_profile.get("annual_income_usd") or fin.get("annual_income_usd", 65000.0))

    work_exp = user_profile.get("work_experience", {})
    years = float(user_profile.get("work_experience_years") or work_exp.get("years", 5))

    # 1. Income score
    income_score = min(100.0, (annual_income / 100000.0) * 100.0 * 0.6 + (liquid_funds / 200000.0) * 100.0 * 0.4)

    # 2. Health score
    health_score = float(user_profile.get("health_status", 80.0))

    # 3. Time cost inverted
    time_cost_inv = max(30.0, 100.0 - (years * 5.0))

    # 4. Freedom score
    demographics = user_profile.get("demographics", {})
    nationality = user_profile.get("nationality") or demographics.get("nationality", "CN")
    freedom_score = 90.0 if nationality in ["DE", "US", "EU"] else 70.0

    # 5. Family stability score
    dependents = int(user_profile.get("dependents", 0))
    family_stability = max(50.0, 85.0 - (dependents * 5.0))

    # 6. Stress inverted
    work_hours = float(user_profile.get("work_hours_per_week", 40.0))
    stress_inverted = max(20.0, 100.0 - (work_hours * 0.875))

    return {
        "income": round(income_score, 2),
        "health": round(health_score, 2),
        "time_cost_inverted": round(time_cost_inv, 2),
        "freedom": round(freedom_score, 2),
        "family_stability": round(family_stability, 2),
        "stress_inverted": round(stress_inverted, 2)
    }

def calculate_parameter_sensitivity(user_profile: Dict[str, Any], domain_rule_pack: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Evaluates parameter sensitivity by mapping user_profile to MAUT scores and computing dynamic utility delta gains.
    """
    try:
        if not isinstance(user_profile, dict):
            return {"status": "ERROR", "error_code": "INVALID_USER_PROFILE", "message": "Expected dict for user_profile"}

        # Dynamic MAUT Mapping
        base_scores = compute_maut_attribute_scores_from_profile(user_profile)

        base_maut = maut_utility_engine.evaluate_maut_utility(base_scores) if maut_utility_engine else {
            "maut_total_utility_score": sum(base_scores.values()) / len(base_scores)
        }
        base_utility_val = base_maut.get("maut_total_utility_score", 70.0)

        # Compute dynamic marginal gains based on attribute deltas
        # Action 1: Language level upgrade (boosts freedom & income potential)
        prop_scores_de = dict(base_scores)
        prop_scores_de["freedom"] = min(100.0, prop_scores_de["freedom"] + 15.0)
        prop_scores_de["income"] = min(100.0, prop_scores_de["income"] + 10.0)
        util_de = maut_utility_engine.evaluate_maut_utility(prop_scores_de).get("maut_total_utility_score", base_utility_val + 5.0) if maut_utility_engine else base_utility_val + 5.0
        de_utility_gain = round(util_de - base_utility_val, 2)

        # Action 2: Capital topup (boosts income attribute)
        prop_scores_cap = dict(base_scores)
        prop_scores_cap["income"] = min(100.0, prop_scores_cap["income"] + 12.0)
        util_cap = maut_utility_engine.evaluate_maut_utility(prop_scores_cap).get("maut_total_utility_score", base_utility_val + 2.0) if maut_utility_engine else base_utility_val + 2.0
        cap_utility_gain = round(util_cap - base_utility_val, 2)

        languages = user_profile.get("languages", {})
        current_de = user_profile.get("german_level") or languages.get("secondary", "A2")
        fin = user_profile.get("financial_assets", {})
        current_funds = float(user_profile.get("liquid_funds_usd") or fin.get("liquid_funds_usd", 40000.0))

        sensitivities = [
            {
                "parameter": "German Language Level",
                "current_value": current_de,
                "proposed_value": "B1",
                "effort_type": "STUDY_AND_EXAM",
                "maut_utility_gain": de_utility_gain,
                "effort_months": 4,
                "roi_rank_score": round(de_utility_gain / 4.0, 2),
                "action_recommendation": f"Upgrade German from {current_de} to B1 for a dynamic +{de_utility_gain} MAUT utility boost!"
            },
            {
                "parameter": "Liquid Capital Reserves",
                "current_value": f"${current_funds:,.2f}",
                "proposed_value": f"${current_funds + 5000.0:,.2f}",
                "effort_type": "CAPITAL_ALLOCATION",
                "maut_utility_gain": cap_utility_gain,
                "effort_months": 1,
                "roi_rank_score": round(cap_utility_gain / 1.0, 2),
                "action_recommendation": f"Top up liquid capital reserves by $5,000 for a dynamic +{cap_utility_gain} MAUT utility buffer."
            }
        ]

        sensitivities.sort(key=lambda x: x["roi_rank_score"], reverse=True)
        top_rec = sensitivities[0]["action_recommendation"] if sensitivities else "Maintain current status."

        return {
            "status": "SUCCESS",
            "mapped_maut_base_scores": base_scores,
            "maut_evaluation": base_maut,
            "sensitivity_summary": {
                "parameters_audited": len(sensitivities),
                "maut_total_utility_score": base_utility_val,
                "top_recommended_action": top_rec
            },
            "ranked_personal_action_rois": sensitivities
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_code": "GRAPH_SENSITIVITY_EXCEPTION",
            "message": str(e)
        }

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                data = json.load(f)
                prof = data.get("profile", data)
        else:
            prof = {"german_level": "A2", "liquid_funds_usd": 40000.0, "annual_income_usd": 65000.0, "work_experience_years": 5}

        res = calculate_parameter_sensitivity(prof)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
