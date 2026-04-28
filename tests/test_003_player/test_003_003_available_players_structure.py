"""
Test: test_003_003_available_players_structure.py
Suite: 003 Player
Purpose: Available Players Structure
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_available_players_is_dict():
    
    assert isinstance(player.AVAILABLE_PLAYERS, dict)

def test_available_players_has_parole():
    
    assert 'parole' in player.AVAILABLE_PLAYERS

def test_available_players_has_cvlc():
    
    assert 'cvlc' in player.AVAILABLE_PLAYERS

def test_available_players_has_vlc():
    
    assert 'vlc' in player.AVAILABLE_PLAYERS

def test_available_players_has_ffplay():
    
    assert 'ffplay' in player.AVAILABLE_PLAYERS

def test_available_players_has_aplay():
    
    assert 'aplay' in player.AVAILABLE_PLAYERS

def test_available_players_entry_structure():
    
    for player_id, info in player.AVAILABLE_PLAYERS.items():
        assert 'name' in info, f"Missing name for {player_id}"
        assert 'cmd' in info, f"Missing cmd for {player_id}"
        assert 'os' in info, f"Missing os for {player_id}"
        assert isinstance(info['os'], list), f"os should be a list for {player_id}"

def test_available_players_count():
    
    assert len(player.AVAILABLE_PLAYERS) == 5

if __name__ == '__main__':
    test_available_players_is_dict()
    test_available_players_has_parole()
    test_available_players_has_cvlc()
    test_available_players_has_vlc()
    test_available_players_has_ffplay()
    test_available_players_has_aplay()
    test_available_players_entry_structure()
    test_available_players_count()
    print("✓ All test_003_003_available_players_structure tests passed")
