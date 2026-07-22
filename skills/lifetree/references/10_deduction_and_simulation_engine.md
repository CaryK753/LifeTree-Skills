# Deduction & Simulation Mode Engine (推演模式)

## 1. Overview
The **Deduction Mode** enables interactive multi-year scenario simulation (`scripts/deduction_simulation_engine.py`). It allows users to project decision outcomes over a 1-to-10 year horizon, inject hypothetical shocks, and observe real-time probability curves and Plan B triggers.

## 2. Dynamic Features
- **Multi-Year Timeline Playback**: Step forward/backward through simulated yearly milestones (+1Y, +2Y, +5Y).
- **Hypothetical Shock Injection**: Inject positive/negative shocks (e.g. inflation surge, language test drop, market crash) into specific timeline years.
- **Probability & Risk Trajectory**: Computes path success probability decay and cumulative risk scores.
- **Deduction UI Contract**: Rendered via `resources/deduction_ui_spec.json`.
