#!/usr/bin/env python3
"""
LifeTree Long-Term Data Accumulation & Temporal Store Manager
Persists historical policy evolution logs, temporal knowledge graph snapshots, and user decision journals over time.
"""

import sys
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

def append_temporal_snapshot(existing_store: Dict[str, Any], new_snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Appends a new temporal snapshot to the long-term data store.
    Tracks historical data points over months/years to enable long-term trend forecasting.
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    snapshots = existing_store.get("snapshots", [])
    history_logs = existing_store.get("history_logs", [])

    snapshot_id = f"snap_{len(snapshots) + 1}_{now_iso[:10]}"
    
    new_snapshot = {
        "snapshot_id": snapshot_id,
        "timestamp": now_iso,
        "nodes_count": len(new_snapshot_data.get("nodes", [])),
        "edges_count": len(new_snapshot_data.get("edges", [])),
        "nodes_data": new_snapshot_data.get("nodes", []),
        "edges_data": new_snapshot_data.get("edges", [])
    }
    snapshots.append(new_snapshot)

    # Log specific metric evolution for long-term pattern extraction
    for node in new_snapshot_data.get("nodes", []):
        if "metric_value" in node:
            history_logs.append({
                "timestamp": now_iso,
                "node_id": node.get("id"),
                "metric_name": node.get("label"),
                "value": node.get("metric_value"),
                "source_id": node.get("source_id")
            })

    return {
        "store_summary": {
            "total_snapshots": len(snapshots),
            "total_logged_metrics": len(history_logs),
            "latest_snapshot_id": snapshot_id,
            "last_updated": now_iso
        },
        "snapshots": snapshots,
        "history_logs": history_logs
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            store = data.get("store", {})
            snap = data.get("new_snapshot", {})
    else:
        store = {"snapshots": [], "history_logs": []}
        snap = {
            "nodes": [
                {"id": "n_sperrkonto", "label": "Blocked Account Minimum EUR", "metric_value": 12000.0, "source_id": "SRC_GOV_DE"},
                {"id": "n_bluecard", "label": "EU Blue Card Threshold EUR", "metric_value": 45300.0, "source_id": "SRC_GOV_DE"}
            ],
            "edges": []
        }

    res = append_temporal_snapshot(store, snap)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
