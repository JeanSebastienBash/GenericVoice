"""
Test: test_003_004_default_players_structure.py
Suite: 003 Player
Purpose: Default Players Structure
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_default_players_is_dict():
    
    assert isinstance(player.DEFAULT_PLAYERS, dict)

def test_default_players_has_ubuntu():
    
    assert 'ubuntu' in player.DEFAULT_PLAYERS

def test_default_players_has_linux():
    
    assert 'linux' in player.DEFAULT_PLAYERS

def test_default_players_has_macos():
    
    assert 'macos' in player.DEFAULT_PLAYERS

def test_default_players_has_windows():
    
    assert 'windows' in player.DEFAULT_PLAYERS

def test_default_players_ubuntu_value():
    
    assert player.DEFAULT_PLAYERS['ubuntu'] == 'parole'

def test_default_players_linux_value():
    
    assert player.DEFAULT_PLAYERS['linux'] == 'cvlc'

def test_default_players_macos_value():
    
    assert player.DEFAULT_PLAYERS['macos'] == 'vlc'

def test_default_players_windows_value():
    
    assert player.DEFAULT_PLAYERS['windows'] == 'vlc'

def test_default_players_count():
    
    assert len(player.DEFAULT_PLAYERS) == 4

if __name__ == '__main__':
    test_default_players_is_dict()
    test_default_players_has_ubuntu()
    test_default_players_has_linux()
    test_default_players_has_macos()
    test_default_players_has_windows()
    test_default_players_ubuntu_value()
    test_default_players_linux_value()
    test_default_players_macos_value()
    test_default_players_windows_value()
    test_default_players_count()
    print("✓ All test_003_004_default_players_structure tests passed")
