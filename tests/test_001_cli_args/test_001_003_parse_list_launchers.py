"""
Test: test_001_003_parse_list_launchers.py
Suite: 001 Cli Args
Purpose: Parse List Launchers
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_list_launchers():
    
    result = parse_args(['--list-launchers'])
    assert result.get('list_launchers') == True

def test_list_launchers_default_false():
    
    result = parse_args([])
    assert result.get('list_launchers') == False

def test_list_launchers_with_list_engines():
    
    result = parse_args(['--list-launchers', '--list-engines'])
    assert result.get('list_launchers') == True
    assert result.get('list_engines') == True

def test_list_launchers_no_value_needed():
    
    result = parse_args(['--list-launchers'])
    assert 'list_launchers' in result
    assert result['list_launchers'] == True

def test_list_launchers_with_help():
    
    result = parse_args(['--list-launchers', '--help'])
    assert result.get('list_launchers') == True
    assert result.get('help') == True

if __name__ == '__main__':
    test_parse_list_launchers()
    test_list_launchers_default_false()
    test_list_launchers_with_list_engines()
    test_list_launchers_no_value_needed()
    test_list_launchers_with_help()
    print("✓ All test_001_003_parse_list_launchers tests passed")
