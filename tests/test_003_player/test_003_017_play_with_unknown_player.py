"""
Test: test_003_017_play_with_unknown_player.py
Suite: 003 Player
Purpose: Play With Unknown Player
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_available_players_constant():
    
    assert isinstance(player.AVAILABLE_PLAYERS, dict)
    assert 'parole' in player.AVAILABLE_PLAYERS
    assert 'cvlc' in player.AVAILABLE_PLAYERS
    assert 'vlc' in player.AVAILABLE_PLAYERS
    assert 'ffplay' in player.AVAILABLE_PLAYERS
    assert 'aplay' in player.AVAILABLE_PLAYERS

def test_default_players_constant():
    
    assert isinstance(player.DEFAULT_PLAYERS, dict)
    assert 'ubuntu' in player.DEFAULT_PLAYERS
    assert 'linux' in player.DEFAULT_PLAYERS
    assert 'macos' in player.DEFAULT_PLAYERS
    assert 'windows' in player.DEFAULT_PLAYERS

def test_player_module_exports():
    
    exports = player.__all__
    assert 'get_platform_os' in exports
    assert 'get_os_name' in exports
    assert 'get_available_players' in exports
    assert 'get_default_player' in exports
    assert 'is_player_available' in exports
    assert 'play' in exports

def test_available_players_has_required_keys():
    
    required_keys = ['name', 'cmd', 'os']
    for player_id, info in player.AVAILABLE_PLAYERS.items():
        for key in required_keys:
            assert key in info, f"Missing {key} in {player_id}"

if __name__ == '__main__':
    test_available_players_constant()
    test_default_players_constant()
    test_player_module_exports()
    test_available_players_has_required_keys()
    print("OK: test_003_017_player_constants")
