"""
Test: test_003_010_get_default_player_linux.py
Suite: 003 Player
Purpose: Get Default Player Linux
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_default_player_linux():
    
    result = player.get_default_player('linux')
    assert isinstance(result, str)
    assert result == 'cvlc'

def test_get_default_player_linux_is_cvlc():
    
    result = player.get_default_player('linux')
    assert result == 'cvlc'

def test_get_default_player_linux_is_string():
    
    result = player.get_default_player('linux')
    assert isinstance(result, str)

if __name__ == '__main__':
    test_get_default_player_linux()
    test_get_default_player_linux_is_cvlc()
    test_get_default_player_linux_is_string()
    print("OK: test_003_010_get_default_player_linux")
