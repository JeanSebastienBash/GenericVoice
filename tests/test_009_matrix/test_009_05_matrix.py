"""
Test: test_009_05_matrix.py
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

def test_matrix_output_with_tts():
    
    result = parse_args(['--tts', 'piper', '--output', '/tmp/test.wav'])
    assert result.get('tts') == 'piper'
    assert result.get('output') == '/tmp/test.wav'

def test_matrix_output_all():
    
    result = parse_args(['--tts', 'edge', '--text', 'Hello', '--voice', 'en-US', '--output', 'output.wav'])
    assert result.get('tts') == 'edge'
    assert result.get('text') == 'Hello'
    assert result.get('voice') == 'en-US'
    assert result.get('output') == 'output.wav'

def test_matrix_output_paths():
    
    for path in ['/tmp/test.wav', 'output.wav', './audio.wav']:
        result = parse_args(['--output', path])
        assert result.get('output') == path

if __name__ == '__main__':
    test_matrix_output_with_tts()
    test_matrix_output_all()
    test_matrix_output_paths()
    print("OK: test_009_05_matrix")
