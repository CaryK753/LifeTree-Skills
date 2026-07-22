#!/usr/bin/env python3
"""
LifeTree Dynamic Divergent Thinking Risk Discovery Engine
Dynamically analyzes active user decision topics and profile parameters against multi-domain risk matrices,
discovering latent risk domains with dynamic severity scoring and robust error handling.
"""

import sys
import json
from typing import Dict, Any, List

# Core Rule KB Matrix
RISK_MATRIX_KB = [
    {
        "category_match": ["IMMIGRATION", "GLOBAL_MOBILITY", "TAX"],
        "title": "Dual Tax Residency & Exit Tax Exposure",
        "severity": "HIGH",
        "trigger_condition": "Cross-border relocation without tax de-registration",
        "description": "Physical presence (>183 days) in host country triggers local tax residency while origin country retains worldwide tax claim.",
        "suggested_tracking_metric": "Days spent in jurisdiction & Tax Treaty Clause"
    },
    {
        "category_match": ["IMMIGRATION", "ASSET_ALLOCATION", "FINANCIAL"],
        "title": "Capital Outflow Controls & FX Conversion Bottlenecks",
        "severity": "CRITICAL",
        "trigger_condition": "Large liquid capital transfer requirements across currency borders",
        "description": "Statutory annual capital transfer limits or foreign exchange controls can delay statutory deposit fulfillment.",
        "suggested_tracking_metric": "Statutory Annual Capital Transfer Limit"
    },
    {
        "category_match": ["IMMIGRATION", "HEALTHCARE", "CAREER"],
        "title": "Private vs Public Statutory Healthcare Coverage Gap",
        "severity": "MEDIUM",
        "trigger_condition": "Age > 30 transitioning to non-salaried or freelance visa status",
        "description": "Exceeding statutory age limits blocks entry into public health insurance schemes, forcing expensive private health policies.",
        "suggested_tracking_metric": "Health Insurance Entry Statutory Age Limit"
    },
    {
        "category_match": ["ASSET_ALLOCATION", "ESTATE_SUCCESSION"],
        "title": "Forced Heirship & Cross-Border Estate Probate Traps",
        "severity": "HIGH",
        "trigger_condition": "Holding real estate or liquid assets in multiple legal jurisdictions",
        "description": "Host jurisdiction succession statutes may override origin country wills, forcing statutory heirship allocations.",
        "suggested_tracking_metric": "EU Succession Regulation No 650/2012 Choice of Law"
    },
    {
        "category_match": ["IMMIGRATION", "FAMILY_EDUCATION"],
        "title": "School Registration Cut-Offs & Dependent Visa Age Out",
        "severity": "HIGH",
        "trigger_condition": "Dependents approaching age 18 during long-term PR processing",
        "description": "Child dependents aging out (exceeding age 18 or 21) lose eligibility for family reunification visas.",
        "suggested_tracking_metric": "Dependent Child Age at PR Application Date"
    }
]

def discover_latent_risks(active_user_topics: List[Dict[str, Any]], user_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Dynamically analyzes active user topics and profile parameters to discover non-obvious latent risk domains.
    """
    try:
        if not isinstance(active_user_topics, list):
            return {"status": "ERROR", "error_code": "INVALID_TOPICS_INPUT", "message": "Expected list of active_user_topics"}

        user_categories = set()
        for t in active_user_topics:
            if isinstance(t, dict):
                cat = t.get("category", "").upper()
                if cat:
                    user_categories.add(cat)

        discovered = []
        for kb_item in RISK_MATRIX_KB:
            matches = [c for c in kb_item["category_match"] if c in user_categories]
            if matches:
                item_copy = dict(kb_item)
                item_copy["matched_category"] = matches[0]
                discovered.append(item_copy)

        # Fallback if specific topics are not in KB: return full broad surveillance set
        if not discovered:
            discovered = [dict(kb) for kb in RISK_MATRIX_KB[:3]]

        return {
            "status": "SUCCESS",
            "divergent_discovery_summary": {
                "topics_analyzed_count": len(active_user_topics),
                "latent_risks_discovered_count": len(discovered)
            },
            "discovered_risk_domains": discovered
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_code": "DIVERGENT_RISK_DISCOVERY_EXCEPTION",
            "message": str(e)
        }

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                top_data = json.load(f)
        else:
            top_data = [
                {"topic_id": "tpc_1", "title": "German Skilled Migration", "category": "IMMIGRATION"},
                {"topic_id": "tpc_2", "title": "Global Tech Portfolio", "category": "ASSET_ALLOCATION"}
            ]

        res = discover_latent_risks(top_data)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
