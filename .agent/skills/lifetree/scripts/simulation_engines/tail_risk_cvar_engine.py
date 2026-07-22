#!/usr/bin/env python3
"""
LifeTree Tail Risk CVaR & Copula Dependency Engine
Calculates Conditional Value at Risk (CVaR / Expected Shortfall ES_0.95) and systemic risk correlation using Copula structures.
"""

import sys
import json
import random
import math
from typing import Dict, Any, List

def calculate_cvar_expected_shortfall(simulated_losses: List[float], alpha: float = 0.95) -> Dict[str, Any]:
    """
    Calculates VaR_alpha and CVaR_alpha (Expected Shortfall / Average Loss in Tail 1 - alpha).
    CVaR_alpha = E[Loss | Loss >= VaR_alpha]
    """
    try:
        if not isinstance(simulated_losses, list) or not simulated_losses:
            return {"status": "ERROR", "error_code": "INVALID_LOSSES", "message": "Expected non-empty list of simulated_losses"}

        losses = sorted([float(x) for x in simulated_losses])
        n = len(losses)
        var_idx = int(math.floor(alpha * n))
        var_idx = min(var_idx, n - 1)

        var_alpha = losses[var_idx]
        tail_losses = losses[var_idx:]
        cvar_alpha = sum(tail_losses) / len(tail_losses) if tail_losses else var_alpha

        return {
            "status": "SUCCESS",
            "alpha_confidence": alpha,
            "var_value_at_risk": round(var_alpha, 2),
            "cvar_expected_shortfall": round(cvar_alpha, 2),
            "tail_sample_size": len(tail_losses),
            "tail_severity_ratio": round(cvar_alpha / var_alpha, 3) if var_alpha > 0 else 1.0
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "CVAR_CALCULATION_EXCEPTION", "message": str(e)}

def simulate_copula_systemic_risks(base_cost: float = 15000.0, correlation_rho: float = 0.65, num_trials: int = 5000) -> Dict[str, Any]:
    """
    Simulates correlated systemic risks using Gaussian Copula transformation.
    Correlates Macro Economy Shock, Income Loss, and FX Asset Depreciation.
    """
    try:
        trials = max(100, int(num_trials))
        joint_disaster_count = 0
        losses = []

        for _ in range(trials):
            # Generate correlated normal variables via Cholesky decomposition
            z1 = random.gauss(0, 1)
            z2_independent = random.gauss(0, 1)
            z2 = correlation_rho * z1 + math.sqrt(max(0.0, 1.0 - correlation_rho**2)) * z2_independent

            # Transform to cost shocks
            macro_shock = math.exp(0.25 * z1)
            income_drop_shock = math.exp(0.35 * z2)
            total_loss = base_cost * macro_shock * income_drop_shock

            losses.append(total_loss)

            # Systemic disaster threshold: both z1 > 1.64 and z2 > 1.64 (tail 95%)
            if z1 > 1.64 and z2 > 1.64:
                joint_disaster_count += 1

        cvar_res = calculate_cvar_expected_shortfall(losses, alpha=0.95)

        return {
            "status": "SUCCESS",
            "copula_simulation": {
                "num_trials": trials,
                "correlation_rho": correlation_rho,
                "joint_tail_disaster_trials": joint_disaster_count,
                "joint_disaster_prob_pct": round((joint_disaster_count / trials) * 100.0, 2),
                "var_95_max_cost_usd": cvar_res["var_value_at_risk"],
                "cvar_expected_shortfall_usd": cvar_res["cvar_expected_shortfall"],
                "tail_severity_ratio": cvar_res["tail_severity_ratio"]
            }
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "COPULA_SIMULATION_EXCEPTION", "message": str(e)}

def main():
    try:
        res = simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=5000)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
