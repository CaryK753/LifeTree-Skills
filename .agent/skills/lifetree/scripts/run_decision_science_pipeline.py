#!/usr/bin/env python3
"""
LifeTree Master Decision Science Pipeline Runner
Executes end-to-end decision science models: Prospect Theory loss aversion, MAUT,
Influence Diagrams, Tail Risk CVaR, Copula Correlation, Bayesian Belief updating, and Optimal Stopping timing.

Bug 3: Consolidated imports — utility_theory_engine & bayesian_belief_engine
(decision_analysis/) deleted; their functions merged into the decision_models/
canonical versions (prospect_theory_engine, maut_utility_engine, bayesian_belief_updater).
"""

import os
import sys
import json

# Task 5: centralized sys.path setup via the scripts package.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)
import scripts  # noqa: F401 — runs __init__.py which sets up sys.path

# Bug 3: use canonical decision_models/ engines
import prospect_theory_engine       # CPT + probability weighting (was utility_theory_engine)
import maut_utility_engine          # MAUT + AHP (was utility_theory_engine.calculate_maut_utility)
import bayesian_belief_updater      # Bayesian + evidence_basis (was bayesian_belief_engine)
import cvar_risk_engine             # CVaR + bankruptcy risk (canonical CVaR)
import influence_diagram_engine
import influence_diagram_layer      # Bug 4: tag graph nodes before ID evaluation
import tail_risk_cvar_engine        # Copula simulation (CVaR delegated to cvar_risk_engine)
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
    cpt_res = prospect_theory_engine.calculate_prospect_utility([
        {"payoff_usd": 45000.0, "probability": 0.85},
        {"payoff_usd": -18000.0, "probability": 0.15}
    ])
    maut_res = maut_utility_engine.evaluate_maut_utility({
        "income": 75.0, "health": 85.0, "time_cost_inverted": 70.0, "family_stability": 90.0, "stress_inverted": 65.0
    })
    print(f"\n[1] Prospect Theory & MAUT Utility Evaluation")
    print(f"  ✓ Cumulative Prospect Utility (CPT Score): {cpt_res['cpt_utility_score']}")
    print(f"  ✓ MAUT Multi-Attribute Utility Score: {maut_res['maut_total_utility_score']} / 100.0")

    # 2. Influence Diagram Backward Induction
    # Bug 4: first tag a knowledge graph with Influence Diagram semantic types
    sample_graph = {
        "nodes": [
            {"id": "usr_person", "label": "Applicant", "entity_type": "PERSON"},
            {"id": "route_chancen", "label": "Chancenkarte Visa", "entity_type": "PATHWAY_ROUTE"},
            {"id": "asset_sperrkonto", "label": "€12,000 Sperrkonto", "entity_type": "CAPITAL_ASSET"}
        ],
        "edges": [
            {"source": "usr_person", "target": "route_chancen", "relation_type": "DECISION_CHOICE"},
            {"source": "route_chancen", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL"}
        ]
    }
    id_layer_res = influence_diagram_layer.construct_influence_diagram_layer(sample_graph)
    print(f"\n[2a] Influence Diagram Semantic Layer")
    print(f"  ✓ Tagged: {id_layer_res['influence_diagram_summary']['decision_nodes_count']} decision / "
          f"{id_layer_res['influence_diagram_summary']['chance_nodes_count']} chance / "
          f"{id_layer_res['influence_diagram_summary']['value_nodes_count']} value nodes")

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
    print(f"\n[2b] Influence Diagram Backward Induction")
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
    bayes_res = bayesian_belief_updater.update_bayesian_belief(0.85, 0.92, 0.15)
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
        "influence_diagram_layer": id_layer_res,
        "influence_diagram": id_res,
        "cvar_tail_risk": cvar_res,
        "bayesian_belief": bayes_res,
        "optimal_stopping": stopping_res,
        "hyperbolic_discounting": discount_res
    }

if __name__ == "__main__":
    run_decision_science_suite()
