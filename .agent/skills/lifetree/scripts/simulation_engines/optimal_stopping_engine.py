#!/usr/bin/env python3
"""
LifeTree Optimal Stopping & Hyperbolic Discounting Engine
Calculates optimal timing thresholds for job pivots and asset liquidations (37% rule / Snell Envelope)
and models behavioral hyperbolic time discounting U(t) = V / (1 + k*t).
"""

import sys
import json
import math
from typing import Dict, Any, List

def calculate_optimal_stopping_threshold(total_options_count: int, observation_ratio: float = 0.368) -> Dict[str, Any]:
    """
    Calculates 37% Optimal Stopping Rule (Secretarial Problem / Snell Envelope threshold).
    observation_count = round(n / e) = n * 0.368
    """
    try:
        n = max(1, int(total_options_count))
        cutoff = int(math.floor(n * observation_ratio))
        cutoff = max(1, min(n - 1, cutoff)) if n > 1 else 1

        return {
            "status": "SUCCESS",
            "optimal_stopping_rule": {
                "total_opportunities_n": n,
                "observation_cutoff_sample_k": cutoff,
                "rule_strategy": f"Observe and reject the first {cutoff} opportunities; accept the very next opportunity that ranks better than all previous ones.",
                "theoretical_success_prob_pct": round(observation_ratio * 100.0, 2)
            }
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "OPTIMAL_STOPPING_EXCEPTION", "message": str(e)}

def calculate_hyperbolic_discounting(future_value_usd: float, delay_years: float, discount_k: float = 0.15) -> Dict[str, Any]:
    """
    Calculates Hyperbolic Discounting Present Utility:
    U(t) = V / (1 + k * t)
    Compares against exponential discounting PVE = V * (1 + r)^(-t).
    """
    try:
        v = float(future_value_usd)
        t = max(0.0, float(delay_years))
        k = float(discount_k)

        # Hyperbolic Present Value
        hyperbolic_pv = v / (1.0 + k * t)

        # Exponential Present Value for comparison (r = 0.05)
        exponential_pv = v * math.pow(1.0 + 0.05, -t)

        return {
            "status": "SUCCESS",
            "future_nominal_value_usd": v,
            "delay_years": t,
            "discount_parameter_k": k,
            "hyperbolic_present_utility_usd": round(hyperbolic_pv, 2),
            "exponential_present_value_usd": round(exponential_pv, 2),
            "present_bias_ratio": round(hyperbolic_pv / v, 4) if v > 0 else 1.0
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "HYPERBOLIC_DISCOUNTING_EXCEPTION", "message": str(e)}

def main():
    try:
        os_res = calculate_optimal_stopping_threshold(total_options_count=10)
        hd_res = calculate_hyperbolic_discounting(future_value_usd=100000.0, delay_years=5.0, discount_k=0.15)
        print(json.dumps({"optimal_stopping_result": os_res, "hyperbolic_discounting_result": hd_res}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
