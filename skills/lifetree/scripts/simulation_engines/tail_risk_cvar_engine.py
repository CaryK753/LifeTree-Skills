#!/usr/bin/env python3
"""
LifeTree Tail Risk CVaR & Copula Dependency Engine
Simulates correlated systemic risks using Gaussian Copula transformation and
delegates VaR/CVaR calculation to the canonical cvar_risk_engine in decision_models/.

Bug 3 consolidation: The standalone calculate_cvar_expected_shortfall() function
has been removed — it duplicated cvar_risk_engine.calculate_cvar_metrics(). The
Copula simulation now delegates to cvar_risk_engine for VaR/CVaR so there is a
single source of truth for tail-risk computation. This module retains its unique
Copula simulation logic (which has no duplicate anywhere else).
"""

import sys
import os
import json
import random
import math
from typing import Dict, Any, List

# Bug 3: delegate CVaR calculation to the canonical decision_models/ engine
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(os.path.dirname(_SCRIPT_DIR))
_DECISION_MODELS_DIR = os.path.join(_SKILL_ROOT, "scripts", "decision_models")
if _DECISION_MODELS_DIR not in sys.path:
    sys.path.insert(0, _DECISION_MODELS_DIR)

try:
    import cvar_risk_engine
except ImportError:
    cvar_risk_engine = None


def simulate_copula_systemic_risks(base_cost: float = 15000.0, correlation_rho: float = 0.65,
                                   num_trials: int = 5000, volatility: float = 0.25,
                                   shock_magnitude_macro: float = None,
                                   shock_magnitude_income: float = None,
                                   initial_capital_usd: float = None) -> Dict[str, Any]:
    """
    Simulates correlated systemic risks using Gaussian Copula transformation.
    Correlates Macro Economy Shock, Income Loss, and FX Asset Depreciation.

    C2 fix: Shock magnitudes are now mean-preserving (mu = -b^2/2 so E[shock]=1.0)
    and parameterized by `volatility` (default 0.25, matching Monte Carlo). With the
    default volatility=0.25 and correlation_rho=0.65, the Copula VaR95 lands within
    ~5-15% of the Monte Carlo VaR95 for the same base_cost.

    Bug 3: VaR/CVaR now computed via cvar_risk_engine.calculate_cvar_metrics() (the
    canonical CVaR engine) instead of a local duplicate. If initial_capital_usd is
    supplied, the response also includes bankruptcy-risk assessment.

    Bug 6: Callers can now pass simulated_costs directly via the
    `calculate_cvar_from_mc_costs()` helper to avoid running a separate Copula
    simulation when Monte Carlo costs are already available.
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
            macro_shock = math.exp(macro_mu + b_macro * z1)
            income_drop_shock = math.exp(income_mu + b_income * z2)
            total_loss = base_cost * macro_shock * income_drop_shock

            losses.append(total_loss)

            # Systemic disaster threshold: both z1 > 1.64 and z2 > 1.64 (tail 95%)
            if z1 > 1.64 and z2 > 1.64:
                joint_disaster_count += 1

        # Bug 3: delegate to canonical cvar_risk_engine (single source of truth)
        if cvar_risk_engine is not None:
            cvar_kwargs = {"alpha": 0.95}
            if initial_capital_usd is not None:
                cvar_kwargs["initial_capital_usd"] = initial_capital_usd
            cvar_res = cvar_risk_engine.calculate_cvar_metrics(losses, **cvar_kwargs)
        else:
            # Fallback if import failed (should not happen in normal operation)
            cvar_res = _fallback_cvar(losses, alpha=0.95)

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
                "var_95_max_cost_usd": cvar_res.get("var_95_max_cost_usd", cvar_res.get("var_value_at_risk")),
                "cvar_expected_shortfall_usd": cvar_res.get("cvar_expected_shortfall_usd", cvar_res.get("cvar_expected_shortfall")),
                "tail_severity_ratio": cvar_res.get("tail_severity_ratio"),
                "cvar_engine_source": "decision_models/cvar_risk_engine"
            }
        }
    except Exception as e:
        return {"status": "ERROR", "error_code": "COPULA_SIMULATION_EXCEPTION", "message": str(e)}


def calculate_cvar_from_mc_costs(simulated_costs: List[float],
                                  alpha: float = 0.95,
                                  initial_capital_usd: float = None) -> Dict[str, Any]:
    """
    Bug 6: Compute VaR/CVaR directly from Monte Carlo simulated costs without
    running a separate Copula simulation. This avoids the "same scenario, two
    sets of numbers" problem when MC costs are already available.

    Delegates to cvar_risk_engine.calculate_cvar_metrics() (the canonical CVaR
    engine) so there is a single source of truth for tail-risk computation.
    """
    if cvar_risk_engine is not None:
        kwargs = {"alpha": alpha}
        if initial_capital_usd is not None:
            kwargs["initial_capital_usd"] = initial_capital_usd
        return cvar_risk_engine.calculate_cvar_metrics(simulated_costs, **kwargs)
    return _fallback_cvar(simulated_costs, alpha=alpha)


def _fallback_cvar(losses: List[float], alpha: float = 0.95) -> Dict[str, Any]:
    """Minimal fallback if cvar_risk_engine import fails."""
    losses_sorted = sorted([float(x) for x in losses])
    n = len(losses_sorted)
    var_idx = min(int(math.floor(alpha * n)), n - 1)
    var_alpha = losses_sorted[var_idx]
    tail = losses_sorted[var_idx:]
    cvar_alpha = sum(tail) / len(tail) if tail else var_alpha
    return {
        "status": "SUCCESS",
        "var_95_max_cost_usd": round(var_alpha, 2),
        "cvar_expected_shortfall_usd": round(cvar_alpha, 2),
        "tail_severity_ratio": round(cvar_alpha / var_alpha, 3) if var_alpha > 0 else 1.0
    }


def main():
    try:
        res = simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=5000)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
