"""
Test: test_009_11_matrix.py
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

def test_matrix_tts_values():
    
    for tts in ['piper', 'edge', 'espeak']:
        result = parse_args(['--tts', tts])
        assert result.get('tts') == tts

def test_matrix_tts_with_text():
    
    for tts in ['piper', 'edge', 'espeak']:
        result = parse_args(['--tts', tts, '--text', 'Hello'])
        assert result.get('tts') == tts
        assert result.get('text') == 'Hello'

def test_matrix_tts_with_all():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--voice', 'default', '--output', 'out.wav'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('voice') == 'default'
    assert result.get('output') == 'out.wav'

if __name__ == '__main__':
    test_matrix_tts_values()
    test_matrix_tts_with_text()
    test_matrix_tts_with_all()
    print("OK: test_009_11_matrix")
