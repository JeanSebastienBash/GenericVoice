"""
Test: test_001_018_parse_system_os.py
Suite: 001 Cli Args
Purpose: Parse System Os
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_system_os_ubuntu():
    
    result = parse_args(['--system-os', 'ubuntu'])
    assert result.get('system_os') == 'ubuntu'

def test_parse_system_os_linux():
    
    result = parse_args(['--system-os', 'linux'])
    assert result.get('system_os') == 'linux'

def test_parse_system_os_windows():
    
    result = parse_args(['--system-os', 'windows'])
    assert result.get('system_os') == 'windows'

def test_parse_system_os_darwin():
    
    result = parse_args(['--system-os', 'darwin'])
    assert result.get('system_os') == 'darwin'

def test_parse_system_os_default_none():
    
    result = parse_args([])
    assert result.get('system_os') is None

def test_parse_system_os_with_tts():
    
    result = parse_args(['--tts', 'piper', '--system-os', 'ubuntu'])
    assert result.get('system_os') == 'ubuntu'
    assert result.get('tts') == 'piper'

def test_parse_system_os_custom():
    
    result = parse_args(['--system-os', 'custom_os'])
    assert result.get('system_os') == 'custom_os'

def test_parse_system_os_full_args():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--system-os', 'linux'])
    assert result.get('system_os') == 'linux'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'

if __name__ == '__main__':
    test_parse_system_os_ubuntu()
    test_parse_system_os_linux()
    test_parse_system_os_windows()
    test_parse_system_os_darwin()
    test_parse_system_os_default_none()
    test_parse_system_os_with_tts()
    test_parse_system_os_custom()
    test_parse_system_os_full_args()
    print("✓ All test_001_018_parse_system_os tests passed")
