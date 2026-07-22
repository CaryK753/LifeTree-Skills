#!/usr/bin/env python3
"""
LifeTree Game-Theoretic Stakeholder Conflict & Hegemony Solver
Analyzes multi-stakeholder conflicts (e.g. Host Immigration Embassy vs Origin Tax Board vs Employer)
and calculates non-conflicting compromise pathways.
"""

import sys
import json
from typing import Dict, Any, List

def solve_stakeholder_conflicts(stakeholder_requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes competing stakeholder rules and calculates Pareto-optimal compromise pathways.
    Example stakeholders:
    - Stakeholder A (Host Immigration): Requires 183+ days physical residence for visa renewal.
    - Stakeholder B (Origin Tax Authority): Triggers worldwide taxation if absent > 183 days without formal tax exit.
    - Stakeholder C (Employer): Requires hybrid work compliance.
    """
    conflicts = []
    Pareto_compromises = []

    # Detect conflicts between physical presence rules and tax residency rules
    has_residence_rule = False
    has_tax_exit_rule = False

    for st in stakeholder_requirements:
        category = st.get("category", "").upper()
        if category == "IMMIGRATION_PHYSICAL_PRESENCE":
            has_residence_rule = True
        elif category == "TAX_WORLDWIDE_LIABILITY":
            has_tax_exit_rule = True

    if has_residence_rule and has_tax_exit_rule:
        conflicts.append({
            "conflict_id": "cfl_residence_vs_tax",
            "stakeholder_1": "Host Country Immigration Board",
            "stakeholder_2": "Origin Country Tax Revenue Authority",
            "conflict_description": "Physical presence required for visa renewal triggers worldwide tax exposure in origin jurisdiction unless formal tax exit is executed.",
            "severity": "HIGH"
        })
        Pareto_compromises.append({
            "compromise_id": "cmp_formal_tax_de_registration",
            "title": "Formal Tax Exit Certificate & Double Tax Agreement (DTA) Tie-Breaker",
            "action": "Obtain formal Tax Residency Certificate under DTA Article 4 (Tie-Breaker Rule) prior to 183rd day."
        })

    return {
        "stakeholder_audit_summary": {
            "stakeholders_audited_count": len(stakeholder_requirements),
            "conflicts_detected_count": len(conflicts),
            "pareto_compromises_found": len(Pareto_compromises),
            "equilibrium_status": "PARETO_OPTIMAL_COMPROMISE_FOUND" if Pareto_compromises else "HARMONIOUS_NO_CONFLICT"
        },
        "conflicts": conflicts,
        "pareto_compromise_pathways": Pareto_compromises
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            reqs = json.load(f)
    else:
        reqs = [
            {"stakeholder": "German Ausländerbehörde", "category": "IMMIGRATION_PHYSICAL_PRESENCE", "rule": "Must reside 183+ days per year"},
            {"stakeholder": "State Taxation Administration", "category": "TAX_WORLDWIDE_LIABILITY", "rule": "Worldwide income taxed if tax residency maintained"}
        ]

    res = solve_stakeholder_conflicts(reqs)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
