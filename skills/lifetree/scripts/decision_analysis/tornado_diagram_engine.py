#!/usr/bin/env python3
"""
LifeTree Tornado Diagram Risk Sensitivity Engine
Generates Tornado Diagram analysis ranking external parameters (processing delays, exchange rates,
salary threshold hikes, exam pass rates) by their volatility swing impact on decision success.
"""

import sys
import json
from typing import Dict, Any, List

def calculate_tornado_sensitivity_swings(pathway_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes low/base/high outcome swings for decision parameters to construct Tornado Diagrams.
    """
    base_success = pathway_params.get("base_success_prob", 0.85)

    parameters = [
        {
            "parameter_name": "Statutory Processing Time (Embassy Delay)",
            "base_value": "6 Months",
            "low_swing_val": "3 Months",
            "high_swing_val": "12 Months",
            "success_prob_at_low": round(min(0.98, base_success + 0.10), 2),
            "success_prob_at_high": round(max(0.20, base_success - 0.35), 2),
            "volatility_swing": 0.45,
            "impact_rank": 1
        },
        {
            "parameter_name": "Minimum Salary Threshold (§ 18g Blue Card)",
            "base_value": "€45,300/yr",
            "low_swing_val": "€41,000/yr",
            "high_swing_val": "€50,000/yr",
            "success_prob_at_low": round(min(0.98, base_success + 0.08), 2),
            "success_prob_at_high": round(max(0.20, base_success - 0.25), 2),
            "volatility_swing": 0.33,
            "impact_rank": 2
        },
        {
            "parameter_name": "EUR/USD Currency Exchange Rate Volatility",
            "base_value": "1.08",
            "low_swing_val": "1.02",
            "high_swing_val": "1.15",
            "success_prob_at_low": round(min(0.98, base_success + 0.04), 2),
            "success_prob_at_high": round(max(0.20, base_success - 0.12), 2),
            "volatility_swing": 0.16,
            "impact_rank": 3
        }
    ]

    parameters.sort(key=lambda x: x["volatility_swing"], reverse=True)
    for i, p in enumerate(parameters):
        p["impact_rank"] = i + 1

    return {
        "tornado_analysis_summary": {
            "parameters_audited_count": len(parameters),
            "top_risk_driver": parameters[0]["parameter_name"],
            "max_volatility_swing": parameters[0]["volatility_swing"]
        },
        "tornado_diagram_swings": parameters
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    else:
        cfg = {"base_success_prob": 0.85}

    res = calculate_tornado_sensitivity_swings(cfg)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
