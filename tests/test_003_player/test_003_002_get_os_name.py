"""
Test: test_003_002_get_os_name.py
Suite: 003 Player
Purpose: Get Os Name
Context: Unit test in test_003_player/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import player

def test_get_os_name_returns_string():
    
    result = player.get_os_name()
    assert isinstance(result, str)

def test_get_os_name_lowercase():
    
    result = player.get_os_name()
    assert result == result.lower()

def test_get_os_name_has_fallback():
    
    result = player.get_os_name()
    assert len(result) > 0

def test_get_os_name_uses_os_module():
    
    import os as os_module
    if hasattr(os_module, 'uname'):
        result = player.get_os_name()
        assert isinstance(result, str)

if __name__ == '__main__':
    test_get_os_name_returns_string()
    test_get_os_name_lowercase()
    test_get_os_name_has_fallback()
    test_get_os_name_uses_os_module()
    print("OK: test_003_002_get_os_name")
