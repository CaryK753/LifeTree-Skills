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

def simulate_copula_systemic_risks(base_cost: float = 15000.0, correlation_rho: float = 0.65,
                                   num_trials: int = 5000, volatility: float = 0.25,
                                   shock_magnitude_macro: float = None,
                                   shock_magnitude_income: float = None) -> Dict[str, Any]:
    """
    Simulates correlated systemic risks using Gaussian Copula transformation.
    Correlates Macro Economy Shock, Income Loss, and FX Asset Depreciation.

    C2 fix: Shock magnitudes are now mean-preserving (mu = -b^2/2 so E[shock]=1.0)
    and parameterized by `volatility` (default 0.25, matching Monte Carlo). With the
    default volatility=0.25 and correlation_rho=0.65, the Copula VaR95 lands within
    ~5-15% of the Monte Carlo VaR95 for the same base_cost — previously the Copula
    used exp(0.25*z1)*exp(0.35*z2) which inflated VaR95 by ~2x vs Monte Carlo.

    The shock betas default to volatility * 0.6 (≈0.15 for vol=0.25). At rho=0.65
    this gives combined log-shock 95th percentile ≈ 1.645 * sqrt(2*b² + 2*rho*b²) - b²
    = 0.425, so VaR95 ≈ exp(0.425) * base_cost ≈ 1.53 * base_cost, vs Monte Carlo's
    1.46 * base_cost — within 5%.
    """
    try:
        trials = max(100, int(num_trials))
        # C2: scale shock betas from volatility (same parameter Monte Carlo uses)
        b_macro = float(shock_magnitude_macro) if shock_magnitude_macro is not None else float(volatility) * 0.6
        b_income = float(shock_magnitude_income) if shock_magnitude_income is not None else float(volatility) * 0.6

        joint_disaster_count = 0
        losses = []

        # Pre-compute mean-preserving offsets so E[macro_shock] = E[income_shock] = 1
        macro_mu = -0.5 * b_macro * b_macro
        income_mu = -0.5 * b_income * b_income

        for _ in range(trials):
            # Generate correlated normal variables via Cholesky decomposition
            z1 = random.gauss(0, 1)
            z2_independent = random.gauss(0, 1)
            z2 = correlation_rho * z1 + math.sqrt(max(0.0, 1.0 - correlation_rho**2)) * z2_independent

            # C2 fix: mean-preserving lognormal shocks (E[shock] = 1, same as Monte Carlo).
            # Old formula exp(0.25*z1)*exp(0.35*z2) had E[shock] > 1 and 95th percentile
            # of base_cost * 2.67 — wildly out of line with Monte Carlo.
            macro_shock = math.exp(macro_mu + b_macro * z1)
            income_drop_shock = math.exp(income_mu + b_income * z2)
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
                "volatility": float(volatility),
                "shock_magnitude_macro": b_macro,
                "shock_magnitude_income": b_income,
                "shock_parameterization": "MEAN_PRESERVING_LOGNORMAL (mu = -b²/2)",
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
