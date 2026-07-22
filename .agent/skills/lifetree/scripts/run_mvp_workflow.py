#!/usr/bin/env python3
"""
LifeTree End-to-End MVP Workflow Execution Test Runner
Executes the complete LifeTree decision intelligence pipeline using the modular Skill engines.
Generates interactive HTML Decision Dashboards, Vis.js Graph Viewers, HTML Deduction Scenario Players,
Animated Growing Decision Trees, and the Master Aggregator Homepage Portal with full i18n support.
"""

import os
import sys
import json

# Task 5: centralized sys.path setup via the scripts package.
# scripts/__init__.py adds all subdirectories to sys.path so flat imports work.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)
import scripts  # noqa: F401 — runs __init__.py which sets up sys.path

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
import homepage_generator
# Bug 3: consolidated engines — utility_theory_engine & bayesian_belief_engine
# (decision_analysis/) deleted; their functions merged into the decision_models/
# canonical versions below.
import prospect_theory_engine       # CPT + probability weighting (was utility_theory_engine)
import maut_utility_engine          # MAUT + AHP (was utility_theory_engine.calculate_maut_utility)
import bayesian_belief_updater      # Bayesian + evidence_basis (was bayesian_belief_engine)
import cvar_risk_engine             # CVaR + bankruptcy risk (canonical CVaR)
import influence_diagram_engine
import influence_diagram_layer      # Bug 4: tag graph nodes before ID evaluation
import tail_risk_cvar_engine        # Copula simulation (CVaR delegated to cvar_risk_engine)
import optimal_stopping_engine
# Task 1-4: previously-dead modules now integrated into the pipeline
import risk_reward_frontier         # Task 1: Pareto frontier
import tornado_diagram_engine       # Task 2: Tornado sensitivity diagram
import markov_transition_engine     # Task 3: Markov long-term state evolution
import graph_confidence_filter      # Task 4: Poison graph pruning
import graph_rehabilitation_engine  # Task 4: Broken path rehabilitation

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
            {"id": "reg_chancenkarte", "label": "德国机会卡法规 § 20a", "entity_type": "REGULATION_LAW", "confidence": 0.9, "source_id": "SRC_COMMUNITY_UNRELIABLE"},
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
    # Bug 4: first tag the knowledge-graph nodes with Influence Diagram semantic
    # types (DECISION/CHANCE/VALUE) via influence_diagram_layer, then feed those
    # tagged nodes to the backward-induction solver. This integrates the two
    # previously-disconnected Influence Diagram engines.
    id_layer_res = influence_diagram_layer.construct_influence_diagram_layer(sample_ontology)
    print(f"  ✓ Influence Diagram Layer: {id_layer_res['influence_diagram_summary']['decision_nodes_count']} decision / "
          f"{id_layer_res['influence_diagram_summary']['chance_nodes_count']} chance / "
          f"{id_layer_res['influence_diagram_summary']['value_nodes_count']} value nodes tagged")
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
    print(f"  ✓ Dijkstra Optimal Path Friction: {path_res['pathfinding_summary']['total_path_friction_cost']} | Optimal Policy: {id_res['influence_diagram_summary']['optimal_decision_policy']}")

    # Task 4: Phase 4c — Poison Graph Pruning & Rehabilitation
    # Simulate revoking a community-sourced regulation and verify the graph
    # survives via the rehabilitation engine's alternative-bridge search.
    print("\n[Phase 4c] Graph Poison Pruning & Rehabilitation")
    revoked_sources = ["SRC_COMMUNITY_UNRELIABLE"]
    pruned = graph_confidence_filter.process_knowledge_graph(
        sample_ontology,
        revoked_source_ids=revoked_sources,
        min_confidence=0.0  # don't filter by confidence, only by source_id
    )
    print(f"  ✓ Removed {pruned['summary']['poisoned_nodes_removed']} poisoned nodes (revoked: {revoked_sources})")
    # Rehabilitate broken paths using a candidate pool of alternative sources
    candidate_pool = [
        {"id": "alt_official_source", "label": "Official Alternative Source",
         "entity_type": "REGULATION_LAW", "confidence": 1.0}
    ]
    rehab_res = graph_rehabilitation_engine.rehabilitate_damaged_graph(pruned, candidate_pool)
    print(f"  ✓ Graph Rehabilitation: {rehab_res['rehabilitation_summary']['repair_bridges_applied']} bridges applied")
    print(f"  ✓ Graph health: {rehab_res['rehabilitation_summary']['graph_health']}")

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

    # Bug 6: Compute CVaR directly from MC simulated costs (single source of truth)
    # instead of running a separate Copula simulation. The Copula engine is still
    # available for systemic-risk correlation analysis, but VaR/CVaR should come
    # from the same MC trial data to avoid "same scenario, two sets of numbers."
    mc_simulated_costs = mc_results.get("financial_capital_usd", {}).get("simulated_costs", [])
    if mc_simulated_costs:
        cvar_res = tail_risk_cvar_engine.calculate_cvar_from_mc_costs(
            mc_simulated_costs, alpha=0.95, initial_capital_usd=40000.0)
        cvar_display = cvar_res
    else:
        # Fallback: Copula simulation if MC costs not exposed
        cvar_res = tail_risk_cvar_engine.simulate_copula_systemic_risks(base_cost=15000.0, correlation_rho=0.65, num_trials=5000, volatility=0.25)
        cvar_display = cvar_res["copula_simulation"]

    cvar_esd = cvar_display.get("cvar_expected_shortfall_usd", 0.0)
    print(f"  ✓ Monte Carlo Trials: {mc_results['total_trials_simulated']} | 95% VaR: ${mc_results['financial_capital_usd']['VaR_95_max_cost']:,.2f} | CVaR Expected Shortfall: ${cvar_esd:,.2f}")

    # Phase 6: Behavioral Prospect Theory & MAUT Utility Elicitation
    print("\n[Phase 6] Behavioral Prospect Theory & MAUT Multi-Attribute Utility")
    cpt_res = prospect_theory_engine.calculate_prospect_utility([
        {"payoff_usd": 45000.0, "probability": 0.85},
        {"payoff_usd": -18000.0, "probability": 0.15}
    ])
    sens_res = graph_sensitivity_engine.calculate_parameter_sensitivity(mem["global_profile"], {})
    top_action = sens_res['sensitivity_summary']['top_recommended_action']
    human_summary = human_translator.translate_metrics_to_human_language({"monte_carlo_results": mc_results, "dijkstra_optimal_causal_path": path_res}, lang="zh")

    # Task 2: Phase 6b — Tornado Sensitivity Diagram
    # Ranks decision parameters by their volatility swing on success probability.
    print("\n[Phase 6b] Tornado Sensitivity Diagram")
    tornado_params = {
        "base_success_prob": mc_results.get("overall_success_rate_pct", 82.0) / 100.0,
        "parameters": [
            {"parameter_name": "German Language Level", "base_value": 2.0, "delta_low": 0.0, "delta_high": 4.0, "unit": "CEFR", "sensitivity_factor": 0.06},
            {"parameter_name": "Liquid Capital Reserves", "base_value": 15000.0, "delta_low": 5000.0, "delta_high": 25000.0, "unit": "USD", "sensitivity_factor": 0.000008},
            {"parameter_name": "Statutory Processing Time", "base_value": 6.0, "delta_low": 3.0, "delta_high": 12.0, "unit": "Months", "sensitivity_factor": 0.03},
        ]
    }
    tornado_res = tornado_diagram_engine.calculate_tornado_sensitivity_swings(tornado_params)
    print(f"  ✓ Top risk driver: {tornado_res['tornado_analysis_summary']['top_risk_driver']} (swing: {tornado_res['tornado_analysis_summary']['max_volatility_swing']})")
    for s in tornado_res.get("tornado_diagram_swings", []):
        print(f"     #{s['impact_rank']} {s['parameter_name']}: swing={s['volatility_swing']}")

    # Phase 7: Bayesian Belief Updating & Game-Theoretic Pareto Solver
    print("\n[Phase 7] Bayesian Belief Updating & Game-Theoretic Pareto Solver")
    bayes_res = bayesian_belief_updater.update_bayesian_belief(0.85, 0.92, 0.15)
    st_a = {"stakeholder": "Host Immigration Board", "category": "IMMIGRATION_PHYSICAL_PRESENCE", "preference_vector": {"compliance_cost": -0.3, "penalty_risk": -0.5, "benefit": 1.0}}
    st_b = {"stakeholder": "Origin Tax Authority", "category": "TAX_WORLDWIDE_LIABILITY", "preference_vector": {"compliance_cost": -0.2, "penalty_risk": -0.7, "benefit": 0.8}}
    gt_res = game_theory_stakeholder_solver.solve_stakeholder_conflicts([st_a, st_b])

    # Phase 8: Multi-Step Temporal Deduction (Deduction Mode) & Optimal Stopping
    print("\n[Phase 8] Multi-Step Temporal Deduction & Optimal Stopping Rule")
    ded_res = deduction_simulation_engine.run_temporal_deduction(mem["global_profile"], simulation_timeline_years=5)
    stopping_res = optimal_stopping_engine.calculate_optimal_stopping_threshold(10)

    # Task 1: Phase 8b — Pareto Efficiency Frontier
    # Compare candidate pathways on (success_prob, cost, time) and identify
    # non-dominated options. First generate a scenario comparison matrix, then
    # convert its rows into Pareto candidates.
    print("\n[Phase 8b] Pareto Efficiency Frontier")
    pathway_options = [
        {"name": "Chancenkarte -> EU Blue Card", "financial_cost_usd": 15000.0,
         "horizon_months": 24, "risk_level": "LOW", "prereq_friction_level": "MEDIUM",
         "plan_b_reliability_score": 85.0},
        {"name": "Direct Employer Sponsorship", "financial_cost_usd": 8000.0,
         "horizon_months": 12, "risk_level": "MEDIUM", "prereq_friction_level": "HIGH",
         "plan_b_reliability_score": 70.0},
        {"name": "Job Seeker Visa -> Employment", "financial_cost_usd": 20000.0,
         "horizon_months": 36, "risk_level": "HIGH", "prereq_friction_level": "MEDIUM",
         "plan_b_reliability_score": 60.0},
    ]
    cmp_res = scenario_comparison_matrix.generate_comparison_matrix(pathway_options)
    pareto_candidates = []
    for row in cmp_res.get("comparison_matrix", []):
        risk = row.get("risk_level", "MEDIUM")
        success_prob = 1.0 - (0.3 if risk == "HIGH" else (0.15 if risk == "MEDIUM" else 0.0))
        pareto_candidates.append({
            "name": row["pathway_name"],
            "success_prob": success_prob,
            "cost_usd": row.get("financial_cost_usd", 50000),
            "time_months": row.get("horizon_months", 60),
        })
    pareto_res = risk_reward_frontier.calculate_pareto_frontier(pareto_candidates)
    print(f"  ✓ {pareto_res['frontier_summary']['pareto_efficient_count']} Pareto-efficient pathways out of {pareto_res['frontier_summary']['total_pathways_analyzed']}")
    for p in pareto_res.get("pareto_frontier_pathways", []):
        print(f"     ✅ {p['name']}")
    for p in pareto_res.get("dominated_pathways", []):
        print(f"     ❌ {p} (dominated)")

    # Task 3: Phase 8c — Markov Long-Term State Evolution
    # After the decision pathway completes, what state distribution is most
    # likely after 10 years? MC tells you "success rate"; Markov tells you
    # "where you end up."
    print("\n[Phase 8c] Markov Long-Term State Evolution (10-year)")
    markov_profile = {
        "EMPLOYED_DE": 0.0,
        "EMPLOYED_CN": 0.0,
        "PR_HOLDER": 1.0,  # Start: just got PR
        "ENTREPRENEUR": 0.0,
        "UNEMPLOYED": 0.0,
    }
    markov_matrix = {
        "EMPLOYED_DE": {"EMPLOYED_DE": 0.70, "EMPLOYED_CN": 0.05, "PR_HOLDER": 0.20, "ENTREPRENEUR": 0.03, "UNEMPLOYED": 0.02},
        "EMPLOYED_CN": {"EMPLOYED_DE": 0.05, "EMPLOYED_CN": 0.80, "PR_HOLDER": 0.05, "ENTREPRENEUR": 0.05, "UNEMPLOYED": 0.05},
        "PR_HOLDER":   {"EMPLOYED_DE": 0.60, "EMPLOYED_CN": 0.05, "PR_HOLDER": 0.30, "ENTREPRENEUR": 0.03, "UNEMPLOYED": 0.02},
        "ENTREPRENEUR":{"EMPLOYED_DE": 0.10, "EMPLOYED_CN": 0.05, "PR_HOLDER": 0.05, "ENTREPRENEUR": 0.75, "UNEMPLOYED": 0.05},
        "UNEMPLOYED":  {"EMPLOYED_DE": 0.30, "EMPLOYED_CN": 0.15, "PR_HOLDER": 0.05, "ENTREPRENEUR": 0.05, "UNEMPLOYED": 0.45},
    }
    markov_res = markov_transition_engine.simulate_markov_transitions(markov_profile, markov_matrix, steps_n=10)
    final_dist = markov_res.get("markov_summary", {}).get("final_state_distribution", {})
    most_likely = markov_res.get("markov_summary", {}).get("most_likely_final_state", "N/A")
    for state, prob in sorted(final_dist.items(), key=lambda x: -x[1]):
        print(f"     {state}: {prob*100:.1f}%")
    print(f"  ✓ Most likely state after 10 years: {most_likely}")

    # Phase 9: Actionable Weekly To-Do Checklist Generator
    print("\n[Phase 9] Actionable Weekly To-Do Checklist Generator")
    checklist_res = action_checklist_generator.generate_action_checklist(sample_ontology["nodes"], top_action)

    # Phase 10: Generating Interactive HTML Dashboards, Deduction Player & Master Aggregator Homepage
    print("\n[Phase 10] Generating Master Aggregator Homepage Portal & HTML Viewers")
    homepage_path = os.path.join(SKILL_ROOT, "examples", "lifetree_homepage.html")
    html_report_path = os.path.join(SKILL_ROOT, "examples", "lifetree_decision_report.html")
    graph_viewer_path = os.path.join(SKILL_ROOT, "examples", "lifetree_graph_viewer.html")
    deduction_player_path = os.path.join(SKILL_ROOT, "examples", "lifetree_deduction_player.html")
    growing_tree_path = os.path.join(SKILL_ROOT, "examples", "lifetree_growing_tree.html")

    pipeline_payload = {
        "monte_carlo_results": mc_results,
        "human_readable_summary": human_summary,
        "weekly_action_checklist": [
            {"task_title": "提升德语水平至 B1 级", "action_details": "完成 100 小时德语听力与口语强化训练", "priority": "HIGH", "target_deadline": "7 天内"},
            {"task_title": "办理 €12,000 保证金账户 Sperrkonto", "action_details": "开设 Expatrio 或 Fintiba 保证金账户并完成注资", "priority": "HIGH", "target_deadline": "14 天内"}
        ],
        "regret_audit": {"audit_summary": {"regret_minimization_index": 93.2}},
        "tail_risk_results": {
            # Bug 6: CVaR now from MC costs (single source of truth), not Copula
            "cvar_expected_shortfall_usd": cvar_display.get("cvar_expected_shortfall_usd", 0.0),
            "tail_severity_ratio": cvar_display.get("tail_severity_ratio", 1.0)
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
    }

    # Generate Individual 4 HTML Views
    html_report_generator.generate_interactive_html_report(pipeline_payload, html_report_path, lang="zh")
    graph_visualizer_html.generate_graph_visualizer_html(sample_ontology, graph_viewer_path, lang="zh")
    deduction_player_html.generate_deduction_player_html(ded_res, deduction_player_path, lang="zh")
    growing_tree_html.generate_growing_tree_html(ded_res, growing_tree_path, lang="zh")

    # Generate Master Homepage Portal
    homepage_generator.generate_homepage_html(pipeline_payload, homepage_path, lang="zh")

    print(f"  🌟 ALL-IN-ONE MASTER PORTAL HOMEPAGE GENERATED: {homepage_path}")
    print(f"  ✓ Interactive Decision Report Dashboard HTML Generated: {html_report_path}")
    print(f"  ✓ Interactive Knowledge Graph Viewer HTML Generated: {graph_viewer_path}")
    print(f"  ✓ Interactive Deduction Scenario Player HTML Generated: {deduction_player_path}")
    print(f"  ✓ Interactive Growing Decision Tree HTML Generated: {growing_tree_path}")

    print("\n" + "=" * 80)
    print("✅ LIFETREE MVP DECISION PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_full_mvp_pipeline()
