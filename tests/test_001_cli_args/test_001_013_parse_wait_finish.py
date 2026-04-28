"""
Test: test_001_013_parse_wait_finish.py
Suite: 001 Cli Args
Purpose: Parse Wait Finish
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_wait_finish():
    
    result = parse_args(['--wait-finish'])
    assert result.get('wait_finish') == True

def test_wait_finish_default_false():
    
    result = parse_args([])
    assert result.get('wait_finish') == False

def test_wait_finish_with_auto_play():
    
    result = parse_args(['--auto-play', '--wait-finish'])
    assert result.get('wait_finish') == True
    assert result.get('auto_play') == True

def test_wait_finish_with_player():
    
    result = parse_args(['--auto-play', '--player', 'cvlc', '--wait-finish'])
    assert result.get('wait_finish') == True
    assert result.get('auto_play') == True
    assert result.get('player') == 'cvlc'

def test_wait_finish_no_value_needed():
    
    result = parse_args(['--wait-finish'])
    assert 'wait_finish' in result
    assert result['wait_finish'] == True

def test_wait_finish_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--auto-play', '--player', 'vlc', '--wait-finish'])
    assert result.get('wait_finish') == True
    assert result.get('auto_play') == True
    assert result.get('player') == 'vlc'
    assert result.get('tts') == 'piper'

if __name__ == '__main__':
    test_parse_wait_finish()
    test_wait_finish_default_false()
    test_wait_finish_with_auto_play()
    test_wait_finish_with_player()
    test_wait_finish_no_value_needed()
    test_wait_finish_full_args()
    print("✓ All test_001_013_parse_wait_finish tests passed")
