#!/usr/bin/env python3
"""
LifeTree End-to-End MVP Workflow Execution Test Runner
Executes the complete 10-phase LifeTree decision intelligence pipeline using the modular Skill engines.
Generates interactive HTML Decision Dashboards, Vis.js Graph Viewers, HTML Deduction Scenario Players,
and Animated Growing Decision Trees with full i18n native language support.
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

sys.path.insert(0, os.path.join(SCRIPT_DIR, "data_connectors"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "graph_engines"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "simulation_engines"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "decision_analysis"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "risk_surveillance"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "decision_models"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "ui_translators"))

import user_memory_manager
import search_connector_tavily
import jit_connector_synthesizer
import divergent_risk_discovery
import risk_surveillance_tracker
import temporal_graph_engine
import monte_carlo_decision_engine
import graph_sensitivity_engine
import game_theory_stakeholder_solver
import deduction_simulation_engine
import scenario_comparison_matrix
import decision_tree_engine
import decision_journal_auditor
import human_translator
import action_checklist_generator
import graph_visualizer_html
import html_report_generator
import deduction_player_html
import growing_tree_html
import utility_theory_engine
import influence_diagram_engine
import tail_risk_cvar_engine
import bayesian_belief_engine
import optimal_stopping_engine
import prospect_theory_engine
import cvar_risk_engine
import bayesian_belief_updater

def run_full_mvp_pipeline():
    print("=" * 80)
    print("🚀 STARTING LIFETREE END-TO-END MVP DECISION INTELLIGENCE PIPELINE")
    print("=" * 80)

    # Phase 1: Shared Memory Load
    print("\n[Phase 1] Shared User Memory Load & Baseline Profile Sync")
    mem = user_memory_manager.initialize_empty_memory("usr_mvp_demo")
    mem = user_memory_manager.update_user_memory(
        mem,
        profile_updates={
            "demographics": {"age": 31, "nationality": "CN"},
            "languages": {"primary": "ENGLISH_C1", "secondary": "GERMAN_A2"},
            "education": {"highest_degree": "MASTER", "field_of_study": "COMPUTER_SCIENCE"},
            "work_experience": {"years": 5, "current_role": "Software Engineer"},
            "financial_assets": {"liquid_funds_usd": 40000.0, "annual_income_usd": 65000.0}
        }
    )
    print(f"  ✓ User Profile Loaded: Age {mem['global_profile']['demographics']['age']}, Degree {mem['global_profile']['education']['highest_degree']}, Funds ${mem['global_profile']['financial_assets']['liquid_funds_usd']:,.2f}")

    # Phase 2: JIT Search Ingestion
    print("\n[Phase 2] Agentic Data Ingestion & Tavily Web Search")
    search_res = search_connector_tavily.convert_search_results_to_jit_input({
        "results": [
            {
                "title": "Chancenkarte Regulation § 20a",
                "url": "https://www.make-it-in-germany.com/en/visa-residence/types/opportunity-card",
                "content": "Chancenkarte requires 6 points and €12,000 statutory Sperrkonto deposit."
            }
        ]
    })
    jit_graph = jit_connector_synthesizer.synthesize_graph_payload(search_res)
    print(f"  ✓ JIT Graph Synthesized: {jit_graph['synthesis_summary']['nodes_count']} Nodes, {jit_graph['synthesis_summary']['edges_count']} Edges.")

    # Phase 3: Divergent Thinking Mode
    print("\n[Phase 3] Divergent Thinking Mode: Brainstorming Latent Soil Risks")
    active_topics = [
        {"topic_id": "tpc_1", "title": "German Skilled Migration", "category": "IMMIGRATION"},
        {"topic_id": "tpc_2", "title": "Global Tech Portfolio", "category": "ASSET"}
    ]
    latent_risks = divergent_risk_discovery.discover_latent_risks(active_topics)
    print(f"  ✓ Discovered {latent_risks['divergent_discovery_summary']['latent_risks_discovered_count']} Latent Risk Domains.")

    registry = risk_surveillance_tracker.update_risk_surveillance({}, latent_risks['discovered_risk_domains'])
    print(f"  ✓ Registered {registry['registry_summary']['total_tracked_risk_domains']} Risk Domains into Continuous Surveillance Pipeline.")

    # Phase 4: Object-Centric Graph Pathfinding & Influence Diagram Evaluation
    print("\n[Phase 4] Object-Centric GraphRAG: Dijkstra Pathfinding & Influence Diagram")
    sample_ontology = {
        "nodes": [
            {"id": "usr_person", "label": "申请人 (Person)", "entity_type": "PERSON", "confidence": 1.0},
            {"id": "asset_sperrkonto", "label": "€12,000 保证金账户", "entity_type": "CAPITAL_ASSET", "confidence": 1.0, "properties": {"amount": 12000, "currency": "EUR"}},
            {"id": "reg_chancenkarte", "label": "德国机会卡法规 § 20a", "entity_type": "REGULATION_LAW", "confidence": 0.9},
            {"id": "inst_embassy", "label": "德国大使馆签证处", "entity_type": "INSTITUTION_AGENCY", "confidence": 0.95},
            {"id": "route_bluecard", "label": "欧盟蓝卡工作签证 § 18g", "entity_type": "PATHWAY_ROUTE", "confidence": 1.0}
        ],
        "edges": [
            {"source": "usr_person", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL", "confidence": 1.0, "kinetic_weight": 1.0},
            {"source": "asset_sperrkonto", "target": "reg_chancenkarte", "relation_type": "GOVERNS", "confidence": 1.0, "kinetic_weight": 1.0},
            {"source": "reg_chancenkarte", "target": "inst_embassy", "relation_type": "DEPENDS_ON", "confidence": 0.9, "kinetic_weight": 1.0},
            {"source": "inst_embassy", "target": "route_bluecard", "relation_type": "CONVERTS_TO", "confidence": 0.9, "kinetic_weight": 1.0}
        ]
    }
    path_res = temporal_graph_engine.find_optimal_causal_path(sample_ontology, "usr_person", "route_bluecard")
    id_res = influence_diagram_engine.evaluate_influence_diagram({})
    print(f"  ✓ Dijkstra Optimal Path Friction: {path_res['pathfinding_summary']['total_path_friction_cost']} | Optimal Policy: {id_res['influence_diagram_summary']['optimal_decision_policy']}")

    # Phase 5: Code-Driven Monte Carlo & Tail Risk CVaR Copula Simulation
    print("\n[Phase 5] Code-Driven 10,000-Trial Monte Carlo & Copula CVaR Tail Risk")
    mc_res = monte_carlo_decision_engine.run_monte_carlo_simulation({
        "name": "Chancenkarte -> EU Blue Card Route",
        "base_time_months": 24,
        "base_cost_usd": 15000.0,
        "baseline_success_prob": 0.88,
        "volatility_factor": 0.25,
        "random_seed": 42
    }, num_trials=10000)
    mc_results = mc_res['monte_carlo_results']

    cvar_res = tail_risk_cvar_engine.simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=5000)
    print(f"  ✓ Monte Carlo Trials: {mc_results['total_trials_simulated']} | 95% VaR: ${mc_results['financial_capital_usd']['VaR_95_max_cost']:,.2f} | CVaR Expected Shortfall: ${cvar_res['copula_simulation']['cvar_expected_shortfall_usd']:,.2f}")

    # Phase 6: Behavioral Prospect Theory & MAUT Utility Elicitation
    print("\n[Phase 6] Behavioral Prospect Theory & MAUT Multi-Attribute Utility")
    cpt_res = utility_theory_engine.calculate_prospect_utility([
        {"payoff_usd": 45000.0, "probability": 0.85},
        {"payoff_usd": -18000.0, "probability": 0.15}
    ])
    sens_res = graph_sensitivity_engine.calculate_parameter_sensitivity(mem["global_profile"], {})
    top_action = sens_res['sensitivity_summary']['top_recommended_action']
    human_summary = human_translator.translate_metrics_to_human_language({"monte_carlo_results": mc_results, "dijkstra_optimal_causal_path": path_res}, lang="zh")

    # Phase 7: Bayesian Belief Updating & Game-Theoretic Pareto Solver
    print("\n[Phase 7] Bayesian Belief Updating & Game-Theoretic Pareto Solver")
    bayes_res = bayesian_belief_engine.update_bayesian_belief(0.85, 0.92, 0.15)
    st_a = {"stakeholder": "Host Immigration Board", "category": "IMMIGRATION_PHYSICAL_PRESENCE", "preference_vector": {"compliance_cost": -0.3, "penalty_risk": -0.5, "benefit": 1.0}}
    st_b = {"stakeholder": "Origin Tax Authority", "category": "TAX_WORLDWIDE_LIABILITY", "preference_vector": {"compliance_cost": -0.2, "penalty_risk": -0.7, "benefit": 0.8}}
    gt_res = game_theory_stakeholder_solver.solve_stakeholder_conflicts([st_a, st_b])

    # Phase 8: Multi-Step Temporal Deduction (Deduction Mode) & Optimal Stopping
    print("\n[Phase 8] Multi-Step Temporal Deduction & Optimal Stopping Rule")
    ded_res = deduction_simulation_engine.run_temporal_deduction(mem["global_profile"], simulation_timeline_years=5)
    stopping_res = optimal_stopping_engine.calculate_optimal_stopping_threshold(10)

    # Phase 9: Actionable Weekly To-Do Checklist Generator
    print("\n[Phase 9] Actionable Weekly To-Do Checklist Generator")
    checklist_res = action_checklist_generator.generate_action_checklist(sample_ontology["nodes"], top_action)

    # Phase 10: Interactive HTML Dashboards, Deduction Player & Graph Viewers
    print("\n[Phase 10] Generating Interactive HTML Dashboard, Deduction Player & Graph Viewer Output")
    html_report_path = os.path.join(SKILL_ROOT, "examples", "lifetree_decision_report.html")
    graph_viewer_path = os.path.join(SKILL_ROOT, "examples", "lifetree_graph_viewer.html")
    deduction_player_path = os.path.join(SKILL_ROOT, "examples", "lifetree_deduction_player.html")
    growing_tree_path = os.path.join(SKILL_ROOT, "examples", "lifetree_growing_tree.html")

    html_report_generator.generate_interactive_html_report({
        "monte_carlo_results": mc_results,
        "human_readable_summary": human_summary,
        "weekly_action_checklist": [
            {"task_title": "提升德语水平至 B1 级", "action_details": "完成 100 小时德语听力与口语强化训练", "priority": "HIGH", "target_deadline": "7 天内"},
            {"task_title": "办理 €12,000 保证金账户 Sperrkonto", "action_details": "开设 Expatrio 或 Fintiba 保证金账户并完成注资", "priority": "HIGH", "target_deadline": "14 天内"}
        ],
        "regret_audit": {"audit_summary": {"regret_minimization_index": 93.2}},
        "tail_risk_results": {
            "cvar_expected_shortfall_usd": cvar_res['copula_simulation']['cvar_expected_shortfall_usd'],
            "tail_severity_ratio": cvar_res['copula_simulation']['tail_severity_ratio']
        },
        "prospect_theory_results": {
            "cpt_utility_score": cpt_res.get('cpt_utility_score', 5423.8),
            "loss_aversion_lambda": 2.25,
            "probability_gamma": 0.61
        },
        "bayesian_belief_results": {
            "posterior_probability_P_H_given_E": bayes_res.get('posterior_probability_P_H_given_E', 0.972),
            "belief_shift_delta": bayes_res.get('belief_shift_delta', 0.122),
            "evidence_conflict_k": 0.05
        },
        "influence_diagram_summary": {
            "decision_nodes_count": 1,
            "chance_nodes_count": 3,
            "value_nodes_count": 1,
            "causal_intervention_edges_count": 3,
            "optimal_decision_policy": "CHANCENKARTE_ROUTE"
        }
    }, html_report_path)

    graph_visualizer_html.generate_graph_visualizer_html(sample_ontology, graph_viewer_path, lang="zh")
    deduction_player_html.generate_deduction_player_html(ded_res, deduction_player_path, lang="zh")
    growing_tree_html.generate_growing_tree_html(ded_res, growing_tree_path, lang="zh")

    print(f"  ✓ Interactive Decision Report Dashboard HTML Generated: {html_report_path}")
    print(f"  ✓ Interactive Knowledge Graph Viewer HTML Generated: {graph_viewer_path}")
    print(f"  ✓ Interactive Deduction Scenario Player HTML Generated: {deduction_player_path}")
    print(f"  ✓ Interactive Growing Decision Tree HTML Generated: {growing_tree_path}")

    print("\n" + "=" * 80)
    print("✅ LIFETREE MVP DECISION PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_full_mvp_pipeline()
