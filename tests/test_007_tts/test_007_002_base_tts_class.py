"""
Test: test_007_002_base_tts_class.py
Suite: 007 Tts
Purpose: Base Tts Class
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import BaseTTS

def test_base_tts_defined():
    assert BaseTTS is not None

def test_base_tts_is_class():
    assert isinstance(BaseTTS, type)

if __name__ == '__main__':
    test_base_tts_defined()
    test_base_tts_is_class()
    print("OK: test_007_002_base_tts_class")
