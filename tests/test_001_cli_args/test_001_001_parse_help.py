"""
Test: test_001_001_parse_help.py
Suite: 001 Cli Args
Purpose: Parse Help
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_help_short():
    
    result = parse_args(['-h'])
    assert result.get('help') == True, "Expected help=True when -h is passed"
    assert isinstance(result, dict), "Result should be a dictionary"

def test_parse_help_long():
    
    result = parse_args(['--help'])
    assert result.get('help') == True, "Expected help=True when --help is passed"

def test_help_default_false():
    
    result = parse_args([])
    assert result.get('help') == False, "Expected help=False by default"

def test_help_only_flag():
    
    result = parse_args(['--help'])
    assert result.get('tts') is None
    assert result.get('text') is None
    assert result.get('voice') is None
    assert result.get('help') == True

if __name__ == '__main__':
    test_parse_help_short()
    test_parse_help_long()
    test_help_default_false()
    test_help_only_flag()
    print("✓ All test_001_001_parse_help tests passed")
