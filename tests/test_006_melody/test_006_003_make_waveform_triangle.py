"""
Test: test_006_003_make_waveform_triangle.py
Suite: 006 Melody
Purpose: Make Waveform Triangle
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody
import numpy as np

def test_make_waveform_triangle():
    result = melody.make_waveform(440.0, 1.0, 'triangle')
    assert isinstance(result, np.ndarray)

def test_make_waveform_triangle_length():
    result = melody.make_waveform(440.0, 1.0, 'triangle')
    assert len(result) == 48000

if __name__ == '__main__':
    test_make_waveform_triangle()
    test_make_waveform_triangle_length()
    print("OK: test_006_003_make_waveform_triangle")
