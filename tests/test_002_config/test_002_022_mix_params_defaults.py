"""
Test: test_002_022_mix_params_defaults.py
Suite: 002 Config
Purpose: Mix Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_mix_params_voice():
    
    c = Config()
    assert c.mix.voice == 0.6

def test_mix_params_chord():
    
    c = Config()
    assert c.mix.chord == 0.25

def test_mix_params_perc():
    
    c = Config()
    assert c.mix.perc == 0.30

def test_mix_params_bass():
    
    c = Config()
    assert c.mix.bass == 0.20

def test_mix_params_ascend_curve():
    
    c = Config()
    assert c.mix.ascend_curve == 1.5

def test_mix_params_ascend_start():
    
    c = Config()
    assert c.mix.ascend_start == 0.30

def test_mix_params_compression_drive():
    
    c = Config()
    assert c.mix.compression_drive == 1.4

if __name__ == '__main__':
    test_mix_params_voice()
    test_mix_params_chord()
    test_mix_params_perc()
    test_mix_params_bass()
    test_mix_params_ascend_curve()
    test_mix_params_ascend_start()
    test_mix_params_compression_drive()
    print("✓ All test_002_022_mix_params_defaults tests passed")
