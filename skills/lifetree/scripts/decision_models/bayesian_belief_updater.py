#!/usr/bin/env python3
"""
LifeTree Bayesian Belief Updater & Dempster-Shafer Interval Engine
Dynamically updates posterior belief probabilities upon receiving new evidence P(H|E) = P(E|H)*P(H) / P(E)
and computes Dempster-Shafer upper/lower interval belief bounds to eliminate false precision.
"""

import sys
import json
from typing import Dict, Any, List

def update_posterior_belief(prior_prob: float, evidence_likelihood_h: float, evidence_likelihood_not_h: float) -> Dict[str, Any]:
    """
    Computes posterior probability P(H|E) using Bayes' Rule.
    """
    try:
        p_h = max(0.001, min(0.999, float(prior_prob)))
        p_e_h = max(0.001, min(0.999, float(evidence_likelihood_h)))
        p_e_not_h = max(0.001, min(0.999, float(evidence_likelihood_not_h)))

        p_e = (p_e_h * p_h) + (p_e_not_h * (1.0 - p_h))
        posterior = (p_e_h * p_h) / p_e

        return {
            "status": "SUCCESS",
            "prior_belief_P_H": round(p_h, 4),
            "evidence_likelihood_P_E_given_H": round(p_e_h, 4),
            "evidence_likelihood_P_E_given_Not_H": round(p_e_not_h, 4),
            "posterior_belief_P_H_given_E": round(posterior, 4),
            "belief_shift_delta": round(posterior - p_h, 4)
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "BAYESIAN_UPDATE_EXCEPTION", "message": str(e)}

def compute_dempster_shafer_interval(confirmed_mass: float, contradictory_mass: float) -> Dict[str, Any]:
    """
    Computes Dempster-Shafer Belief (Lower Bound) and Plausibility (Upper Bound) interval [Bel(A), Pl(A)].
    """
    try:
        m_confirm = max(0.0, min(1.0, float(confirmed_mass)))
        m_contradict = max(0.0, min(1.0 - m_confirm, float(contradictory_mass)))

        belief_lower = m_confirm
        plausibility_upper = 1.0 - m_contradict
        ambiguity_width = round(plausibility_upper - belief_lower, 4)

        return {
            "status": "SUCCESS",
            "dempster_shafer_bounds": {
                "belief_lower_bound": round(belief_lower, 4),
                "plausibility_upper_bound": round(plausibility_upper, 4),
                "interval_str": f"[{belief_lower:.2f}, {plausibility_upper:.2f}]",
                "ambiguity_width": ambiguity_width,
                "precision_warning": "HIGH_AMBIGUITY" if ambiguity_width > 0.4 else "WELL_CALIBRATED"
            }
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "DEMPSTER_SHAFER_EXCEPTION", "message": str(e)}

def main():
    try:
        b_res = update_posterior_belief(0.85, 0.95, 0.20)
        ds_res = compute_dempster_shafer_interval(0.60, 0.15)
        print(json.dumps({"bayesian_update": b_res, "dempster_shafer": ds_res}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
