"""
Test: test_007_012_language_class.py
Suite: 007 Tts
Purpose: Language Class
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import Language

def test_language_defined():
    assert Language is not None

def test_language_is_class():
    assert isinstance(Language, type)

if __name__ == '__main__':
    test_language_defined()
    test_language_is_class()
    print("OK: test_007_012_language_class")
