#!/usr/bin/env python3
"""
LifeTree Dynamic Confidence Decay Pattern Engine
Calculates true exponential confidence decay C(t) = C_0 * e^(-lambda * Delta_t)
and extracts dynamic decay trend patterns with robust error handling.
"""

import sys
import json
import math
from typing import Dict, Any, List

def calculate_confidence_decay(initial_confidence: float, elapsed_days: float, decay_lambda: float = 0.002) -> Dict[str, Any]:
    """
    Computes exact exponential decay C(t) = C_0 * e^(-lambda * Delta_t).
    """
    try:
        c0 = float(initial_confidence)
        c0 = max(0.0, min(1.0, c0))
        t = float(elapsed_days)
        t = max(0.0, t)
        lam = float(decay_lambda)

        # Exponential decay formula
        decayed_confidence = c0 * math.exp(-lam * t)
        decayed_confidence = round(max(0.0, min(1.0, decayed_confidence)), 4)

        is_poison = decayed_confidence < 0.60

        return {
            "status": "SUCCESS",
            "decay_calculation": {
                "initial_confidence": c0,
                "elapsed_days": t,
                "decay_lambda": lam,
                "decayed_confidence": decayed_confidence,
                "confidence_drop": round(c0 - decayed_confidence, 4),
                "is_poison_node": is_poison,
                "status_badge": "POISON_PRUNED" if is_poison else "CONFIDENT"
            }
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_code": "CONFIDENCE_DECAY_EXCEPTION",
            "message": str(e)
        }

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                data = json.load(f)
                c0 = data.get("initial_confidence", 0.95)
                t = data.get("elapsed_days", 180)
                lam = data.get("decay_lambda", 0.002)
        else:
            c0 = 0.95
            t = 180
            lam = 0.002

        res = calculate_confidence_decay(c0, t, lam)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))

if __name__ == "__main__":
    main()
