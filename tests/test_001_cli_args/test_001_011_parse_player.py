"""
Test: test_001_011_parse_player.py
Suite: 001 Cli Args
Purpose: Parse Player
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_player_parole():
    
    result = parse_args(['--player', 'parole'])
    assert result.get('player') == 'parole'

def test_parse_player_cvlc():
    
    result = parse_args(['--player', 'cvlc'])
    assert result.get('player') == 'cvlc'

def test_parse_player_vlc():
    
    result = parse_args(['--player', 'vlc'])
    assert result.get('player') == 'vlc'

def test_parse_player_ffplay():
    
    result = parse_args(['--player', 'ffplay'])
    assert result.get('player') == 'ffplay'

def test_parse_player_aplay():
    
    result = parse_args(['--player', 'aplay'])
    assert result.get('player') == 'aplay'

def test_parse_player_default_none():
    
    result = parse_args([])
    assert result.get('player') is None

def test_parse_player_with_auto_play():
    
    result = parse_args(['--auto-play', '--player', 'cvlc'])
    assert result.get('player') == 'cvlc'
    assert result.get('auto_play') == True

def test_parse_player_custom():
    
    result = parse_args(['--player', 'custom_player'])
    assert result.get('player') == 'custom_player'

if __name__ == '__main__':
    test_parse_player_parole()
    test_parse_player_cvlc()
    test_parse_player_vlc()
    test_parse_player_ffplay()
    test_parse_player_aplay()
    test_parse_player_default_none()
    test_parse_player_with_auto_play()
    test_parse_player_custom()
    print("✓ All test_001_011_parse_player tests passed")
