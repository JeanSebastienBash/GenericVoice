"""
Test: test_008_015_list_engines.py
Suite: 008 Integration
Purpose: List Engines
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from gv import list_engines

def test_list_engines_defined():
    assert list_engines is not None

def test_list_engines_callable():
    assert callable(list_engines)

if __name__ == '__main__':
    test_list_engines_defined()
    test_list_engines_callable()
    print("OK: test_008_015_list_engines")
