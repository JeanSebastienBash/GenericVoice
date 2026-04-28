"""
Test: test_008_007_tts_import.py
Suite: 008 Integration
Purpose: Tts Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_tts_import():
    import tts
    assert hasattr(tts, 'get_tts_engine')

def test_tts_classes():
    import tts
    assert hasattr(tts, 'BaseTTS')
    assert hasattr(tts, 'Voice')

if __name__ == '__main__':
    test_tts_import()
    test_tts_classes()
    print("OK: test_008_007_tts_import")
