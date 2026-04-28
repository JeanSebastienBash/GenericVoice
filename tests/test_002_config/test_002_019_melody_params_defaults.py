"""
Test: test_002_019_melody_params_defaults.py
Suite: 002 Config
Purpose: Melody Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_melody_params_root_note():
    
    c = Config()
    assert c.melody.root_note == "C"

def test_melody_params_chord_type():
    
    c = Config()
    assert c.melody.chord_type == "major"

def test_melody_params_chord_voicing():
    
    c = Config()
    assert c.melody.chord_voicing == "close"

def test_melody_params_chord_filter():
    
    c = Config()
    assert c.melody.chord_filter == 3000

def test_melody_params_pad_waveform():
    
    c = Config()
    assert c.melody.pad_waveform == "sine"

def test_melody_params_pad_harmonics():
    
    c = Config()
    assert c.melody.pad_harmonics == 3

if __name__ == '__main__':
    test_melody_params_root_note()
    test_melody_params_chord_type()
    test_melody_params_chord_voicing()
    test_melody_params_chord_filter()
    test_melody_params_pad_waveform()
    test_melody_params_pad_harmonics()
    print("✓ All test_002_019_melody_params_defaults tests passed")
