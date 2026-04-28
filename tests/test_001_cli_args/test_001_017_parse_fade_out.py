"""
Test: test_001_017_parse_fade_out.py
Suite: 001 Cli Args
Purpose: Parse Fade Out
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_fade_out_numeric():
    
    result = parse_args(['--fade-out', '150'])
    assert result.get('fade_out') == '150'

def test_parse_fade_out_default_none():
    
    result = parse_args([])
    assert result.get('fade_out') is None

def test_parse_fade_out_small():
    
    result = parse_args(['--fade-out', '20'])
    assert result.get('fade_out') == '20'

def test_parse_fade_out_large():
    
    result = parse_args(['--fade-out', '10000'])
    assert result.get('fade_out') == '10000'

def test_parse_fade_out_with_tts():
    
    result = parse_args(['--tts', 'piper', '--fade-out', '80'])
    assert result.get('fade_out') == '80'
    assert result.get('tts') == 'piper'

def test_parse_fade_out_with_fade_in():
    
    result = parse_args(['--fade-in', '50', '--fade-out', '100'])
    assert result.get('fade_in') == '50'
    assert result.get('fade_out') == '100'

def test_parse_fade_out_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--fade-out', '120', '--normalize'])
    assert result.get('fade_out') == '120'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('normalize') == True

if __name__ == '__main__':
    test_parse_fade_out_numeric()
    test_parse_fade_out_default_none()
    test_parse_fade_out_small()
    test_parse_fade_out_large()
    test_parse_fade_out_with_tts()
    test_parse_fade_out_with_fade_in()
    test_parse_fade_out_full_args()
    print("✓ All test_001_017_parse_fade_out tests passed")
