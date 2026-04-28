"""
Test: test_009_00_matrix.py
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

def test_matrix_tts_text():
    
    result = parse_args(['--tts', 'piper', '--text', 'Hello'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello'

def test_matrix_tts_voice():
    
    result = parse_args(['--tts', 'edge', '--voice', 'en-US-JennyNeural'])
    assert result.get('tts') == 'edge'
    assert result.get('voice') == 'en-US-JennyNeural'

def test_matrix_all_basic():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--voice', 'default', '--duration', '5'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('voice') == 'default'
    assert result.get('duration') == '5'

if __name__ == '__main__':
    test_matrix_tts_text()
    test_matrix_tts_voice()
    test_matrix_all_basic()
    print("OK: test_009_00_matrix")
