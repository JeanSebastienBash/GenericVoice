"""
Test: test_008_010_version.py
Suite: 008 Integration
Purpose: Version
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_version():
    import gv
    assert gv.__version__ == "1.0.2"

if __name__ == '__main__':
    test_version()
    print("OK: test_008_010_version")
