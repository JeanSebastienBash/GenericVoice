"""
Test: test_007_004_tts_not_available.py
Suite: 007 Tts
Purpose: Tts Not Available
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import TTSEngineNotAvailable

def test_tts_not_available_defined():
    assert TTSEngineNotAvailable is not None

def test_tts_not_available_is_exception():
    assert issubclass(TTSEngineNotAvailable, Exception)

if __name__ == '__main__':
    test_tts_not_available_defined()
    test_tts_not_available_is_exception()
    print("OK: test_007_004_tts_not_available")
