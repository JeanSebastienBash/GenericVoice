"""
Test: test_002_015_default_values.py
Suite: 002 Config
Purpose: Default Values
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config, DEFAULT_TTS, DEFAULT_MODE, DEFAULT_LAUNCHER, DEFAULT_SYSTEM_OS

def test_default_tts():
    
    c = Config()
    assert c.tts == DEFAULT_TTS
    assert c.tts == 'piper'

def test_default_mode():
    
    c = Config()
    assert c.mode == DEFAULT_MODE
    assert c.mode == 'generate'

def test_default_launcher():
    
    c = Config()
    assert c.launcher == DEFAULT_LAUNCHER
    assert c.launcher == 'genericmenu'

def test_default_system_os():
    
    c = Config()
    assert c.system_os == DEFAULT_SYSTEM_OS
    assert c.system_os == 'ubuntu'

def test_default_text():
    
    c = Config()
    assert c.text == ""

def test_default_voice():
    
    c = Config()
    assert c.voice == ""

def test_default_duration():
    
    c = Config()
    assert c.duration == "auto"

def test_default_output():
    
    c = Config()
    assert c.output == ""

def test_default_voice_toggle():
    
    c = Config()
    assert c.voice_toggle == False

def test_default_melody_toggle():
    
    c = Config()
    assert c.melody_toggle == False

def test_default_auto_play():
    
    c = Config()
    assert c.auto_play == False

def test_all_defaults():
    
    c = Config()
    assert c.tts == 'piper'
    assert c.mode == 'generate'
    assert c.launcher == 'genericmenu'
    assert c.system_os == 'ubuntu'
    assert c.auto_fix == False
    assert c.text == ""
    assert c.voice == ""
    assert c.duration == "auto"
    assert c.output == ""
    assert c.voice_toggle == False
    assert c.voice_effect_name == ""
    assert c.melody_toggle == False
    assert c.auto_play == False

if __name__ == '__main__':
    test_default_tts()
    test_default_mode()
    test_default_launcher()
    test_default_system_os()
    test_default_text()
    test_default_voice()
    test_default_duration()
    test_default_output()
    test_default_voice_toggle()
    test_default_melody_toggle()
    test_default_auto_play()
    test_all_defaults()
    print("✓ All test_002_015_default_values tests passed")
