"""
Test: test_003_015_is_player_available_known.py
Suite: 003 Player
Purpose: Is Player Available Known
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_is_player_available_known_parole():
    
    result = player.is_player_available('parole')
    assert isinstance(result, bool)

def test_is_player_available_known_cvlc():
    
    result = player.is_player_available('cvlc')
    assert isinstance(result, bool)

def test_is_player_available_known_vlc():
    
    result = player.is_player_available('vlc')
    assert isinstance(result, bool)

def test_is_player_available_known_ffplay():
    
    result = player.is_player_available('ffplay')
    assert isinstance(result, bool)

def test_is_player_available_known_aplay():
    
    result = player.is_player_available('aplay')
    assert isinstance(result, bool)

def test_is_player_available_in_dict():
    
    for player_id in ['parole', 'cvlc', 'vlc', 'ffplay', 'aplay']:
        assert player_id in player.AVAILABLE_PLAYERS

if __name__ == '__main__':
    test_is_player_available_known_parole()
    test_is_player_available_known_cvlc()
    test_is_player_available_known_vlc()
    test_is_player_available_known_ffplay()
    test_is_player_available_known_aplay()
    test_is_player_available_in_dict()
    print("OK: test_003_015_is_player_available_known")
