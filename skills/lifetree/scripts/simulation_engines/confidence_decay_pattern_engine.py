#!/usr/bin/env python3
"""
LifeTree Time-Based Confidence Decay & Macro Trend Pattern Extractor Engine
Implements Exponential Confidence Decay C(t) = C0 * e^(-lambda * delta_t) and Macro Law/Pattern Extraction
"""

import sys
import json
import math
from datetime import datetime, timezone
from typing import Dict, Any, List

DEFAULT_HALF_LIFE_DAYS = 180.0  # Time in days for confidence score to decay to half if unrefreshed

def calculate_time_decay_confidence(initial_confidence: float, last_fetched_iso: str, half_life_days: float = DEFAULT_HALF_LIFE_DAYS) -> Dict[str, Any]:
    """
    Calculates decayed confidence score using exponential decay:
    C(t) = C0 * exp(-lambda * delta_t_days)
    where lambda = ln(2) / half_life_days
    """
    try:
        last_fetched = datetime.fromisoformat(last_fetched_iso.replace('Z', '+00:00'))
    except Exception:
        last_fetched = datetime.now(timezone.utc)

    now = datetime.now(timezone.utc)
    delta_seconds = (now - last_fetched).total_seconds()
    delta_days = max(0.0, delta_seconds / 86400.0)

    decay_lambda = math.log(2.0) / half_life_days
    decayed_confidence = initial_confidence * math.exp(-decay_lambda * delta_days)
    decayed_confidence = round(max(0.0, min(1.0, decayed_confidence)), 4)

    needs_refresh = (decayed_confidence < 0.6)

    return {
        "initial_confidence": initial_confidence,
        "last_fetched_iso": last_fetched_iso,
        "delta_days": round(delta_days, 1),
        "half_life_days": half_life_days,
        "decayed_confidence": decayed_confidence,
        "needs_refresh": needs_refresh,
        "visual_style": "SOLID" if decayed_confidence >= 0.8 else "DASHED"
    }

def extract_macro_patterns(historical_data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extracts high-level macro patterns from raw data points (e.g. financial deposit requirements vs CPI inflation).
    Example input: [{"year": 2022, "cpi_index": 100, "threshold_eur": 11208}, {"year": 2024, "cpi_index": 107, "threshold_eur": 12000}]
    Calculates annual growth rate & projects multi-year future thresholds.
    """
    if len(historical_data_points) < 2:
        return {
            "pattern_found": False,
            "message": "Insufficient historical data points to extract macro law/pattern."
        }

    sorted_points = sorted(historical_data_points, key=lambda x: x.get("year", 0))
    first = sorted_points[0]
    last = sorted_points[-1]

    years_span = last.get("year", 0) - first.get("year", 0)
    if years_span <= 0:
        years_span = 1

    val_start = first.get("value", 0.0)
    val_end = last.get("value", 0.0)

    # Compound Annual Growth Rate (CAGR)
    if val_start > 0:
        cagr = (val_end / val_start) ** (1.0 / years_span) - 1.0
    else:
        cagr = 0.0

    # Project future 3 years
    proj_3yr = val_end * ((1.0 + cagr) ** 3)

    return {
        "pattern_found": True,
        "metric_name": first.get("metric", "Threshold Value"),
        "historical_span_years": years_span,
        "compound_annual_growth_rate_pct": round(cagr * 100.0, 2),
        "pattern_description": f"Positive correlation detected: '{first.get('metric', 'Metric')}' grows at an average CAGR of {round(cagr*100.0, 2)}% per year.",
        "projections": {
            "current_value": val_end,
            "projected_3year_value": round(proj_3yr, 2)
        }
    }

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
            init_c = data.get("initial_confidence", 1.0)
            last_f = data.get("last_fetched_iso", "2025-01-01T00:00:00Z")
            hist = data.get("historical_data_points", [])
    else:
        init_c = 1.0
        last_f = "2025-01-01T00:00:00Z"
        hist = [
            {"year": 2022, "metric": "Blocked Account Minimum EUR", "value": 11208.0},
            {"year": 2024, "metric": "Blocked Account Minimum EUR", "value": 12000.0}
        ]

    decay_res = calculate_time_decay_confidence(init_c, last_f)
    pattern_res = extract_macro_patterns(hist)

    output = {
        "decay_analysis": decay_res,
        "macro_pattern_extraction": pattern_res
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
