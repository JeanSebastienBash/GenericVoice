"""
Test: test_006_005_chord_layer_major.py
Suite: 006 Melody
Purpose: Chord Layer Major
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody
import numpy as np

def test_generate_chord_layer_major():
    result = melody.generate_chord_layer(261.63, "major", 1.0)
    assert isinstance(result, np.ndarray)

def test_generate_chord_layer_major_length():
    result = melody.generate_chord_layer(261.63, "major", 1.0)
    assert len(result) == 48000

if __name__ == '__main__':
    test_generate_chord_layer_major()
    test_generate_chord_layer_major_length()
    print("OK: test_006_005_chord_layer_major")
