"""
Test: test_008_004_audio_import.py
Suite: 008 Integration
Purpose: Audio Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_audio_import():
    import audio
    assert hasattr(audio, 'load_wav')

def test_audio_functions():
    import audio
    assert hasattr(audio, 'save_wav_16bit')
    assert hasattr(audio, 'save_wav_32bit')

if __name__ == '__main__':
    test_audio_import()
    test_audio_functions()
    print("OK: test_008_004_audio_import")
