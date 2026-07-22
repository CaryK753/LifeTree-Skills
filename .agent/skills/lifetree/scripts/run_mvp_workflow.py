#!/usr/bin/env python3
"""
LifeTree End-to-End MVP Workflow Execution Test Runner
Executes the complete 10-phase LifeTree decision intelligence pipeline using the modular Skill engines.
All calculations are strictly code-driven via Python.
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "data_connectors"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "graph_engines"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "simulation_engines"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "decision_analysis"))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "risk_surveillance"))
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
        {"topic_id": "tpc_2", "title": "Global Tech Portfolio", "category": "ASSET_ALLOCATION"}
    ]
    latent_risks = divergent_risk_discovery.discover_latent_risks(active_topics)
    print(f"  ✓ Discovered {latent_risks['divergent_discovery_summary']['latent_risks_discovered_count']} Latent Risk Domains.")

    registry = risk_surveillance_tracker.update_risk_surveillance({}, latent_risks['discovered_risk_domains'])
    print(f"  ✓ Registered {registry['registry_summary']['total_tracked_risk_domains']} Risk Domains into Continuous Surveillance Pipeline.")

    # Phase 4: Object-Centric Graph Pathfinding
    print("\n[Phase 4] Object-Centric Dynamic Ontology GraphRAG: Dijkstra Pathfinding & Cascade")
    sample_ontology = {
        "nodes": [
            {"id": "usr_person", "label": "Person (Applicant)", "entity_type": "PERSON"},
            {"id": "asset_sperrkonto", "label": "€12,000 Blocked Account", "entity_type": "CAPITAL_ASSET"},
            {"id": "reg_chancenkarte", "label": "Chancenkarte Regulation § 20a", "entity_type": "REGULATION_LAW"},
            {"id": "inst_embassy", "label": "German Embassy", "entity_type": "INSTITUTION_AGENCY"},
            {"id": "route_bluecard", "label": "EU Blue Card Permit § 18g", "entity_type": "PATHWAY_ROUTE"}
        ],
        "edges": [
            {"source": "usr_person", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL", "confidence": 1.0, "kinetic_weight": 1.0},
            {"source": "asset_sperrkonto", "target": "reg_chancenkarte", "relation_type": "GOVERNS", "confidence": 1.0, "kinetic_weight": 1.0},
            {"source": "reg_chancenkarte", "target": "inst_embassy", "relation_type": "DEPENDS_ON", "confidence": 0.9, "kinetic_weight": 1.0},
            {"source": "inst_embassy", "target": "route_bluecard", "relation_type": "CONVERTS_TO", "confidence": 0.9, "kinetic_weight": 1.0}
        ]
    }
    path_res = temporal_graph_engine.find_optimal_causal_path(sample_ontology, "usr_person", "route_bluecard")
    print(f"  ✓ Dijkstra Optimal Causal Path Found! Friction Cost: {path_res['pathfinding_summary']['total_path_friction_cost']}, Hops: {path_res['pathfinding_summary']['hops_count']}")
    
    cascade_res = temporal_graph_engine.simulate_multi_hop_risk_cascade(sample_ontology, "asset_sperrkonto", max_hops=3)
    print(f"  ✓ Multi-Hop Risk Cascade Simulated: Impacted {cascade_res['cascade_summary']['total_impacted_ontology_objects']} Ontology Objects.")

    # Phase 5: Monte Carlo Simulation
    print("\n[Phase 5] Code-Driven 10,000-Trial Monte Carlo Simulation & Value at Risk (VaR)")
    mc_res = monte_carlo_decision_engine.run_monte_carlo_simulation({
        "name": "Chancenkarte -> EU Blue Card Route",
        "base_time_months": 24,
        "base_cost_usd": 15000.0,
        "baseline_success_prob": 0.88,
        "volatility_factor": 0.25,
        "random_seed": 42
    }, num_trials=5000)
    mc_results = mc_res['monte_carlo_results']
    print(f"  ✓ Monte Carlo Trial Complete! Success Rate: {mc_results['overall_success_rate_pct']}%")
    print(f"    - Timeline: P10={mc_results['execution_timeline_months']['P10_optimistic']}m, P50={mc_results['execution_timeline_months']['P50_median']}m, P90={mc_results['execution_timeline_months']['P90_pessimistic']}m (95% VaR: {mc_results['execution_timeline_months']['VaR_95_max_time']}m)")
    print(f"    - Cost: P10=${mc_results['financial_capital_usd']['P10_optimistic']:,.2f}, P50=${mc_results['financial_capital_usd']['P50_median']:,.2f}, P90=${mc_results['financial_capital_usd']['P90_pessimistic']:,.2f} (95% VaR: ${mc_results['financial_capital_usd']['VaR_95_max_cost']:,.2f})")

    # Phase 6: Sensitivity Elasticity & Human Language Translation
    print("\n[Phase 6] Sensitivity Elasticity & Human Language Summary Translation")
    sens_res = graph_sensitivity_engine.calculate_parameter_sensitivity(mem["global_profile"], {})
    top_action = sens_res['sensitivity_summary']['top_recommended_action']
    human_summary = human_translator.translate_metrics_to_human_language({"monte_carlo_results": mc_results, "dijkstra_optimal_causal_path": path_res})
    print(f"  ✓ Top Recommended Action: {top_action}")
    print(f"  ✓ Executive Verdict: Difficulty '{human_summary['executive_verdict']['execution_difficulty']}' | Target Budget: ${human_summary['executive_verdict']['recommended_total_budget_usd']:,.2f}")

    # Phase 7: Game Theory Stakeholder Conflict
    print("\n[Phase 7] Game-Theoretic Stakeholder Conflict & Pareto Compromise Solver")
    gt_res = game_theory_stakeholder_solver.solve_stakeholder_conflicts([
        {"stakeholder": "Host Immigration Board", "category": "IMMIGRATION_PHYSICAL_PRESENCE"},
        {"stakeholder": "Origin Tax Authority", "category": "TAX_WORLDWIDE_LIABILITY"}
    ])
    print(f"  ✓ Identified {gt_res['stakeholder_audit_summary']['conflicts_detected_count']} Regulatory Conflict(s). Pareto Compromise Action:")
    for cmp in gt_res['pareto_compromise_pathways']:
        print(f"    - {cmp['title']}: {cmp['action']}")

    # Phase 8: Multi-Step Temporal Deduction
    print("\n[Phase 8] Multi-Step Temporal Deduction Engine (5-Year Horizon)")
    ded_res = deduction_simulation_engine.run_temporal_deduction(mem["global_profile"], simulation_timeline_years=5, hypothetical_shocks=[
        {"year": 2, "name": "Sperrkonto Increase (+€800)", "impact": "NEGATIVE"},
        {"year": 4, "name": "German B1 Level Attained", "impact": "POSITIVE"}
    ])
    print(f"  ✓ 5-Year Deduction Complete! Final Path Success Probability: {ded_res['deduction_summary']['final_path_probability']*100}%")

    # Phase 9: Immediate Weekly Action Checklist
    print("\n[Phase 9] Actionable Weekly To-Do Checklist Generator")
    checklist_res = action_checklist_generator.generate_action_checklist(sample_ontology["nodes"], top_action)
    print(f"  ✓ Weekly Action Checklist Generated ({checklist_res['checklist_summary']['total_action_items']} Action Items):")
    for item in checklist_res['weekly_action_checklist']:
        print(f"    - [{item['priority']}] {item['task_title']} ({item['target_deadline']})")

    # Phase 10: Decision Journal Audit
    print("\n[Phase 10] Decision Journal Audit & Regret Minimization Review")
    mem = user_memory_manager.update_user_memory(
        mem,
        new_decision={
            "topic_id": "tpc_1",
            "title": "Selected Chancenkarte -> Blue Card Master Route",
            "chosen_pathway": "Chancenkarte § 20a",
            "rationale": "Optimal Pareto balance between entry speed and Plan B reliability.",
            "plan_b_status": "ACTIVE_RESERVE"
        }
    )
    journal_audit = decision_journal_auditor.audit_decision_journal(mem["decision_journal"])
    print(f"  ✓ Decision Journal Audited: Regret Minimization Index = {journal_audit['audit_summary']['regret_minimization_index']}/100. Verdict: {journal_audit['audit_summary']['audit_verdict']}")

    print("\n" + "=" * 80)
    print("✅ LIFETREE MVP DECISION PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    run_full_mvp_pipeline()
