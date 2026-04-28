"""
Test: test_001_010_parse_voice_effect.py
Suite: 001 Cli Args
Purpose: Parse Voice Effect
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_voice_effect_echo():
    
    result = parse_args(['--voice-effect', 'echo'])
    assert result.get('voice_effect') == 'echo'

def test_parse_voice_effect_vibrato():
    
    result = parse_args(['--voice-effect', 'vibrato'])
    assert result.get('voice_effect') == 'vibrato'

def test_parse_voice_effect_reverb():
    
    result = parse_args(['--voice-effect', 'reverb'])
    assert result.get('voice_effect') == 'reverb'

def test_parse_voice_effect_default_none():
    
    result = parse_args([])
    assert result.get('voice_effect') is None

def test_parse_voice_effect_with_tts():
    
    result = parse_args(['--tts', 'piper', '--voice-effect', 'echo'])
    assert result.get('voice_effect') == 'echo'
    assert result.get('tts') == 'piper'

def test_parse_voice_effect_with_melody():
    
    result = parse_args(['--melody', '--voice-effect', 'vibrato'])
    assert result.get('voice_effect') == 'vibrato'
    assert result.get('melody') == True

def test_parse_voice_effect_none():
    
    result = parse_args(['--voice-effect', 'none'])
    assert result.get('voice_effect') == 'none'

def test_parse_voice_effect_with_text():
    
    result = parse_args(['--voice-effect', 'echo', '--text', 'Hello'])
    assert result.get('voice_effect') == 'echo'
    assert result.get('text') == 'Hello'

def test_parse_voice_effect_custom():
    
    result = parse_args(['--voice-effect', 'custom_effect'])
    assert result.get('voice_effect') == 'custom_effect'

def test_parse_voice_effect_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--voice-effect', 'reverb', '--melody'])
    assert result.get('voice_effect') == 'reverb'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('melody') == True

if __name__ == '__main__':
    test_parse_voice_effect_echo()
    test_parse_voice_effect_vibrato()
    test_parse_voice_effect_reverb()
    test_parse_voice_effect_default_none()
    test_parse_voice_effect_with_tts()
    test_parse_voice_effect_with_melody()
    test_parse_voice_effect_none()
    test_parse_voice_effect_with_text()
    test_parse_voice_effect_custom()
    test_parse_voice_effect_full_args()
    print("✓ All test_001_010_parse_voice_effect tests passed")
