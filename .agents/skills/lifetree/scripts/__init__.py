"""LifeTree scripts package.

Task 5: Centralizes sys.path setup so pipeline files no longer need 7 repeated
sys.path.insert() calls. Importing this package adds all script subdirectories
to sys.path, making flat imports (e.g. `import temporal_graph_engine`) work
from any entry point.
"""
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add all subdirectories to sys.path once, centrally
_SUBDIRS = [
    "data_connectors", "graph_engines", "simulation_engines",
    "decision_analysis", "decision_models", "risk_surveillance",
    "ui_translators",
]
for _sub in _SUBDIRS:
    _p = os.path.join(_SCRIPT_DIR, _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)
