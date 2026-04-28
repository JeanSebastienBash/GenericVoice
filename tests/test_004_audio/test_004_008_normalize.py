"""
Test: test_004_008_normalize.py
Suite: 004 Audio
Purpose: Normalize
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_normalize_defined():
    assert hasattr(audio, 'normalize')

def test_normalize_peaks():
    data = np.array([0.1, 0.5, -0.3])
    result = audio.normalize(data, 0.9)
    assert np.max(np.abs(result)) <= 0.9

def test_normalize_zero():
    data = np.zeros(100)
    result = audio.normalize(data)
    assert np.all(result == 0)

if __name__ == '__main__':
    test_normalize_defined()
    test_normalize_peaks()
    test_normalize_zero()
    print("OK: test_004_008_normalize")
