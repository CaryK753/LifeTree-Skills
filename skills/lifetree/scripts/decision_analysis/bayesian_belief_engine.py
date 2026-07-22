#!/usr/bin/env python3
"""
LifeTree Bayesian Belief Inference & Dempster-Shafer Interval Engine
Updates event belief probabilities upon receiving new evidence P(H|E) = P(E|H)*P(H) / P(E)
and models Dempster-Shafer upper/lower interval belief bounds.
"""

import sys
import json
from typing import Dict, Any, List

def update_bayesian_belief(prior_prob: float, likelihood_given_true: float, likelihood_given_false: float) -> Dict[str, Any]:
    """
    Calculates posterior probability P(H|E) using Bayes' Theorem:
    P(H|E) = (P(E|H) * P(H)) / (P(E|H) * P(H) + P(E|~H) * (1 - P(H)))
    """
    try:
        p_h = max(0.001, min(0.999, float(prior_prob)))
        p_e_given_h = max(0.001, min(0.999, float(likelihood_given_true)))
        p_e_given_not_h = max(0.001, min(0.999, float(likelihood_given_false)))

        p_e = (p_e_given_h * p_h) + (p_e_given_not_h * (1.0 - p_h))
        posterior_prob = (p_e_given_h * p_h) / p_e

        return {
            "status": "SUCCESS",
            "prior_probability_P_H": round(p_h, 4),
            "evidence_likelihood_P_E_given_H": round(p_e_given_h, 4),
            "posterior_probability_P_H_given_E": round(posterior_prob, 4),
            "belief_delta": round(posterior_prob - p_h, 4)
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "BAYESIAN_UPDATE_EXCEPTION", "message": str(e)}

def calculate_dempster_shafer_interval(belief_masses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates Dempster-Shafer Belief (lower bound) and Plausibility (upper bound) intervals [Bel(A), Pl(A)].
    """
    try:
        if not isinstance(belief_masses, list) or not belief_masses:
            return {"status": "ERROR", "error_code": "INVALID_MASSES", "message": "Expected list of belief mass dicts"}

        lower_bel = 0.0
        upper_pl = 1.0

        for item in belief_masses:
            mass = float(item.get("mass", 0.0))
            type_str = item.get("type", "UNKNOWN").upper()
            if type_str == "CONFIRMED_EVIDENCE":
                lower_bel += mass
            elif type_str == "CONTRADICTORY_EVIDENCE":
                upper_pl -= mass

        lower_bel = max(0.0, min(1.0, lower_bel))
        upper_pl = max(lower_bel, min(1.0, upper_pl))

        return {
            "status": "SUCCESS",
            "dempster_shafer_interval": {
                "lower_belief_bound": round(lower_bel, 4),
                "upper_plausibility_bound": round(upper_pl, 4),
                "interval_range_str": f"[{lower_bel:.2f}, {upper_pl:.2f}]",
                "ambiguity_width": round(upper_pl - lower_bel, 4)
            }
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "DEMPSTER_SHAFER_EXCEPTION", "message": str(e)}

def main():
    try:
        b_res = update_bayesian_belief(0.85, 0.90, 0.20)
        ds_res = calculate_dempster_shafer_interval([
            {"type": "CONFIRMED_EVIDENCE", "mass": 0.65},
            {"type": "UNCERTAIN", "mass": 0.25},
            {"type": "CONTRADICTORY_EVIDENCE", "mass": 0.10}
        ])
        print(json.dumps({"bayesian_result": b_res, "dempster_shafer_result": ds_res}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
