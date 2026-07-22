#!/usr/bin/env python3
"""
LifeTree Prospect Theory (Kahneman-Tversky) Loss Aversion Engine
Evaluates human psychological choices under Loss Aversion (lambda = 2.25) vs Rational Economic Man expected monetary value.
"""

import sys
import json
import math
from typing import Dict, Any, List

LAMBDA_LOSS = 2.25 # Loss aversion multiplier
ALPHA = 0.88
BETA = 0.88

def value_func(x: float) -> float:
    if x >= 0:
        return math.pow(x, ALPHA)
    else:
        return -LAMBDA_LOSS * math.pow(abs(x), BETA)

def evaluate_prospect_theory(choice_a_payoffs: List[Dict[str, float]], choice_b_payoffs: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Compares Choice A vs Choice B under CPT (Cumulative Prospect Theory) vs Rational Expected Value (EV).
    """
    try:
        def calc_ev_and_cpt(payoffs):
            ev = sum(item["payoff_usd"] * item["prob"] for item in payoffs)
            cpt = sum(value_func(item["payoff_usd"]) * item["prob"] for item in payoffs)
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
        a = [{"payoff_usd": 30000.0, "prob": 0.80}, {"payoff_usd": -10000.0, "prob": 0.20}]
        b = [{"payoff_usd": 18000.0, "prob": 1.00}]
        res = evaluate_prospect_theory(a, b)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
