"""
Test: test_004_007_load_nonexistent.py
Suite: 004 Audio
Purpose: Load Nonexistent
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio

def test_load_nonexistent_returns_none():
    sr, data = audio.load_wav('/nonexistent/file.wav')
    assert data is None

def test_load_nonexistent_returns_rate():
    sr, data = audio.load_wav('/nonexistent/file.wav')
    assert sr == 48000

if __name__ == '__main__':
    test_load_nonexistent_returns_none()
    test_load_nonexistent_returns_rate()
    print("OK: test_004_007_load_nonexistent")
