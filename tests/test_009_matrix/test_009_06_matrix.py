"""
Test: test_009_06_matrix.py
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

def test_matrix_duration_values():
    
    for dur in ['5', '10', '30', '60', 'auto']:
        result = parse_args(['--duration', dur])
        assert result.get('duration') == dur

def test_matrix_duration_with_text():
    
    result = parse_args(['--duration', '10', '--text', 'Test'])
    assert result.get('duration') == '10'
    assert result.get('text') == 'Test'

def test_matrix_duration_full():
    
    result = parse_args(['--tts', 'piper', '--text', 'Hello', '--duration', '15', '--output', 'out.wav'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello'
    assert result.get('duration') == '15'
    assert result.get('output') == 'out.wav'

if __name__ == '__main__':
    test_matrix_duration_values()
    test_matrix_duration_with_text()
    test_matrix_duration_full()
    print("OK: test_009_06_matrix")
