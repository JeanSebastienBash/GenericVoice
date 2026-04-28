"""
Test: test_003_005_get_available_players_ubuntu.py
Suite: 003 Player
Purpose: Get Available Players Ubuntu
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_available_players_ubuntu():
    
    players = player.get_available_players('ubuntu')
    assert isinstance(players, list)
    assert len(players) > 0

def test_get_available_players_ubuntu_parole():
    
    players = player.get_available_players('ubuntu')
    player_ids = [p[0] for p in players]
    assert 'parole' in player_ids

def test_get_available_players_ubuntu_format():
    
    players = player.get_available_players('ubuntu')
    for player_id, player_name in players:
        assert isinstance(player_id, str)
        assert isinstance(player_name, str)

def test_get_available_players_ubuntu_count():
    
    players = player.get_available_players('ubuntu')
    player_ids = [p[0] for p in players]
    assert 'parole' in player_ids
    assert 'aplay' in player_ids

def test_get_available_players_ubuntu_no_dupes():
    
    players = player.get_available_players('ubuntu')
    player_ids = [p[0] for p in players]
    assert len(player_ids) == len(set(player_ids))

if __name__ == '__main__':
    test_get_available_players_ubuntu()
    test_get_available_players_ubuntu_parole()
    test_get_available_players_ubuntu_format()
    test_get_available_players_ubuntu_count()
    test_get_available_players_ubuntu_no_dupes()
    print("✓ All test_003_005_get_available_players_ubuntu tests passed")
