#!/usr/bin/env python3
"""
LifeTree Prospect Theory (Kahneman-Tversky) Loss Aversion Engine
Implements Cumulative Prospect Theory (CPT) with loss aversion (lambda = 2.25),
probability weighting, and multi-choice comparison under behavioral economics.

Bug 3 consolidation: This module now subsumes the functionality previously
duplicated in decision_analysis/utility_theory_engine.py. The probability
weighting function (which the old decision_models/ version lacked) has been
merged in so callers get the full CPT implementation regardless of which
entry point they use.
"""

import sys
import json
import math
from typing import Dict, Any, List

# Kahneman-Tversky Prospect Theory Parameters
ALPHA = 0.88          # Gain exponent
BETA = 0.88           # Loss exponent
LAMBDA_LOSS = 2.25    # Loss Aversion Coefficient
GAMMA_GAIN = 0.61     # Probability Weighting Gain Parameter
DELTA_LOSS = 0.69     # Probability Weighting Loss Parameter


def value_function_prospect_theory(x: float) -> float:
    """
    Kahneman-Tversky Value Function v(x):
    v(x) = x^alpha if x >= 0 else -lambda * (-x)^beta
    """
    if x >= 0:
        return math.pow(x, ALPHA)
    else:
        return -LAMBDA_LOSS * math.pow(abs(x), BETA)


def probability_weighting_function(p: float, is_gain: bool = True) -> float:
    """
    Kahneman-Tversky Probability Weighting Function w(p).
    Overweights small probabilities, underweights moderate/high probabilities.
    """
    p = max(0.0001, min(0.9999, float(p)))
    gamma = GAMMA_GAIN if is_gain else DELTA_LOSS
    numerator = math.pow(p, gamma)
    denominator = math.pow(numerator + math.pow(1.0 - p, gamma), 1.0 / gamma)
    return numerator / denominator


# Backward-compatible alias (old decision_models/ name)
value_func = value_function_prospect_theory


def calculate_prospect_utility(outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates Cumulative Prospect Theory (CPT) Utility over a set of monetary/time outcomes.
    outcomes: list of dicts with {"payoff_usd": float, "probability": float}

    This is the primary CPT entry point, merged from decision_analysis/utility_theory_engine.py.
    It applies both the value function AND probability weighting (the old
    decision_models/ evaluate_prospect_theory only applied the value function
    without weighting, which underestimates small-probability tail events).
    """
    try:
        if not isinstance(outcomes, list):
            return {"status": "ERROR", "error_code": "INVALID_OUTCOMES", "message": "Expected list of outcome dicts"}

        cpt_utility = 0.0
        details = []

        for item in outcomes:
            payoff = float(item.get("payoff_usd", 0.0))
            prob = float(item.get("probability", item.get("prob", 0.5)))

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


def evaluate_prospect_theory(choice_a_payoffs: List[Dict[str, float]], choice_b_payoffs: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Compares Choice A vs Choice B under CPT (with probability weighting) vs
    Rational Expected Value (EV).

    Bug 3 consolidation: Now delegates to calculate_prospect_utility so both
    choices use the full CPT with probability weighting (previously this
    function skipped the weighting step, producing inconsistent results
    depending on which entry point the caller used). Accepts both "prob" and
    "probability" keys for backward compatibility.
    """
    try:
        def calc_ev_and_cpt(payoffs):
            ev = sum(float(item.get("payoff_usd", 0.0)) * float(item.get("probability", item.get("prob", 0.5))) for item in payoffs)
            cpt_res = calculate_prospect_utility(payoffs)
            cpt = cpt_res.get("cpt_utility_score", 0.0)
            return round(ev, 2), round(cpt, 2)

        ev_a, cpt_a = calc_ev_and_cpt(choice_a_payoffs)
        ev_b, cpt_b = calc_ev_and_cpt(choice_b_payoffs)

        rational_winner = "Choice A" if ev_a >= ev_b else "Choice B"
        human_psychology_winner = "Choice A" if cpt_a >= cpt_b else "Choice B"

        return {
            "status": "SUCCESS",
            "choice_a_metrics": {"expected_monetary_value_EV": ev_a, "prospect_theory_cpt_utility": cpt_a},
            "choice_b_metrics": {"expected_monetary_value_EV": ev_b, "prospect_theory_cpt_utility": cpt_b},
            "comparison": {
                "rational_economic_man_optimal": rational_winner,
                "human_psychology_acceptable": human_psychology_winner,
                "loss_aversion_divergence": rational_winner != human_psychology_winner
            }
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "PROSPECT_THEORY_EXCEPTION", "message": str(e)}


def main():
    try:
        # Demonstrate single-choice CPT
        cpt_res = calculate_prospect_utility([
            {"payoff_usd": 30000.0, "probability": 0.85},
            {"payoff_usd": -15000.0, "probability": 0.15}
        ])
        print(json.dumps({"single_choice_cpt": cpt_res}, indent=2, ensure_ascii=False))

        # Demonstrate dual-choice comparison
        a = [{"payoff_usd": 30000.0, "prob": 0.80}, {"payoff_usd": -10000.0, "prob": 0.20}]
        b = [{"payoff_usd": 18000.0, "prob": 1.00}]
        res = evaluate_prospect_theory(a, b)
        print(json.dumps({"dual_choice_comparison": res}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
