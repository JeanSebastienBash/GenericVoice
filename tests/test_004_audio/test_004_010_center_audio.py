"""
Test: test_004_010_center_audio.py
Suite: 004 Audio
Purpose: Center Audio
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_center_audio_defined():
    assert hasattr(audio, 'center_audio')

def test_center_audio_returns_array():
    data = np.random.rand(4800).astype(np.float32)
    result = audio.center_audio(data, 1.0, 0.0)
    assert isinstance(result, np.ndarray)

def test_center_audio_correct_length():
    data = np.random.rand(4800).astype(np.float32)
    result = audio.center_audio(data, 1.0, 0.0)
    assert len(result) == 48000

if __name__ == '__main__':
    test_center_audio_defined()
    test_center_audio_returns_array()
    test_center_audio_correct_length()
    print("OK: test_004_010_center_audio")
