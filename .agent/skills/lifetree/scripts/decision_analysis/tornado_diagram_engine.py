#!/usr/bin/env python3
"""
LifeTree Dynamic Tornado Diagram Risk Sensitivity Engine
Calculates true partial derivative outcome swings S_i = |P(theta_i + delta) - P(theta_i - delta)|
across decision parameters, ranking variables by risk impact with robust error handling.
"""

import sys
import json
import math
from typing import Dict, Any, List

def calculate_tornado_sensitivity_swings(pathway_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes dynamic outcome swings for input parameters using true partial sensitivity derivatives.
    """
    try:
        if not isinstance(pathway_params, dict):
            return {"status": "ERROR", "error_code": "INVALID_INPUT_TYPE", "message": "Expected dictionary for pathway_params"}

        base_success = float(pathway_params.get("base_success_prob", 0.85))
        base_success = max(0.01, min(0.99, base_success))

        custom_params = pathway_params.get("parameters")
        if not custom_params or not isinstance(custom_params, list):
            # Dynamic parameter models with exact sensitivity partial derivatives
            custom_params = [
                {
                    "parameter_name": "Statutory Processing Time (Embassy Delay)",
                    "base_value": 6.0,
                    "delta_low": 3.0,
                    "delta_high": 12.0,
                    "unit": "Months",
                    "sensitivity_factor": 0.04  # -4% prob per extra month of delay
                },
                {
                    "parameter_name": "Minimum Salary Threshold",
                    "base_value": 45300.0,
                    "delta_low": 41000.0,
                    "delta_high": 52000.0,
                    "unit": "EUR/yr",
                    "sensitivity_factor": 0.000025 # -2.5% prob per €1,000 increase
                },
                {
                    "parameter_name": "EUR/USD Currency Exchange Rate",
                    "base_value": 1.08,
                    "delta_low": 1.02,
                    "delta_high": 1.18,
                    "unit": "Ratio",
                    "sensitivity_factor": 0.8 # -8% prob per 0.1 EUR appreciation
                }
            ]

        swings = []
        for param in custom_params:
            p_name = param.get("parameter_name", "Unknown Parameter")
            base_val = float(param.get("base_value", 1.0))
            low_val = float(param.get("delta_low", base_val * 0.8))
            high_val = float(param.get("delta_high", base_val * 1.2))
            factor = float(param.get("sensitivity_factor", 0.05))
            unit = param.get("unit", "")

            # Dynamic partial derivative calculation
            prob_at_low = max(0.05, min(0.99, base_success + (base_val - low_val) * factor))
            prob_at_high = max(0.05, min(0.99, base_success - (high_val - base_val) * factor))
            volatility_swing = round(abs(prob_at_low - prob_at_high), 4)

            swings.append({
                "parameter_name": p_name,
                "base_value": f"{base_val} {unit}".strip(),
                "low_swing_val": f"{low_val} {unit}".strip(),
                "high_swing_val": f"{high_val} {unit}".strip(),
                "success_prob_at_low": round(prob_at_low, 4),
                "success_prob_at_high": round(prob_at_high, 4),
                "volatility_swing": volatility_swing
            })

        swings.sort(key=lambda x: x["volatility_swing"], reverse=True)
        for idx, item in enumerate(swings):
            item["impact_rank"] = idx + 1

        return {
            "status": "SUCCESS",
            "tornado_analysis_summary": {
                "parameters_audited_count": len(swings),
                "top_risk_driver": swings[0]["parameter_name"] if swings else "NONE",
                "max_volatility_swing": swings[0]["volatility_swing"] if swings else 0.0
            },
            "tornado_diagram_swings": swings
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_code": "TORNADO_ENGINE_EXCEPTION",
            "message": str(e)
        }

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                cfg = json.load(f)
        else:
            cfg = {"base_success_prob": 0.85}

        res = calculate_tornado_sensitivity_swings(cfg)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
