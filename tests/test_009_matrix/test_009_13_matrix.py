"""
Test: test_009_13_matrix.py
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

def test_matrix_all_boolean_flags():
    
    result = parse_args(['--melody', '--auto-play', '--wait-finish', '--normalize', '--auto-fix'])
    assert result.get('melody') == True
    assert result.get('auto_play') == True
    assert result.get('wait_finish') == True
    assert result.get('normalize') == True
    assert result.get('auto_fix') == True

def test_matrix_boolean_defaults():
    
    result = parse_args([])
    assert result.get('melody') == False
    assert result.get('auto_play') == False
    assert result.get('wait_finish') == False
    assert result.get('normalize') == False
    assert result.get('auto_fix') == False

def test_matrix_boolean_with_tts():
    
    result = parse_args(['--tts', 'piper', '--melody', '--normalize'])
    assert result.get('tts') == 'piper'
    assert result.get('melody') == True
    assert result.get('normalize') == True

if __name__ == '__main__':
    test_matrix_all_boolean_flags()
    test_matrix_boolean_defaults()
    test_matrix_boolean_with_tts()
    print("OK: test_009_13_matrix")
