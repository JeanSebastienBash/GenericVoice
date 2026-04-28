"""
Test: test_001_021_parse_multiple_args.py
Suite: 001 Cli Args
Purpose: Parse Multiple Args
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_multiple_basic():
    
    result = parse_args(['--tts', 'piper', '--text', 'Hello', '--voice', 'en_US-lessac'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello'
    assert result.get('voice') == 'en_US-lessac'

def test_parse_multiple_flags():
    
    result = parse_args(['--melody', '--normalize', '--auto-play'])
    assert result.get('melody') == True
    assert result.get('normalize') == True
    assert result.get('auto_play') == True

def test_parse_full_command():
    
    result = parse_args([
        '--tts', 'piper',
        '--text', 'Hello World',
        '--voice', 'en_US-lessac-high',
        '--output', '/tmp/test.wav',
        '--melody',
        '--auto-play',
        '--player', 'cvlc'
    ])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello World'
    assert result.get('voice') == 'en_US-lessac-high'
    assert result.get('output') == '/tmp/test.wav'
    assert result.get('melody') == True
    assert result.get('auto_play') == True
    assert result.get('player') == 'cvlc'

def test_parse_all_audio_flags():
    
    result = parse_args([
        '--normalize',
        '--wav-format', '32-bit',
        '--fade-in', '100',
        '--fade-out', '150'
    ])
    assert result.get('normalize') == True
    assert result.get('wav_format') == '32-bit'
    assert result.get('fade_in') == '100'
    assert result.get('fade_out') == '150'

def test_parse_all_list_flags():
    
    result = parse_args(['--help', '--list-engines', '--list-launchers'])
    assert result.get('help') == True
    assert result.get('list_engines') == True
    assert result.get('list_launchers') == True

def test_parse_mixed_args():
    
    result = parse_args([
        '--tts', 'edge',
        '--auto-play',
        '--text', 'Test message',
        '--normalize'
    ])
    assert result.get('tts') == 'edge'
    assert result.get('auto_play') == True
    assert result.get('text') == 'Test message'
    assert result.get('normalize') == True

def test_parse_all_boolean_flags():
    
    result = parse_args([
        '--melody',
        '--auto-play',
        '--wait-finish',
        '--normalize',
        '--auto-fix'
    ])
    assert result.get('melody') == True
    assert result.get('auto_play') == True
    assert result.get('wait_finish') == True
    assert result.get('normalize') == True
    assert result.get('auto_fix') == True

def test_parse_complex_command():
    
    result = parse_args([
        '--tts', 'piper',
        '--text', 'Complex test',
        '--voice', 'fr_FR-siwis-medium',
        '--duration', '10',
        '--output', 'output/test.wav',
        '--melody',
        '--voice-effect', 'echo',
        '--player', 'cvlc',
        '--auto-play',
        '--normalize',
        '--wav-format', '16-bit',
        '--fade-in', '50',
        '--fade-out', '80'
    ])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Complex test'
    assert result.get('voice') == 'fr_FR-siwis-medium'
    assert result.get('duration') == '10'
    assert result.get('output') == 'output/test.wav'
    assert result.get('melody') == True
    assert result.get('voice_effect') == 'echo'
    assert result.get('player') == 'cvlc'
    assert result.get('auto_play') == True
    assert result.get('normalize') == True
    assert result.get('wav_format') == '16-bit'
    assert result.get('fade_in') == '50'
    assert result.get('fade_out') == '80'

if __name__ == '__main__':
    test_parse_multiple_basic()
    test_parse_multiple_flags()
    test_parse_full_command()
    test_parse_all_audio_flags()
    test_parse_all_list_flags()
    test_parse_mixed_args()
    test_parse_all_boolean_flags()
    test_parse_complex_command()
    print("✓ All test_001_021_parse_multiple_args tests passed")
