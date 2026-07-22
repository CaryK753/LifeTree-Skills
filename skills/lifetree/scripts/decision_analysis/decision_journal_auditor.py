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

        # m2 fix: Regret Minimization score now uses real decision-quality criteria
        # instead of `50 + rationale_length * 0.2`. The old formula gave a 250-char
        # rationale a score of 100 regardless of content, and a 10-char rationale a
        # score of 52 — completely uncorrelated with decision quality.
        #
        # New criteria (each 0..25, summed to 0..100):
        #   1. Rationale quality    — score 0..25 based on documented research depth
        #                             (presence of alternatives_considered, evidence_links,
        #                             quant_analysis fields), NOT on string length.
        #   2. Goal alignment       — score 0..25 based on entry's alignment_with_stated_goal
        #                             field, or 12.5 (neutral) if not recorded.
        #   3. Plan B readiness     — score 0..25 based on plan_b_status:
        #                             READY/ACTIVE_RESERVE=25, DRAFT=15, INACTIVE=0.
        #   4. Reversibility guard  — score 0..25: if entry marked is_reversible=true → 25,
        #                             is_reversible=false → 5 (irreversible = higher regret
        #                             risk), unknown → 12.5.
        rationale_text = str(entry.get("user_rationale", ""))

        # (1) Rationale quality: look for structured research markers, not length.
        research_markers = 0
        for marker_field in ["alternatives_considered", "evidence_links", "quant_analysis",
                             "data_sources", "consulted_advisors"]:
            if entry.get(marker_field):
                research_markers += 1
        # Bonus for rationales that mention concrete numbers/percentages (≥3 digits)
        import re as _re
        if _re.search(r"\d{3,}", rationale_text):
            research_markers += 1
        rationale_quality = min(25.0, research_markers * 5.0)

        # (2) Goal alignment
        goal_align_raw = entry.get("alignment_with_stated_goal")
        if goal_align_raw is None:
            goal_alignment = 12.5  # neutral when not recorded
        else:
            try:
                goal_alignment = max(0.0, min(25.0, float(goal_align_raw) * 25.0))
            except (TypeError, ValueError):
                goal_alignment = 12.5

        # (3) Plan B readiness
        plan_b_readiness = {"READY": 25.0, "ACTIVE_RESERVE": 25.0, "DRAFT": 15.0,
                             "INACTIVE": 0.0}.get(plan_b_status, 0.0)

        # (4) Reversibility guard
        is_reversible = entry.get("is_reversible", None)
        if is_reversible is True:
            reversibility = 25.0
        elif is_reversible is False:
            reversibility = 5.0
        else:
            reversibility = 12.5

        regret_score = rationale_quality + goal_alignment + plan_b_readiness + reversibility
        # Penalyze undocumented strategic pivots — switching paths without research
        # is the canonical high-regret move.
        if is_pivot and research_markers == 0:
            regret_score = max(0.0, regret_score - 15.0)

        audited_entries.append({
            "entry_id": entry.get("entry_id"),
            "timestamp": entry.get("timestamp"),
            "topic_id": entry.get("topic_id"),
            "chosen_pathway": curr_path,
            "is_strategic_pivot": is_pivot,
            "regret_minimization_score": round(regret_score, 1),
            "regret_score_breakdown": {
                "rationale_quality": round(rationale_quality, 1),
                "goal_alignment": round(goal_alignment, 1),
                "plan_b_readiness": round(plan_b_readiness, 1),
                "reversibility_guard": round(reversibility, 1),
                "undocumented_pivot_penalty": -15.0 if (is_pivot and research_markers == 0) else 0.0
            }
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
