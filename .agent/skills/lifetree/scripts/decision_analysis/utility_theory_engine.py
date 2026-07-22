#!/usr/bin/env python3
"""
LifeTree Prospect Theory & Multi-Attribute Utility Theory (MAUT) Engine
Implements Kahneman-Tversky Prospect Theory (Loss Aversion & Probability Weighting)
and Multi-Attribute Utility Theory (MAUT) for human behavioral personal decision modeling.
"""

import sys
import json
import math
from typing import Dict, Any, List

# Kahneman-Tversky Prospect Theory Parameters
ALPHA = 0.88
BETA = 0.88
LAMBDA_LOSS = 2.25  # Loss Aversion Coefficient
GAMMA_GAIN = 0.61   # Probability Weighting Gain Parameter
DELTA_LOSS = 0.69   # Probability Weighting Loss Parameter

def value_function_prospect_theory(x: float) -> float:
    """
    Calculates Kahneman-Tversky Value Function v(x):
    v(x) = x^alpha if x >= 0 else -lambda * (-x)^beta
    """
    if x >= 0:
        return math.pow(x, ALPHA)
    else:
        return -LAMBDA_LOSS * math.pow(abs(x), BETA)

def probability_weighting_function(p: float, is_gain: bool = True) -> float:
    """
    Calculates Kahneman-Tversky Probability Weighting Function w(p):
    Overweights small probabilities, underweights moderate/high probabilities.
    """
    p = max(0.0001, min(0.9999, float(p)))
    gamma = GAMMA_GAIN if is_gain else DELTA_LOSS
    numerator = math.pow(p, gamma)
    denominator = math.pow(numerator + math.pow(1.0 - p, gamma), 1.0 / gamma)
    return numerator / denominator

def calculate_prospect_utility(outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates Cumulative Prospect Theory (CPT) Utility over a set of monetary/time outcomes.
    outcomes: list of dicts with {"payoff_usd": float, "probability": float}
    """
    try:
        if not isinstance(outcomes, list):
            return {"status": "ERROR", "error_code": "INVALID_OUTCOMES", "message": "Expected list of outcome dicts"}

        cpt_utility = 0.0
        details = []

        for item in outcomes:
            payoff = float(item.get("payoff_usd", 0.0))
            prob = float(item.get("probability", 0.5))

            v_x = value_function_prospect_theory(payoff)
            w_p = probability_weighting_function(prob, is_gain=(payoff >= 0))
            weighted_utility = v_x * w_p
            cpt_utility += weighted_utility

            details.append({
                "payoff_usd": payoff,
                "raw_probability": prob,
                "prospect_value_v": round(v_x, 4),
                "weighted_prob_w": round(w_p, 4),
                "weighted_utility_contrib": round(weighted_utility, 4)
            })

        return {
            "status": "SUCCESS",
            "cpt_utility_score": round(cpt_utility, 4),
            "loss_aversion_coef": LAMBDA_LOSS,
            "outcome_details": details
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "PROSPECT_THEORY_EXCEPTION", "message": str(e)}

def calculate_maut_utility(attributes: Dict[str, Any], weights: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Calculates Multi-Attribute Utility (MAUT) across 5 personal life dimensions:
    Income/Wealth, Health, Time Freedom, Family Security, Stress (Inverted).
    """
    try:
        if not isinstance(attributes, dict):
            return {"status": "ERROR", "error_code": "INVALID_ATTRIBUTES", "message": "Expected dict for attributes"}

        default_weights = {
            "income": 0.25,
            "health": 0.25,
            "time_freedom": 0.20,
            "family_security": 0.20,
            "stress_inverted": 0.10
        }
        w = weights or default_weights

        # Normalize total weights to 1.0
        total_w = sum(w.values())
        norm_w = {k: v / total_w for k, v in w.items()}

        total_maut = 0.0
        score_breakdown = {}

        for k, weight in norm_w.items():
            val = float(attributes.get(k, 50.0)) # Scale 0 to 100
            val = max(0.0, min(100.0, val))
            contrib = val * weight
            total_maut += contrib
            score_breakdown[k] = {
                "raw_score_0_100": val,
                "attribute_weight": round(weight, 4),
                "weighted_contrib": round(contrib, 4)
            }

        return {
            "status": "SUCCESS",
            "maut_total_utility_score": round(total_maut, 2),
            "attribute_breakdown": score_breakdown
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "MAUT_EXCEPTION", "message": str(e)}

def main():
    try:
        cpt_res = calculate_prospect_utility([
            {"payoff_usd": 30000.0, "probability": 0.85},
            {"payoff_usd": -15000.0, "probability": 0.15}
        ])
        maut_res = calculate_maut_utility({
            "income": 80.0, "health": 85.0, "time_freedom": 60.0, "family_security": 90.0, "stress_inverted": 70.0
        })
        print(json.dumps({"cpt_result": cpt_res, "maut_result": maut_res}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
