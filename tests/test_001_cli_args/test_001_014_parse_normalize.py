"""
Test: test_001_014_parse_normalize.py
Suite: 001 Cli Args
Purpose: Parse Normalize
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_normalize():
    
    result = parse_args(['--normalize'])
    assert result.get('normalize') == True

def test_normalize_default_false():
    
    result = parse_args([])
    assert result.get('normalize') == False

def test_normalize_with_tts():
    
    result = parse_args(['--tts', 'piper', '--normalize'])
    assert result.get('normalize') == True
    assert result.get('tts') == 'piper'

def test_normalize_with_wav_format():
    
    result = parse_args(['--normalize', '--wav-format', '32-bit'])
    assert result.get('normalize') == True
    assert result.get('wav_format') == '32-bit'

def test_normalize_no_value_needed():
    
    result = parse_args(['--normalize'])
    assert 'normalize' in result
    assert result['normalize'] == True

def test_normalize_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--normalize', '--auto-play'])
    assert result.get('normalize') == True
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('auto_play') == True

if __name__ == '__main__':
    test_parse_normalize()
    test_normalize_default_false()
    test_normalize_with_tts()
    test_normalize_with_wav_format()
    test_normalize_no_value_needed()
    test_normalize_full_args()
    print("✓ All test_001_014_parse_normalize tests passed")
