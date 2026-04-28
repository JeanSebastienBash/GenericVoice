"""
Test: test_009_02_matrix.py
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

def test_matrix_normalize_wav_format():
    
    result = parse_args(['--normalize', '--wav-format', '32-bit'])
    assert result.get('normalize') == True
    assert result.get('wav_format') == '32-bit'

def test_matrix_fade_in_out():
    
    result = parse_args(['--fade-in', '50', '--fade-out', '100'])
    assert result.get('fade_in') == '50'
    assert result.get('fade_out') == '100'

def test_matrix_all_audio():
    
    result = parse_args(['--normalize', '--wav-format', '32-bit', '--fade-in', '75', '--fade-out', '150'])
    assert result.get('normalize') == True
    assert result.get('wav_format') == '32-bit'
    assert result.get('fade_in') == '75'
    assert result.get('fade_out') == '150'

if __name__ == '__main__':
    test_matrix_normalize_wav_format()
    test_matrix_fade_in_out()
    test_matrix_all_audio()
    print("OK: test_009_02_matrix")
