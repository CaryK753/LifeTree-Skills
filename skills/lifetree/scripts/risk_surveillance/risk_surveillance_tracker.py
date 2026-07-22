#!/usr/bin/env python3
"""
LifeTree Continuous Risk Surveillance & Tracking Manager
Manages long-term continuous surveillance subscriptions for discovered latent risk domains
"""

import sys
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

def update_risk_surveillance(surveillance_registry: Dict[str, Any], new_risk_domains: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Registers new latent risk domains into the continuous surveillance registry.
    Updates active monitoring flags, metric tracking frequency, and circuit breaker status.
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    tracked_items = surveillance_registry.get("tracked_risk_domains", {})

    added_count = 0
    updated_count = 0

    for risk in new_risk_domains:
        rid = risk.get("risk_id")
        if rid not in tracked_items:
            tracked_items[rid] = {
                "risk_id": rid,
                "title": risk.get("title"),
                "category": risk.get("category"),
                "severity": risk.get("severity"),
                "description": risk.get("description"),
                "tracking_metric": risk.get("suggested_tracking_metric"),
                "first_discovered_at": now_iso,
                "last_checked_at": now_iso,
                "surveillance_status": "ACTIVE_SURVEILLANCE",
                "circuit_breaker_threshold": "CRITICAL_POLICY_CHANGE"
            }
            added_count += 1
        else:
            tracked_items[rid]["last_checked_at"] = now_iso
            updated_count += 1

    return {
        "registry_summary": {
            "total_tracked_risk_domains": len(tracked_items),
            "newly_registered_count": added_count,
            "updated_surveillance_count": updated_count,
            "last_surveillance_run": now_iso
        },
        "tracked_risk_domains": tracked_items
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            reg = data.get("registry", {})
            new_r = data.get("new_risks", [])
    else:
        reg = {"tracked_risk_domains": {}}
        new_r = [
            {
                "risk_id": "risk_latent_tax_residency_trap",
                "title": "Dual Tax Residency & Exit Tax Exposure",
                "category": "TAX_RESIDENCY_TRAP",
                "severity": "HIGH",
                "description": "Cross-border relocation tax exposure",
                "suggested_tracking_metric": "183-day rule & Tax Treaty"
            }
        ]

    res = update_risk_surveillance(reg, new_r)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
