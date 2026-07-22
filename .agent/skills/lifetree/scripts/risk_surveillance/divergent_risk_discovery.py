#!/usr/bin/env python3
"""
LifeTree Combinatorial Divergent Risk Discovery Engine
Generates dynamic latent risk hypotheses across Risk Categories, Impact Subjects, and Causal Mechanisms,
replacing static knowledge bases with true combinatorial risk discovery.
"""

import sys
import json
from typing import Dict, Any, List

# Risk Categories
RISK_CATEGORIES = ["TAX", "LEGAL", "HEALTH", "EDUCATION", "FAMILY", "ASSET", "CAREER", "IMMIGRATION"]

# Impact Subjects
IMPACT_SUBJECTS = ["PERSON", "REGULATION_LAW", "CAPITAL_ASSET", "PATHWAY_ROUTE"]

# Causal Mechanisms & Base Severity Weights
CAUSAL_MECHANISMS = {
    "TRIGGER": {"weight": 0.8, "desc": "Triggers unforeseen statutory or financial liabilities"},
    "BLOCK": {"weight": 1.0, "desc": "Completely blocks target pathway progression"},
    "DELAY": {"weight": 0.6, "desc": "Imposes significant statutory processing delays"},
    "COST_INCREASE": {"weight": 0.7, "desc": "Causes unanticipated statutory capital expenditure"},
    "CONFLICT": {"weight": 0.9, "desc": "Creates irreconcilable multi-jurisdictional legal conflicts"}
}

def calculate_dynamic_severity(impact_subject: str, causal_mechanism: str) -> str:
    """
    Dynamically computes severity based on subject and mechanism.
    BLOCK + PATHWAY_ROUTE -> CRITICAL
    CONFLICT + REGULATION_LAW -> HIGH
    """
    if causal_mechanism == "BLOCK" and impact_subject == "PATHWAY_ROUTE":
        return "CRITICAL"
    elif causal_mechanism in ["BLOCK", "CONFLICT"]:
        return "HIGH"
    elif causal_mechanism in ["TRIGGER", "COST_INCREASE"]:
        return "MEDIUM"
    else:
        return "LOW"

def discover_latent_risks(active_user_topics: List[Dict[str, Any]], user_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates combinatorial latent risk hypotheses based on input active topics.
    """
    try:
        if not isinstance(active_user_topics, list):
            return {"status": "ERROR", "error_code": "INVALID_TOPICS", "message": "Expected list for active_user_topics"}

        # Extract target categories from active user topics
        target_categories = set()
        for t in active_user_topics:
            if isinstance(t, dict):
                cat = t.get("category", "").upper()
                if cat:
                    target_categories.add(cat)

        if not target_categories:
            target_categories = {"IMMIGRATION", "ASSET", "CAREER"}

        generated_risks = []
        risk_counter = 1

        # Combinatorial Risk Generation over target categories
        for cat in sorted(list(target_categories)):
            for subject in IMPACT_SUBJECTS:
                for mech_key, mech_val in CAUSAL_MECHANISMS.items():
                    # Filter relevant combinations
                    if (cat == "TAX" and subject in ["PERSON", "REGULATION_LAW"] and mech_key in ["TRIGGER", "CONFLICT", "COST_INCREASE"]) or \
                       (cat in ["IMMIGRATION", "CAREER"] and subject == "PATHWAY_ROUTE" and mech_key in ["BLOCK", "DELAY"]) or \
                       (cat == "ASSET" and subject == "CAPITAL_ASSET" and mech_key in ["COST_INCREASE", "BLOCK"]) or \
                       (cat in ["HEALTH", "EDUCATION", "FAMILY"] and subject == "PERSON" and mech_key in ["TRIGGER", "DELAY"]):

                        severity = calculate_dynamic_severity(subject, mech_key)
                        risk_id = f"rsk_gen_{risk_counter:03d}"
                        title = f"Latent {cat} {mech_key} Risk on {subject}"
                        description = f"Combinatorial Hypothesis: {cat} constraints may {mech_val['desc']} impacting {subject}."
                        tracking_metric = f"Statutory {cat} {mech_key} Threshold"

                        generated_risks.append({
                            "risk_id": risk_id,
                            "title": title,
                            "category": cat,
                            "impact_subject": subject,
                            "causal_mechanism": mech_key,
                            "severity": severity,
                            "description": description,
                            "suggested_tracking_metric": tracking_metric
                        })
                        risk_counter += 1

        return {
            "status": "SUCCESS",
            "divergent_discovery_summary": {
                "topics_analyzed_count": len(active_user_topics),
                "latent_risks_discovered_count": len(generated_risks),
                "generation_mode": "COMBINATORIAL_RISK_GENERATOR"
            },
            "discovered_risk_domains": generated_risks
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "DIVERGENT_RISK_GENERATOR_EXCEPTION", "message": str(e)}

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                topics = json.load(f)
        else:
            topics = [
                {"topic_id": "t1", "category": "IMMIGRATION"},
                {"topic_id": "t2", "category": "ASSET"}
            ]

        res = discover_latent_risks(topics)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
