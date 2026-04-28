"""
Test: test_008_014_load_ihm.py
Suite: 008 Integration
Purpose: Load Ihm
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from gv import load_ihm

def test_load_ihm():
    ihm = load_ihm()
    assert ihm is not None

if __name__ == '__main__':
    test_load_ihm()
    print("OK: test_008_014_load_ihm")
