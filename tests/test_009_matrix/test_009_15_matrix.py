"""
Test: test_009_15_matrix.py
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

def test_matrix_empty_text():
    
    result = parse_args(['--tts', 'piper', '--text', ''])
    assert result.get('text') == ''
    assert result.get('tts') == 'piper'

def test_matrix_long_text():
    
    long_text = "This is a very long text message. " * 10
    result = parse_args(['--tts', 'piper', '--text', long_text])
    assert result.get('text') == long_text

def test_matrix_special_chars():
    
    result = parse_args(['--text', 'Hello! How are you? Testing special chars: @#$%'])
    assert result.get('text') == 'Hello! How are you? Testing special chars: @#$%'

if __name__ == '__main__':
    test_matrix_empty_text()
    test_matrix_long_text()
    test_matrix_special_chars()
    print("OK: test_009_15_matrix")
