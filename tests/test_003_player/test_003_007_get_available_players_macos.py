"""
Test: test_003_007_get_available_players_macos.py
Suite: 003 Player
Purpose: Get Available Players Macos
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_available_players_macos():
    
    players = player.get_available_players('macos')
    assert isinstance(players, list)
    assert len(players) > 0

def test_get_available_players_macos_format():
    
    players = player.get_available_players('macos')
    for player_id, player_name in players:
        assert isinstance(player_id, str)
        assert isinstance(player_name, str)

def test_get_available_players_macos_vlc():
    
    players = player.get_available_players('macos')
    player_ids = [p[0] for p in players]
    assert 'vlc' in player_ids

def test_get_available_players_macos_ffplay():
    
    players = player.get_available_players('macos')
    player_ids = [p[0] for p in players]
    assert 'ffplay' in player_ids

if __name__ == '__main__':
    test_get_available_players_macos()
    test_get_available_players_macos_format()
    test_get_available_players_macos_vlc()
    test_get_available_players_macos_ffplay()
    print("OK: test_003_007_get_available_players_macos")
