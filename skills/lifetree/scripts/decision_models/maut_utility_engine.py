#!/usr/bin/env python3
"""
LifeTree Multi-Attribute Utility Theory (MAUT) & Analytic Hierarchy Process (AHP) Engine
Provides multi-dimensional goal modeling (Income, Time Cost, Health, Freedom, Family Stability, Stress)
and AHP pairwise comparison matrix weight elicitation (Aw = lambda_max * w).
"""

import sys
import json
import math
from typing import Dict, Any, List, Tuple

DEFAULT_ATTRIBUTES = ["income", "time_cost_inverted", "health", "freedom", "family_stability", "stress_inverted"]

def calculate_ahp_weights(pairwise_matrix: List[List[float]]) -> Tuple[List[float], float, bool]:
    """
    Calculates AHP weights using the Principal Eigenvector method.
    Returns (weights, Consistency_Ratio_CR, is_consistent).
    Consistency Ratio CR < 0.10 indicates acceptable consistency.
    """
    n = len(pairwise_matrix)
    if n == 0:
        return [], 0.0, True

    # Random Index (RI) values for n = 1..10
    ri_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

    # Normalize columns and average rows to approximate eigenvector
    col_sums = [sum(pairwise_matrix[row][col] for row in range(n)) for col in range(n)]
    weights = []
    for row in range(n):
        row_avg = sum(pairwise_matrix[row][col] / col_sums[col] for col in range(n)) / n
        weights.append(row_avg)

    # M1 fix: lambda_max is the principal eigenvalue Aw = lambda_max * w. The correct
    # approximation from the normalized column-average method is the Rayleigh quotient
    #   lambda_max = (1/n) * sum_i [ (sum_j a_ij * w_j) / w_i ]
    # The previous formula `sum(col_sums[col] * weights[col])` returned a value close
    # to 1 (because col_sums[col] * weights[col] ≈ 1 for each col after normalization),
    # producing meaningless CR values close to (1 - n) / ((n-1) * RI) which are always
    # negative and thus always "consistent" — masking arbitrary weight matrices.
    lambda_max = 0.0
    for i in range(n):
        aw_i = sum(pairwise_matrix[i][j] * weights[j] for j in range(n))
        if weights[i] > 1e-12:
            lambda_max += aw_i / weights[i]
    lambda_max = lambda_max / n if n > 0 else 0.0

    # Consistency Index (CI) and Consistency Ratio (CR)
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = ri_dict.get(n, 1.24)
    cr = ci / ri if ri > 0 else 0.0
    is_consistent = cr < 0.10

    return weights, round(cr, 4), is_consistent

def evaluate_maut_utility(attribute_scores: Dict[str, float], custom_weights: Dict[str, float] = None, pairwise_matrix: List[List[float]] = None) -> Dict[str, Any]:
    """
    Calculates standardized Multi-Attribute Utility Score (0.0 to 100.0).
    """
    try:
        if not isinstance(attribute_scores, dict):
            return {"status": "ERROR", "error_code": "INVALID_SCORES", "message": "Expected dict for attribute_scores"}

        attributes = list(attribute_scores.keys()) if attribute_scores else DEFAULT_ATTRIBUTES

        # Elicit weights via AHP matrix if provided
        ahp_cr = 0.0
        ahp_consistent = True
        if pairwise_matrix and len(pairwise_matrix) == len(attributes):
            weights_list, ahp_cr, ahp_consistent = calculate_ahp_weights(pairwise_matrix)
            weights = {attributes[i]: weights_list[i] for i in range(len(attributes))}
        elif custom_weights:
            total_w = sum(custom_weights.values())
            weights = {k: v / total_w for k, v in custom_weights.items()}
        else:
            # Equal weighting default
            w_val = 1.0 / len(attributes)
            weights = {attr: w_val for attr in attributes}

        total_maut_score = 0.0
        decomposition = []

        for attr in attributes:
            raw_score = float(attribute_scores.get(attr, 50.0))
            raw_score = max(0.0, min(100.0, raw_score)) # Standardize to [0, 100]
            weight = weights.get(attr, 0.0)
            contrib = raw_score * weight
            total_maut_score += contrib

            decomposition.append({
                "attribute_name": attr,
                "raw_score_0_100": raw_score,
                "elicited_weight": round(weight, 4),
                "utility_contribution": round(contrib, 4)
            })

        return {
            "status": "SUCCESS",
            "maut_total_utility_score": round(total_maut_score, 2),
            "ahp_consistency_ratio": ahp_cr,
            "ahp_is_consistent": ahp_consistent,
            "attribute_decomposition": decomposition
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "MAUT_ENGINE_EXCEPTION", "message": str(e)}

def main():
    try:
        scores = {
            "income": 85.0,
            "time_cost_inverted": 60.0,
            "health": 90.0,
            "freedom": 75.0,
            "family_stability": 95.0,
            "stress_inverted": 65.0
        }
        res = evaluate_maut_utility(scores)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
