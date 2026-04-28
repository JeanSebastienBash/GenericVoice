"""
Test: test_007_003_get_tts_engine_edge.py
Suite: 007 Tts
Purpose: Get Tts Engine Edge
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import get_tts_engine, TTSEngineNotAvailable

def test_get_tts_engine_edge_available():
    
    try:
        engine = get_tts_engine('edge')
        assert engine is not None
    except TTSEngineNotAvailable:
        pass

def test_get_tts_engine_edge_name():
    
    try:
        engine = get_tts_engine('edge')
        assert engine.name == 'edge'
    except TTSEngineNotAvailable:
        pass

def test_get_tts_engine_edge_callable():
    
    assert callable(get_tts_engine)

if __name__ == '__main__':
    test_get_tts_engine_edge_available()
    test_get_tts_engine_edge_name()
    test_get_tts_engine_edge_callable()
    print("OK: test_007_003_get_tts_engine_edge")
