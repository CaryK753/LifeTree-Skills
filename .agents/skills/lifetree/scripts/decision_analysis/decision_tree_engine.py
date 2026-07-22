#!/usr/bin/env python3
"""
LifeTree Universal Decision Tree Path Solver & What-If Engine
Generates GenUI compliant node trees with Top-3 Smart Pruning & Default Collapse
"""

import sys
import json
from typing import Dict, Any, List

def build_decision_tree(user_profile: Dict[str, Any], evaluation_results: List[Dict[str, Any]], top_k: int = 3) -> Dict[str, Any]:
    """
    Builds a GenUI visual tree contract containing:
    - TRUNK: Baseline current state
    - MAIN_BRANCH: Optimal approved pathways (Top-K visible by default, others collapsed)
    - SIDE_BUD: What-If simulation variations
    - DEAD_BRANCH: Blocked or high-risk paths (collapsed by default to prevent choice paralysis)
    - PLAN_B_HEDGE: Fallback mitigation branch
    """
    tree_id = f"tree_{user_profile.get('user_id', 'anon')}"

    trunk_node = {
        "id": "trunk_baseline",
        "type": "TRUNK",
        "label": f"Current Profile ({user_profile.get('nationality', 'Global')})",
        "data": user_profile,
        "style": {"color": "#2E7D32", "line_width": 4, "pattern": "SOLID"},
        "ui_state": {"expanded": True}
    }

    approved_evals = [e for e in evaluation_results if e.get("eligible", False)]
    blocked_evals = [e for e in evaluation_results if not e.get("eligible", False)]

    # Sort approved evaluations by score or preference
    sorted_approved = sorted(approved_evals, key=lambda x: x.get("points_audit", {}).get("total_points", 0), reverse=True)

    branches = []
    dead_branches = []
    side_buds = []

    # Smart Pruning: Top-K paths are expanded by default, remaining paths are collapsed
    for idx, eval_res in enumerate(sorted_approved):
        domain_title = eval_res.get("domain_title", f"Approved Path {idx+1}")
        is_top_k = (idx < top_k)
        
        branch_id = f"branch_app_{idx+1}"
        branches.append({
            "id": branch_id,
            "parent_id": "trunk_baseline",
            "type": "MAIN_BRANCH",
            "label": f"Pathway: {domain_title}",
            "status": "APPROVED",
            "rank": idx + 1,
            "ui_state": {
                "expanded_by_default": is_top_k,
                "badge": "TOP_RECOMMENDED" if is_top_k else None
            },
            "style": {"color": "#1976D2", "line_width": 3, "pattern": "SOLID"}
        })

    # Blocked paths (DEAD_BRANCH) are collapsed by default to prevent choice paralysis
    for idx, eval_res in enumerate(blocked_evals):
        domain_title = eval_res.get("domain_title", f"Blocked Path {idx+1}")
        failures = eval_res.get("thresholds_audit", {}).get("failures", []) + eval_res.get("prerequisites_audit", {}).get("failures", [])
        
        branch_id = f"branch_blk_{idx+1}"
        dead_branches.append({
            "id": branch_id,
            "parent_id": "trunk_baseline",
            "type": "DEAD_BRANCH",
            "label": f"Blocked: {domain_title}",
            "status": "BLOCKED",
            "rejection_reasons": failures,
            "ui_state": {
                "expanded_by_default": False, # COLLAPSED BY DEFAULT
                "badge": "RISK_ALERT"
            },
            "style": {"color": "#D32F2F", "line_width": 2, "pattern": "DASHED"}
        })

    # What-If Hypotheses
    what_ifs = user_profile.get("hypothetical_variables", [])
    for widx, wvar in enumerate(what_ifs):
        side_buds.append({
            "id": f"bud_{widx+1}",
            "parent_id": "trunk_baseline",
            "type": "SIDE_BUD",
            "label": f"What-If: {wvar.get('name')}",
            "delta": wvar.get("delta"),
            "ui_state": {"expanded_by_default": True},
            "style": {"color": "#9C27B0", "line_width": 2, "pattern": "DASHED"}
        })

    # Plan B Hedge
    plan_b = {
        "id": "branch_plan_b",
        "parent_id": "trunk_baseline",
        "type": "PLAN_B_HEDGE",
        "label": "Plan B Risk Hedging Pathway",
        "mitigation_strategy": "Maintain dual status liquidity and reserve assets in default local jurisdiction.",
        "ui_state": {"expanded_by_default": True, "badge": "ALTERNATIVE"},
        "style": {"color": "#F57C00", "line_width": 2, "pattern": "SOLID"}
    }

    return {
        "tree_id": tree_id,
        "smart_pruning_policy": {
            "top_k_visible": top_k,
            "collapsed_edge_cases_count": max(0, len(branches) - top_k) + len(dead_branches)
        },
        "nodes": [trunk_node] + branches + dead_branches + side_buds + [plan_b],
        "summary": {
            "total_approved_paths": len(branches),
            "top_recommended_paths": min(top_k, len(branches)),
            "blocked_paths_collapsed": len(dead_branches),
            "what_if_count": len(side_buds),
            "has_plan_b": True
        }
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            profile = data.get("profile", {})
            evals = data.get("evaluations", [])
    else:
        profile = {"user_id": "usr_123", "nationality": "Global Citizen"}
        evals = [
            {"domain_title": "Option A - Fast Track", "eligible": True, "points_audit": {"total_points": 10}},
            {"domain_title": "Option B - Direct Entry", "eligible": True, "points_audit": {"total_points": 8}},
            {"domain_title": "Option C - Employer Sponsored", "eligible": True, "points_audit": {"total_points": 7}},
            {"domain_title": "Option D - Regional Stream", "eligible": True, "points_audit": {"total_points": 6}},
            {"domain_title": "Option E - High Risk Stream", "eligible": False, "thresholds_audit": {"failures": [{"message": "Capital below minimum"}]}}
        ]

    res = build_decision_tree(profile, evals, top_k=3)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
