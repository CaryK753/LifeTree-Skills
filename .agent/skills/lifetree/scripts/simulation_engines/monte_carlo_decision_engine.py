#!/usr/bin/env python3
"""
LifeTree Monte Carlo Stochastic Decision Simulation & Tail Risk Engine
Runs 10,000 stochastic simulation trials over decision pathways to calculate P10/P50/P90 confidence intervals,
Value at Risk (VaR), and tail risk probabilities with robust error handling.
"""

import sys
import os
import json
import random
import math
from typing import Dict, Any, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    import config_loader
except ImportError:
    config_loader = None

def run_monte_carlo_simulation(pathway_config: Dict[str, Any], num_trials: int = None) -> Dict[str, Any]:
    """
    Runs stochastic Monte Carlo trials over a pathway.
    """
    try:
        if not isinstance(pathway_config, dict):
            return {"status": "ERROR", "error_code": "INVALID_CONFIG", "message": "Expected dict for pathway_config"}

        cfg_defaults = config_loader.load_config().get("monte_carlo", {}) if config_loader else {}
        trials = num_trials or pathway_config.get("num_trials") or cfg_defaults.get("default_trials", 10000)
        trials = max(100, int(trials))

        base_time_months = float(pathway_config.get("base_time_months", 24))
        base_cost_usd = float(pathway_config.get("base_cost_usd", 15000.0))
        baseline_success_prob = float(pathway_config.get("baseline_success_prob", 0.85))
        volatility = float(pathway_config.get("volatility_factor") or cfg_defaults.get("volatility_factor", 0.25))

        successful_trials = 0
        simulated_times = []
        simulated_costs = []

        seed = pathway_config.get("random_seed")
        if seed is not None:
            random.seed(seed)

        for _ in range(trials):
            is_success = (random.random() <= baseline_success_prob)
            if is_success:
                successful_trials += 1

            time_noise = random.gauss(0, base_time_months * volatility)
            actual_time = max(1.0, base_time_months + time_noise)
            simulated_times.append(actual_time)

            cost_noise = random.lognormvariate(0, volatility * 0.5)
            actual_cost = base_cost_usd * cost_noise
            simulated_costs.append(actual_cost)

        simulated_times.sort()
        simulated_costs.sort()

        overall_success_rate = round((successful_trials / trials) * 100.0, 2)

        p10_time = round(simulated_times[int(trials * 0.10)], 1)
        p50_time = round(simulated_times[int(trials * 0.50)], 1)
        p90_time = round(simulated_times[int(trials * 0.90)], 1)

        p10_cost = round(simulated_costs[int(trials * 0.10)], 2)
        p50_cost = round(simulated_costs[int(trials * 0.50)], 2)
        p90_cost = round(simulated_costs[int(trials * 0.90)], 2)

        var_95_cost = round(simulated_costs[int(trials * 0.95)], 2)
        var_95_time = round(simulated_times[int(trials * 0.95)], 1)

        return {
            "status": "SUCCESS",
            "pathway_name": pathway_config.get("name", "Target Pathway"),
            "simulation_config": {
                "num_trials": trials,
                "baseline_success_prob": baseline_success_prob,
                "volatility_factor": volatility
            },
            "monte_carlo_results": {
                "total_trials_simulated": trials,
                "overall_success_rate_pct": overall_success_rate,
                "execution_timeline_months": {
                    "P10_optimistic": p10_time,
                    "P50_median": p50_time,
                    "P90_pessimistic": p90_time,
                    "VaR_95_max_time": var_95_time,
                    "VaR_95_max_timeline": f"{var_95_time} Months"
                },
                "financial_capital_usd": {
                    "P10_optimistic": p10_cost,
                    "P50_median": p50_cost,
                    "P90_pessimistic": p90_cost,
                    "VaR_95_max_cost": var_95_cost
                }
            },
            "tail_risk_verdict": "LOW_VOLATILITY" if volatility < 0.2 else ("MODERATE_VOLATILITY" if volatility < 0.35 else "HIGH_TAIL_RISK_WARNING")
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_code": "MONTE_CARLO_ENGINE_EXCEPTION",
            "message": str(e)
        }

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                cfg = json.load(f)
        else:
            cfg = {
                "name": "EU Blue Card Skilled Pathway",
                "base_time_months": 24,
                "base_cost_usd": 15000.0,
                "baseline_success_prob": 0.88,
                "volatility_factor": 0.25,
                "random_seed": 42
            }

        res = run_monte_carlo_simulation(cfg, num_trials=10000)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
