"""
Test: test_004_006_save_and_load_wav_32bit.py
Suite: 004 Audio
Purpose: Save And Load Wav 32Bit
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio
import numpy as np
import tempfile

def test_save_wav_32bit_defined():
    assert hasattr(audio, 'save_wav_32bit')

def test_save_and_load_wav_32bit():
    data = np.random.rand(4800).astype(np.float32) * 0.5
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        audio.save_wav_32bit(f.name, data)
        sr, loaded = audio.load_wav(f.name)
        os.unlink(f.name)
        assert sr == 48000

if __name__ == '__main__':
    test_save_wav_32bit_defined()
    test_save_and_load_wav_32bit()
    print("OK: test_004_006_save_and_load_wav_32bit")
