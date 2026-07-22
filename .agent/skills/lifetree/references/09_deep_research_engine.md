# Deep Research Engine & Structured Report Generation

## 1. Overview
The **Deep Research Engine** is a specialized framework within LifeTree designed for single-shot, comprehensive decision evaluations. It orchestrates multi-step GraphRAG traversal, What-If sensitivity matrix computation, and cross-topic ripple calculations into a multi-page structured document.

## 2. Execution Pipeline
1. **Fact Base Aggregation**: Fetch user profile from encrypted local memory and query cloud GraphRAG for active temporal policy sub-graphs.
2. **Multi-Path Deduction**: Run `scripts/decision_tree_engine.py` with Top-3 smart pruning policy.
3. **What-If Stress Testing**: Simulate edge-case variables (e.g. language score drop, inflation surge).
4. **Cross-Topic Ripple Analysis**: Run `scripts/ripple_effect_calculator.py` across all active user topics.
5. **Report Rendering**: Populate `resources/deep_research_report_template.md` (exportable to Markdown / PDF).
6. **Advisor Brief Bridge**: Generate an accompanying `resources/brief_for_advisor_template.md` for professional vetting.
