#!/usr/bin/env python3
"""
LifeTree Copula Systemic Risk Correlation Engine
Simulates correlated systemic risk cascades (macro downturn, income drop, currency devaluation)
using Gaussian Copula matrix transformations.
"""

import sys
import json
import random
import math
from typing import Dict, Any, List

def simulate_gaussian_copula_shocks(base_capital_usd: float = 40000.0, correlation_rho: float = 0.65, num_trials: int = 5000) -> Dict[str, Any]:
    """
    Simulates correlated systemic shocks via bivariate Gaussian Copula.
    """
    try:
        trials = max(100, int(num_trials))
        base_cap = float(base_capital_usd)
        rho = float(correlation_rho)
        rho = max(-0.99, min(0.99, rho))

        simulated_losses = []
        joint_disaster_trials = 0

        for _ in range(trials):
            z1 = random.gauss(0, 1)
            z2_ind = random.gauss(0, 1)
            z2 = rho * z1 + math.sqrt(max(0.0, 1.0 - rho**2)) * z2_ind

            # Correlated shocks
            macro_factor = math.exp(0.20 * z1)
            income_drop_factor = math.exp(0.30 * z2)

            loss = 15000.0 * macro_factor * income_drop_factor
            simulated_losses.append(loss)

            # Tail 95% joint disaster check
            if z1 > 1.64 and z2 > 1.64:
                joint_disaster_trials += 1

        simulated_losses.sort()
        var_95 = round(simulated_losses[int(trials * 0.95)], 2)
        cvar_95 = round(sum(simulated_losses[int(trials * 0.95):]) / len(simulated_losses[int(trials * 0.95):]), 2)

        return {
            "status": "SUCCESS",
            "copula_simulation": {
                "num_trials": trials,
                "correlation_rho": rho,
                "joint_tail_disaster_trials": joint_disaster_trials,
                "joint_disaster_prob_pct": round((joint_disaster_trials / trials) * 100.0, 2),
                "var_95_max_cost_usd": var_95,
                "cvar_expected_shortfall_usd": cvar_95,
                "tail_severity_ratio": round(cvar_95 / var_95, 3) if var_95 > 0 else 1.0
            }
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "COPULA_ENGINE_EXCEPTION", "message": str(e)}

def main():
    try:
        res = simulate_gaussian_copula_shocks(40000.0, 0.65, 5000)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
