"""
Test: test_006_009_full_melody_composition.py
Suite: 006 Melody
Purpose: Full Melody Composition
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody
import numpy as np

def test_full_melody_composition():
    chord = melody.generate_chord_layer(261.63, "major", 1.0)
    perc = melody.generate_percussion_layer(1.0)
    bass = melody.generate_bass_layer(130.81, 1.0)
    assert len(chord) == len(perc) == len(bass)

if __name__ == '__main__':
    test_full_melody_composition()
    print("OK: test_006_009_full_melody_composition")
