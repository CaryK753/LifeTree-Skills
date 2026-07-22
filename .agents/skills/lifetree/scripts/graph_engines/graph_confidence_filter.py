#!/usr/bin/env python3
"""
Graph Confidence Filter & Poison Tree Pruning Engine
Part of LifeTree Decision Intelligence System
"""

import sys
import json
from typing import Dict, Any, List, Set

def process_knowledge_graph(graph_data: Dict[str, Any], revoked_source_ids: List[str] = None, min_confidence: float = 0.0) -> Dict[str, Any]:
    if revoked_source_ids is None:
        revoked_source_ids = []

    revoked_set: Set[str] = set(revoked_source_ids)
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    pruned_nodes: List[Dict[str, Any]] = []
    poisoned_node_ids: Set[str] = set()

    # Step 1: Identify and prune poison nodes (Source_ID matching revoked connectors/sources)
    for node in nodes:
        source_id = node.get("source_id", "")
        confidence = node.get("confidence", 1.0)
        
        if source_id in revoked_set:
            poisoned_node_ids.add(node.get("id"))
            continue

        if confidence < min_confidence:
            continue

        # Add visual rendering metadata
        # Official (1.0) / Community (0.8) -> SOLID line; Model prediction (0.5) -> DASHED line
        render_style = "SOLID" if confidence >= 0.8 else "DASHED"
        node_copy = dict(node)
        node_copy["visual_style"] = render_style
        pruned_nodes.append(node_copy)

    # Step 2: Prune edges connected to poisoned/removed nodes
    valid_node_ids: Set[str] = {n["id"] for n in pruned_nodes}
    pruned_edges: List[Dict[str, Any]] = []

    for edge in edges:
        source_node = edge.get("source")
        target_node = edge.get("target")
        edge_source_id = edge.get("source_id", "")
        edge_confidence = edge.get("confidence", 1.0)

        if edge_source_id in revoked_set:
            continue

        if source_node in valid_node_ids and target_node in valid_node_ids:
            edge_copy = dict(edge)
            edge_copy["visual_style"] = "SOLID" if edge_confidence >= 0.8 else "DASHED"
            pruned_edges.append(edge_copy)

    return {
        "summary": {
            "original_nodes_count": len(nodes),
            "retained_nodes_count": len(pruned_nodes),
            "poisoned_nodes_removed": len(poisoned_node_ids),
            "revoked_source_ids": revoked_source_ids,
            "min_confidence_threshold": min_confidence
        },
        "nodes": pruned_nodes,
        "edges": pruned_edges
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Fallback synthetic graph
        data = {
            "nodes": [
                {"id": "node_1", "label": "Chancenkarte Law 2024", "source_id": "SRC_GOV_DE", "confidence": 1.0},
                {"id": "node_2", "label": "Community Forum Post on Visa Processing Time", "source_id": "SRC_COMMUNITY_REDDIT", "confidence": 0.8},
                {"id": "node_3", "label": "AI Predicted 2026 Quota Increase", "source_id": "SRC_LLM_PREDICT", "confidence": 0.5},
                {"id": "node_4", "label": "Fake Agency Advice", "source_id": "SRC_POISONED_PLUGIN", "confidence": 0.8}
            ],
            "edges": [
                {"source": "node_1", "target": "node_2", "source_id": "SRC_GOV_DE", "confidence": 0.9},
                {"source": "node_1", "target": "node_3", "source_id": "SRC_LLM_PREDICT", "confidence": 0.5},
                {"source": "node_2", "target": "node_4", "source_id": "SRC_POISONED_PLUGIN", "confidence": 0.8}
            ]
        }

    res = process_knowledge_graph(data, revoked_source_ids=["SRC_POISONED_PLUGIN"], min_confidence=0.0)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
