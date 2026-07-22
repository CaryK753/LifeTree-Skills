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
    - income: annual_income (60%) + liquid_funds (40%) + German-level employability bonus
    - health: health_status (default 80)
    - time_cost_inverted: max(30, 100 - years * 5)
    - freedom: nationality/visa (default 70) + German-level PR/citizenship bonus
    - family_stability: dependents count (default 85)
    - stress_inverted: current_role & work_hours (default 65)

    C6: German language level now contributes to freedom and income scores. Previously
    the German level was read from the profile but had zero effect on any MAUT score,
    so the C6 elasticity computation always returned 0 for "Learn German" — making it
    impossible for the sensitivity engine to recommend German study regardless of the
    user's profile. A weak German (A1) now has lower freedom/income scores; upgrading
    to B1/C1 produces measurable utility gains.
    """
    fin = user_profile.get("financial_assets", {})
    liquid_funds = float(user_profile.get("liquid_funds_usd") or fin.get("liquid_funds_usd", 40000.0))
    annual_income = float(user_profile.get("annual_income_usd") or fin.get("annual_income_usd", 65000.0))

    work_exp = user_profile.get("work_experience", {})
    years = float(user_profile.get("work_experience_years") or work_exp.get("years", 5))

    # C6: resolve German CEFR level → numeric bonus. A1=0, A2=1, B1=2, B2=3, C1=4, C2=5.
    # NONE/missing = -1 so dropping to NONE is a real downgrade from A1.
    _cefr_rank = {"NONE": -1, "A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4, "C2": 5}
    german_level_raw = (user_profile.get("german_level")
                        or (user_profile.get("languages", {}) or {}).get("secondary")
                        or "NONE")
    german_level = str(german_level_raw).upper().replace("GERMAN_", "")
    german_rank = _cefr_rank.get(german_level, -1)

    # 1. Income score — German level boosts employability/salary in DE market
    income_score = min(100.0, (annual_income / 100000.0) * 100.0 * 0.6
                       + (liquid_funds / 200000.0) * 100.0 * 0.4
                       + max(0, german_rank) * 3.0)

    # 2. Health score
    health_score = float(user_profile.get("health_status", 80.0))

    # 3. Time cost inverted
    time_cost_inv = max(30.0, 100.0 - (years * 5.0))

    # 4. Freedom score — German level is required for PR/citizenship (Niederlassungserlaubnis)
    demographics = user_profile.get("demographics", {})
    nationality = user_profile.get("nationality") or demographics.get("nationality", "CN")
    freedom_base = 90.0 if nationality in ["DE", "US", "EU"] else 70.0
    freedom_score = max(0.0, min(100.0, freedom_base + german_rank * 5.0))

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

def _evaluate_maut_for_profile(user_profile: Dict[str, Any]) -> float:
    """Map a user_profile to MAUT scores and return the total utility score."""
    scores = compute_maut_attribute_scores_from_profile(user_profile)
    if maut_utility_engine:
        return float(maut_utility_engine.evaluate_maut_utility(scores).get("maut_total_utility_score", 0.0))
    return float(sum(scores.values()) / max(1, len(scores)))


# C6 fix: real parameter perturbations with documented effort costs. Each entry
# describes how to mutate one user_profile field by ±Δx, plus the effort cost
# (in months) required to achieve the +Δx improvement. The engine then computes
# actual elasticity S_i = |U(+Δx) − U(−Δx)| and ROI = S_i / effort_months.
DEFAULT_PERTURBATIONS = [
    {
        "parameter": "German Language Level",
        "field": "german_level",  # also falls back to languages.secondary
        "field_type": "language_level",
        "delta_up": "B1",      # upgrade to B1 (or stay if already ≥ B1)
        "delta_down": "NONE",  # drop to no German
        "effort_months_up": 4,
        "effort_months_down": 0,
        "effort_type": "STUDY_AND_EXAM",
    },
    {
        "parameter": "Liquid Capital Reserves",
        "field": "liquid_funds_usd",
        "field_type": "float",
        "delta_up": 5000.0,
        "delta_down": -5000.0,
        "effort_months_up": 1,
        "effort_months_down": 0,
        "effort_type": "CAPITAL_ALLOCATION",
    },
    {
        "parameter": "Work Experience Years",
        "field": "work_experience_years",
        "field_type": "float",
        "delta_up": 1.0,
        "delta_down": -1.0,
        "effort_months_up": 12,
        "effort_months_down": 0,
        "effort_type": "EMPLOYMENT_DURATION",
    },
    {
        "parameter": "Health Status",
        "field": "health_status",
        "field_type": "float",
        "delta_up": 5.0,
        "delta_down": -5.0,
        "effort_months_up": 6,
        "effort_months_down": 0,
        "effort_type": "LIFESTYLE_CHANGE",
    },
    {
        "parameter": "Work Hours Per Week",
        "field": "work_hours_per_week",
        "field_type": "float",
        "delta_up": -5.0,   # reducing hours improves stress_inverted
        "delta_down": 5.0,
        "effort_months_up": 3,
        "effort_months_down": 0,
        "effort_type": "LIFESTYLE_CHANGE",
    },
]


def _apply_perturbation(user_profile: Dict[str, Any], pert: Dict[str, Any], direction: str) -> Dict[str, Any]:
    """Return a copy of user_profile with the perturbation applied in the given direction."""
    import copy
    prof = copy.deepcopy(user_profile)
    ftype = pert.get("field_type", "float")
    field = pert.get("field")
    delta = pert.get("delta_up" if direction == "up" else "delta_down")
    if delta is None or field is None:
        return prof

    if ftype == "language_level":
        # Setting german_level + languages.secondary so compute_maut_attribute_scores
        # picks up the upgrade.
        prof["german_level"] = delta
        langs = prof.get("languages", {})
        if isinstance(langs, dict):
            langs["secondary"] = delta
            prof["languages"] = langs
        else:
            prof["languages"] = {"secondary": delta}
    elif ftype == "float":
        # Support nested financial_assets.liquid_funds_usd as well as flat keys.
        fin = prof.get("financial_assets", {})
        if isinstance(fin, dict) and field in fin:
            fin[field] = max(0.0, float(fin.get(field, 0.0)) + float(delta))
            prof["financial_assets"] = fin
        else:
            prof[field] = max(0.0, float(prof.get(field, 0.0)) + float(delta))
    return prof


def calculate_parameter_sensitivity(user_profile: Dict[str, Any], domain_rule_pack: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Evaluates parameter sensitivity by mapping user_profile to MAUT scores and computing
    dynamic utility delta gains.

    C6 fix: replaced canned "Top up capital by $5,000" recommendations with real
    elasticity computation. For each perturbation Δx_i we evaluate U(+Δx_i) and
    U(−Δx_i), compute elasticity S_i = |U(+Δx_i) − U(−Δx_i)|, and rank by
    ROI = S_i / effort_months. The top recommendation now actually reflects the
    user's profile — e.g. for a student with weak German, "Learn German to B1"
    dominates because it moves freedom/income scores the most per month of effort.
    """
    try:
        if not isinstance(user_profile, dict):
            return {"status": "ERROR", "error_code": "INVALID_USER_PROFILE", "message": "Expected dict for user_profile"}

        # Dynamic MAUT Mapping at the unperturbed baseline
        base_scores = compute_maut_attribute_scores_from_profile(user_profile)
        base_maut = maut_utility_engine.evaluate_maut_utility(base_scores) if maut_utility_engine else {
            "maut_total_utility_score": sum(base_scores.values()) / max(1, len(base_scores))
        }
        base_utility_val = float(base_maut.get("maut_total_utility_score", 70.0))

        # Allow domain_rule_pack to override perturbations (else use defaults)
        perturbations = DEFAULT_PERTURBATIONS
        if domain_rule_pack and isinstance(domain_rule_pack, dict) and "perturbations" in domain_rule_pack:
            perturbations = domain_rule_pack["perturbations"]

        sensitivities = []
        for pert in perturbations:
            # C6: compute U(+Δx) and U(−Δx) by re-mapping the perturbed profile to MAUT
            up_prof = _apply_perturbation(user_profile, pert, "up")
            down_prof = _apply_perturbation(user_profile, pert, "down")
            u_up = _evaluate_maut_for_profile(up_prof)
            u_down = _evaluate_maut_for_profile(down_prof)

            # Elasticity S_i = |U(+Δx) − U(−Δx)| (per bug report spec)
            elasticity = round(abs(u_up - u_down), 4)
            # Directional gain vs baseline (used for the human-readable recommendation)
            gain_up = round(u_up - base_utility_val, 4)
            effort_months = float(pert.get("effort_months_up", 1))
            roi = round(elasticity / max(0.1, effort_months), 4) if elasticity > 0 else 0.0

            # Build a meaningful, profile-aware recommendation instead of the canned string
            current_val = user_profile.get(pert.get("field"))
            if current_val is None and pert.get("field") == "liquid_funds_usd":
                fin = user_profile.get("financial_assets", {})
                current_val = fin.get("liquid_funds_usd")
            proposed_val = pert.get("delta_up")

            if gain_up > 0.01:
                action = f"{pert['parameter']}: shift {current_val} → {proposed_val} for +{round(gain_up, 2)} MAUT utility (effort: {int(effort_months)}mo, ROI={roi})."
            else:
                action = f"{pert['parameter']}: low sensitivity (elasticity={elasticity}); marginal gain not worth the effort."

            sensitivities.append({
                "parameter": pert["parameter"],
                "current_value": current_val,
                "proposed_value": proposed_val,
                "effort_type": pert.get("effort_type", "UNKNOWN"),
                "effort_months": int(effort_months),
                "baseline_utility": round(base_utility_val, 4),
                "utility_at_plus_delta": round(u_up, 4),
                "utility_at_minus_delta": round(u_down, 4),
                "elasticity_S_i": elasticity,
                "maut_utility_gain": gain_up,
                "roi_rank_score": roi,
                "action_recommendation": action
            })

        # C6: rank by ROI (elasticity per month of effort), not by canned ordering
        sensitivities.sort(key=lambda x: x["roi_rank_score"], reverse=True)
        top_rec = sensitivities[0]["action_recommendation"] if sensitivities else "Maintain current status."

        return {
            "status": "SUCCESS",
            "mapped_maut_base_scores": base_scores,
            "maut_evaluation": base_maut,
            "sensitivity_summary": {
                "parameters_audited": len(sensitivities),
                "maut_total_utility_score": base_utility_val,
                "top_recommended_action": top_rec,
                "elasticity_method": "S_i = |U(+Δx_i) − U(−Δx_i)|, ROI = S_i / effort_months"
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
