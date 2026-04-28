"""
Test: test_008_008_system_import.py
Suite: 008 Integration
Purpose: System Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib', 'system'))

def test_system_import():
    import system
    assert hasattr(system, 'detect')
    assert hasattr(system, 'adapt')

if __name__ == '__main__':
    test_system_import()
    print("OK: test_008_008_system_import")
