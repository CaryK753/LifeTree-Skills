#!/usr/bin/env python3
"""
LifeTree Monte Carlo Stochastic Decision Simulation Engine (CVaR Expected Shortfall Integrated)
Runs 10,000 stochastic simulation trials over decision pathways to calculate P10/P50/P90 confidence intervals,
VaR_0.95, and CVaR_0.95 Expected Shortfall tail risk metrics.
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

def _lognorm_mean_preserving(sigma: float) -> float:
    """
    C1 fix: random.lognormvariate(mu, sigma) returns X = exp(mu + sigma*Z) where Z~N(0,1).
    The mean is exp(mu + sigma^2/2). To get a multiplicative shock whose mean is 1.0
    (so base_cost_usd remains the center of the distribution) and whose dispersion is
    controlled by volatility, use mu = -sigma^2/2 so E[shock] = 1.0 exactly.
    With sigma = volatility (e.g. 0.20), the 95th percentile of the shock is
    exp(-sigma^2/2 + sigma*1.645) = exp(0.318) ≈ 1.37, so VaR95 ≈ 1.37 * base_cost.
    """
    return random.lognormvariate(-0.5 * sigma * sigma, sigma)


def _build_decision_stages(pathway_config: Dict[str, Any], base_time_months: float,
                           base_cost_usd: float, baseline_success_prob: float) -> List[Dict[str, Any]]:
    """
    M4 fix: Build a sequential Markov chain of decision stages. A stage failure aborts
    the whole pathway, so overall_success = product of stage probs. Each stage carries
    its own time/cost distribution so the simulation tells users WHICH stage is riskiest.
    If the caller supplies explicit `stages`, they are used as-is; otherwise a sensible
    5-stage decomposition (Education → Language → Visa → Employment → PR Grant) is built
    from the aggregate baseline_success_prob.
    """
    stages_in = pathway_config.get("stages")
    if stages_in and isinstance(stages_in, list) and len(stages_in) >= 2:
        return [{
            "name": str(s.get("name", f"Stage_{i}")),
            "prob": float(s.get("prob", 0.85)),
            "time_months": float(s.get("time_months", 0.0)),
            "cost_usd": float(s.get("cost_usd", 0.0)),
        } for i, s in enumerate(stages_in)]

    # Default decomposition: time/cost split heuristically; stage probs default to a
    # profile that multiplies to ~baseline_success_prob after rescaling below.
    default_split = [
        ("Education",   0.85, 0.65, 0.30),
        ("Language",    0.80, 0.15, 0.15),
        ("Visa",        0.90, 0.05, 0.25),
        ("Employment",  0.75, 0.10, 0.20),
        ("PRGrant",     0.95, 0.05, 0.10),
    ]
    stages = [{
        "name": name,
        "prob": p,
        "time_months": base_time_months * t_frac,
        "cost_usd": base_cost_usd * c_frac,
    } for name, p, t_frac, c_frac in default_split]

    # Rescale stage log-odds so the product equals baseline_success_prob (geometric
    # shift in logit space). This preserves backward compatibility: callers that only
    # supply baseline_success_prob still get the same overall success rate, but now the
    # *sequential structure* makes stage-failure diagnostics meaningful.
    if 0.001 < baseline_success_prob < 0.999:
        target_logit = math.log(baseline_success_prob / (1.0 - baseline_success_prob))
        stage_product = 1.0
        for s in stages:
            stage_product *= max(0.001, min(0.999, s["prob"]))
        if stage_product > 0.001:
            current_logit = math.log(stage_product / (1.0 - stage_product))
            shift = (target_logit - current_logit) / len(stages)
            for s in stages:
                p = max(0.001, min(0.999, s["prob"]))
                new_logit = math.log(p / (1.0 - p)) + shift
                s["prob"] = 1.0 / (1.0 + math.exp(-new_logit))
    return stages


def run_monte_carlo_simulation(pathway_config: Dict[str, Any], num_trials: int = None) -> Dict[str, Any]:
    """
    Runs stochastic Monte Carlo trials over a pathway and computes VaR_0.95 and CVaR_0.95 Expected Shortfall.

    C1 fix: lognormal cost shocks now use mean-preserving parameterization
             (mu = -sigma^2/2) so volatility actually drives dispersion.
    M4 fix: trials are sequential Markov-chain stages (Education → Language → Visa →
             Employment → PRGrant) rather than i.i.d. Bernoulli. A stage failure aborts
             the pathway; failure_counts expose which stage is riskiest.
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
        sigma_cost = max(0.01, volatility)

        stages = _build_decision_stages(pathway_config, base_time_months, base_cost_usd, baseline_success_prob)
        stage_failure_counts = {s["name"]: 0 for s in stages}

        successful_trials = 0
        simulated_times = []
        simulated_costs = []

        seed = pathway_config.get("random_seed")
        if seed is not None:
            random.seed(seed)

        for _ in range(trials):
            # Sequential Markov chain: a stage failure aborts the whole pathway.
            # TIME accumulates per-stage (each stage has its own gaussian noise).
            # COST uses ONE multiplicative lognormal shock on base_cost_usd (not
            # per-stage shocks) — this preserves the C1 fix's expected VaR95 ratio
            # (~1.4x base_cost at volatility=0.20). Per-stage shocks would diversify
            # the variance away and produce a misleadingly tight cost distribution.
            is_success = True
            actual_time = 0.0
            for s in stages:
                p_s = max(0.001, min(0.999, s["prob"]))
                if random.random() > p_s:
                    is_success = False
                    stage_failure_counts[s["name"]] += 1
                    break
                t_mean = float(s.get("time_months", 0.0))
                t_noise = random.gauss(0, max(1.0, t_mean * volatility * 0.5))
                actual_time += max(0.0, t_mean + t_noise)

            if is_success:
                successful_trials += 1

            simulated_times.append(max(1.0, actual_time))
            # C1: single mean-preserving lognormal shock on the whole base_cost.
            simulated_costs.append(max(0.0, base_cost_usd * _lognorm_mean_preserving(sigma_cost)))

        simulated_times.sort()
        simulated_costs.sort()

        overall_success_rate = round((successful_trials / trials) * 100.0, 2)

        p10_time = round(simulated_times[int(trials * 0.10)], 1)
        p50_time = round(simulated_times[int(trials * 0.50)], 1)
        p90_time = round(simulated_times[int(trials * 0.90)], 1)

        p10_cost = round(simulated_costs[int(trials * 0.10)], 2)
        p50_cost = round(simulated_costs[int(trials * 0.50)], 2)
        p90_cost = round(simulated_costs[int(trials * 0.90)], 2)

        # 1. VaR 95%
        var_95_cost = round(simulated_costs[int(trials * 0.95)], 2)
        var_95_time = round(simulated_times[int(trials * 0.95)], 1)

        # 2. CVaR 95% Expected Shortfall (Average loss in upper 5% tail)
        tail_costs = simulated_costs[int(trials * 0.95):]
        cvar_95_cost = round(sum(tail_costs) / len(tail_costs), 2) if tail_costs else var_95_cost
        tail_severity_ratio = round(cvar_95_cost / var_95_cost, 3) if var_95_cost > 0 else 1.0

        # M4: identify which stage caused the most failures (actionable diagnostic)
        stage_diagnostics = []
        for s in stages:
            fails = stage_failure_counts.get(s["name"], 0)
            stage_diagnostics.append({
                "stage_name": s["name"],
                "stage_success_prob": round(s["prob"], 4),
                "failure_count": fails,
                "failure_rate_pct": round((fails / trials) * 100.0, 2),
                "is_bottleneck": False,
            })
        if stage_diagnostics:
            bottleneck = max(stage_diagnostics, key=lambda x: x["failure_count"])
            bottleneck["is_bottleneck"] = bottleneck["failure_count"] > 0

        return {
            "status": "SUCCESS",
            "pathway_name": pathway_config.get("name", "Target Pathway"),
            "simulation_config": {
                "num_trials": trials,
                "baseline_success_prob": baseline_success_prob,
                "volatility_factor": volatility,
                "is_sequential_markov_chain": True,
                "stages_modeled": len(stages)
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
                    "VaR_95_max_cost": var_95_cost,
                    "CVaR_95_expected_shortfall_cost": cvar_95_cost,
                    "tail_severity_ratio": tail_severity_ratio
                },
                "stage_diagnostics": stage_diagnostics,
                "riskiest_stage": next((d["stage_name"] for d in stage_diagnostics if d.get("is_bottleneck")), None)
            },
            "tail_risk_verdict": "CRITICAL_TAIL_SHORTFALL_WARNING" if tail_severity_ratio > 1.25 else "NORMAL_VOLATILITY"
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
