#!/usr/bin/env python3
"""
LifeTree Monte Carlo Stochastic Decision Simulation & Tail Risk Engine
Runs 10,000 stochastic simulation trials over decision pathways to calculate P10/P50/P90 confidence intervals,
Value at Risk (VaR), and tail risk probabilities.
"""

import sys
import json
import random
import math
from typing import Dict, Any, List

def run_monte_carlo_simulation(pathway_config: Dict[str, Any], num_trials: int = 5000) -> Dict[str, Any]:
    """
    Runs stochastic Monte Carlo trials over a pathway.
    Stochastic variables:
    - Base execution time (months) + random normal delay
    - Base cost (USD) + random lognormal inflation shock
    - Success outcome (Bernoulli trial based on baseline probability)
    """
    base_time_months = pathway_config.get("base_time_months", 24)
    base_cost_usd = pathway_config.get("base_cost_usd", 15000.0)
    baseline_success_prob = pathway_config.get("baseline_success_prob", 0.85)
    volatility = pathway_config.get("volatility_factor", 0.2) # 0.1 to 0.5

    successful_trials = 0
    simulated_times = []
    simulated_costs = []

    # Set deterministic seed if provided for reproducible testing
    seed = pathway_config.get("random_seed")
    if seed is not None:
        random.seed(seed)

    for _ in range(num_trials):
        # 1. Success trial (Bernoulli)
        is_success = (random.random() <= baseline_success_prob)
        if is_success:
            successful_trials += 1

        # 2. Time delay (Truncated Normal distribution)
        time_noise = random.gauss(0, base_time_months * volatility)
        actual_time = max(1.0, base_time_months + time_noise)
        simulated_times.append(actual_time)

        # 3. Cost inflation (Lognormal distribution)
        cost_noise = random.lognormvariate(0, volatility * 0.5)
        actual_cost = base_cost_usd * cost_noise
        simulated_costs.append(actual_cost)

    simulated_times.sort()
    simulated_costs.sort()

    overall_success_rate = round((successful_trials / num_trials) * 100.0, 2)

    # Percentiles: P10 (optimistic), P50 (median), P90 (pessimistic / VaR)
    p10_time = round(simulated_times[int(num_trials * 0.10)], 1)
    p50_time = round(simulated_times[int(num_trials * 0.50)], 1)
    p90_time = round(simulated_times[int(num_trials * 0.90)], 1)

    p10_cost = round(simulated_costs[int(num_trials * 0.10)], 2)
    p50_cost = round(simulated_costs[int(num_trials * 0.50)], 2)
    p90_cost = round(simulated_costs[int(num_trials * 0.90)], 2)

    # Value at Risk (VaR 95%): Maximum expected cost at 95% confidence level
    var_95_cost = round(simulated_costs[int(num_trials * 0.95)], 2)
    var_95_time = round(simulated_times[int(num_trials * 0.95)], 1)

    return {
        "pathway_name": pathway_config.get("name", "Target Pathway"),
        "simulation_config": {
            "num_trials": num_trials,
            "baseline_success_prob": baseline_success_prob,
            "volatility_factor": volatility
        },
        "monte_carlo_results": {
            "overall_success_rate_pct": overall_success_rate,
            "execution_timeline_months": {
                "P10_optimistic": p10_time,
                "P50_median": p50_time,
                "P90_pessimistic": p90_time,
                "VaR_95_max_time": var_95_time
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

def main():
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

    res = run_monte_carlo_simulation(cfg, num_trials=5000)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
