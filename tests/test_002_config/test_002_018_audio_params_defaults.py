"""
Test: test_002_018_audio_params_defaults.py
Suite: 002 Config
Purpose: Audio Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config, AudioParams

def test_audio_params_wav_format():
    
    c = Config()
    assert c.audio.wav_format == "16-bit"

def test_audio_params_normalize():
    
    c = Config()
    assert c.audio.normalize == False

def test_audio_params_fade_in():
    
    c = Config()
    assert c.audio.fade_in_ms == 50

def test_audio_params_fade_out():
    
    c = Config()
    assert c.audio.fade_out_ms == 80

def test_audio_params_wait_finish():
    
    c = Config()
    assert c.audio.wait_finish == False

def test_audio_params_normalize_peak():
    
    c = Config()
    assert c.audio.normalize_peak == 0.85

def test_audio_params_center_start_time():
    
    c = Config()
    assert c.audio.center_start_time == 0.5

if __name__ == '__main__':
    test_audio_params_wav_format()
    test_audio_params_normalize()
    test_audio_params_fade_in()
    test_audio_params_fade_out()
    test_audio_params_wait_finish()
    test_audio_params_normalize_peak()
    test_audio_params_center_start_time()
    print("✓ All test_002_018_audio_params_defaults tests passed")
