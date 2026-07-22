#!/usr/bin/env python3
"""
LifeTree 2x2 Game-Theoretic Nash Equilibrium & Pareto Solver
Calculates Pure Strategy Nash Equilibria, Mixed Strategy Nash Equilibria (p, q),
and Pareto Efficiency over 2x2 stakeholder payoff matrices, with backward compatibility fallback.
"""

import sys
import json
from typing import Dict, Any, List, Tuple, Optional

def build_payoff_matrix(stakeholder_a: Dict[str, Any], stakeholder_b: Dict[str, Any]) -> List[List[Tuple[float, float]]]:
    """
    Builds a 2x2 Payoff Matrix [[(a1,b1), (a1,b2)], [(a2,b1), (a2,b2)]] based on preference vectors.
    Strategies for Player A & B: ["COOPERATE", "DEFECT"]
    """
    pref_a = stakeholder_a.get("preference_vector", {"compliance_cost": -0.3, "penalty_risk": -0.5, "benefit": 1.0})
    pref_b = stakeholder_b.get("preference_vector", {"compliance_cost": -0.3, "penalty_risk": -0.5, "benefit": 1.0})

    out_a = float(stakeholder_a.get("outside_option", 0.0))
    out_b = float(stakeholder_b.get("outside_option", 0.0))

    # Calculate utilities for (Cooperate, Cooperate), (Cooperate, Defect), (Defect, Cooperate), (Defect, Defect)
    # 0,0: Both Cooperate
    u_a_cc = pref_a.get("benefit", 1.0) + pref_a.get("compliance_cost", -0.3)
    u_b_cc = pref_b.get("benefit", 1.0) + pref_b.get("compliance_cost", -0.3)

    # 0,1: A Cooperate, B Defect
    u_a_cd = pref_a.get("compliance_cost", -0.3) + pref_a.get("penalty_risk", -0.5)
    u_b_cd = pref_b.get("benefit", 1.0) + out_b

    # 1,0: A Defect, B Cooperate
    u_a_dc = pref_a.get("benefit", 1.0) + out_a
    u_b_dc = pref_b.get("compliance_cost", -0.3) + pref_b.get("penalty_risk", -0.5)

    # 1,1: Both Defect
    u_a_dd = out_a + pref_a.get("penalty_risk", -0.5)
    u_b_dd = out_b + pref_b.get("penalty_risk", -0.5)

    matrix = [
        [(round(u_a_cc, 2), round(u_b_cc, 2)), (round(u_a_cd, 2), round(u_b_cd, 2))],
        [(round(u_a_dc, 2), round(u_b_dc, 2)), (round(u_a_dd, 2), round(u_b_dd, 2))]
    ]
    return matrix

def find_pure_strategy_nash_equilibrium(matrix: List[List[Tuple[float, float]]]) -> List[Dict[str, Any]]:
    """
    Finds Pure Strategy Nash Equilibria using Best Response intersection.
    Strategies: 0 -> COOPERATE, 1 -> DEFECT
    """
    strategies = ["COOPERATE", "DEFECT"]
    pure_nes = []

    # Player A best response for each column (Player B strategy)
    # Player B best response for each row (Player A strategy)
    best_a_for_col = []
    for col in range(2):
        a_payoff_0 = matrix[0][col][0]
        a_payoff_1 = matrix[1][col][0]
        if a_payoff_0 > a_payoff_1:
            best_a_for_col.append([0])
        elif a_payoff_1 > a_payoff_0:
            best_a_for_col.append([1])
        else:
            best_a_for_col.append([0, 1])

    best_b_for_row = []
    for row in range(2):
        b_payoff_0 = matrix[row][0][1]
        b_payoff_1 = matrix[row][1][1]
        if b_payoff_0 > b_payoff_1:
            best_b_for_row.append([0])
        elif b_payoff_1 > b_payoff_0:
            best_b_for_row.append([1])
        else:
            best_b_for_row.append([0, 1])

    # Check intersections
    all_outcomes = []
    for r in range(2):
        for c in range(2):
            p_a, p_b = matrix[r][c]
            is_a_best = r in best_a_for_col[c]
            is_b_best = c in best_b_for_row[r]
            is_ne = is_a_best and is_b_best
            all_outcomes.append({"row": r, "col": c, "payoff_a": p_a, "payoff_b": p_b, "is_ne": is_ne})

    # Determine Pareto efficiency among outcomes
    for out in all_outcomes:
        if out["is_ne"]:
            r, c = out["row"], out["col"]
            p_a, p_b = out["payoff_a"], out["payoff_b"]
            is_pareto = not any(o["payoff_a"] >= p_a and o["payoff_b"] >= p_b and (o["payoff_a"] > p_a or o["payoff_b"] > p_b) for o in all_outcomes)
            pure_nes.append({
                "strategy_a": strategies[r],
                "strategy_b": strategies[c],
                "payoff_a": p_a,
                "payoff_b": p_b,
                "is_pareto_optimal": is_pareto
            })

    return pure_nes

def find_mixed_strategy_nash_equilibrium(matrix: List[List[Tuple[float, float]]]) -> Dict[str, Any]:
    """
    Calculates Mixed Strategy Nash Equilibrium probabilities p, q:
    p: Prob(A plays COOPERATE) making B indifferent
    q: Prob(B plays COOPERATE) making A indifferent
    """
    try:
        (a11, b11), (a12, b12) = matrix[0][0], matrix[0][1]
        (a21, b21), (a22, b22) = matrix[1][0], matrix[1][1]

        # Player A indifferent between Cooperate & Defect: q*a11 + (1-q)*a12 = q*a21 + (1-q)*a22
        denom_a = (a11 - a12 - a21 + a22)
        q = (a22 - a12) / denom_a if abs(denom_a) > 0.0001 else 0.5

        # Player B indifferent between Cooperate & Defect: p*b11 + (1-p)*b21 = p*b12 + (1-p)*b22
        denom_b = (b11 - b21 - b12 + b22)
        p = (b22 - b21) / denom_b if abs(denom_b) > 0.0001 else 0.5

        p = round(max(0.0, min(1.0, p)), 4)
        q = round(max(0.0, min(1.0, q)), 4)

        exp_a = round(p * q * a11 + p * (1 - q) * a12 + (1 - p) * q * a21 + (1 - p) * (1 - q) * a22, 2)
        exp_b = round(p * q * b11 + p * (1 - q) * b12 + (1 - p) * q * b21 + (1 - p) * (1 - q) * b22, 2)

        return {
            "prob_a_play_cooperate": p,
            "prob_b_play_cooperate": q,
            "expected_payoff_a": exp_a,
            "expected_payoff_b": exp_b
        }
    except Exception as e:
        return {"prob_a_play_cooperate": 0.5, "prob_b_play_cooperate": 0.5, "expected_payoff_a": 0.0, "expected_payoff_b": 0.0}

def solve_stakeholder_conflicts(stakeholder_requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Executes 2x2 Nash Equilibrium solver when preference_vector is provided;
    otherwise falls back to rule-matching engine.
    """
    try:
        if not isinstance(stakeholder_requirements, list):
            return {"status": "ERROR", "error_code": "INVALID_STAKEHOLDERS", "message": "Expected list for stakeholder_requirements"}

        # Check if preference_vector is present in input
        has_pref = len(stakeholder_requirements) >= 2 and all("preference_vector" in s for s in stakeholder_requirements[:2])

        if has_pref:
            st_a = stakeholder_requirements[0]
            st_b = stakeholder_requirements[1]
            matrix = build_payoff_matrix(st_a, st_b)
            pure_nes = find_pure_strategy_nash_equilibrium(matrix)
            mixed_ne = find_mixed_strategy_nash_equilibrium(matrix)

            return {
                "status": "SUCCESS",
                "solver_mode": "2X2_NASH_EQUILIBRIUM_SOLVER",
                "stakeholder_a": st_a.get("stakeholder", "Player A"),
                "stakeholder_b": st_b.get("stakeholder", "Player B"),
                "payoff_matrix": matrix,
                "pure_strategy_nash_equilibria": pure_nes,
                "mixed_strategy_nash_equilibrium": mixed_ne
            }

        # Fallback to Rule Matching Engine
        conflicts = []
        pareto_compromises = []
        categories_present = {st.get("category", "").upper() for st in stakeholder_requirements if isinstance(st, dict)}

        if "IMMIGRATION_PHYSICAL_PRESENCE" in categories_present and "TAX_WORLDWIDE_LIABILITY" in categories_present:
            conflicts.append({
                "conflict_id": "cfl_residence_vs_tax",
                "stakeholder_1": "Host Country Immigration Board",
                "stakeholder_2": "Origin Country Tax Revenue Authority",
                "conflict_description": "Physical presence required for visa renewal triggers worldwide tax exposure in origin jurisdiction.",
                "severity": "HIGH"
            })
            pareto_compromises.append({
                "compromise_id": "cmp_formal_tax_exit",
                "title": "Formal Tax Exit Certificate & DTA Tie-Breaker",
                "action": "Obtain formal Tax Residency Certificate under DTA Article 4 prior to 183rd day."
            })

        return {
            "status": "SUCCESS",
            "solver_mode": "RULE_MATCHING_FALLBACK",
            "stakeholder_audit_summary": {
                "stakeholders_audited_count": len(stakeholder_requirements),
                "conflicts_detected_count": len(conflicts),
                "pareto_compromises_found": len(pareto_compromises)
            },
            "conflicts": conflicts,
            "pareto_compromise_pathways": pareto_compromises
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "GAME_THEORY_SOLVER_EXCEPTION", "message": str(e)}

def main():
    try:
        st_a = {"stakeholder": "Applicant", "preference_vector": {"compliance_cost": -0.2, "penalty_risk": -0.6, "benefit": 1.2}}
        st_b = {"stakeholder": "Immigration Office", "preference_vector": {"compliance_cost": -0.1, "penalty_risk": -0.8, "benefit": 0.9}}
        res = solve_stakeholder_conflicts([st_a, st_b])
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
