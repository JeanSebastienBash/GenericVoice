"""
Test: test_009_07_matrix.py
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

def test_matrix_launcher_values():
    
    result = parse_args(['--launcher', 'genericmenu'])
    assert result.get('launcher') == 'genericmenu'

def test_matrix_launcher_with_tts():
    
    result = parse_args(['--tts', 'piper', '--launcher', 'genericmenu'])
    assert result.get('tts') == 'piper'
    assert result.get('launcher') == 'genericmenu'

def test_matrix_launcher_full():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--launcher', 'genericmenu', '--auto-play'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('launcher') == 'genericmenu'
    assert result.get('auto_play') == True

if __name__ == '__main__':
    test_matrix_launcher_values()
    test_matrix_launcher_with_tts()
    test_matrix_launcher_full()
    print("OK: test_009_07_matrix")
