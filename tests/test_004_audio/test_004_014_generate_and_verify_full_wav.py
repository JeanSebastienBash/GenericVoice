"""
Test: test_004_014_generate_and_verify_full_wav.py
Suite: 004 Audio
Purpose: Generate And Verify Full Wav
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

def test_generate_and_save_wav():
    data = np.random.rand(48000).astype(np.float32) * 0.5
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        audio.save_wav_16bit(f.name, data)
        sr, loaded = audio.load_wav(f.name)
        os.unlink(f.name)
        assert sr == 48000
        assert len(loaded) == 48000

if __name__ == '__main__':
    test_generate_and_save_wav()
    print("OK: test_004_014_generate_and_verify_full_wav")
