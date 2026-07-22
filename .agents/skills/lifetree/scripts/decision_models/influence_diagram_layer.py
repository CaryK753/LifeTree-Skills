#!/usr/bin/env python3
"""
LifeTree Influence Diagram Semantic Layer & Causal Intervention Engine
Superimposes Decision Nodes (Square), Chance/Uncertainty Nodes (Circle), and Value Nodes (Diamond)
over knowledge graphs and distinguishes causal intervention links from correlation links.
"""

import sys
import json
from typing import Dict, Any, List

def construct_influence_diagram_layer(knowledge_graph: Dict[str, Any]) -> Dict[str, Any]:
    """
    Superimposes Influence Diagram semantics (Decision, Chance, Value) over an input Knowledge Graph
    and tags causal intervention vs correlation edges.
    """
    try:
        if not isinstance(knowledge_graph, dict):
            return {"status": "ERROR", "error_code": "INVALID_GRAPH", "message": "Expected dict for knowledge_graph"}

        nodes = knowledge_graph.get("nodes", [])
        edges = knowledge_graph.get("edges", [])

        typed_nodes = []
        typed_edges = []

        for n in nodes:
            nid = n.get("id")
            label = n.get("label", nid)
            etype = n.get("entity_type", "").upper()

            # Assign Influence Diagram Node Type
            if etype in ["ACTION", "PATHWAY_ROUTE", "DECISION"]:
                id_type = "DECISION_NODE" # Square ⬜
                symbol = "⬜"
            elif etype in ["MACRO_EVENT", "REGULATION_LAW", "INSTITUTION_AGENCY"]:
                id_type = "CHANCE_NODE"   # Circle ⚪
                symbol = "⚪"
            elif etype in ["CAPITAL_ASSET", "VALUE", "UTILITY"]:
                id_type = "VALUE_NODE"    # Diamond ♢
                symbol = "♢"
            else:
                id_type = "CHANCE_NODE"
                symbol = "⚪"

            typed_nodes.append({
                "id": nid,
                "label": f"{symbol} {label}",
                "influence_node_type": id_type,
                "original_entity_type": etype,
                "raw_data": n
            })

        for e in edges:
            rel = e.get("relation_type", "IMPACTS").upper()
            # Distinguish Causal Intervention vs Mere Correlation
            is_causal_intervention = rel in ["REQUIRES_CAPITAL", "MUTATES_STATE", "TRIGGERS_EVENT", "GOVERNS", "CONVERTS_TO"]
            
            typed_edges.append({
                "source": e.get("source"),
                "target": e.get("target"),
                "relation_type": rel,
                "link_semantics": "CAUSAL_INTERVENTION" if is_causal_intervention else "STATISTICAL_CORRELATION",
                "is_causal_intervention": is_causal_intervention,
                "confidence": e.get("confidence", 1.0)
            })

        return {
            "status": "SUCCESS",
            "influence_diagram_summary": {
                "total_nodes_count": len(typed_nodes),
                "decision_nodes_count": sum(1 for n in typed_nodes if n["influence_node_type"] == "DECISION_NODE"),
                "chance_nodes_count": sum(1 for n in typed_nodes if n["influence_node_type"] == "CHANCE_NODE"),
                "value_nodes_count": sum(1 for n in typed_nodes if n["influence_node_type"] == "VALUE_NODE"),
                "causal_intervention_edges_count": sum(1 for e in typed_edges if e["is_causal_intervention"])
            },
            "influence_nodes": typed_nodes,
            "influence_edges": typed_edges
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "INFLUENCE_DIAGRAM_LAYER_EXCEPTION", "message": str(e)}

def main():
    try:
        g = {
            "nodes": [
                {"id": "usr_person", "label": "Applicant", "entity_type": "PERSON"},
                {"id": "route_chancen", "label": "Chancenkarte Visa", "entity_type": "PATHWAY_ROUTE"},
                {"id": "asset_sperrkonto", "label": "€12,000 Sperrkonto", "entity_type": "CAPITAL_ASSET"}
            ],
            "edges": [
                {"source": "usr_person", "target": "route_chancen", "relation_type": "DECISION_CHOICE"},
                {"source": "route_chancen", "target": "asset_sperrkonto", "relation_type": "REQUIRES_CAPITAL"}
            ]
        }
        res = construct_influence_diagram_layer(g)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
