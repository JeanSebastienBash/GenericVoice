"""
Test: test_009_19_matrix.py
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

def test_matrix_simple_tts():
    
    result = parse_args(['--tts', 'piper', '--text', 'Hello World'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello World'

def test_matrix_production_workflow():
    
    result = parse_args([
        '--tts', 'piper',
        '--text', 'Production test',
        '--voice', 'en_US-lessac-high',
        '--output', '/tmp/production.wav',
        '--normalize',
        '--wav-format', '16-bit'
    ])
    assert result.get('tts') == 'piper'
    assert result.get('normalize') == True
    assert result.get('wav_format') == '16-bit'

def test_matrix_development_workflow():
    
    result = parse_args([
        '--tts', 'espeak',
        '--text', 'Dev test',
        '--system-os', 'ubuntu',
        '--auto-play'
    ])
    assert result.get('tts') == 'espeak'
    assert result.get('system_os') == 'ubuntu'
    assert result.get('auto_play') == True

def test_matrix_full_features():
    
    result = parse_args([
        '--tts', 'piper',
        '--text', 'Full features test',
        '--voice', 'en_US-lessac',
        '--duration', '10',
        '--output', 'full.wav',
        '--melody',
        '--voice-effect', 'echo',
        '--normalize',
        '--auto-play',
        '--player', 'cvlc',
        '--wait-finish'
    ])
    assert result.get('tts') == 'piper'
    assert result.get('melody') == True
    assert result.get('normalize') == True
    assert result.get('auto_play') == True
    assert result.get('wait_finish') == True

if __name__ == '__main__':
    test_matrix_simple_tts()
    test_matrix_production_workflow()
    test_matrix_development_workflow()
    test_matrix_full_features()
    print("OK: test_009_19_matrix")
