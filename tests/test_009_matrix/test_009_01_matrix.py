"""
Test: test_009_01_matrix.py
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

def test_matrix_auto_play_player():
    
    result = parse_args(['--auto-play', '--player', 'cvlc'])
    assert result.get('auto_play') == True
    assert result.get('player') == 'cvlc'

def test_matrix_auto_play_wait():
    
    result = parse_args(['--auto-play', '--wait-finish'])
    assert result.get('auto_play') == True
    assert result.get('wait_finish') == True

def test_matrix_auto_play_all():
    
    result = parse_args(['--auto-play', '--player', 'vlc', '--wait-finish'])
    assert result.get('auto_play') == True
    assert result.get('player') == 'vlc'
    assert result.get('wait_finish') == True

if __name__ == '__main__':
    test_matrix_auto_play_player()
    test_matrix_auto_play_wait()
    test_matrix_auto_play_all()
    print("OK: test_009_01_matrix")
