"""
Test: test_007_005_get_tts_engine.py
Suite: 007 Tts
Purpose: Get Tts Engine
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import get_tts_engine

def test_get_tts_engine_defined():
    assert get_tts_engine is not None

def test_get_tts_engine_callable():
    assert callable(get_tts_engine)

if __name__ == '__main__':
    test_get_tts_engine_defined()
    test_get_tts_engine_callable()
    print("OK: test_007_005_get_tts_engine")
