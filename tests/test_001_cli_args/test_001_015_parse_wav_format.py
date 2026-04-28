"""
Test: test_001_015_parse_wav_format.py
Suite: 001 Cli Args
Purpose: Parse Wav Format
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_wav_format_16bit():
    
    result = parse_args(['--wav-format', '16-bit'])
    assert result.get('wav_format') == '16-bit'

def test_parse_wav_format_32bit():
    
    result = parse_args(['--wav-format', '32-bit'])
    assert result.get('wav_format') == '32-bit'

def test_parse_wav_format_default_none():
    
    result = parse_args([])
    assert result.get('wav_format') is None

def test_parse_wav_format_with_tts():
    
    result = parse_args(['--tts', 'piper', '--wav-format', '32-bit'])
    assert result.get('wav_format') == '32-bit'
    assert result.get('tts') == 'piper'

def test_parse_wav_format_with_normalize():
    
    result = parse_args(['--wav-format', '32-bit', '--normalize'])
    assert result.get('wav_format') == '32-bit'
    assert result.get('normalize') == True

def test_parse_wav_format_custom():
    
    result = parse_args(['--wav-format', 'custom'])
    assert result.get('wav_format') == 'custom'

def test_parse_wav_format_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--wav-format', '16-bit', '--normalize'])
    assert result.get('wav_format') == '16-bit'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('normalize') == True

if __name__ == '__main__':
    test_parse_wav_format_16bit()
    test_parse_wav_format_32bit()
    test_parse_wav_format_default_none()
    test_parse_wav_format_with_tts()
    test_parse_wav_format_with_normalize()
    test_parse_wav_format_custom()
    test_parse_wav_format_full_args()
    print("✓ All test_001_015_parse_wav_format tests passed")
