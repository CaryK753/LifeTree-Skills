#!/usr/bin/env python3
"""
LifeTree Central Configuration & Environment Variable Loader
Dynamically loads configurations from resources/config/lifetree_config.json and respects environment variables.
"""

import os
import sys
import json
from typing import Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE_PATH = os.path.join(SKILL_ROOT, "resources", "config", "lifetree_config.json")

def load_config() -> Dict[str, Any]:
    """
    Loads configuration dictionary with environment variable overrides.
    """
    cfg = {}
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}

    # Environment variable overrides
    trials_env = os.environ.get("LIFETREE_MONTE_CARLO_TRIALS")
    if trials_env and trials_env.isdigit():
        cfg.setdefault("monte_carlo", {})["default_trials"] = int(trials_env)

    volatility_env = os.environ.get("LIFETREE_VOLATILITY_FACTOR")
    if volatility_env:
        try:
            cfg.setdefault("monte_carlo", {})["volatility_factor"] = float(volatility_env)
        except ValueError:
            pass

    return cfg

def main():
    cfg = load_config()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
