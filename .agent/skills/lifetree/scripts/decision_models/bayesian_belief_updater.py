#!/usr/bin/env python3
"""
LifeTree Bayesian Belief Updater & Dempster-Shafer Interval Engine
Dynamically updates posterior belief probabilities upon receiving new evidence
P(H|E) = P(E|H)*P(H) / P(E), and computes Dempster's Rule of Combination
m_1,2(A) for multi-source evidence fusion.

Bug 3 consolidation: This module now subsumes the functionality previously
duplicated in decision_analysis/bayesian_belief_engine.py. The evidence_basis
provenance tracking and speculative-belief flagging (M3 fix) from the old
decision_analysis/ version has been merged in so callers always get the
safety annotations regardless of which entry point they use.
"""

import sys
import json
from typing import Dict, Any, List


def update_bayesian_belief(prior_prob: float,
                           likelihood_given_true: float,
                           likelihood_given_false: float,
                           evidence_basis: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Computes posterior probability P(H|E) using Bayes' Rule.

    M3 fix (merged from decision_analysis/): When evidence_basis is None or
    marks the likelihood as speculative, the response carries is_speculative=true
    and a warnings list so downstream UIs can warn the user that the posterior
    is not grounded in verified evidence.

    Args:
        prior_prob: Prior belief P(H).
        likelihood_given_true: P(E|H) — likelihood of evidence given hypothesis is true.
        likelihood_given_false: P(E|¬H) — likelihood of evidence given hypothesis is false.
        evidence_basis: Optional provenance dict, e.g.
            {"source": "German Embassy 2024 stats", "is_speculative": false}.
            When omitted, the posterior is flagged as speculative.
    """
    try:
        p_h = max(0.001, min(0.999, float(prior_prob)))
        p_e_h = max(0.001, min(0.999, float(likelihood_given_true)))
        p_e_not_h = max(0.001, min(0.999, float(likelihood_given_false)))

        p_e = (p_e_h * p_h) + (p_e_not_h * (1.0 - p_h))
        posterior = (p_e_h * p_h) / p_e

        # M3: provenance & speculative flag
        warnings = []
        is_speculative = False
        if evidence_basis is None:
            is_speculative = True
            warnings.append(
                "No evidence_basis supplied — posterior is computed from unverified "
                "likelihoods. Treat as speculative until grounded in cited data."
            )
        else:
            if evidence_basis.get("is_speculative", False):
                is_speculative = True
                warnings.append(
                    f"evidence_basis marks this likelihood as speculative "
                    f"(source: {evidence_basis.get('source', 'UNKNOWN')})."
                )
            if not evidence_basis.get("source"):
                warnings.append(
                    "evidence_basis has no 'source' field — provenance untraceable."
                )

        return {
            "status": "SUCCESS",
            "prior_probability_P_H": round(p_h, 4),
            "likelihood_P_E_given_H": round(p_e_h, 4),
            "likelihood_P_E_given_Not_H": round(p_e_not_h, 4),
            "posterior_probability_P_H_given_E": round(posterior, 4),
            "belief_delta": round(posterior - p_h, 4),
            "evidence_basis": evidence_basis or {},
            "is_speculative": is_speculative,
            "warnings": warnings
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "BAYESIAN_UPDATE_EXCEPTION", "message": str(e)}


def update_posterior_belief(prior_prob: float,
                            evidence_likelihood_h: float,
                            evidence_likelihood_not_h: float) -> Dict[str, Any]:
    """
    Backward-compatible thin wrapper around update_bayesian_belief.
    Returns a simplified payload (without evidence_basis fields) so existing
    callers that only need the numbers are not affected.
    """
    full = update_bayesian_belief(prior_prob, evidence_likelihood_h, evidence_likelihood_not_h)
    if full.get("status") != "SUCCESS":
        return full
    return {
        "status": "SUCCESS",
        "prior_belief_P_H": full["prior_probability_P_H"],
        "evidence_likelihood_P_E_given_H": full["likelihood_P_E_given_H"],
        "evidence_likelihood_P_E_given_Not_H": full["likelihood_P_E_given_Not_H"],
        "posterior_belief_P_H_given_E": full["posterior_probability_P_H_given_E"],
        "belief_shift_delta": full["belief_delta"]
    }


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


def calculate_dempster_shafer_interval(belief_masses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes Belief (Bel) and Plausibility (Pl) intervals from a list of
    single-source mass functions. Merged from decision_analysis/bayesian_belief_engine.py.
    """
    try:
        if not isinstance(belief_masses, list) or not belief_masses:
            return {"status": "ERROR", "error_code": "INVALID_MASSES", "message": "Expected non-empty list of belief mass dicts"}

        bel_true = 0.0
        pl_true = 0.0
        source_count = len(belief_masses)

        for mass in belief_masses:
            m_true = float(mass.get("TRUE", mass.get("belief_true", 0.0)))
            m_uncertain = float(mass.get("UNCERTAIN", mass.get("belief_uncertain", 0.0)))
            bel_true += m_true
            pl_true += m_true + m_uncertain

        bel_avg = bel_true / source_count if source_count > 0 else 0.0
        pl_avg = pl_true / source_count if source_count > 0 else 0.0

        return {
            "status": "SUCCESS",
            "belief_lower_bound_Bel": round(bel_avg, 4),
            "plausibility_upper_bound_Pl": round(pl_avg, 4),
            "epistemic_uncertainty_gap": round(pl_avg - bel_avg, 4),
            "source_count": source_count
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "DEMPSTER_SHAFER_INTERVAL_EXCEPTION", "message": str(e)}


def main():
    try:
        # Bayesian update with evidence basis
        res = update_bayesian_belief(0.85, 0.92, 0.15,
                                     evidence_basis={"source": "German Embassy 2024 rejection stats",
                                                     "is_speculative": False})
        print(json.dumps({"bayesian_update": res}, indent=2, ensure_ascii=False))

        # Dempster's combination
        m1 = {"TRUE": 0.60, "FALSE": 0.10, "UNCERTAIN": 0.30}
        m2 = {"TRUE": 0.70, "FALSE": 0.05, "UNCERTAIN": 0.25}
        ds_res = combine_dempster_shafer_evidence(m1, m2)
        print(json.dumps({"dempster_combination": ds_res}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
