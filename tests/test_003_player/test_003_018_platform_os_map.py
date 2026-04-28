"""
Test: test_003_018_platform_os_map.py
Suite: 003 Player
Purpose: Platform Os Map
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_platform_os_map_defined():
    
    assert hasattr(player, 'PLATFORM_OS_MAP')

def test_platform_os_map_is_dict():
    
    assert isinstance(player.PLATFORM_OS_MAP, dict)

def test_platform_os_map_has_ubuntu():
    
    assert 'ubuntu' in player.PLATFORM_OS_MAP

def test_platform_os_map_has_linux():
    
    assert 'linux' in player.PLATFORM_OS_MAP

def test_platform_os_map_has_darwin():
    
    assert 'darwin' in player.PLATFORM_OS_MAP

def test_platform_os_map_has_win32():
    
    assert 'win32' in player.PLATFORM_OS_MAP

def test_platform_os_map_values():
    
    for key, value in player.PLATFORM_OS_MAP.items():
        assert isinstance(value, str)

def test_platform_os_map_count():
    
    assert len(player.PLATFORM_OS_MAP) >= 4

if __name__ == '__main__':
    test_platform_os_map_defined()
    test_platform_os_map_is_dict()
    test_platform_os_map_has_ubuntu()
    test_platform_os_map_has_linux()
    test_platform_os_map_has_darwin()
    test_platform_os_map_has_win32()
    test_platform_os_map_values()
    test_platform_os_map_count()
    print("OK: test_003_018_platform_os_map")
