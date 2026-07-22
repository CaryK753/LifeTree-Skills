#!/usr/bin/env python3
"""
LifeTree Incremental Diff Engine & Tiered Push Alert Manager
Implements Event-Driven Incremental Polling, Daily/Weekly Brief Queuing, and High-Risk Circuit Breaker Alerts
"""

import sys
import json
from typing import Dict, Any, List

def process_event_diff(previous_state: Dict[str, Any], current_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares previous knowledge graph/policy state against current state.
    - If NO diff: returns silent (0 notification resource consumed).
    - If LOW/MEDIUM risk diff: queues for Daily/Weekly Brief.
    - If HIGH/CRITICAL risk diff: triggers Urgent Circuit Breaker Alert (SMS / Direct Push).
    """
    prev_nodes = {n["id"]: n for n in previous_state.get("nodes", [])}
    curr_nodes = {n["id"]: n for n in current_state.get("nodes", [])}

    added_nodes = []
    modified_nodes = []
    removed_nodes = []

    for nid, node in curr_nodes.items():
        if nid not in prev_nodes:
            added_nodes.append(node)
        else:
            prev_node = prev_nodes[nid]
            if prev_node != node:
                modified_nodes.append({
                    "id": nid,
                    "previous": prev_node,
                    "current": node
                })

    for nid, node in prev_nodes.items():
        if nid not in curr_nodes:
            removed_nodes.append(node)

    has_changes = bool(added_nodes or modified_nodes or removed_nodes)

    if not has_changes:
        return {
            "status": "SILENT_NO_CHANGE",
            "message": "Incremental Diff Engine: No changes detected. Silent mode active (0 notification resources used).",
            "push_action": "NONE",
            "diff_summary": {"added": 0, "modified": 0, "removed": 0}
        }

    # Evaluate Risk Severity of Changes
    max_severity = "LOW"
    circuit_breaker_triggers = []
    queued_brief_items = []

    for node in added_nodes + [m["current"] for m in modified_nodes]:
        risk_level = node.get("risk_level", "LOW").upper()
        label = node.get("label", "Unknown Entity")

        if risk_level in ["CRITICAL", "HIGH"]:
            max_severity = "CRITICAL" if risk_level == "CRITICAL" else max(max_severity, "HIGH")
            circuit_breaker_triggers.append({
                "severity": risk_level,
                "entity": label,
                "action_required": "URGENT_CIRCUIT_BREAKER_ALERT",
                "message": f"CRITICAL RISK EVENT: '{label}' status updated! Instant review required."
            })
        else:
            queued_brief_items.append({
                "severity": risk_level,
                "entity": label,
                "message": f"Routine policy update: '{label}' modified."
            })

    for node in removed_nodes:
        label = node.get("label", "Unknown Entity")
        circuit_breaker_triggers.append({
            "severity": "HIGH",
            "entity": label,
            "action_required": "URGENT_CIRCUIT_BREAKER_ALERT",
            "message": f"HIGH RISK: Node '{label}' revoked or removed from official gazette!"
        })

    # Determine Dispatch Channel
    if max_severity in ["CRITICAL", "HIGH"]:
        push_action = "URGENT_SMS_AND_STRONG_PUSH"
    else:
        push_action = "QUEUE_FOR_DAILY_WEEKLY_BRIEF"

    return {
        "status": "DIFF_DETECTED",
        "has_changes": True,
        "max_severity": max_severity,
        "push_action": push_action,
        "diff_summary": {
            "added_count": len(added_nodes),
            "modified_count": len(modified_nodes),
            "removed_count": len(removed_nodes)
        },
        "urgent_alerts": circuit_breaker_triggers,
        "queued_brief_items": queued_brief_items
    }

def main():
    if len(sys.argv) > 2:
        with open(sys.argv[1], 'r', encoding='utf-8') as f1, open(sys.argv[2], 'r', encoding='utf-8') as f2:
            prev = json.load(f1)
            curr = json.load(f2)
    else:
        prev = {
            "nodes": [
                {"id": "n1", "label": "Chancenkarte Quota", "risk_level": "LOW"}
            ]
        }
        curr = {
            "nodes": [
                {"id": "n1", "label": "Chancenkarte Quota", "risk_level": "CRITICAL"},
                {"id": "n2", "label": "New Sperrkonto Limit €12,500", "risk_level": "HIGH"}
            ]
        }

    res = process_event_diff(prev, curr)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
