#!/usr/bin/env python3
"""
LifeTree Object-Centric Temporal Knowledge Graph Engine
Implements Object-Centric Dynamic Ontology, Kinetic Links, Dijkstra Causal Pathfinding,
Multi-Hop Risk Cascade Propagation, and High-Centrality Bottleneck Identification.
"""

import sys
import json
import heapq
from typing import Dict, Any, List, Set, Tuple

def find_optimal_causal_path(graph: Dict[str, Any], start_node_id: str, target_node_id: str) -> Dict[str, Any]:
    """
    Implements Dijkstra-based Causal Pathfinding through Object-Centric Ontology.
    Minimizes path friction while maximizing link confidence.
    Edge Weight = (1.0 / (Confidence * Weight)) + Friction_Penalty
    """
    nodes_map = {n["id"]: n for n in graph.get("nodes", [])}
    if start_node_id not in nodes_map or target_node_id not in nodes_map:
        return {"error": "START_OR_TARGET_NODE_NOT_FOUND", "optimal_path": []}

    adj: Dict[str, List[Tuple[str, float, Dict[str, Any]]]] = {n["id"]: [] for n in graph.get("nodes", [])}
    for edge in graph.get("edges", []):
        u = edge.get("source")
        v = edge.get("target")
        if u in adj and v in adj:
            conf = max(0.1, edge.get("confidence", 1.0))
            w = max(0.1, edge.get("kinetic_weight", 1.0))
            friction = edge.get("friction_penalty", 0.0)
            cost = (1.0 / (conf * w)) + friction
            adj[u].append((v, cost, edge))

    # Dijkstra shortest path
    distances = {n: float('inf') for n in nodes_map}
    distances[start_node_id] = 0.0
    pq = [(0.0, start_node_id, [])]
    
    best_path_nodes = []
    best_path_edges = []
    total_cost = float('inf')

    while pq:
        curr_cost, curr_node, path_edges = heapq.heappop(pq)

        if curr_cost > distances[curr_node]:
            continue

        if curr_node == target_node_id:
            total_cost = curr_cost
            best_path_edges = path_edges
            break

        for neighbor, edge_cost, edge_obj in adj[curr_node]:
            new_cost = curr_cost + edge_cost
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path_edges + [edge_obj]))

    if total_cost == float('inf'):
        return {"found": False, "message": f"No valid causal path connects '{start_node_id}' to '{target_node_id}'."}

    path_node_ids = [start_node_id]
    for edge in best_path_edges:
        path_node_ids.append(edge["target"])

    path_nodes = [nodes_map[nid] for nid in path_node_ids if nid in nodes_map]

    return {
        "found": True,
        "pathfinding_summary": {
            "start_node": start_node_id,
            "target_node": target_node_id,
            "total_path_friction_cost": round(total_cost, 2),
            "hops_count": len(best_path_edges)
        },
        "path_nodes": path_nodes,
        "path_edges": best_path_edges
    }

def simulate_multi_hop_risk_cascade(graph: Dict[str, Any], trigger_event_node_id: str, max_hops: int = 3) -> Dict[str, Any]:
    """
    Simulates Multi-Hop Risk Cascade Propagation.
    When a shock event triggers on a node, it propagates across Kinetic Links to N-hop neighbors.
    """
    nodes_map = {n["id"]: n for n in graph.get("nodes", [])}
    if trigger_event_node_id not in nodes_map:
        return {"error": "TRIGGER_NODE_NOT_FOUND"}

    adj: Dict[str, List[Tuple[str, Dict[str, Any]]]] = {n["id"]: [] for n in graph.get("nodes", [])}
    for edge in graph.get("edges", []):
        u = edge.get("source")
        v = edge.get("target")
        if u in adj and v in adj:
            adj[u].append((v, edge))
            adj[v].append((u, edge))

    visited = {trigger_event_node_id: 0}
    queue = [(trigger_event_node_id, 0, 1.0)]
    
    impacted_objects = []

    while queue:
        curr_id, hop, intensity = queue.pop(0)

        if curr_id != trigger_event_node_id:
            impacted_objects.append({
                "object_id": curr_id,
                "label": nodes_map[curr_id].get("label", curr_id),
                "object_type": nodes_map[curr_id].get("entity_type", "UNKNOWN"),
                "hop_distance": hop,
                "cascade_risk_intensity": round(intensity, 3),
                "severity": "CRITICAL" if intensity >= 0.7 else ("HIGH" if intensity >= 0.4 else "MEDIUM")
            })

        if hop < max_hops:
            for neighbor, edge_obj in adj[curr_id]:
                decay_factor = edge_obj.get("confidence", 0.8) * 0.7
                next_intensity = intensity * decay_factor
                if neighbor not in visited or visited[neighbor] > hop + 1:
                    visited[neighbor] = hop + 1
                    queue.append((neighbor, hop + 1, next_intensity))

    return {
        "cascade_summary": {
            "trigger_node_id": trigger_event_node_id,
            "trigger_label": nodes_map[trigger_event_node_id].get("label"),
            "max_propagation_hops": max_hops,
            "total_impacted_ontology_objects": len(impacted_objects)
        },
        "impacted_objects": impacted_objects
    }

def identify_bottleneck_nodes(graph: Dict[str, Any]) -> Dict[str, Any]:
    """
    Identifies high-centrality bottleneck nodes in the Ontology Network.
    Nodes with high in/out degree or prerequisite connections are marked as Single Points of Failure.
    """
    in_degree: Dict[str, int] = {n["id"]: 0 for n in graph.get("nodes", [])}
    out_degree: Dict[str, int] = {n["id"]: 0 for n in graph.get("nodes", [])}

    for edge in graph.get("edges", []):
        u = edge.get("source")
        v = edge.get("target")
        if u in out_degree:
            out_degree[u] += 1
        if v in in_degree:
            in_degree[v] += 1

    bottlenecks = []
    for node in graph.get("nodes", []):
        nid = node["id"]
        degree = in_degree.get(nid, 0) + out_degree.get(nid, 0)
        if degree >= 2:
            bottlenecks.append({
                "node_id": nid,
                "label": node.get("label"),
                "entity_type": node.get("entity_type"),
                "total_degree_centrality": degree,
                "is_single_point_of_failure": degree >= 3,
                "recommendation": "Build Plan B hedge for this high-centrality bottleneck node!"
            })

    bottlenecks.sort(key=lambda x: x["total_degree_centrality"], reverse=True)

    return {
        "bottlenecks_summary": {
            "total_nodes_audited": len(graph.get("nodes", [])),
            "bottlenecks_identified_count": len(bottlenecks)
        },
        "bottleneck_nodes": bottlenecks
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            g = json.load(f)
    else:
        g = {
            "nodes": [
                {"id": "usr_person", "label": "Person (Applicant)", "entity_type": "PERSON"},
                {"id": "reg_chancenkarte", "label": "Chancenkarte Regulation § 20a", "entity_type": "REGULATION_LAW"},
                {"id": "asset_sperrkonto", "label": "€12,000 Blocked Account", "entity_type": "CAPITAL_ASSET"},
                {"id": "route_bluecard", "label": "EU Blue Card Permit § 18g", "entity_type": "PATHWAY_ROUTE"},
                {"id": "inst_embassy", "label": "German Federal Embassy", "entity_type": "INSTITUTION_AGENCY"}
            ],
            "edges": [
                {"source": "usr_person", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL", "confidence": 1.0, "kinetic_weight": 1.0},
                {"source": "asset_sperrkonto", "target": "reg_chancenkarte", "relation_type": "GOVERNS", "confidence": 1.0, "kinetic_weight": 1.0},
                {"source": "reg_chancenkarte", "target": "inst_embassy", "relation_type": "DEPENDS_ON", "confidence": 0.9, "kinetic_weight": 1.0},
                {"source": "inst_embassy", "target": "route_bluecard", "relation_type": "CONVERTS_TO", "confidence": 0.9, "kinetic_weight": 1.0}
            ]
        }

    path_res = find_optimal_causal_path(g, "usr_person", "route_bluecard")
    cascade_res = simulate_multi_hop_risk_cascade(g, "asset_sperrkonto", max_hops=3)
    bottleneck_res = identify_bottleneck_nodes(g)

    output = {
        "dijkstra_optimal_causal_path": path_res,
        "multi_hop_risk_cascade": cascade_res,
        "ontology_bottlenecks_audit": bottleneck_res
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
