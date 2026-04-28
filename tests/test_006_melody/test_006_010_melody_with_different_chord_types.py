"""
Test: test_006_010_melody_with_different_chord_types.py
Suite: 006 Melody
Purpose: Melody With Different Chord Types
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody
import numpy as np

def test_chord_types():
    chord_types = ["major", "minor", "sus2", "sus4"]
    for ct in chord_types:
        result = melody.generate_chord_layer(261.63, ct, 1.0)
        assert isinstance(result, np.ndarray)
        assert len(result) == 48000

if __name__ == '__main__':
    test_chord_types()
    print("OK: test_006_010_melody_with_different_chord_types")
