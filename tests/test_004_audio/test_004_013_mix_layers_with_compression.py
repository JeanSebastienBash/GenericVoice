"""
Test: test_004_013_mix_layers_with_compression.py
Suite: 004 Audio
Purpose: Mix Layers With Compression
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np

def test_mix_layers_compression():
    layers = [np.random.rand(4800).astype(np.float32) for _ in range(3)]
    levels = [1.0, 1.0, 1.0]
    result = audio.mix_layers(layers, levels, 0.1, compression_drive=1.4)
    assert np.max(np.abs(result)) <= 1.0

if __name__ == '__main__':
    test_mix_layers_compression()
    print("OK: test_004_013_mix_layers_with_compression")
