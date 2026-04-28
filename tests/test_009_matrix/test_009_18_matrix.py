"""
Test: test_009_18_matrix.py
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
from gv import parse_args, validate_params

def test_matrix_player_requires_auto_play():
    
    try:
        validate_params({'player': 'vlc', 'auto_play': False})
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass

def test_matrix_wait_finish_requires_auto_play():
    
    try:
        validate_params({'wait_finish': True, 'auto_play': False})
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass

def test_matrix_valid_combinations():
    
    validate_params({'tts': 'piper', 'text': 'Hello'})
    validate_params({'auto_play': True, 'player': 'vlc'})
    validate_params({'auto_play': True, 'wait_finish': True})

if __name__ == '__main__':
    test_matrix_player_requires_auto_play()
    test_matrix_wait_finish_requires_auto_play()
    test_matrix_valid_combinations()
    print("OK: test_009_18_matrix")
