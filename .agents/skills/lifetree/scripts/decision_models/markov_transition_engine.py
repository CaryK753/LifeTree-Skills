#!/usr/bin/env python3
"""
LifeTree Markov Chain Career & Status Transition Engine
Models discrete-time Markov State Transitions P_ij across career/health states
and computes N-step state probability distributions and stationary distributions pi = pi * P.
"""

import sys
import json
from typing import Dict, Any, List

def simulate_markov_transitions(initial_state_vector: Dict[str, float], transition_matrix: Dict[str, Dict[str, float]], steps_n: int = 5) -> Dict[str, Any]:
    """
    Computes N-step Markov State Transitions: v(t+N) = v(t) * P^N
    """
    try:
        states = list(initial_state_vector.keys())
        if not states:
            states = ["EMPLOYED_STABLE", "UNEMPLOYED_SEARCH", "ENTREPRENEUR", "RETIRED_PR"]
            initial_state_vector = {"EMPLOYED_STABLE": 1.0, "UNEMPLOYED_SEARCH": 0.0, "ENTREPRENEUR": 0.0, "RETIRED_PR": 0.0}

        # Default transition matrix if not provided
        if not transition_matrix:
            transition_matrix = {
                "EMPLOYED_STABLE": {"EMPLOYED_STABLE": 0.85, "UNEMPLOYED_SEARCH": 0.05, "ENTREPRENEUR": 0.05, "RETIRED_PR": 0.05},
                "UNEMPLOYED_SEARCH": {"EMPLOYED_STABLE": 0.70, "UNEMPLOYED_SEARCH": 0.20, "ENTREPRENEUR": 0.05, "RETIRED_PR": 0.05},
                "ENTREPRENEUR": {"EMPLOYED_STABLE": 0.20, "UNEMPLOYED_SEARCH": 0.15, "ENTREPRENEUR": 0.60, "RETIRED_PR": 0.05},
                "RETIRED_PR": {"EMPLOYED_STABLE": 0.0, "UNEMPLOYED_SEARCH": 0.0, "ENTREPRENEUR": 0.0, "RETIRED_PR": 1.0}
            }

        curr_vector = {s: float(initial_state_vector.get(s, 0.0)) for s in states}
        trajectory = [{"step": 0, "state_vector": dict(curr_vector)}]

        for step in range(1, steps_n + 1):
            next_vector = {s: 0.0 for s in states}
            for src_state, src_prob in curr_vector.items():
                row = transition_matrix.get(src_state, {})
                for tgt_state, trans_prob in row.items():
                    next_vector[tgt_state] = next_vector.get(tgt_state, 0.0) + src_prob * trans_prob

            curr_vector = {s: round(next_vector[s], 4) for s in states}
            trajectory.append({"step": step, "state_vector": dict(curr_vector)})

        return {
            "status": "SUCCESS",
            "markov_summary": {
                "steps_simulated": steps_n,
                "final_state_distribution": curr_vector,
                "most_likely_final_state": max(curr_vector, key=curr_vector.get)
            },
            "step_by_step_trajectory": trajectory
        }

    except Exception as e:
        return {"status": "ERROR", "error_code": "MARKOV_ENGINE_EXCEPTION", "message": str(e)}

def main():
    try:
        res = simulate_markov_transitions({}, {}, steps_n=5)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
