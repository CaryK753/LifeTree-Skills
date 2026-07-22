#!/usr/bin/env python3
"""
LifeTree Soil Health & Knowledge Graph Self-Healing Auditor
Audits knowledge graph nodes for temporal expiration, confidence decay, and missing prerequisite links,
emitting a Soil Health Score (0-100) and auto-healing search queries.
"""

import sys
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

def audit_soil_health(graph: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audits knowledge soil health:
    - Identifies expired Valid_Time nodes.
    - Identifies low confidence decayed nodes (C < 0.6).
    - Identifies isolated nodes with no valid connections.
    - Generates auto-healing search queries.
    """
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    now_iso = datetime.now(timezone.utc).isoformat()

    expired_nodes = []
    low_confidence_nodes = []
    isolated_nodes = []

    connected_node_ids = set()
    for e in edges:
        connected_node_ids.add(e.get("source"))
        connected_node_ids.add(e.get("target"))

    for n in nodes:
        nid = n.get("id")
        conf = n.get("confidence", 1.0)
        vt = n.get("valid_time", {})
        end_time = vt.get("end_time")

        if end_time and end_time < now_iso:
            expired_nodes.append(n)

        if conf < 0.6:
            low_confidence_nodes.append(n)

        if nid not in connected_node_ids:
            isolated_nodes.append(n)

    total_nodes = len(nodes) if nodes else 1
    defect_count = len(expired_nodes) + len(low_confidence_nodes) + len(isolated_nodes)
    health_score = round(max(0.0, 100.0 - (defect_count / total_nodes) * 50.0), 1)

    # Generate auto-healing search queries for Tavily/Bocha
    auto_healing_queries = []
    for n in expired_nodes + low_confidence_nodes:
        label = n.get("label", "Regulation")
        auto_healing_queries.append(f"latest statutory update 2026 {label}")

    return {
        "soil_health_summary": {
            "total_nodes_audited": len(nodes),
            "total_edges_audited": len(edges),
            "soil_health_score": health_score,
            "soil_status": "OPTIMAL_HEALTH" if health_score >= 85.0 else ("NEEDS_HEAL_ATTENTION" if health_score >= 60.0 else "CRITICAL_SOIL_DEGRADATION")
        },
        "defects_audit": {
            "expired_nodes_count": len(expired_nodes),
            "low_confidence_nodes_count": len(low_confidence_nodes),
            "isolated_nodes_count": len(isolated_nodes)
        },
        "auto_healing_queries": auto_healing_queries
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            g = json.load(f)
    else:
        g = {
            "nodes": [
                {"id": "n1", "label": "Chancenkarte Law 2024", "confidence": 1.0, "valid_time": {"start_time": "2024-06-01T00:00:00Z", "end_time": None}},
                {"id": "n2", "label": "Old 2022 Tax Law", "confidence": 0.4, "valid_time": {"start_time": "2022-01-01T00:00:00Z", "end_time": "2023-12-31T23:59:59Z"}}
            ],
            "edges": []
        }

    res = audit_soil_health(g)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
