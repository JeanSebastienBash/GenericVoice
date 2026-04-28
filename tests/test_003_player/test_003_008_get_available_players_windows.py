"""
Test: test_003_008_get_available_players_windows.py
Suite: 003 Player
Purpose: Get Available Players Windows
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_available_players_windows():
    
    players = player.get_available_players('windows')
    assert isinstance(players, list)
    assert len(players) > 0

def test_get_available_players_windows_format():
    
    players = player.get_available_players('windows')
    for player_id, player_name in players:
        assert isinstance(player_id, str)
        assert isinstance(player_name, str)

def test_get_available_players_windows_vlc():
    
    players = player.get_available_players('windows')
    player_ids = [p[0] for p in players]
    assert 'vlc' in player_ids

def test_get_available_players_windows_ffplay():
    
    players = player.get_available_players('windows')
    player_ids = [p[0] for p in players]
    assert 'ffplay' in player_ids

if __name__ == '__main__':
    test_get_available_players_windows()
    test_get_available_players_windows_format()
    test_get_available_players_windows_vlc()
    test_get_available_players_windows_ffplay()
    print("OK: test_003_008_get_available_players_windows")
