"""
Test: test_009_10_matrix.py
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

def test_matrix_voice_with_tts():
    
    for tts in ['piper', 'edge', 'espeak']:
        result = parse_args(['--tts', tts, '--voice', 'test_voice'])
        assert result.get('tts') == tts
        assert result.get('voice') == 'test_voice'

def test_matrix_voice_with_text():
    
    result = parse_args(['--voice', 'en-US-JennyNeural', '--text', 'Hello World'])
    assert result.get('voice') == 'en-US-JennyNeural'
    assert result.get('text') == 'Hello World'

def test_matrix_voice_full():
    
    result = parse_args(['--tts', 'piper', '--voice', 'en_US-lessac', '--text', 'Test', '--duration', '5'])
    assert result.get('tts') == 'piper'
    assert result.get('voice') == 'en_US-lessac'
    assert result.get('text') == 'Test'
    assert result.get('duration') == '5'

if __name__ == '__main__':
    test_matrix_voice_with_tts()
    test_matrix_voice_with_text()
    test_matrix_voice_full()
    print("OK: test_009_10_matrix")
