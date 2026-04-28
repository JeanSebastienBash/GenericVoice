"""
Test: test_004_004_time_array.py
Suite: 004 Audio
Purpose: Time Array
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_time_array_defined():
    assert hasattr(audio, 'time_array')

def test_time_array_returns_array():
    result = audio.time_array(1.0)
    assert isinstance(result, np.ndarray)

def test_time_array_length():
    result = audio.time_array(1.0)
    assert len(result) == 48000

if __name__ == '__main__':
    test_time_array_defined()
    test_time_array_returns_array()
    test_time_array_length()
    print("OK: test_004_004_time_array")
