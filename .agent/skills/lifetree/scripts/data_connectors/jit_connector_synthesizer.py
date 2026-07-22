#!/usr/bin/env python3
"""
LifeTree Agentic JIT (Just-In-Time) Connector Synthesizer
Converts raw unstructured text/JSON scraped by an AI Agent into validated GraphRAG Node/Edge payloads
"""

import sys
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List

def synthesize_graph_payload(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes clean GraphRAG nodes and edges from raw Agent-extracted facts.
    Input structure:
    {
      "source_url": "https://...",
      "source_type": "OFFICIAL_GAZETTE" | "COMMUNITY_FORUM" | "MODEL_PREDICTION",
      "valid_start": "2024-06-01T00:00:00Z",
      "valid_end": null,
      "raw_entities": [
        {"id": "ent_1", "label": "Chancenkarte § 20a", "type": "POLICY_LAW"}
      ],
      "raw_relations": [
        {"source": "ent_1", "target": "ent_2", "type": "REQUIRES"}
      ]
    }
    """
    source_url = raw_data.get("source_url", "https://lifetree.local/unknown_source")
    source_type = raw_data.get("source_type", "COMMUNITY_FORUM").upper()
    
    # Generate deterministic Source_ID tag from source URL
    source_hash = hashlib.sha256(source_url.encode('utf-8')).hexdigest()[:12]
    source_id = f"SRC_AGENT_{source_type}_{source_hash}"

    # Default Confidence Assignment based on Source Type
    confidence_map = {
        "OFFICIAL_GAZETTE": 1.0,
        "INSTITUTIONAL_API": 1.0,
        "COMMUNITY_FORUM": 0.8,
        "MODEL_PREDICTION": 0.5
    }
    confidence = confidence_map.get(source_type, 0.8)

    valid_start = raw_data.get("valid_start") or datetime.now(timezone.utc).isoformat()
    valid_end = raw_data.get("valid_end")

    valid_time_obj = {
        "start_time": valid_start,
        "end_time": valid_end
    }

    synthesized_nodes = []
    for ent in raw_data.get("raw_entities", []):
        node_id = ent.get("id") or f"node_{hashlib.md5(ent.get('label', '').encode('utf-8')).hexdigest()[:8]}"
        synthesized_nodes.append({
            "id": node_id,
            "label": ent.get("label", "Unnamed Entity"),
            "entity_type": ent.get("type", "POLICY_LAW"),
            "valid_time": valid_time_obj,
            "source_id": source_id,
            "source_url": source_url,
            "confidence": confidence,
            "visual_style": "SOLID" if confidence >= 0.8 else "DASHED"
        })

    synthesized_edges = []
    for rel in raw_data.get("raw_relations", []):
        synthesized_edges.append({
            "source": rel.get("source"),
            "target": rel.get("target"),
            "relation_type": rel.get("type", "IMPACTS"),
            "source_id": source_id,
            "confidence": confidence,
            "visual_style": "SOLID" if confidence >= 0.8 else "DASHED"
        })

    return {
        "synthesis_summary": {
            "source_id": source_id,
            "source_url": source_url,
            "source_type": source_type,
            "assigned_confidence": confidence,
            "nodes_count": len(synthesized_nodes),
            "edges_count": len(synthesized_edges)
        },
        "graph_data": {
            "nodes": synthesized_nodes,
            "edges": synthesized_edges
        }
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Sample Agent raw extraction input
        data = {
            "source_url": "https://www.gesetze-im-internet.de/aufenthg_2004/_20a.html",
            "source_type": "OFFICIAL_GAZETTE",
            "valid_start": "2024-06-01T00:00:00Z",
            "valid_end": None,
            "raw_entities": [
                {"id": "ent_chancenkarte", "label": "Chancenkarte § 20a", "type": "POLICY_LAW"},
                {"id": "ent_points", "label": "6 Points Requirement", "type": "FEES_REQUIREMENT"}
            ],
            "raw_relations": [
                {"source": "ent_chancenkarte", "target": "ent_points", "type": "REQUIRES"}
            ]
        }

    res = synthesize_graph_payload(data)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
