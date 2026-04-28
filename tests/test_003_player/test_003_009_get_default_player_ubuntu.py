"""
Test: test_003_009_get_default_player_ubuntu.py
Suite: 003 Player
Purpose: Get Default Player Ubuntu
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_default_player_ubuntu():
    
    result = player.get_default_player('ubuntu')
    assert isinstance(result, str)
    assert result == 'parole'

def test_get_default_player_ubuntu_is_parole():
    
    result = player.get_default_player('ubuntu')
    assert result == 'parole'

def test_get_default_player_ubuntu_is_string():
    
    result = player.get_default_player('ubuntu')
    assert isinstance(result, str)

if __name__ == '__main__':
    test_get_default_player_ubuntu()
    test_get_default_player_ubuntu_is_parole()
    test_get_default_player_ubuntu_is_string()
    print("OK: test_003_009_get_default_player_ubuntu")
