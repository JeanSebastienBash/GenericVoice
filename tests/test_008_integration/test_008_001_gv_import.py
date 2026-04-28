"""
Test: test_008_001_gv_import.py
Suite: 008 Integration
Purpose: Gv Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def test_gv_import():
    import gv
    assert hasattr(gv, 'parse_args')

def test_gv_version():
    import gv
    assert hasattr(gv, '__version__')

if __name__ == '__main__':
    test_gv_import()
    test_gv_version()
    print("OK: test_008_001_gv_import")
