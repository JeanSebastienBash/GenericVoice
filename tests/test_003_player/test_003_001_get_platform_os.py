"""
Test: test_003_001_get_platform_os.py
Suite: 003 Player
Purpose: Get Platform Os
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_platform_os_returns_string():
    
    result = player.get_platform_os()
    assert isinstance(result, str)

def test_get_platform_os_valid_value():
    
    result = player.get_platform_os()
    valid_values = ['ubuntu', 'linux', 'windows', 'macos']
    assert result in valid_values

def test_get_platform_os_consistent():
    
    result1 = player.get_platform_os()
    result2 = player.get_platform_os()
    assert result1 == result2

def test_platform_os_map_defined():
    
    assert hasattr(player, 'PLATFORM_OS_MAP')
    assert isinstance(player.PLATFORM_OS_MAP, dict)

def test_get_platform_os_from_map():
    
    import sys as sys_module
    platform = sys_module.platform.lower()
    expected = player.PLATFORM_OS_MAP.get(platform, 'linux')
    result = player.get_platform_os()
    assert result == expected

if __name__ == '__main__':
    test_get_platform_os_returns_string()
    test_get_platform_os_valid_value()
    test_get_platform_os_consistent()
    test_platform_os_map_defined()
    test_get_platform_os_from_map()
    print("✓ All test_003_001_get_platform_os tests passed")
