"""
Test: test_007_008_edge_import.py
Suite: 007 Tts
Purpose: Edge Import
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import EdgeTTS

def test_edge_tts_defined():
    assert EdgeTTS is not None

def test_edge_tts_is_class():
    assert isinstance(EdgeTTS, type)

if __name__ == '__main__':
    test_edge_tts_defined()
    test_edge_tts_is_class()
    print("OK: test_007_008_edge_import")
