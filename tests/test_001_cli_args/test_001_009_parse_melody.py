"""
Test: test_001_009_parse_melody.py
Suite: 001 Cli Args
Purpose: Parse Melody
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_melody():
    
    result = parse_args(['--melody'])
    assert result.get('melody') == True

def test_melody_default_false():
    
    result = parse_args([])
    assert result.get('melody') == False

def test_melody_with_tts():
    
    result = parse_args(['--tts', 'piper', '--melody'])
    assert result.get('melody') == True
    assert result.get('tts') == 'piper'

def test_melody_with_voice_effect():
    
    result = parse_args(['--melody', '--voice-effect', 'echo'])
    assert result.get('melody') == True
    assert result.get('voice_effect') == 'echo'

def test_melody_no_value_needed():
    
    result = parse_args(['--melody'])
    assert 'melody' in result
    assert result['melody'] == True

def test_melody_with_text():
    
    result = parse_args(['--melody', '--text', 'Hello'])
    assert result.get('melody') == True
    assert result.get('text') == 'Hello'

def test_melody_with_all_flags():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--melody', '--auto-play'])
    assert result.get('melody') == True
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('auto_play') == True

def test_melody_alone():
    
    result = parse_args(['--melody'])
    assert len([k for k, v in result.items() if v]) == 1
    assert result['melody'] == True

if __name__ == '__main__':
    test_parse_melody()
    test_melody_default_false()
    test_melody_with_tts()
    test_melody_with_voice_effect()
    test_melody_no_value_needed()
    test_melody_with_text()
    test_melody_with_all_flags()
    test_melody_alone()
    print("✓ All test_001_009_parse_melody tests passed")
