"""
Test: test_009_14_matrix.py
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

def test_matrix_complete_piper():
    
    result = parse_args([
        '--tts', 'piper',
        '--text', 'Hello World',
        '--voice', 'en_US-lessac',
        '--output', 'output.wav',
        '--auto-play',
        '--player', 'vlc'
    ])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello World'
    assert result.get('voice') == 'en_US-lessac'
    assert result.get('output') == 'output.wav'
    assert result.get('auto_play') == True
    assert result.get('player') == 'vlc'

def test_matrix_complete_edge():
    
    result = parse_args([
        '--tts', 'edge',
        '--text', 'Test message',
        '--voice', 'en-US-JennyNeural',
        '--normalize',
        '--wav-format', '32-bit'
    ])
    assert result.get('tts') == 'edge'
    assert result.get('text') == 'Test message'
    assert result.get('voice') == 'en-US-JennyNeural'
    assert result.get('normalize') == True
    assert result.get('wav_format') == '32-bit'

def test_matrix_complete_melody():
    
    result = parse_args([
        '--tts', 'piper',
        '--text', 'Music test',
        '--melody',
        '--voice-effect', 'reverb',
        '--normalize'
    ])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Music test'
    assert result.get('melody') == True
    assert result.get('voice_effect') == 'reverb'
    assert result.get('normalize') == True

if __name__ == '__main__':
    test_matrix_complete_piper()
    test_matrix_complete_edge()
    test_matrix_complete_melody()
    print("OK: test_009_14_matrix")
