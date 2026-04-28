"""
Test: test_007_004_get_tts_engine_espeak.py
Suite: 007 Tts
Purpose: Get Tts Engine Espeak
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import get_tts_engine, TTSEngineNotAvailable

def test_get_tts_engine_espeak_available():
    
    try:
        engine = get_tts_engine('espeak')
        assert engine is not None
    except TTSEngineNotAvailable:
        pass

def test_get_tts_engine_espeak_name():
    
    try:
        engine = get_tts_engine('espeak')
        assert engine.name == 'espeak'
    except TTSEngineNotAvailable:
        pass

def test_get_tts_engine_espeak_callable():
    
    assert callable(get_tts_engine)

if __name__ == '__main__':
    test_get_tts_engine_espeak_available()
    test_get_tts_engine_espeak_name()
    test_get_tts_engine_espeak_callable()
    print("OK: test_007_004_get_tts_engine_espeak")
