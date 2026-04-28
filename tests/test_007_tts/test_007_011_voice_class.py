"""
Test: test_007_011_voice_class.py
Suite: 007 Tts
Purpose: Voice Class
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import Voice

def test_voice_defined():
    assert Voice is not None

def test_voice_is_class():
    assert isinstance(Voice, type)

if __name__ == '__main__':
    test_voice_defined()
    test_voice_is_class()
    print("OK: test_007_011_voice_class")
