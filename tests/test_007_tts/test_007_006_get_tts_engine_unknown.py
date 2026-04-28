"""
Test: test_007_006_get_tts_engine_unknown.py
Suite: 007 Tts
Purpose: Get Tts Engine Unknown
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import get_tts_engine, TTSEngineNotAvailable

def test_get_tts_engine_unknown_raises():
    
    try:
        engine = get_tts_engine('unknown_engine')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_get_tts_engine_fake_raises():
    
    try:
        engine = get_tts_engine('fake_tts')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_get_tts_engine_empty_raises():
    
    try:
        engine = get_tts_engine('')
        assert False, "Should have raised error"
    except (ValueError, TTSEngineNotAvailable):
        pass

if __name__ == '__main__':
    test_get_tts_engine_unknown_raises()
    test_get_tts_engine_fake_raises()
    test_get_tts_engine_empty_raises()
    print("OK: test_007_006_get_tts_engine_unknown")
