#!/usr/bin/env python3
"""
LifeTree Bayesian Belief Updater & Dempster-Shafer Interval Engine
Dynamically updates posterior belief probabilities upon receiving new evidence P(H|E) = P(E|H)*P(H) / P(E)
and computes Dempster's Rule of Combination m_1,2(A) for multi-source evidence fusion.
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

def combine_dempster_shafer_evidence(m1: Dict[str, float], m2: Dict[str, float]) -> Dict[str, Any]:
    """
    Combines two independent evidence mass functions m1 and m2 using Dempster's Rule of Combination:
    m_1,2(A) = (sum_{B intersect C = A} m1(B)*m2(C)) / (1 - K)
    K = sum_{B intersect C = empty} m1(B)*m2(C)
    """
    try:
        # Mass functions over hypothesis space: {"TRUE": prob, "FALSE": prob, "UNCERTAIN": prob}
        m1_t, m1_f, m1_u = m1.get("TRUE", 0.0), m1.get("FALSE", 0.0), m1.get("UNCERTAIN", 0.0)
        m2_t, m2_f, m2_u = m2.get("TRUE", 0.0), m2.get("FALSE", 0.0), m2.get("UNCERTAIN", 0.0)

        # Conflict measure K
        k_conflict = (m1_t * m2_f) + (m1_f * m2_t)

        if k_conflict >= 0.99:
            return {"status": "ERROR", "error_code": "TOTAL_EVIDENCE_CONFLICT", "message": "Evidence sources are in total conflict (K >= 0.99)"}

        denom = 1.0 - k_conflict

        # Combined masses
        m_combined_true = ((m1_t * m2_t) + (m1_t * m2_u) + (m1_u * m2_t)) / denom
        m_combined_false = ((m1_f * m2_f) + (m1_f * m2_u) + (m1_u * m2_f)) / denom
        m_combined_uncertain = (m1_u * m2_u) / denom

        return {
            "status": "SUCCESS",
            "dempster_combination": {
                "conflict_k": round(k_conflict, 4),
                "combined_mass_true": round(m_combined_true, 4),
                "combined_mass_false": round(m_combined_false, 4),
                "combined_mass_uncertain": round(m_combined_uncertain, 4),
                "belief_lower_bound": round(m_combined_true, 4),
                "plausibility_upper_bound": round(m_combined_true + m_combined_uncertain, 4)
            }
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "DEMPSTER_COMBINATION_EXCEPTION", "message": str(e)}

def main():
    try:
        m1 = {"TRUE": 0.60, "FALSE": 0.10, "UNCERTAIN": 0.30}
        m2 = {"TRUE": 0.70, "FALSE": 0.05, "UNCERTAIN": 0.25}
        res = combine_dempster_shafer_evidence(m1, m2)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
