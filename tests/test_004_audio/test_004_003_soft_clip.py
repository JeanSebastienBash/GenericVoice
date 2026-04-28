"""
Test: test_004_003_soft_clip.py
Suite: 004 Audio
Purpose: Soft Clip
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_soft_clip_defined():
    assert hasattr(audio, 'soft_clip')

def test_soft_clip_returns_array():
    x = np.array([0.5, 1.0, 2.0])
    result = audio.soft_clip(x)
    assert isinstance(result, np.ndarray)

def test_soft_clip_clips_values():
    x = np.array([10.0])
    result = audio.soft_clip(x)
    assert result[0] < 1.0

if __name__ == '__main__':
    test_soft_clip_defined()
    test_soft_clip_returns_array()
    test_soft_clip_clips_values()
    print("OK: test_004_003_soft_clip")
