"""
Test: test_003_012_get_default_player_windows.py
Suite: 003 Player
Purpose: Get Default Player Windows
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_default_player_windows():
    
    result = player.get_default_player('windows')
    assert isinstance(result, str)
    assert result == 'vlc'

def test_get_default_player_windows_is_vlc():
    
    result = player.get_default_player('windows')
    assert result == 'vlc'

def test_get_default_player_windows_is_string():
    
    result = player.get_default_player('windows')
    assert isinstance(result, str)

if __name__ == '__main__':
    test_get_default_player_windows()
    test_get_default_player_windows_is_vlc()
    test_get_default_player_windows_is_string()
    print("OK: test_003_012_get_default_player_windows")
