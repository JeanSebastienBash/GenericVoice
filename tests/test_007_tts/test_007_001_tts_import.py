"""
Test: test_007_001_tts_import.py
Suite: 007 Tts
Purpose: Tts Import
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_tts_import():
    import tts
    assert hasattr(tts, 'get_tts_engine')

def test_tts_base_import():
    import tts
    assert hasattr(tts, 'BaseTTS')

if __name__ == '__main__':
    test_tts_import()
    test_tts_base_import()
    print("OK: test_007_001_tts_import")
