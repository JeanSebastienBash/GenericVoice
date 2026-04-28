"""
Test: test_003_006_get_available_players_linux.py
Suite: 003 Player
Purpose: Get Available Players Linux
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_available_players_linux():
    
    players = player.get_available_players('linux')
    assert isinstance(players, list)
    assert len(players) > 0

def test_get_available_players_linux_format():
    
    players = player.get_available_players('linux')
    for player_id, player_name in players:
        assert isinstance(player_id, str)
        assert isinstance(player_name, str)

def test_get_available_players_linux_cvlc():
    
    players = player.get_available_players('linux')
    player_ids = [p[0] for p in players]
    assert 'cvlc' in player_ids

def test_get_available_players_linux_ffplay():
    
    players = player.get_available_players('linux')
    player_ids = [p[0] for p in players]
    assert 'ffplay' in player_ids

def test_get_available_players_linux_no_dupes():
    
    players = player.get_available_players('linux')
    player_ids = [p[0] for p in players]
    assert len(player_ids) == len(set(player_ids))

if __name__ == '__main__':
    test_get_available_players_linux()
    test_get_available_players_linux_format()
    test_get_available_players_linux_cvlc()
    test_get_available_players_linux_ffplay()
    test_get_available_players_linux_no_dupes()
    print("OK: test_003_006_get_available_players_linux")
