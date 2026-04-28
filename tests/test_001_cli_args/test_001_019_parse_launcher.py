"""
Test: test_001_019_parse_launcher.py
Suite: 001 Cli Args
Purpose: Parse Launcher
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_launcher_genericmenu():
    
    result = parse_args(['--launcher', 'genericmenu'])
    assert result.get('launcher') == 'genericmenu'

def test_parse_launcher_default_none():
    
    result = parse_args([])
    assert result.get('launcher') is None

def test_parse_launcher_with_tts():
    
    result = parse_args(['--tts', 'piper', '--launcher', 'genericmenu'])
    assert result.get('launcher') == 'genericmenu'
    assert result.get('tts') == 'piper'

def test_parse_launcher_custom():
    
    result = parse_args(['--launcher', 'custom_launcher'])
    assert result.get('launcher') == 'custom_launcher'

def test_parse_launcher_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--launcher', 'genericmenu', '--auto-play'])
    assert result.get('launcher') == 'genericmenu'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('auto_play') == True

if __name__ == '__main__':
    test_parse_launcher_genericmenu()
    test_parse_launcher_default_none()
    test_parse_launcher_with_tts()
    test_parse_launcher_custom()
    test_parse_launcher_full_args()
    print("✓ All test_001_019_parse_launcher tests passed")
