"""
Test: test_001_020_parse_auto_fix.py
Suite: 001 Cli Args
Purpose: Parse Auto Fix
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_auto_fix():
    
    result = parse_args(['--auto-fix'])
    assert result.get('auto_fix') == True

def test_auto_fix_default_false():
    
    result = parse_args([])
    assert result.get('auto_fix') == False

def test_auto_fix_with_tts():
    
    result = parse_args(['--tts', 'piper', '--auto-fix'])
    assert result.get('auto_fix') == True
    assert result.get('tts') == 'piper'

def test_auto_fix_no_value_needed():
    
    result = parse_args(['--auto-fix'])
    assert 'auto_fix' in result
    assert result['auto_fix'] == True

def test_auto_fix_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--auto-fix'])
    assert result.get('auto_fix') == True
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'

def test_auto_fix_with_system_os():
    
    result = parse_args(['--auto-fix', '--system-os', 'ubuntu'])
    assert result.get('auto_fix') == True
    assert result.get('system_os') == 'ubuntu'

if __name__ == '__main__':
    test_parse_auto_fix()
    test_auto_fix_default_false()
    test_auto_fix_with_tts()
    test_auto_fix_no_value_needed()
    test_auto_fix_full_args()
    test_auto_fix_with_system_os()
    print("✓ All test_001_020_parse_auto_fix tests passed")
