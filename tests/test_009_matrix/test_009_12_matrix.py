"""
Test: test_009_12_matrix.py
Suite: 009 Matrix
Purpose: Matrix
Context: Unit test in test_009_matrix/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: Complete system
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from gv import parse_args

def test_matrix_player_values():
    
    for player in ['parole', 'cvlc', 'vlc', 'ffplay', 'aplay']:
        result = parse_args(['--auto-play', '--player', player])
        assert result.get('player') == player
        assert result.get('auto_play') == True

def test_matrix_player_with_auto_play():
    
    result = parse_args(['--auto-play', '--player', 'vlc'])
    assert result.get('player') == 'vlc'
    assert result.get('auto_play') == True

def test_matrix_player_with_wait():
    
    result = parse_args(['--auto-play', '--player', 'cvlc', '--wait-finish'])
    assert result.get('player') == 'cvlc'
    assert result.get('auto_play') == True
    assert result.get('wait_finish') == True

if __name__ == '__main__':
    test_matrix_player_values()
    test_matrix_player_with_auto_play()
    test_matrix_player_with_wait()
    print("OK: test_009_12_matrix")
