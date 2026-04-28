"""
Test: test_001_002_parse_list_engines.py
Suite: 001 Cli Args
Purpose: Parse List Engines
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_list_engines():
    
    result = parse_args(['--list-engines'])
    assert result.get('list_engines') == True

def test_list_engines_default_false():
    
    result = parse_args([])
    assert result.get('list_engines') == False

def test_list_engines_with_other_flags():
    
    result = parse_args(['--list-engines', '--help'])
    assert result.get('list_engines') == True
    assert result.get('help') == True

def test_list_engines_no_value_needed():
    
    result = parse_args(['--list-engines'])
    assert 'list_engines' in result
    assert result['list_engines'] == True

def test_list_engines_alone():
    
    result = parse_args(['--list-engines'])
    assert len([k for k,v in result.items() if v]) == 1
    assert result['list_engines'] == True

if __name__ == '__main__':
    test_parse_list_engines()
    test_list_engines_default_false()
    test_list_engines_with_other_flags()
    test_list_engines_no_value_needed()
    test_list_engines_alone()
    print("✓ All test_001_002_parse_list_engines tests passed")
