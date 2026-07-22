---
name: lifetree
description: LifeTree Personal Decision Intelligence System (Life OS) Skill. Enables AI agents to model complex high-risk personal decisions (global mobility, asset allocation, career pivots, medical choices, tax optimization), compute object-centric temporal GraphRAG pathways (Dijkstra causal pathfinding & multi-hop risk cascade simulation), run 10,000-trial Monte Carlo stochastic simulations, calculate sensitivity ROI elasticity, solve game-theoretic stakeholder conflicts, audit knowledge soil health & auto-heal missing nodes, compute Pareto risk-reward frontiers, manage shared global user memory & decision journals via embedded local SQLite database with FTS5 full-text search (sqlite3), format multi-language i18n reports (en, zh-CN, de-DE), generate interactive HTML Decision Dashboards, render dynamic Vis.js Knowledge Graph Viewers, execute Tavily/Bocha AI web searches, run universal domain rule engines, execute multi-step temporal deductions (Deduction Mode UI), brainstorm latent risk domains via Divergent Thinking Mode, maintain continuous risk surveillance, accumulate long-term temporal data, rehabilitate damaged graph pathways, generate multi-pathway trade-off matrices, audit decision journals with Regret Minimization framework, prune poison graph nodes, translate metrics into plain human language, generate weekly action checklists, evaluate Prospect Theory loss aversion and MAUT utility models, solve Influence Diagrams, calculate tail-risk CVaR Expected Shortfall with Copula correlation, execute Bayesian belief inference, and optimize career pivot timing via Optimal Stopping.
---

# LifeTree (人生树) — Personal Decision Intelligence (Life OS) Skill

## 1. System Vision & Core Philosophy

LifeTree is a personal decision intelligence system (PDI) and personal decision operating system (Life OS) based on an Object-Centric Dynamic Ontology GraphRAG architecture, code-driven decision science models, and a local-first privacy model.

### Philosophy & Metaphor:
- **The Soil / Network (网/土壤)**: Public policies, statutes, market shifts, and causal constraints forming a dynamic reality knowledge graph.
- **The Tree / Fate (树/命运)**: The user's personal profile and decision choices growing like a tree out of the knowledge soil.
- **Core Claim**: The Soil provides objective facts and resistance; the Tree presents personal choices and possibilities, ensuring every major decision maintains controllable "Plan B side buds".

> [!IMPORTANT]
> **STRICT CODE-DRIVEN MATHEMATICAL ENGINE POLICY**:
> The AI Agent MUST NOT guess, hallucinate, or estimate mathematical values (such as Monte Carlo P10/P50/P90 probabilities, 95% Value at Risk, CVaR Expected Shortfall, Prospect Theory utility scores, Bayesian posterior probabilities, or Dijkstra shortest path costs) via LLM text generation. ALL numerical computations, graph traversals, and matrix scores MUST be computed exclusively by running the Python tools in `scripts/` using structured JSON inputs or local SQLite database queries!

---

## 2. Categorized Skill Resource Directory Structure

```
lifetree/
├── SKILL.md                            # Master Operational Directives
├── README.md                           # Comprehensive Technical Manual
├── scripts/                            # Categorized Python Engines & Tools
│   ├── graph_engines/                  # GraphRAG, Pathfinding, SQLite, Influence Diagrams & Vis.js Viewer
│   │   ├── temporal_graph_engine.py
│   │   ├── sqlite_graph_store.py
│   │   ├── influence_diagram_engine.py # [NEW] Influence Diagram Decision Engine
│   │   ├── graph_visualizer_html.py
│   │   ├── graph_confidence_filter.py
│   │   ├── graph_rehabilitation_engine.py
│   │   └── soil_health_auditor.py
│   ├── simulation_engines/             # Monte Carlo, Tail Risk CVaR, Optimal Stopping & Deduction
│   │   ├── monte_carlo_decision_engine.py
│   │   ├── tail_risk_cvar_engine.py    # [NEW] CVaR Expected Shortfall & Copula Correlation
│   │   ├── optimal_stopping_engine.py  # [NEW] Snell Envelope Optimal Timing & Hyperbolic Discounting
│   │   ├── deduction_simulation_engine.py
│   │   ├── deduction_interactive_controller.py
│   │   ├── confidence_decay_pattern_engine.py
│   │   └── long_term_data_store.py
│   ├── decision_analysis/              # Utility Theory, Sensitivity, Bayesian Belief & Game Theory
│   │   ├── utility_theory_engine.py    # [NEW] Prospect Theory Loss Aversion & MAUT Engine
│   │   ├── bayesian_belief_engine.py   # [NEW] Bayesian Belief Updating & Dempster-Shafer Engine
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
│   ├── ui_translators/                 # Human Translators, Action Checklists, Dashboards & Growing Trees
│   └── run_mvp_workflow.py             # End-to-End Workflow Execution Test Runner
├── resources/                          # Schemas, Databases & Templates
├── references/                         # 23 Reference Architecture Subdocs
├── tests/                             # Automated Unit & Benchmark Test Suite
└── examples/                          # Example Profile, Graph Inputs & Output HTMLs
```

---

## 3. Subdoc Sitemap & Quick Reference

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
- **Decision Science & Behavioral Utility Architecture**: [references/23_decision_science_and_utility_frameworks.md](references/23_decision_science_and_utility_frameworks.md)
