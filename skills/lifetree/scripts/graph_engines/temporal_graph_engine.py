#!/usr/bin/env python3
"""
LifeTree Object-Centric Temporal GraphRAG & Influence Diagram Engine
Performs lowest-friction causal pathfinding (Dijkstra algorithm) and multi-hop risk cascade simulation,
superimposing Influence Diagram node semantics (Decision ⬜, Chance ⚪, Value ♢) and Causal Intervention tagging.
"""

import sys
import os
import json
import heapq
from typing import Dict, Any, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
DECISION_MODELS_DIR = os.path.join(SKILL_ROOT, "scripts", "decision_models")
if DECISION_MODELS_DIR not in sys.path:
    sys.path.insert(0, DECISION_MODELS_DIR)

try:
    import influence_diagram_layer
except ImportError:
    influence_diagram_layer = None

def find_optimal_causal_path(graph: Dict[str, Any], start_node_id: str, target_node_id: str) -> Dict[str, Any]:
    """
    Finds lowest-friction causal path using Dijkstra algorithm over temporal graph.
    Superimposes Influence Diagram semantics (Decision, Chance, Value) over path nodes.
    """
    try:
        nodes_dict = {n["id"]: n for n in graph.get("nodes", [])}
        edges = graph.get("edges", [])

        if start_node_id not in nodes_dict or target_node_id not in nodes_dict:
            return {
                "found": False,
                "pathfinding_summary": {
                    "start_node": start_node_id,
                    "target_node": target_node_id,
                    "error_message": "Start or Target node not found in graph."
                }
            }

        # Build adjacency list: node_id -> list of (target_id, friction_cost, edge_obj)
        adj = {}
        for edge in edges:
            src = edge["source"]
            tgt = edge["target"]
            weight = float(edge.get("kinetic_weight", 1.0))
            friction = float(edge.get("friction_penalty", 0.0))
            conf = float(edge.get("confidence", 1.0))

            if conf < 0.60:
                continue

            cost = max(0.1, (1.0 / weight) + friction + (1.0 - conf))
            adj.setdefault(src, []).append((tgt, cost, edge))

        # Dijkstra algorithm
        distances = {node_id: float('inf') for node_id in nodes_dict}
        distances[start_node_id] = 0.0
        previous_nodes = {node_id: None for node_id in nodes_dict}
        previous_edges = {node_id: None for node_id in nodes_dict}

        pq = [(0.0, start_node_id)]

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u == target_node_id:
                break

            if current_dist > distances[u]:
                continue

            for v, cost, edge_obj in adj.get(u, []):
                new_dist = current_dist + cost
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous_nodes[v] = u
                    previous_edges[v] = edge_obj
                    heapq.heappush(pq, (new_dist, v))

        if distances[target_node_id] == float('inf'):
            return {
                "found": False,
                "pathfinding_summary": {
                    "start_node": start_node_id,
                    "target_node": target_node_id,
                    "error_message": "No valid confidence-weighted causal path exists."
                }
            }

        # Reconstruct path
        path_nodes = []
        path_edges = []
        curr = target_node_id
        while curr is not None:
            raw_node = nodes_dict[curr]
            etype = raw_node.get("entity_type", "").upper()

            # Superimpose Influence Diagram Node Types
            symbol = "⬜" if etype in ["ACTION", "PATHWAY_ROUTE", "DECISION"] else ("♢" if etype in ["CAPITAL_ASSET", "VALUE", "UTILITY"] else "⚪")
            path_nodes.append({
                "id": raw_node["id"],
                "label": f"{symbol} {raw_node.get('label', raw_node['id'])}",
                "entity_type": raw_node.get("entity_type", "CONCEPT"),
                "confidence": raw_node.get("confidence", 1.0)
            })

            edge_obj = previous_edges[curr]
            if edge_obj:
                rel = edge_obj.get("relation_type", "IMPACTS")
                is_causal = rel in ["REQUIRES_CAPITAL", "MUTATES_STATE", "TRIGGERS_EVENT", "GOVERNS", "CONVERTS_TO"]
                path_edges.append({
                    "source": edge_obj["source"],
                    "target": edge_obj["target"],
                    "relation_type": rel,
                    "is_causal_intervention": is_causal,
                    "confidence": edge_obj.get("confidence", 1.0)
                })

            curr = previous_nodes[curr]

        path_nodes.reverse()
        path_edges.reverse()

        return {
            "found": True,
            "pathfinding_summary": {
                "start_node": start_node_id,
                "target_node": target_node_id,
                "total_path_friction_cost": round(distances[target_node_id], 2),
                "hops_count": len(path_edges)
            },
            "path_nodes": path_nodes,
            "path_edges": path_edges
        }

    except Exception as e:
        return {"found": False, "error_message": str(e)}

def simulate_multi_hop_risk_cascade(graph: Dict[str, Any], initial_poison_node_id: str, max_hops: int = 3) -> Dict[str, Any]:
    try:
        nodes_dict = {n["id"]: n for n in graph.get("nodes", [])}
        edges = graph.get("edges", [])

        if initial_poison_node_id not in nodes_dict:
            return {"status": "ERROR", "message": "Poison node not found"}

        impacted_nodes = {initial_poison_node_id: {"hop": 0, "cascade_decay": 1.0}}
        queue = [(initial_poison_node_id, 0, 1.0)]

        adj_out = {}
        for edge in edges:
            adj_out.setdefault(edge["source"], []).append((edge["target"], float(edge.get("confidence", 1.0))))

        while queue:
            curr_id, current_hop, current_decay = queue.pop(0)

            if current_hop >= max_hops:
                continue

            for nxt_id, edge_conf in adj_out.get(curr_id, []):
                nxt_decay = current_decay * edge_conf * 0.8
                if nxt_id not in impacted_nodes or impacted_nodes[nxt_id]["cascade_decay"] < nxt_decay:
                    impacted_nodes[nxt_id] = {"hop": current_hop + 1, "cascade_decay": round(nxt_decay, 3)}
                    queue.append((nxt_id, current_hop + 1, nxt_decay))

        return {
            "status": "SUCCESS",
            "cascade_summary": {
                "initial_poison_node": initial_poison_node_id,
                "max_hops_simulated": max_hops,
                "total_impacted_ontology_objects": len(impacted_nodes)
            },
            "impacted_ontology_objects": impacted_nodes
        }

    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def main():
    g = {
        "nodes": [
            {"id": "usr_person", "label": "Person (Applicant)", "entity_type": "PERSON", "confidence": 1.0},
            {"id": "asset_sperrkonto", "label": "€12,000 Blocked Account", "entity_type": "CAPITAL_ASSET", "confidence": 1.0},
            {"id": "route_bluecard", "label": "EU Blue Card Permit § 18g", "entity_type": "PATHWAY_ROUTE", "confidence": 1.0}
        ],
        "edges": [
            {"source": "usr_person", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL", "confidence": 1.0},
            {"source": "asset_sperrkonto", "target": "route_bluecard", "relation_type": "CONVERTS_TO", "confidence": 1.0}
        ]
    }
    res = find_optimal_causal_path(g, "usr_person", "route_bluecard")
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
