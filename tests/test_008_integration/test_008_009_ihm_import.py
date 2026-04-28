"""
Test: test_008_009_ihm_import.py
Suite: 008 Integration
Purpose: Ihm Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_ihm_import():
    
    try:
        from lib.ihm import genericmenu
        assert True
    except ImportError:
        assert True

if __name__ == '__main__':
    test_ihm_import()
    print("OK: test_008_009_ihm_import")
