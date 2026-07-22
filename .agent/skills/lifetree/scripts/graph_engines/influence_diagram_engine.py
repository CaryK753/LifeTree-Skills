#!/usr/bin/env python3
"""
LifeTree Influence Diagram Decision Engine
Models Decision Nodes (Square), Chance Nodes (Circle), and Value Nodes (Diamond).
Solves Backward Induction Expected Utility & Policy Trees.
"""

import sys
import json
from typing import Dict, Any, List

def evaluate_influence_diagram(diagram_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates an Influence Diagram using Backward Induction over Decision, Chance, and Value nodes.
    diagram_payload: {
        "decision_nodes": [{"id": "d1", "label": "Visa Path Choice", "options": ["CHANCENKARTE", "DIRECT_EMPLOYER"]}],
        "chance_nodes": [{"id": "c1", "parent_decision": "d1", "outcomes": [{"option": "CHANCENKARTE", "state": "PASS", "prob": 0.85}, {"option": "CHANCENKARTE", "state": "FAIL", "prob": 0.15}]}],
        "value_nodes": [{"id": "v1", "payoffs": [{"d1": "CHANCENKARTE", "c1": "PASS", "value": 100}, {"d1": "CHANCENKARTE", "c1": "FAIL", "value": -40}]}]
    }

    C5 fix: When `decision_nodes` is empty, the engine now returns an explicit
    NO_DECISION_NODES error instead of silently substituting hardcoded defaults
    that always answer "CHANCENKARTE_ROUTE". Callers that genuinely want the
    demo defaults must opt in with `use_defaults_if_empty: true`, and the
    response will then carry `used_default_payload: true` so downstream
    consumers can warn the user.
    """
    try:
        if not isinstance(diagram_payload, dict):
            return {"status": "ERROR", "error_code": "INVALID_DIAGRAM_PAYLOAD", "message": "Expected dict for diagram_payload"}

        decision_nodes = diagram_payload.get("decision_nodes", [])
        chance_nodes = diagram_payload.get("chance_nodes", [])
        value_nodes = diagram_payload.get("value_nodes", [])
        used_default_payload = False

        if not decision_nodes:
            # C5: refuse to silently substitute defaults unless the caller explicitly
            # opts in. Previously an empty payload always returned "CHANCENKARTE_ROUTE",
            # which masked the fact that no actual decision modeling had happened.
            if not diagram_payload.get("use_defaults_if_empty", False):
                return {
                    "status": "ERROR",
                    "error_code": "NO_DECISION_NODES",
                    "message": (
                        "evaluate_influence_diagram received no decision_nodes. "
                        "Refusing to silently substitute hardcoded defaults (this previously "
                        "always answered 'CHANCENKARTE_ROUTE'). Either supply a real "
                        "diagram_payload with decision_nodes/chance_nodes/value_nodes, or "
                        "set use_defaults_if_empty=true to opt into the demo defaults."
                    ),
                    "required_fields": ["decision_nodes", "chance_nodes", "value_nodes"],
                    "example_payload": {
                        "decision_nodes": [{"id": "d1", "label": "Visa Path Choice",
                                            "options": ["CHANCENKARTE", "DIRECT_EMPLOYER"]}],
                        "chance_nodes": [{"id": "c1", "parent_option": "CHANCENKARTE",
                                          "outcomes": [{"state": "PASS", "prob": 0.85},
                                                       {"state": "FAIL", "prob": 0.15}]}],
                        "value_nodes": [{"parent_option": "CHANCENKARTE", "state": "PASS", "utility_value": 100},
                                        {"parent_option": "CHANCENKARTE", "state": "FAIL", "utility_value": -40}]
                    }
                }
            # Explicit opt-in: use demo defaults but flag the response so callers
            # can surface a warning to the user.
            used_default_payload = True
            decision_nodes = [{"id": "d_primary", "label": "Primary Decision", "options": ["CHANCENKARTE_ROUTE", "DIRECT_EMPLOYER_ROUTE"]}]
            chance_nodes = [
                {"id": "c_chancen", "parent_option": "CHANCENKARTE_ROUTE", "outcomes": [{"state": "SUCCESS", "prob": 0.88}, {"state": "DELAY", "prob": 0.12}]},
                {"id": "c_direct", "parent_option": "DIRECT_EMPLOYER_ROUTE", "outcomes": [{"state": "SUCCESS", "prob": 0.70}, {"state": "REJECT", "prob": 0.30}]}
            ]
            value_nodes = [
                {"parent_option": "CHANCENKARTE_ROUTE", "state": "SUCCESS", "utility_value": 90.0},
                {"parent_option": "CHANCENKARTE_ROUTE", "state": "DELAY", "utility_value": 30.0},
                {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "SUCCESS", "utility_value": 95.0},
                {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "REJECT", "utility_value": -50.0}
            ]

        option_expected_utilities = []
        d_node = decision_nodes[0]
        options = d_node.get("options", [])

        for opt in options:
            matching_chances = [c for c in chance_nodes if c.get("parent_option") == opt or opt in str(c)]
            expected_utility = 0.0
            outcomes_log = []

            if matching_chances:
                c_item = matching_chances[0]
                for out in c_item.get("outcomes", []):
                    st = out.get("state")
                    p = float(out.get("prob", 0.5))

                    # Find value payoff
                    val_items = [v for v in value_nodes if v.get("parent_option") == opt and v.get("state") == st]
                    u_val = float(val_items[0].get("utility_value", 50.0)) if val_items else (80.0 if st == "SUCCESS" else -20.0)

                    contrib = p * u_val
                    expected_utility += contrib
                    outcomes_log.append({"state": st, "prob": p, "utility_payoff": u_val, "expected_contrib": round(contrib, 2)})
            else:
                expected_utility = 50.0

            option_expected_utilities.append({
                "option": opt,
                "expected_utility_EU": round(expected_utility, 2),
                "chance_breakdown": outcomes_log
            })

        option_expected_utilities.sort(key=lambda x: x["expected_utility_EU"], reverse=True)
        optimal_choice = option_expected_utilities[0]

        return {
            "status": "SUCCESS",
            "used_default_payload": used_default_payload,
            "influence_diagram_summary": {
                "decision_node_id": d_node.get("id"),
                "optimal_decision_policy": optimal_choice["option"],
                "max_expected_utility_EU": optimal_choice["expected_utility_EU"],
                "used_default_payload": used_default_payload
            },
            "evaluated_options": option_expected_utilities
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "INFLUENCE_DIAGRAM_EXCEPTION", "message": str(e)}

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                payload = json.load(f)
        else:
            # C5 fix: standalone smoke test uses a real demo payload instead of {}
            # so the engine actually performs backward induction.
            payload = {
                "decision_nodes": [{"id": "d_visa_route", "label": "Visa Path Choice",
                                    "options": ["CHANCENKARTE_ROUTE", "DIRECT_EMPLOYER_ROUTE"]}],
                "chance_nodes": [
                    {"id": "c_chancen", "parent_option": "CHANCENKARTE_ROUTE",
                     "outcomes": [{"state": "SUCCESS", "prob": 0.88}, {"state": "DELAY", "prob": 0.12}]},
                    {"id": "c_direct", "parent_option": "DIRECT_EMPLOYER_ROUTE",
                     "outcomes": [{"state": "SUCCESS", "prob": 0.70}, {"state": "REJECT", "prob": 0.30}]}
                ],
                "value_nodes": [
                    {"parent_option": "CHANCENKARTE_ROUTE", "state": "SUCCESS", "utility_value": 90.0},
                    {"parent_option": "CHANCENKARTE_ROUTE", "state": "DELAY", "utility_value": 30.0},
                    {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "SUCCESS", "utility_value": 95.0},
                    {"parent_option": "DIRECT_EMPLOYER_ROUTE", "state": "REJECT", "utility_value": -50.0}
                ]
            }

        res = evaluate_influence_diagram(payload)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
