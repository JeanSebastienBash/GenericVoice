"""
Test: test_008_005_effects_import.py
Suite: 008 Integration
Purpose: Effects Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/effects.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_effects_import():
    import effects
    assert hasattr(effects, 'apply_voice_effect')

def test_effects_functions():
    import effects
    assert hasattr(effects, 'add_echo')
    assert hasattr(effects, 'add_vibrato')

if __name__ == '__main__':
    test_effects_import()
    test_effects_functions()
    print("OK: test_008_005_effects_import")
