"""
Test: test_006_001_sample_rate_duration.py
Suite: 006 Melody
Purpose: Sample Rate Duration
Context: Unit test in test_006_melody/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import melody

def test_sample_rate_defined():
    assert hasattr(melody, 'SAMPLE_RATE')

def test_sample_rate_value():
    assert melody.SAMPLE_RATE == 48000

def test_duration_defined():
    assert hasattr(melody, 'DURATION')

def test_duration_value():
    assert melody.DURATION == 5.0

if __name__ == '__main__':
    test_sample_rate_defined()
    test_sample_rate_value()
    test_duration_defined()
    test_duration_value()
    print("OK: test_006_001_sample_rate_duration")
