#!/usr/bin/env python3
"""
LifeTree Decision Journal Auditor & Regret Minimization Engine
Audits historical user decision entries, evaluates decision drift, and applies the Regret Minimization Framework
"""

import sys
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

def audit_decision_journal(journal_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Audits user's historical decision entries over time.
    Evaluates:
    - Decision Stability & Pivots Count
    - Regret Minimization Index (0-100): High score means choice aligns with long-term 80-year-old self perspective.
    - Plan B Preparedness Score
    """
    if not journal_entries:
        return {
            "audit_summary": {
                "total_decisions_logged": 0,
                "regret_minimization_index": 50.0,
                "verdict": "No decision journal entries logged yet."
            }
        }

    total_decisions = len(journal_entries)
    plan_b_active_count = 0
    pivots_count = 0
    audited_entries = []

    last_path = None
    for entry in journal_entries:
        curr_path = entry.get("chosen_pathway")
        plan_b_status = entry.get("plan_b_status", "INACTIVE")

        is_pivot = (last_path is not None and curr_path != last_path)
        if is_pivot:
            pivots_count += 1
        last_path = curr_path

        if plan_b_status in ["READY", "ACTIVE_RESERVE"]:
            plan_b_active_count += 1

        # Regret Minimization Evaluation
        # High rationale clarity + active Plan B -> High Regret Minimization Score
        rationale_length = len(entry.get("user_rationale", ""))
        regret_score = min(100.0, 50.0 + (rationale_length * 0.2) + (30.0 if plan_b_status != "INACTIVE" else 0.0))

        audited_entries.append({
            "entry_id": entry.get("entry_id"),
            "timestamp": entry.get("timestamp"),
            "topic_id": entry.get("topic_id"),
            "chosen_pathway": curr_path,
            "is_strategic_pivot": is_pivot,
            "regret_minimization_score": round(regret_score, 1)
        })

    avg_regret_score = round(sum(e["regret_minimization_score"] for e in audited_entries) / total_decisions, 1)
    plan_b_readiness_pct = round((plan_b_active_count / total_decisions) * 100.0, 1)

    return {
        "audit_summary": {
            "total_decisions_logged": total_decisions,
            "strategic_pivots_count": pivots_count,
            "plan_b_readiness_pct": plan_b_readiness_pct,
            "regret_minimization_index": avg_regret_score,
            "audit_verdict": "HIGHLY_ROBUST" if avg_regret_score >= 80.0 else ("MODERATE_ALIGNMENT" if avg_regret_score >= 60.0 else "HIGH_REGRET_RISK")
        },
        "audited_entries": audited_entries,
        "regret_minimization_guidance": "Regret Minimization Principle: Ensure every major pivot maintains an active Plan B reserve to prevent irreversible downside risk."
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            entries = json.load(f)
    else:
        entries = [
            {
                "entry_id": "dec_1",
                "timestamp": "2026-01-15T00:00:00Z",
                "topic_id": "tpc_mobility",
                "chosen_pathway": "Chancenkarte § 20a",
                "user_rationale": "High score margin with German B1 and C1 English.",
                "plan_b_status": "READY"
            },
            {
                "entry_id": "dec_2",
                "timestamp": "2026-06-20T00:00:00Z",
                "topic_id": "tpc_mobility",
                "chosen_pathway": "EU Blue Card § 18g",
                "user_rationale": "Transitioned to direct software engineering offer.",
                "plan_b_status": "ACTIVE_RESERVE"
            }
        ]

    res = audit_decision_journal(entries)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
