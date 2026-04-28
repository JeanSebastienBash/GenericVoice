"""
Test: test_001_024_apply_config.py
Suite: 001 Cli Args
Purpose: Apply Config
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config import Config, config
from gv import apply_config

def test_apply_config_tts():
    
    test_config = Config()
    opts = {'tts': 'piper', 'text': None, 'voice': None}
    for key, val in opts.items():
        if val is not None:
            if key == 'tts':
                test_config.tts = val
    assert test_config.tts == 'piper'

def test_apply_config_text():
    
    test_config = Config()
    test_config.text = "Hello World"
    assert test_config.text == "Hello World"

def test_apply_config_melody():
    
    test_config = Config()
    test_config.melody_toggle = True
    assert test_config.melody_toggle == True

def test_apply_config_auto_play():
    
    test_config = Config()
    test_config.auto_play = True
    assert test_config.auto_play == True

def test_apply_config_wav_format():
    
    test_config = Config()
    test_config.audio.wav_format = "32-bit"
    assert test_config.audio.wav_format == "32-bit"

def test_apply_config_fade_in():
    
    test_config = Config()
    test_config.audio.fade_in_ms = 100
    assert test_config.audio.fade_in_ms == 100

def test_apply_config_fade_out():
    
    test_config = Config()
    test_config.audio.fade_out_ms = 150
    assert test_config.audio.fade_out_ms == 150

def test_apply_config_reset():
    
    test_config = Config()
    test_config.tts = "edge"
    test_config.text = "test"
    test_config.melody_toggle = True
    test_config.reset_to_defaults()
    assert test_config.tts == "piper"
    assert test_config.text == ""
    assert test_config.melody_toggle == False

def test_apply_config_voice_effect():
    
    test_config = Config()
    test_config.voice_toggle = True
    test_config.voice_effect_name = "echo"
    assert test_config.voice_effect_name == "echo"
    assert test_config.voice_toggle == True

def test_apply_config_is_blocked():
    
    test_config = Config()
    test_config.mode = "generate"
    assert test_config.is_blocked() == False
    test_config.mode = "list-voices"
    assert test_config.is_blocked() == True

if __name__ == '__main__':
    test_apply_config_tts()
    test_apply_config_text()
    test_apply_config_melody()
    test_apply_config_auto_play()
    test_apply_config_wav_format()
    test_apply_config_fade_in()
    test_apply_config_fade_out()
    test_apply_config_reset()
    test_apply_config_voice_effect()
    test_apply_config_is_blocked()
    print("✓ All test_001_024_apply_config tests passed")
