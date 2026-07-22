#!/usr/bin/env python3
"""
LifeTree Divergent Thinking Mode Engine (思维发散模式)
Proactively discovers latent, non-obvious risk domains connected to explicit user research topics
"""

import sys
import json
from typing import Dict, Any, List

LATENT_RISK_DOMAIN_KNOWLEDGE_BASE = [
    {
        "category": "TAX_RESIDENCY_TRAP",
        "trigger_topics": ["IMMIGRATION", "GLOBAL_MOBILITY", "CAREER_PIVOT"],
        "title": "Dual Tax Residency & Exit Tax Exposure",
        "description": "Cross-border relocation may trigger unexpected tax residency status, worldwide income taxation, or exit tax liabilities in origin/destination jurisdictions.",
        "severity": "HIGH",
        "suggested_tracking_metric": "Days spent in jurisdiction & Tax Treaty Clause"
    },
    {
        "category": "FOREIGN_EXCHANGE_RESTRICTION",
        "trigger_topics": ["ASSET_ALLOCATION", "IMMIGRATION", "REAL_ESTATE"],
        "title": "Capital Outflow Controls & FX Conversion Bottlenecks",
        "description": "Strict foreign exchange quotas or tightening capital controls in origin country may delay statutory deposits or property purchases.",
        "severity": "CRITICAL",
        "suggested_tracking_metric": "Statutory Annual Capital Transfer Limit"
    },
    {
        "category": "HEALTHCARE_INSURANCE_GAP",
        "trigger_topics": ["IMMIGRATION", "RETIREMENT", "FAMILY_SUCCESSION"],
        "title": "Pre-existing Condition Exclusion & Coverage Void",
        "description": "Transitioning between national healthcare systems or private health insurance may leave temporary 3-6 month coverage gaps for pre-existing medical conditions.",
        "severity": "HIGH",
        "suggested_tracking_metric": "Statutory Waiting Period (Wartezeit)"
    },
    {
        "category": "FAMILY_ESTATE_SUCCESSION",
        "trigger_topics": ["ASSET_ALLOCATION", "FAMILY_PLANNING"],
        "title": "Forced Heirship & Cross-Border Estate Tax Conflict",
        "description": "Holding international real estate or offshore accounts can expose wealth to conflicting inheritance laws (e.g. Napoleonic Code forced heirship vs common law probate).",
        "severity": "MEDIUM",
        "suggested_tracking_metric": "EU Succession Regulation No 650/2012 / Local Probate Laws"
    },
    {
        "category": "EDUCATION_QUOTA_SHIFT",
        "trigger_topics": ["FAMILY_PLANNING", "IMMIGRATION"],
        "title": "Public School Enrollment Residency Cut-off",
        "description": "Children's admission to public schools or university tuition discounts depends on strict municipal registration dates, not visa issue date.",
        "severity": "MEDIUM",
        "suggested_tracking_metric": "Municipal School Registration Cut-off Date"
    }
]

def discover_latent_risks(active_topics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Scans active user research topics using Divergent Thinking Mode to uncover hidden risk domains.
    Returns a structured Latent Risk Map for continuous surveillance.
    """
    topic_categories = {t.get("category", "GENERAL").upper() for t in active_topics}
    
    discovered_risks = []
    
    for latent_rule in LATENT_RISK_DOMAIN_KNOWLEDGE_BASE:
        triggers = latent_rule["trigger_topics"]
        if any(trg in topic_categories for trg in triggers):
            discovered_risks.append({
                "risk_id": f"risk_latent_{latent_rule['category'].lower()}",
                "title": latent_rule["title"],
                "category": latent_rule["category"],
                "severity": latent_rule["severity"],
                "description": latent_rule["description"],
                "suggested_tracking_metric": latent_rule["suggested_tracking_metric"],
                "status": "DISCOVERED_FOR_SURVEILLANCE"
            })

    return {
        "divergent_discovery_summary": {
            "scanned_topics_count": len(active_topics),
            "latent_risks_discovered_count": len(discovered_risks),
            "divergent_mode_status": "ACTIVE"
        },
        "discovered_risk_domains": discovered_risks,
        "recommendation": "Register discovered risk domains into continuous surveillance tracking pipeline."
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            topics = json.load(f)
    else:
        topics = [
            {"topic_id": "t1", "title": "German Skilled Migration", "category": "IMMIGRATION"},
            {"topic_id": "t2", "title": "Global Tech Stock Portfolio", "category": "ASSET_ALLOCATION"}
        ]

    res = discover_latent_risks(topics)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
