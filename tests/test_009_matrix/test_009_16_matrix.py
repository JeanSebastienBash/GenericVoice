"""
Test: test_009_16_matrix.py
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

def test_matrix_flags_independence():
    
    result = parse_args(['--tts', 'piper', '--melody', '--normalize'])
    assert result.get('tts') == 'piper'
    assert result.get('melody') == True
    assert result.get('normalize') == True

def test_matrix_flags_override():
    
    result = parse_args(['--tts', 'piper', '--tts', 'edge'])
    assert result.get('tts') == 'edge'

def test_matrix_flags_with_defaults():
    
    result = parse_args(['--tts', 'piper'])
    assert result.get('tts') == 'piper'
    assert result.get('text') is None
    assert result.get('voice') is None
    assert result.get('melody') == False

if __name__ == '__main__':
    test_matrix_flags_independence()
    test_matrix_flags_override()
    test_matrix_flags_with_defaults()
    print("OK: test_009_16_matrix")
