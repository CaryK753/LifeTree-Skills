# Continuous Risk Surveillance & Tracking Architecture (风险领域持续跟踪)

## 1. Overview
Once a latent risk domain is discovered by Divergent Thinking Mode (`scripts/divergent_risk_discovery.py`), it is automatically registered into the **Continuous Risk Surveillance Registry** (`scripts/risk_surveillance_tracker.py`).

## 2. Tracking Lifecycle
1. **Registration**: Newly discovered risk domains are assigned tracking metrics (e.g. 183-day tax rule, statutory capital outflow limit, waiting period duration).
2. **Scheduled Polling**: Background scheduled acquisition monitors regulatory changes for tracked metrics.
3. **Diff Check & Alerting**: If a tracked risk metric shifts (e.g. tax treaty law amended), `scripts/event_push_diff_engine.py` triggers an **Urgent Circuit Breaker Push Alert**.
