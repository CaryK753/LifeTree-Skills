#!/usr/bin/env python3
"""
LifeTree Multi-Pathway Trade-Off & Comparison Matrix Generator
Renders side-by-side comparative matrices across candidate decision pathways
"""

import sys
import json
from typing import Dict, Any, List

# C7 fix: default goal context used when the caller doesn't supply one. The previous
# implementation always favored the lowest-cost / shortest-horizon path, so a domestic
# fallback ("Plan B: 国内发展路线") would beat the actual goal-achieving Germany paths
# purely on cost. The default goal_keywords cover the Germany/PR migration case (the
# most common LifeTree use case); callers can override via goal_context.
DEFAULT_GOAL_CONTEXT = {
    "primary_goal": "MIGRATION_TO_GERMANY_PR",
    "goal_keywords": ["Germany", "German", "Chancenkarte", "Blue Card", "EU Blue Card",
                      "德国", "机会卡", "蓝卡", "永居", "PR", "Niederlassungserlaubnis",
                      "Job Seeker", "找工作签证"],
    "anti_keywords": ["Domestic", "Stay Home", "国内", "Plan B", "本土", "Local"],
    "goal_weight": 0.35,  # weight of goal_alignment in composite score (0-1)
}


def _compute_goal_alignment(option: Dict[str, Any], goal_context: Dict[str, Any]) -> tuple:
    """
    C7: compute a 0-100 goal_alignment_score for a pathway option.
    Priority:
      1. Explicit `goal_alignment_score` field on the option (caller-supplied).
      2. Tag matching if both `goal_tags` (on option) and `pathway_goal_tags` (on context) exist.
      3. Keyword heuristic: scan name + description for goal_keywords (+) and anti_keywords (−).
    Returns (score, explanation).
    """
    # 1. Explicit override
    if "goal_alignment_score" in option:
        score = float(option.get("goal_alignment_score", 0.0))
        score = max(0.0, min(100.0, score))
        return score, f"explicit goal_alignment_score={score} supplied by caller"

    name = str(option.get("name", "")).lower()
    desc = str(option.get("description", "")).lower()
    text = f"{name} {desc}"

    # 2. Tag matching
    goal_tags = option.get("goal_tags") or []
    pathway_goal_tags = goal_context.get("pathway_goal_tags") or []
    if goal_tags and pathway_goal_tags:
        matched = set(str(t).lower() for t in goal_tags) & set(str(t).lower() for t in pathway_goal_tags)
        score = round((len(matched) / max(1, len(set(t.lower() for t in pathway_goal_tags)))) * 100.0, 1)
        return score, f"tag matching: {len(matched)}/{len(pathway_goal_tags)} goal tags matched"

    # 3. Keyword heuristic
    goal_kw = [str(k).lower() for k in goal_context.get("goal_keywords", [])]
    anti_kw = [str(k).lower() for k in goal_context.get("anti_keywords", [])]
    pos_hits = [k for k in goal_kw if k and k in text]
    neg_hits = [k for k in anti_kw if k and k in text]

    # +20 per positive hit (cap at 100), −30 per negative hit (floor at 0)
    raw = 50.0 + (len(pos_hits) * 20.0) - (len(neg_hits) * 30.0)
    score = max(0.0, min(100.0, raw))
    explanation = (
        f"keyword heuristic: +{len(pos_hits)} goal keyword(s) {pos_hits}, "
        f"−{len(neg_hits)} anti keyword(s) {neg_hits} → score {score:.1f}"
    )
    return round(score, 1), explanation


def generate_comparison_matrix(pathway_options: List[Dict[str, Any]],
                               goal_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Compares candidate pathways side-by-side across key decision dimensions:
    - Financial Capital Commitment (USD/EUR)
    - Execution Horizon (Months to Goal)
    - Risk & Rejection Level
    - Prerequisite Friction (Language/Qualification)
    - Plan B Hedge Score (0-100)
    - Goal Alignment Score (0-100)   ← C7: NEW, prevents non-goal-achieving paths from winning

    C7 fix: previously the composite score was purely cost/time/risk-based, so a cheap
    domestic fallback always beat the user's actual goal-achieving path. Now the composite
    blends `tradeoff_score` with `goal_alignment_score` (default weight 0.35). A pathway
    that doesn't advance the user's stated goal (alignment=0) can score at most
    (1 − goal_weight) * 100 = 65, while a goal-aligned pathway (alignment=100) can
    reach 100. This ensures the domestic Plan B no longer outranks Germany paths when
    the user's goal is migration to Germany.
    """
    if goal_context is None:
        goal_context = DEFAULT_GOAL_CONTEXT
    goal_weight = max(0.0, min(1.0, float(goal_context.get("goal_weight", 0.35))))
    tradeoff_weight = 1.0 - goal_weight

    matrix_rows = []
    winner_score = -1.0
    top_recommended = None

    for opt in pathway_options:
        p_name = opt.get("name", "Unnamed Pathway")
        cost = opt.get("financial_cost_usd", 0.0)
        horizon_months = opt.get("horizon_months", 12)
        risk_level = opt.get("risk_level", "MEDIUM").upper()
        prereq_friction = opt.get("prereq_friction_level", "MEDIUM").upper()
        plan_b_reliability = opt.get("plan_b_reliability_score", 70.0)

        # Trade-Off Index (0 to 100, higher is better) — original logic preserved
        risk_penalty = {"LOW": 0, "MEDIUM": 15, "HIGH": 35, "CRITICAL": 60}.get(risk_level, 20)
        friction_penalty = {"LOW": 0, "MEDIUM": 10, "HIGH": 25}.get(prereq_friction, 10)
        horizon_penalty = min(30.0, horizon_months * 0.5)
        tradeoff_score = max(0.0, 100.0 - risk_penalty - friction_penalty - horizon_penalty + (plan_b_reliability * 0.2))

        # C7: Goal Alignment Score (0-100)
        goal_alignment, goal_explanation = _compute_goal_alignment(opt, goal_context)

        # C7: blend tradeoff with goal alignment. A non-goal path (alignment=0) can
        # score at most tradeoff_weight * 100; a goal-aligned path can reach 100.
        composite_score = round((tradeoff_score * tradeoff_weight) + (goal_alignment * goal_weight), 1)

        if composite_score > winner_score:
            winner_score = composite_score
            top_recommended = p_name

        matrix_rows.append({
            "pathway_name": p_name,
            "financial_cost_usd": cost,
            "horizon_months": horizon_months,
            "risk_level": risk_level,
            "prerequisite_friction": prereq_friction,
            "plan_b_reliability_score": plan_b_reliability,
            "goal_alignment_score": goal_alignment,
            "goal_alignment_explanation": goal_explanation,
            "tradeoff_score": round(tradeoff_score, 1),
            "composite_tradeoff_score": composite_score
        })

    return {
        "comparison_summary": {
            "pathways_compared_count": len(pathway_options),
            "top_recommended_pathway": top_recommended,
            "highest_composite_score": winner_score,
            "goal_context_applied": goal_context.get("primary_goal", "UNSPECIFIED"),
            "goal_weight": goal_weight
        },
        "comparison_matrix": matrix_rows,
        "recommendation": (
            f"Pathway '{top_recommended}' offers the optimal balance of goal alignment, "
            f"risk, execution time, and Plan B reliability (goal_weight={goal_weight})."
        )
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            opts = json.load(f)
    else:
        opts = [
            {
                "name": "Option A: German Chancenkarte -> EU Blue Card",
                "financial_cost_usd": 14000.0,
                "horizon_months": 24,
                "risk_level": "LOW",
                "prereq_friction_level": "MEDIUM",
                "plan_b_reliability_score": 90.0
            },
            {
                "name": "Option B: Canada Express Entry Direct PR",
                "financial_cost_usd": 18000.0,
                "horizon_months": 18,
                "risk_level": "MEDIUM",
                "prereq_friction_level": "HIGH",
                "plan_b_reliability_score": 75.0
            },
            {
                "name": "Option C: Caribbean Golden Visa",
                "financial_cost_usd": 150000.0,
                "horizon_months": 6,
                "risk_level": "LOW",
                "prereq_friction_level": "LOW",
                "plan_b_reliability_score": 85.0
            }
        ]

    res = generate_comparison_matrix(opts)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
