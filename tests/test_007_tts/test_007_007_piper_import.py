"""
Test: test_007_007_piper_import.py
Suite: 007 Tts
Purpose: Piper Import
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import PiperTTS

def test_piper_tts_defined():
    assert PiperTTS is not None

def test_piper_tts_is_class():
    assert isinstance(PiperTTS, type)

if __name__ == '__main__':
    test_piper_tts_defined()
    test_piper_tts_is_class()
    print("OK: test_007_007_piper_import")
