"""
Test: test_006_002_make_waveform_sine.py
Suite: 006 Melody
Purpose: Make Waveform Sine
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody
import numpy as np

def test_make_waveform_sine_defined():
    assert hasattr(melody, 'make_waveform')

def test_make_waveform_sine_returns_array():
    result = melody.make_waveform(440.0, 1.0, 'sine')
    assert isinstance(result, np.ndarray)

def test_make_waveform_sine_length():
    result = melody.make_waveform(440.0, 1.0, 'sine')
    assert len(result) == 48000

if __name__ == '__main__':
    test_make_waveform_sine_defined()
    test_make_waveform_sine_returns_array()
    test_make_waveform_sine_length()
    print("OK: test_006_002_make_waveform_sine")
