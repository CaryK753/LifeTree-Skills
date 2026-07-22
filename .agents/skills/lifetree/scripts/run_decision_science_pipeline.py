#!/usr/bin/env python3
"""
LifeTree Master Decision Science Pipeline Runner
Executes end-to-end decision science models: Prospect Theory loss aversion, MAUT,
Influence Diagrams, Tail Risk CVaR, Copula Correlation, Bayesian Belief updating, and Optimal Stopping timing.
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, os.path.join(SCRIPT_DIR, "decision_analysis"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "graph_engines"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "simulation_engines"))

import utility_theory_engine
import influence_diagram_engine
import tail_risk_cvar_engine
import bayesian_belief_engine
import optimal_stopping_engine

def run_decision_science_suite(input_payload: dict = None) -> dict:
    """
    Executes all decision science engines in sequence and aggregates results.
    """
    payload = input_payload or {}
    user_prof = payload.get("user_profile", {"liquid_funds_usd": 40000.0, "german_level": "A2"})

    print("=" * 80)
    print("🧠 RUNNING LIFETREE DECISION SCIENCE & BEHAVIORAL UTILITY SUITE")
    print("=" * 80)

    # 1. Prospect Theory Loss Aversion & MAUT
    cpt_res = utility_theory_engine.calculate_prospect_utility([
        {"payoff_usd": 45000.0, "probability": 0.85},
        {"payoff_usd": -18000.0, "probability": 0.15}
    ])
    maut_res = utility_theory_engine.calculate_maut_utility({
        "income": 75.0, "health": 85.0, "time_freedom": 70.0, "family_security": 90.0, "stress_inverted": 65.0
    })
    print(f"\n[1] Prospect Theory & MAUT Utility Evaluation")
    print(f"  ✓ Cumulative Prospect Utility (CPT Score): {cpt_res['cpt_utility_score']}")
    print(f"  ✓ MAUT Multi-Attribute Utility Score: {maut_res['maut_total_utility_score']} / 100.0")

    # 2. Influence Diagram Backward Induction
    # C5 fix: pass a real decision diagram instead of {} so the engine does actual
    # backward-induction instead of silently returning hardcoded "CHANCENKARTE_ROUTE".
    id_res = influence_diagram_engine.evaluate_influence_diagram({
        "decision_nodes": [{"id": "d_visa_route", "label": "Visa Path Choice",
                            "options": ["CHANCENKARTE_ROUTE", "DIRECT_EMPLOYER_ROUTE"]}],
        "chance_nodes": [
            {"id": "c_chancen", "parent_option": "CHANCENKARTE_ROUTE",
             "outcomes": [{"state": "SUCCESS", "prob": 0.88}, {"state": "DELAY", "prob": 0.12}]},
            {"id": "c_direct", "parent_option": "DIRECT_EMPLOYER_ROUTE",
             "outcomes": [{"state": "SUCCESS", "prob": 0.70}, {"state": "REJECT", "prob": 0.30}]}
        ],
        "value_nodes": [
            {"parent_option": "CHANCENKARTE_ROUTE", "state": "SUCCESS", "utility_value": 90.0},
            {"parent_option": "CHANCENKARTE_ROUTE", "state": "DELAY", "utility_value": 30.0},
            {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "SUCCESS", "utility_value": 95.0},
            {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "REJECT", "utility_value": -50.0}
        ]
    })
    print(f"\n[2] Influence Diagram Backward Induction")
    print(f"  ✓ Optimal Decision Policy: {id_res['influence_diagram_summary']['optimal_decision_policy']}")
    print(f"  ✓ Max Expected Utility (EU): {id_res['influence_diagram_summary']['max_expected_utility_EU']}")

    # 3. Tail Risk CVaR & Copula Systemic Correlation
    cvar_res = tail_risk_cvar_engine.simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=5000, volatility=0.25)
    cop = cvar_res["copula_simulation"]
    print(f"\n[3] Tail Risk CVaR & Copula Correlation")
    print(f"  ✓ 95% Value at Risk (VaR): ${cop['var_95_max_cost_usd']:,.2f}")
    print(f"  ✓ 95% Conditional VaR (CVaR Expected Shortfall): ${cop['cvar_expected_shortfall_usd']:,.2f}")
    print(f"  ✓ Tail Severity Multiplier: {cop['tail_severity_ratio']}x")

    # 4. Recursive Bayesian Belief Updating
    bayes_res = bayesian_belief_engine.update_bayesian_belief(0.85, 0.92, 0.15)
    print(f"\n[4] Recursive Bayesian Belief Inference")
    print(f"  ✓ Posterior Probability P(H|E): {bayes_res['posterior_probability_P_H_given_E']*100:.2f}% (Delta: +{bayes_res['belief_delta']*100:.2f}%)")

    # 5. Optimal Stopping & Hyperbolic Discounting
    stopping_res = optimal_stopping_engine.calculate_optimal_stopping_threshold(10)
    discount_res = optimal_stopping_engine.calculate_hyperbolic_discounting(100000.0, 5.0)
    print(f"\n[5] Optimal Stopping & Hyperbolic Time Preference")
    print(f"  ✓ 37% Optimal Stopping Cutoff: Observe first {stopping_res['optimal_stopping_rule']['observation_cutoff_sample_k']} opportunities")
    print(f"  ✓ Hyperbolic Present Utility (5-Year Delay): ${discount_res['hyperbolic_present_utility_usd']:,.2f}")

    print("\n" + "=" * 80)
    print("✅ DECISION SCIENCE SUITE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

    return {
        "prospect_theory": cpt_res,
        "maut_utility": maut_res,
        "influence_diagram": id_res,
        "cvar_tail_risk": cvar_res,
        "bayesian_belief": bayes_res,
        "optimal_stopping": stopping_res,
        "hyperbolic_discounting": discount_res
    }

if __name__ == "__main__":
    run_decision_science_suite()
