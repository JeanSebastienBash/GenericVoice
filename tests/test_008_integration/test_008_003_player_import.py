"""
Test: test_008_003_player_import.py
Suite: 008 Integration
Purpose: Player Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/player.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_player_import():
    import player
    assert hasattr(player, 'get_platform_os')

def test_player_functions():
    import player
    assert hasattr(player, 'get_available_players')
    assert hasattr(player, 'get_default_player')

if __name__ == '__main__':
    test_player_import()
    test_player_functions()
    print("OK: test_008_003_player_import")
