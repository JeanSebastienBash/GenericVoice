"""
Test: test_002_023_espeak_params_defaults.py
Suite: 002 Config
Purpose: Espeak Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_espeak_params_variant():
    
    c = Config()
    assert c.espeak.variant == 1

def test_espeak_params_pitch():
    
    c = Config()
    assert c.espeak.pitch == 50

def test_espeak_params_speed():
    
    c = Config()
    assert c.espeak.speed == 140

if __name__ == '__main__':
    test_espeak_params_variant()
    test_espeak_params_pitch()
    test_espeak_params_speed()
    print("✓ All test_002_023_espeak_params_defaults tests passed")
