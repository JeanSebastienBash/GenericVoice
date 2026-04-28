"""
Test: test_001_004_parse_tts.py
Suite: 001 Cli Args
Purpose: Parse Tts
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_tts_piper():
    
    result = parse_args(['--tts', 'piper'])
    assert result.get('tts') == 'piper'

def test_parse_tts_edge():
    
    result = parse_args(['--tts', 'edge'])
    assert result.get('tts') == 'edge'

def test_parse_tts_espeak():
    
    result = parse_args(['--tts', 'espeak'])
    assert result.get('tts') == 'espeak'

def test_parse_tts_default_none():
    
    result = parse_args([])
    assert result.get('tts') is None

def test_parse_tts_custom_value():
    
    result = parse_args(['--tts', 'custom_engine'])
    assert result.get('tts') == 'custom_engine'

def test_parse_tts_with_text():
    
    result = parse_args(['--tts', 'piper', '--text', 'Hello'])
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Hello'

def test_parse_tts_case_sensitive():
    
    result = parse_args(['--tts', 'Piper'])
    assert result.get('tts') == 'Piper'

def test_parse_tts_with_voice():
    
    result = parse_args(['--tts', 'piper', '--voice', 'en_US-lessac'])
    assert result.get('tts') == 'piper'
    assert result.get('voice') == 'en_US-lessac'

if __name__ == '__main__':
    test_parse_tts_piper()
    test_parse_tts_edge()
    test_parse_tts_espeak()
    test_parse_tts_default_none()
    test_parse_tts_custom_value()
    test_parse_tts_with_text()
    test_parse_tts_case_sensitive()
    test_parse_tts_with_voice()
    print("✓ All test_001_004_parse_tts tests passed")
