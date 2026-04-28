"""
Test: test_003_013_get_default_player_auto.py
Suite: 003 Player
Purpose: Get Default Player Auto
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_default_player_auto():
    
    result = player.get_default_player(None)
    assert isinstance(result, str)
    assert len(result) > 0

def test_get_default_player_auto_is_string():
    
    result = player.get_default_player()
    assert isinstance(result, str)

def test_get_default_player_auto_is_valid():
    
    result = player.get_default_player()
    assert result in player.AVAILABLE_PLAYERS

def test_get_default_player_auto_uses_platform():
    
    result_none = player.get_default_player(None)
    result_empty = player.get_default_player()
    assert result_none == result_empty

if __name__ == '__main__':
    test_get_default_player_auto()
    test_get_default_player_auto_is_string()
    test_get_default_player_auto_is_valid()
    test_get_default_player_auto_uses_platform()
    print("OK: test_003_013_get_default_player_auto")
