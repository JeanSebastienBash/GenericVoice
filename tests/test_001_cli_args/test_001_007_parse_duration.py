"""
Test: test_001_007_parse_duration.py
Suite: 001 Cli Args
Purpose: Parse Duration
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_duration_numeric():
    
    result = parse_args(['--duration', '10'])
    assert result.get('duration') == '10'

def test_parse_duration_auto():
    
    result = parse_args(['--duration', 'auto'])
    assert result.get('duration') == 'auto'

def test_parse_duration_float():
    
    result = parse_args(['--duration', '5.5'])
    assert result.get('duration') == '5.5'

def test_parse_duration_default_none():
    
    result = parse_args([])
    assert result.get('duration') is None

def test_parse_duration_with_tts():
    
    result = parse_args(['--tts', 'piper', '--duration', '15'])
    assert result.get('duration') == '15'
    assert result.get('tts') == 'piper'

def test_parse_duration_large():
    
    result = parse_args(['--duration', '120'])
    assert result.get('duration') == '120'

def test_parse_duration_zero():
    
    result = parse_args(['--duration', '0'])
    assert result.get('duration') == '0'

def test_parse_duration_one():
    
    result = parse_args(['--duration', '1'])
    assert result.get('duration') == '1'

def test_parse_duration_with_text():
    
    result = parse_args(['--duration', '30', '--text', 'Hello'])
    assert result.get('duration') == '30'
    assert result.get('text') == 'Hello'

if __name__ == '__main__':
    test_parse_duration_numeric()
    test_parse_duration_auto()
    test_parse_duration_float()
    test_parse_duration_default_none()
    test_parse_duration_with_tts()
    test_parse_duration_large()
    test_parse_duration_zero()
    test_parse_duration_one()
    test_parse_duration_with_text()
    print("✓ All test_001_007_parse_duration tests passed")
