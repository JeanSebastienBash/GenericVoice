"""
Test: test_009_08_matrix.py
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

def test_matrix_auto_fix():
    
    result = parse_args(['--auto-fix'])
    assert result.get('auto_fix') == True

def test_matrix_auto_fix_with_system_os():
    
    result = parse_args(['--auto-fix', '--system-os', 'ubuntu'])
    assert result.get('auto_fix') == True
    assert result.get('system_os') == 'ubuntu'

def test_matrix_auto_fix_with_tts():
    
    result = parse_args(['--auto-fix', '--tts', 'piper'])
    assert result.get('auto_fix') == True
    assert result.get('tts') == 'piper'

if __name__ == '__main__':
    test_matrix_auto_fix()
    test_matrix_auto_fix_with_system_os()
    test_matrix_auto_fix_with_tts()
    print("OK: test_009_08_matrix")
