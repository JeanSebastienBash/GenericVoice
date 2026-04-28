"""
Test: test_006_007_percussion_layer.py
Suite: 006 Melody
Purpose: Percussion Layer
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody
import numpy as np

def test_generate_percussion_layer():
    result = melody.generate_percussion_layer(1.0)
    assert isinstance(result, np.ndarray)

def test_generate_percussion_layer_length():
    result = melody.generate_percussion_layer(1.0)
    assert len(result) == 48000

if __name__ == '__main__':
    test_generate_percussion_layer()
    test_generate_percussion_layer_length()
    print("OK: test_006_007_percussion_layer")
