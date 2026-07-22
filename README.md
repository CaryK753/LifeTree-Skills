# LifeTree (人生树) — Personal Decision Intelligence System (Life OS)

> **Object-Centric Temporal GraphRAG & Code-Driven Monte Carlo Personal Decision Operating System**

LifeTree (人生树) is a next-generation **Personal Decision Intelligence (PDI) Operating System (Life OS)**. It bridges public policy networks, macroeconomic trends, regulatory laws, and personal life choices into an interactive, dynamic decision-tree architecture with real-time risk hedging, code-driven stochastic forecasting, and game-theoretic conflict resolution.

> [!IMPORTANT]
> **STRICT CODE-DRIVEN MATHEMATICAL ENGINE & LOCAL SQLITE DATABASE**:
> All probabilistic simulations, Value at Risk (VaR) calculations, Dijkstra causal pathfinding, sensitivity ROIs, and friction matrices are strictly computed by executing Python tools in `scripts/` or querying the embedded zero-dependency local SQLite database (`resources/database/lifetree_local_db.sqlite`). No mathematical calculations are guessed or manually estimated by LLM text generation!

---

## 🌟 Core Philosophy & Metaphor

- **The Soil / Network (网/土壤)**: Public policies, statutes, geopolitical shifts, tax treaties, and market constraints forming a dynamic reality knowledge graph.
- **The Tree / Fate (树/命运)**: The user's personal profile, goals, and decision choices growing like a tree out of the knowledge soil.
- **Core Principle**: *The Soil provides objective facts and resistance; the Tree presents personal choices and possibilities, ensuring every major decision maintains controllable "Plan B side buds".*

---

## 🛠️ Professional Categorized Skill Architecture

```
lifetree/
├── SKILL.md                            # Master Operational Directives
├── README.md                           # Comprehensive Technical Manual
├── scripts/                            # Categorized Python Engines & Tools
│   ├── graph_engines/                  # GraphRAG, Pathfinding & SQLite Storage
│   │   ├── temporal_graph_engine.py
│   │   ├── sqlite_graph_store.py
│   │   ├── graph_confidence_filter.py
│   │   ├── graph_rehabilitation_engine.py
│   │   └── soil_health_auditor.py
│   ├── simulation_engines/             # Monte Carlo & Temporal Deduction
│   │   ├── monte_carlo_decision_engine.py
│   │   ├── deduction_simulation_engine.py
│   │   ├── deduction_interactive_controller.py
│   │   ├── confidence_decay_pattern_engine.py
│   │   └── long_term_data_store.py
│   ├── decision_analysis/              # Sensitivity, Game Theory & Trade-Offs
│   │   ├── graph_sensitivity_engine.py
│   │   ├── game_theory_stakeholder_solver.py
│   │   ├── risk_reward_frontier.py
│   │   ├── scenario_comparison_matrix.py
│   │   ├── decision_tree_engine.py
│   │   ├── decision_journal_auditor.py
│   │   └── rule_evaluator_engine.py
│   ├── risk_surveillance/              # Latent Risk Discovery & Surveillance
│   │   ├── divergent_risk_discovery.py
│   │   ├── risk_surveillance_tracker.py
│   │   ├── ripple_effect_calculator.py
│   │   └── event_push_diff_engine.py
│   ├── data_connectors/                # Search & Memory Connectors
│   │   ├── search_connector_tavily.py
│   │   ├── jit_connector_synthesizer.py
│   │   └── user_memory_manager.py
│   ├── ui_translators/                 # Human Translators & Action Checklists
│   │   ├── human_translator.py
│   │   ├── action_checklist_generator.py
│   │   └── i18n_report_formatter.py
│   └── run_mvp_workflow.py             # End-to-End Workflow Execution Test Runner
├── resources/                          # Schemas, Databases & Templates
│   ├── schemas/                        # JSON Schemas & UI Specifications
│   │   ├── core_ontology_schema.json
│   │   ├── domain_rule_schema.json
│   │   ├── divergent_risk_map_schema.json
│   │   ├── scenario_comparison_schema.json
│   │   ├── monte_carlo_report_schema.json
│   │   ├── deduction_ui_spec.json
│   │   └── GenUI_tree_spec.json
│   ├── database/                       # Database DDL & SQLite Storage
│   │   ├── sqlite_db_schema.sql
│   │   ├── lifetree_local_db.sqlite
│   │   └── user_global_memory_store.json
│   └── templates/                      # Export Markdown Templates
│       ├── brief_for_advisor_template.md
│       └── deep_research_report_template.md
├── references/                         # 21 Reference Architecture Subdocs
└── examples/                          # Example Profile & Graph Inputs
    ├── input_user_profile.json
    ├── sample_ontology_graph.json
    └── sample_advisor_brief.md
```

---

## 💻 Quick Start & Engine Execution

### 1. Run Complete End-to-End MVP Decision Pipeline
```bash
python3 .agent/skills/lifetree/scripts/run_mvp_workflow.py
```

### 2. Run Embedded Local SQLite Database Manager (FTS5 Search)
```bash
python3 .agent/skills/lifetree/scripts/graph_engines/sqlite_graph_store.py
```

### 3. Run 10,000-Trial Monte Carlo Stochastic Simulation & VaR
```bash
python3 .agent/skills/lifetree/scripts/simulation_engines/monte_carlo_decision_engine.py
```

---

## 📜 License
Internal AI Agent Skill & Operating System Framework — All Rights Reserved.
