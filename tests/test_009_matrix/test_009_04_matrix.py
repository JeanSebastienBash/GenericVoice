"""
Test: test_009_04_matrix.py
Suite: 009 Matrix
Purpose: Matrix
Context: Unit test in test_009_matrix/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: Complete system
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from gv import parse_args

def test_matrix_system_os_values():
    
    for os_val in ['ubuntu', 'linux', 'windows', 'darwin']:
        result = parse_args(['--system-os', os_val])
        assert result.get('system_os') == os_val

def test_matrix_system_os_with_tts():
    
    result = parse_args(['--system-os', 'ubuntu', '--tts', 'piper'])
    assert result.get('system_os') == 'ubuntu'
    assert result.get('tts') == 'piper'

def test_matrix_system_os_with_all():
    
    result = parse_args(['--system-os', 'linux', '--tts', 'piper', '--text', 'Test', '--auto-play'])
    assert result.get('system_os') == 'linux'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'
    assert result.get('auto_play') == True

if __name__ == '__main__':
    test_matrix_system_os_values()
    test_matrix_system_os_with_tts()
    test_matrix_system_os_with_all()
    print("OK: test_009_04_matrix")
