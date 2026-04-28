"""
Test: test_002_021_bass_params_defaults.py
Suite: 002 Config
Purpose: Bass Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_bass_params_bass_type():
    
    c = Config()
    assert c.bass.bass_type == "sine"

def test_bass_params_bass_filter():
    
    c = Config()
    assert c.bass.bass_filter == 300

def test_bass_params_bass_saturation():
    
    c = Config()
    assert c.bass.bass_saturation == 1.5

def test_bass_params_bass_note_style():
    
    c = Config()
    assert c.bass.bass_note_style == "root"

if __name__ == '__main__':
    test_bass_params_bass_type()
    test_bass_params_bass_filter()
    test_bass_params_bass_saturation()
    test_bass_params_bass_note_style()
    print("✓ All test_002_021_bass_params_defaults tests passed")
