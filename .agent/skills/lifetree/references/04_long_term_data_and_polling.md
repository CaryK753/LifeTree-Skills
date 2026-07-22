# Long-Term Data Accumulation & Scheduled Data Acquisition

## 1. Long-Term Data Accumulation Architecture
To enable multi-year temporal forecasting, LifeTree maintains persistent historical data stores (`scripts/long_term_data_store.py`):
- **Temporal Graph Snapshots**: Captures versioned snapshots of knowledge graph states over months/years.
- **Metric Evolution Logs**: Logs changes in key numerical indicators (statutory deposit minimums, income thresholds, processing times).
- **User Decision Journals**: Stores historical state transitions, user choices, and evaluated pathways.

## 2. Autonomous Scheduled Data Acquisition
- **Background Cron / Polling**: The AI Agent or background process periodically queries tracked official sources and regulatory databases.
- **Source Freshness Tracking**: Each node's `last_fetched_iso` timestamp is updated upon retrieval, triggering `scripts/confidence_decay_pattern_engine.py` to recalibrate confidence scores.
- **Zero-Resource Diff Polling**: If no changes occur, `scripts/event_push_diff_engine.py` keeps notification dispatch 100% silent.
