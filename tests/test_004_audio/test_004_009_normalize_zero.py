"""
Test: test_004_009_normalize_zero.py
Suite: 004 Audio
Purpose: Normalize Zero
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_normalize_zero_array():
    data = np.zeros(100)
    result = audio.normalize(data, 0.85)
    assert np.allclose(result, np.zeros(100))

if __name__ == '__main__':
    test_normalize_zero_array()
    print("OK: test_004_009_normalize_zero")
