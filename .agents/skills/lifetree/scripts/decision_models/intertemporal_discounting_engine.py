#!/usr/bin/env python3
"""
LifeTree Intertemporal Utility Discounting Engine
Computes Exponential Discounting (Classical) vs Hyperbolic Discounting (Behavioral Present Bias)
to correct systemic overestimation of far-future decision payoffs.
"""

import sys
import json
import math
from typing import Dict, Any, List

def calculate_intertemporal_discounting(nominal_future_value_usd: float, delay_years: float, discount_k: float = 0.15, exponential_rate_r: float = 0.05) -> Dict[str, Any]:
    """
    Computes hyperbolic utility discounting U(t) = V / (1 + k*t) and exponential discounting PV = V * e^(-r*t).
    """
    try:
        v = float(nominal_future_value_usd)
        t = max(0.0, float(delay_years))
        k = float(discount_k)
        r = float(exponential_rate_r)

        # 1. Hyperbolic Discounting (Behavioral Economics Present Bias)
        hyperbolic_utility = v / (1.0 + k * t)

        # 2. Exponential Discounting (Classical Economics)
        exponential_utility = v * math.exp(-r * t)

        present_bias_ratio = round(hyperbolic_utility / v, 4) if v > 0 else 1.0

        return {
            "status": "SUCCESS",
            "nominal_future_value_usd": v,
            "delay_years": t,
            "hyperbolic_discounted_utility_usd": round(hyperbolic_utility, 2),
            "exponential_discounted_utility_usd": round(exponential_utility, 2),
            "present_bias_ratio": present_bias_ratio,
            "discounting_summary": f"A ${v:,.0f} payoff in {t} years is subjectively valued at ${hyperbolic_utility:,.2f} today under behavioral hyperbolic discounting."
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "DISCOUNTING_ENGINE_EXCEPTION", "message": str(e)}

def main():
    try:
        res = calculate_intertemporal_discounting(100000.0, 5.0, discount_k=0.15, exponential_rate_r=0.05)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
