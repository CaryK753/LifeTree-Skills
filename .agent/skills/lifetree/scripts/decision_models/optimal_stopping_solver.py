#!/usr/bin/env python3
"""
LifeTree Optimal Stopping Threshold Solver
Calculates the 37% Rule / Snell Envelope observation cutoff k* = floor(n / e)
for optimal timing of job pivots, asset liquidations, and exit windows.
"""

import sys
import json
import math
from typing import Dict, Any

def solve_optimal_stopping(total_options_count: int = 10, current_evaluated_idx: int = 0) -> Dict[str, Any]:
    """
    Computes optimal stopping threshold k* = floor(n / e) approx 0.368 * n.
    """
    try:
        n = max(1, int(total_options_count))
        curr_idx = max(0, int(current_evaluated_idx))
        k_cutoff = max(1, int(math.floor(n / math.e))) if n > 1 else 1

        is_observation_phase = curr_idx < k_cutoff
        should_accept_now = not is_observation_phase

        action_recommendation = (
            f"OBSERVE_PHASE: Evaluate and reject the first {k_cutoff} options (current: {curr_idx}/{n}) to establish baseline."
            if is_observation_phase else
            f"DECISION_PHASE: Option {curr_idx} is past cutoff {k_cutoff}. Accept immediately if it exceeds all previously observed options!"
        )

        return {
            "status": "SUCCESS",
            "optimal_stopping": {
                "total_opportunities_n": n,
                "current_evaluated_idx": curr_idx,
                "observation_cutoff_k": k_cutoff,
                "is_observation_phase": is_observation_phase,
                "should_accept_now": should_accept_now,
                "theoretical_success_prob_pct": 36.8,
                "action_recommendation": action_recommendation
            }
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "OPTIMAL_STOPPING_SOLVER_EXCEPTION", "message": str(e)}

def main():
    try:
        res = solve_optimal_stopping(total_options_count=10, current_evaluated_idx=4)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
