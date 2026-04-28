"""
Test: test_004_011_center_audio_with_fades.py
Suite: 004 Audio
Purpose: Center Audio With Fades
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_center_audio_with_fade_in():
    data = np.random.rand(4800).astype(np.float32)
    result = audio.center_audio(data, 1.0, 0.0, fade_in_ms=50, fade_out_ms=80)
    assert isinstance(result, np.ndarray)

def test_center_audio_with_fades_zeros():
    data = np.zeros(100)
    result = audio.center_audio(data, 0.1, 0.0, fade_in_ms=10, fade_out_ms=10)
    assert np.allclose(result, np.zeros(4800))

if __name__ == '__main__':
    test_center_audio_with_fade_in()
    test_center_audio_with_fades_zeros()
    print("OK: test_004_011_center_audio_with_fades")
