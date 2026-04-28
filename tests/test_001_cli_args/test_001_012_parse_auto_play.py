"""
Test: test_001_012_parse_auto_play.py
Suite: 001 Cli Args
Purpose: Parse Auto Play
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_auto_play():
    
    result = parse_args(['--auto-play'])
    assert result.get('auto_play') == True

def test_auto_play_default_false():
    
    result = parse_args([])
    assert result.get('auto_play') == False

def test_auto_play_with_player():
    
    result = parse_args(['--auto-play', '--player', 'cvlc'])
    assert result.get('auto_play') == True
    assert result.get('player') == 'cvlc'

def test_auto_play_with_tts():
    
    result = parse_args(['--tts', 'piper', '--auto-play'])
    assert result.get('auto_play') == True
    assert result.get('tts') == 'piper'

def test_auto_play_with_wait_finish():
    
    result = parse_args(['--auto-play', '--wait-finish'])
    assert result.get('auto_play') == True
    assert result.get('wait_finish') == True

def test_auto_play_no_value_needed():
    
    result = parse_args(['--auto-play'])
    assert 'auto_play' in result
    assert result['auto_play'] == True

def test_auto_play_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--auto-play', '--player', 'vlc'])
    assert result.get('auto_play') == True
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('player') == 'vlc'

if __name__ == '__main__':
    test_parse_auto_play()
    test_auto_play_default_false()
    test_auto_play_with_player()
    test_auto_play_with_tts()
    test_auto_play_with_wait_finish()
    test_auto_play_no_value_needed()
    test_auto_play_full_args()
    print("✓ All test_001_012_parse_auto_play tests passed")
