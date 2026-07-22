#!/usr/bin/env python3
"""
LifeTree Master Unit Test Suite Runner
Runs all unit and integration tests across graph engines, simulation engines, decision analysis, and UI generators.
"""

import unittest
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

def main():
    loader = unittest.TestLoader()
    suite = loader.discover(SCRIPT_DIR, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())

if __name__ == "__main__":
    main()
