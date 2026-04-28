"""
Test: test_004_001_sample_rate.py
Suite: 004 Audio
Purpose: Sample Rate
Context: Unit test in test_004_audio/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/audio.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import audio

def test_sample_rate_defined():
    
    assert hasattr(audio, 'SAMPLE_RATE')

def test_sample_rate_value():
    
    assert audio.SAMPLE_RATE == 48000

def test_sample_rate_type():
    
    assert isinstance(audio.SAMPLE_RATE, int)

if __name__ == '__main__':
    test_sample_rate_defined()
    test_sample_rate_value()
    test_sample_rate_type()
    print("OK: test_004_001_sample_rate")
