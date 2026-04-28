"""
Test: test_001_016_parse_fade_in.py
Suite: 001 Cli Args
Purpose: Parse Fade In
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_fade_in_numeric():
    
    result = parse_args(['--fade-in', '100'])
    assert result.get('fade_in') == '100'

def test_parse_fade_in_default_none():
    
    result = parse_args([])
    assert result.get('fade_in') is None

def test_parse_fade_in_small():
    
    result = parse_args(['--fade-in', '10'])
    assert result.get('fade_in') == '10'

def test_parse_fade_in_large():
    
    result = parse_args(['--fade-in', '5000'])
    assert result.get('fade_in') == '5000'

def test_parse_fade_in_with_tts():
    
    result = parse_args(['--tts', 'piper', '--fade-in', '50'])
    assert result.get('fade_in') == '50'
    assert result.get('tts') == 'piper'

def test_parse_fade_in_with_fade_out():
    
    result = parse_args(['--fade-in', '100', '--fade-out', '200'])
    assert result.get('fade_in') == '100'
    assert result.get('fade_out') == '200'

def test_parse_fade_in_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--fade-in', '75', '--normalize'])
    assert result.get('fade_in') == '75'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('normalize') == True

if __name__ == '__main__':
    test_parse_fade_in_numeric()
    test_parse_fade_in_default_none()
    test_parse_fade_in_small()
    test_parse_fade_in_large()
    test_parse_fade_in_with_tts()
    test_parse_fade_in_with_fade_out()
    test_parse_fade_in_full_args()
    print("✓ All test_001_016_parse_fade_in tests passed")
