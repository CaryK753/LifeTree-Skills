---
name: lifetree
description: LifeTree Personal Decision Intelligence System (Life OS) Skill. Enables AI agents to model complex high-risk personal decisions (global mobility, asset allocation, career pivots, medical choices, tax optimization), compute object-centric temporal GraphRAG pathways (Dijkstra causal pathfinding & multi-hop risk cascade simulation), run 10,000-trial Monte Carlo stochastic simulations, calculate sensitivity ROI elasticity, solve game-theoretic stakeholder conflicts, audit knowledge soil health & auto-heal missing nodes, compute Pareto risk-reward frontiers, manage shared global user memory & decision journals via embedded local SQLite database with FTS5 full-text search (sqlite3), format multi-language i18n reports (en, zh-CN, de-DE), generate interactive HTML Decision Dashboards, render dynamic Vis.js Knowledge Graph Viewers, execute Tavily/Bocha AI web searches, run universal domain rule engines, execute multi-step temporal deductions (Deduction Mode UI), brainstorm latent risk domains via Divergent Thinking Mode, maintain continuous risk surveillance, accumulate long-term temporal data, rehabilitate damaged graph pathways, generate multi-pathway trade-off matrices, audit decision journals with Regret Minimization framework, prune poison graph nodes, translate metrics into plain human language, generate weekly action checklists, and export professional advisor briefs.
---

# LifeTree (人生树) — Personal Decision Intelligence (Life OS) Skill

## 1. System Vision & Core Philosophy

LifeTree is a personal decision intelligence system (PDI) and personal decision operating system (Life OS) based on an Object-Centric Dynamic Ontology GraphRAG architecture and a local-first privacy model.

### Philosophy & Metaphor:
- **The Soil / Network (网/土壤)**: Public policies, statutes, market shifts, and causal constraints forming a dynamic reality knowledge graph.
- **The Tree / Fate (树/命运)**: The user's personal profile and decision choices growing like a tree out of the knowledge soil.
- **Core Claim**: The Soil provides objective facts and resistance; the Tree presents personal choices and possibilities, ensuring every major decision maintains controllable "Plan B side buds".

> [!IMPORTANT]
> **STRICT CODE-DRIVEN MATHEMATICAL ENGINE POLICY**:
> The AI Agent MUST NOT guess, hallucinate, or estimate mathematical values (such as Monte Carlo P10/P50/P90 probabilities, 95% Value at Risk, Dijkstra shortest path costs, sensitivity partial derivatives, or trade-off matrix scores) via LLM text generation. ALL numerical computations, graph traversals, and matrix scores MUST be computed exclusively by running the Python tools in `scripts/` using structured JSON inputs or local SQLite database queries!

---

## 2. Categorized Skill Resource Directory Structure

```
lifetree/
├── SKILL.md                            # Master Operational Directives
├── README.md                           # Comprehensive Technical Manual
├── scripts/                            # Categorized Python Engines & Tools
│   ├── graph_engines/                  # GraphRAG, Pathfinding, SQLite & HTML Graph Visualizer
│   │   ├── temporal_graph_engine.py
│   │   ├── sqlite_graph_store.py
│   │   ├── graph_visualizer_html.py     # [NEW] Vis.js Interactive Knowledge Graph Viewer Generator
│   │   ├── graph_confidence_filter.py
│   │   ├── graph_rehabilitation_engine.py
│   │   └── soil_health_auditor.py
│   ├── simulation_engines/             # Monte Carlo & Temporal Deduction
│   │   ├── monte_carlo_decision_engine.py
│   │   ├── deduction_simulation_engine.py
│   │   ├── deduction_interactive_controller.py
│   │   ├── confidence_decay_pattern_engine.py
│   │   └── long_term_data_store.py
│   ├── decision_analysis/              # Sensitivity, Tornado Diagrams & Game Theory
│   │   ├── graph_sensitivity_engine.py
│   │   ├── tornado_diagram_engine.py
│   │   ├── game_theory_stakeholder_solver.py
│   │   ├── risk_reward_frontier.py
│   │   ├── scenario_comparison_matrix.py
│   │   ├── decision_tree_engine.py
│   │   ├── decision_journal_auditor.py
│   │   └── rule_evaluator_engine.py
│   ├── risk_surveillance/              # Latent Risk Discovery & Surveillance
│   ├── data_connectors/                # Search & Memory Connectors
│   ├── ui_translators/                 # Human Translators, Action Checklists & HTML Dashboard
│   │   ├── human_translator.py
│   │   ├── action_checklist_generator.py
│   │   ├── html_report_generator.py     # [NEW] Interactive HTML Decision Dashboard Generator
│   │   └── i18n_report_formatter.py
│   └── run_mvp_workflow.py             # End-to-End Workflow Execution Test Runner
├── resources/                          # Schemas, Databases & Templates
├── references/                         # 22 Reference Architecture Subdocs
└── examples/                          # Example Profile, Graph Inputs & Output HTMLs
    ├── input_user_profile.json
    ├── sample_ontology_graph.json
    ├── sample_advisor_brief.md
    ├── lifetree_decision_report.html   # [NEW] Sample Interactive Decision Dashboard HTML
    └── lifetree_graph_viewer.html      # [NEW] Sample Interactive Graph Viewer HTML
```

---

## 3. Decision Modeling Workflow

```
[Step 1: Progressive Onboarding, SQLite FTS Search & Tavily] ──> [Step 2: Divergent Risk Discovery & Surveillance]
                                                                                │
                                                                                ▼
[Step 5: HTML Dashboard, Vis.js Viewer & Advisor Brief] <─── [Step 4: Execute Dijkstra, Sensitivity ROI & Game Theory] <─── [Step 3: Run 10,000-Trial Monte Carlo Engine]
```

### Step 1: Progressive Onboarding, FTS Search & Memory Sync
1. Query/init SQLite database (`scripts/graph_engines/sqlite_graph_store.py`).
2. Search node graph via FTS5 fuzzy search: `python3 scripts/graph_engines/sqlite_graph_store.py "blocked account"`.
3. Audit knowledge soil health (`scripts/graph_engines/soil_health_auditor.py`).
4. Execute web search / extraction using Tavily / Bocha tool (`scripts/data_connectors/search_connector_tavily.py`) and synthesize facts into SQLite ontology graph using `scripts/data_connectors/jit_connector_synthesizer.py`.

### Step 2: Divergent Thinking & Risk Surveillance Registration
1. Run Divergent Thinking Mode (`scripts/risk_surveillance/divergent_risk_discovery.py`).
2. Register discovered risk domains into continuous surveillance registry (`scripts/risk_surveillance/risk_surveillance_tracker.py`).

### Step 3: Code-Driven Stochastic Simulation & Advanced Graph Algorithms
- **Monte Carlo 10,000-Trial Stochastic Simulation**: `python3 scripts/simulation_engines/monte_carlo_decision_engine.py <pathway_config.json>`
- **Sensitivity ROI Elasticity Analysis**: `python3 scripts/decision_analysis/graph_sensitivity_engine.py <user_profile.json> <rule_pack.json>`
- **Tornado Diagram Risk Ranking**: `python3 scripts/decision_analysis/tornado_diagram_engine.py <config.json>`
- **Pareto Risk-Reward Frontier**: `python3 scripts/decision_analysis/risk_reward_frontier.py <candidates.json>`
- **Game-Theoretic Stakeholder Conflict Solver**: `python3 scripts/decision_analysis/game_theory_stakeholder_solver.py <stakeholders.json>`
- **Dijkstra Optimal Pathfinding**: `python3 scripts/graph_engines/temporal_graph_engine.py <ontology_graph.json>`

### Step 4: Interactive Deduction & Regret Audit
1. Run interactive deduction action: `python3 scripts/simulation_engines/deduction_interactive_controller.py <timeline.json> <action.json>`
2. Audit decision journal entries using Regret Minimization Framework (`scripts/decision_analysis/decision_journal_auditor.py`).

### Step 5: HTML Dashboard, Vis.js Viewer & Report Generation
- Generate **Interactive HTML Decision Dashboard**:
  ```bash
  python3 scripts/ui_translators/html_report_generator.py <pipeline_data.json> <output_report.html>
  ```
- Generate **Dynamic Vis.js Knowledge Graph Viewer**:
  ```bash
  python3 scripts/graph_engines/graph_visualizer_html.py <ontology_graph.json> <output_viewer.html>
  ```
- Format multi-language headers: `python3 scripts/ui_translators/i18n_report_formatter.py <lang>`
- Export formal **Brief for Professional Advisor** (`resources/templates/brief_for_advisor_template.md`).

---

## 4. Subdoc Sitemap & Quick Reference

For detailed specifications, consult the reference documents in `references/`:
- **Architecture & Metaphor**: [references/01_architecture_overview.md](references/01_architecture_overview.md)
- **Temporal GraphRAG & Poison Pruning**: [references/02_temporal_graphrag.md](references/02_temporal_graphrag.md)
- **Agentic Dynamic Data Ingestion**: [references/03_agentic_data_ingestion.md](references/03_agentic_data_ingestion.md)
- **Long-Term Data & Scheduled Polling**: [references/04_long_term_data_and_polling.md](references/04_long_term_data_and_polling.md)
- **Universal Domain Rule Engine System**: [references/05_domain_rule_engines.md](references/05_domain_rule_engines.md)
- **Monetization & B2B SaaS**: [references/06_monetization_and_b2b.md](references/06_monetization_and_b2b.md)
- **Risk Control & Advisor Safeguards**: [references/07_risk_and_legal_safeguards.md](references/07_risk_and_legal_safeguards.md)
- **Diff Engine & Tiered Push Alerts**: [references/08_push_and_diff_engine.md](references/08_push_and_diff_engine.md)
- **Deep Research Engine**: [references/09_deep_research_engine.md](references/09_deep_research_engine.md)
- **Deduction & Simulation Mode Engine**: [references/10_deduction_and_simulation_engine.md](references/10_deduction_and_simulation_engine.md)
- **Divergent Thinking Risk Discovery**: [references/11_divergent_thinking_risk_discovery.md](references/11_divergent_thinking_risk_discovery.md)
- **Continuous Risk Surveillance**: [references/12_continuous_risk_surveillance.md](references/12_continuous_risk_surveillance.md)
- **Tavily & Bocha Search Integration**: [references/13_tavily_bocha_search_integration.md](references/13_tavily_bocha_search_integration.md)
- **Shared User Memory & Decision Journal**: [references/14_user_memory_and_decision_journal.md](references/14_user_memory_and_decision_journal.md)
- **Graph Rehabilitation & Alternative Bridge**: [references/15_graph_rehabilitation_and_repair.md](references/15_graph_rehabilitation_and_repair.md)
- **Scenario Comparison & Regret Audit**: [references/16_scenario_comparison_and_regret_audit.md](references/16_scenario_comparison_and_regret_audit.md)
- **Object-Centric Dynamic Ontology GraphRAG**: [references/17_object_centric_graphrag_architecture.md](references/17_object_centric_graphrag_architecture.md)
- **Code-Driven Mathematical Algorithms**: [references/18_advanced_algorithms_monte_carlo_sensitivity_game_theory.md](references/18_advanced_algorithms_monte_carlo_sensitivity_game_theory.md)
- **Soil Health, i18n & Pareto Frontier**: [references/19_soil_health_i18n_and_pareto_frontier.md](references/19_soil_health_i18n_and_pareto_frontier.md)
- **Embedded Local SQLite Database Architecture**: [references/20_local_sqlite_database_architecture.md](references/20_local_sqlite_database_architecture.md)
- **User Experience Perfection & FTS5 Database Optimization**: [references/21_user_experience_and_fts5_database_optimization.md](references/21_user_experience_and_fts5_database_optimization.md)
- **Interactive HTML Dashboards & Graph Viewers**: [references/22_html_dashboards_and_graph_visualizer.md](references/22_html_dashboards_and_graph_visualizer.md)
