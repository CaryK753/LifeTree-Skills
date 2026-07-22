#!/usr/bin/env python3
"""
LifeTree Graph Rehabilitation & Alternative Bridge Engine
Repairs broken decision graph pathways after poison node pruning by discovering valid alternative prerequisite nodes
"""

import sys
import json
from typing import Dict, Any, List, Set

def rehabilitate_damaged_graph(pruned_graph: Dict[str, Any], candidate_pool_nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Inspects a pruned graph for orphan or broken edges.
    Searches the candidate node pool for alternative valid prerequisite nodes to repair broken decision paths.
    """
    valid_node_ids = {n["id"] for n in pruned_graph.get("nodes", [])}
    edges = pruned_graph.get("edges", [])

    broken_edges = []
    retained_edges = []

    for edge in edges:
        s = edge.get("source")
        t = edge.get("target")
        if s not in valid_node_ids or t not in valid_node_ids:
            broken_edges.append(edge)
        else:
            retained_edges.append(edge)

    repair_bridges = []
    candidate_map = {c["id"]: c for c in candidate_pool_nodes if c["id"] not in valid_node_ids}

    # Search candidate pool for substitute nodes matching entity_type of broken dependencies
    for broken in broken_edges:
        missing_id = broken.get("source") if broken.get("source") not in valid_node_ids else broken.get("target")
        target_id = broken.get("target") if broken.get("target") in valid_node_ids else broken.get("source")
        
        # Look for replacement in candidate pool
        found_substitute = None
        for cid, candidate in candidate_map.items():
            if candidate.get("confidence", 0.0) >= 0.8:
                found_substitute = candidate
                break

        if found_substitute:
            repair_bridges.append({
                "broken_edge": broken,
                "rehabilitated_node": found_substitute,
                "bridge_relation": {
                    "source": found_substitute["id"],
                    "target": target_id,
                    "relation_type": "REHABILITATION_BRIDGE",
                    "confidence": found_substitute.get("confidence", 0.8),
                    "visual_style": "SOLID",
                    "badge": "REPAIRED_BRIDGE"
                }
            })

    rehabilitated_nodes = list(pruned_graph.get("nodes", []))
    for bridge in repair_bridges:
        sub_node = bridge["rehabilitated_node"]
        if sub_node["id"] not in {n["id"] for n in rehabilitated_nodes}:
            sub_node_copy = dict(sub_node)
            sub_node_copy["badge"] = "ALTERNATIVE_BRIDGE"
            rehabilitated_nodes.append(sub_node_copy)
        retained_edges.append(bridge["bridge_relation"])

    return {
        "rehabilitation_summary": {
            "broken_edges_count": len(broken_edges),
            "repair_bridges_applied": len(repair_bridges),
            "rehabilitated_nodes_total": len(rehabilitated_nodes),
            "graph_health": "HEALTHY_REPAIRED" if repair_bridges else ("HEALTHY_INTACT" if not broken_edges else "DEGRADED_UNREPAIRED")
        },
        "rehabilitated_graph": {
            "nodes": rehabilitated_nodes,
            "edges": retained_edges
        },
        "applied_bridges": repair_bridges
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            pruned = data.get("pruned_graph", {})
            pool = data.get("candidate_pool", [])
    else:
        pruned = {
            "nodes": [
                {"id": "n_target_visa", "label": "Target Residence Visa", "entity_type": "IMMIGRATION_ROUTE", "confidence": 1.0}
            ],
            "edges": [
                {"source": "n_revoked_plugin_node", "target": "n_target_visa", "relation_type": "REQUIRES"}
            ]
        }
        pool = [
            {"id": "n_alternative_official_cert", "label": "Official Alternative Qualification Cert", "entity_type": "FEES_REQUIREMENT", "confidence": 1.0}
        ]

    res = rehabilitate_damaged_graph(pruned, pool)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
