#!/usr/bin/env python3
"""
LifeTree Tail Risk CVaR (Conditional Value at Risk / Expected Shortfall) Engine
Extends Monte Carlo sampling results to calculate VaR_alpha vs CVaR_alpha (Expected Shortfall)
and evaluates extreme irreversible disaster risk warnings.
"""

import sys
import json
import math
from typing import Dict, Any, List

def calculate_cvar_metrics(simulated_costs_usd: List[float], alpha: float = 0.95, initial_capital_usd: float = 40000.0) -> Dict[str, Any]:
    """
    Calculates 95% VaR and 95% CVaR (Expected Shortfall).
    CVaR_alpha = E[Cost | Cost >= VaR_alpha]
    """
    try:
        if not isinstance(simulated_costs_usd, list) or not simulated_costs_usd:
            return {"status": "ERROR", "error_code": "INVALID_COSTS", "message": "Expected non-empty list for simulated_costs_usd"}

        costs = sorted([float(c) for c in simulated_costs_usd])
        n = len(costs)
        var_idx = int(math.floor(alpha * n))
        var_idx = min(var_idx, n - 1)

        var_95 = costs[var_idx]
        tail_costs = costs[var_idx:]
        cvar_95 = sum(tail_costs) / len(tail_costs) if tail_costs else var_95

        # Check for irreversible capital bankruptcy (CVaR cost exceeding available liquid capital)
        is_capital_bankruptcy_risk = cvar_95 > initial_capital_usd
        tail_severity_ratio = round(cvar_95 / var_95, 3) if var_95 > 0 else 1.0

        risk_warning_level = "LOW_RISK"
        risk_alert_msg = "Path capital costs remain within normal statistical volatility boundaries."

        if is_capital_bankruptcy_risk:
            risk_warning_level = "CRITICAL_TAIL_DISASTER_WARNING"
            risk_alert_msg = f"⚠️ CRITICAL: Tail Expected Shortfall (${cvar_95:,.2f}) EXCEEDS available capital (${initial_capital_usd:,.2f}). High risk of irreversible insolvency!"
        elif tail_severity_ratio > 1.25:
            risk_warning_level = "HIGH_TAIL_FAT_TAIL_WARNING"
            risk_alert_msg = "⚠️ WARNING: Fat-tail disaster distribution detected! CVaR expected shortfall significantly exceeds VaR limit."

        return {
            "status": "SUCCESS",
            "confidence_alpha": alpha,
            "var_95_max_cost_usd": round(var_95, 2),
            "cvar_expected_shortfall_usd": round(cvar_95, 2),
            "tail_severity_ratio": tail_severity_ratio,
            "initial_capital_usd": initial_capital_usd,
            "capital_bankruptcy_risk": is_capital_bankruptcy_risk,
            "risk_warning_level": risk_warning_level,
            "risk_alert_message": risk_alert_msg
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "CVAR_ENGINE_EXCEPTION", "message": str(e)}

def main():
    try:
        # Sample 10,000 simulated costs with fat tail
        import random
        sim_costs = [15000.0 * random.lognormvariate(0, 0.3) for _ in range(5000)]
        res = calculate_cvar_metrics(sim_costs, alpha=0.95, initial_capital_usd=25000.0)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
