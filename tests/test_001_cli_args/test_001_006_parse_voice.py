"""
Test: test_001_006_parse_voice.py
Suite: 001 Cli Args
Purpose: Parse Voice
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_voice_simple():
    
    result = parse_args(['--voice', 'en_US-ljspeech-high'])
    assert result.get('voice') == 'en_US-ljspeech-high'

def test_parse_voice_default_none():
    
    result = parse_args([])
    assert result.get('voice') is None

def test_parse_voice_with_tts():
    
    result = parse_args(['--tts', 'piper', '--voice', 'fr_FR-siwis-medium'])
    assert result.get('voice') == 'fr_FR-siwis-medium'
    assert result.get('tts') == 'piper'

def test_parse_voice_edge_voice():
    
    result = parse_args(['--tts', 'edge', '--voice', 'en-US-JennyNeural'])
    assert result.get('voice') == 'en-US-JennyNeural'

def test_parse_voice_espeak_variant():
    
    result = parse_args(['--tts', 'espeak', '--voice', 'mb-fr1'])
    assert result.get('voice') == 'mb-fr1'

def test_parse_voice_with_text():
    
    result = parse_args(['--tts', 'piper', '--voice', 'en_US-lessac-high', '--text', 'Hello'])
    assert result.get('voice') == 'en_US-lessac-high'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello'

def test_parse_voice_short():
    
    result = parse_args(['--voice', 'default'])
    assert result.get('voice') == 'default'

def test_parse_voice_with_hyphens():
    
    result = parse_args(['--voice', 'en-US-AriaNeural'])
    assert result.get('voice') == 'en-US-AriaNeural'

def test_parse_voice_multiple_args():
    
    result = parse_args(['--tts', 'piper', '--voice', 'test_voice', '--text', 'Hi', '--output', 'out.wav'])
    assert result.get('voice') == 'test_voice'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hi'
    assert result.get('output') == 'out.wav'

if __name__ == '__main__':
    test_parse_voice_simple()
    test_parse_voice_default_none()
    test_parse_voice_with_tts()
    test_parse_voice_edge_voice()
    test_parse_voice_espeak_variant()
    test_parse_voice_with_text()
    test_parse_voice_short()
    test_parse_voice_with_hyphens()
    test_parse_voice_multiple_args()
    print("✓ All test_001_006_parse_voice tests passed")
