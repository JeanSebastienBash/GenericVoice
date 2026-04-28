"""
Test: test_009_17_matrix.py
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

def test_matrix_help_alone():
    
    result = parse_args(['--help'])
    assert result.get('help') == True

def test_matrix_help_with_other():
    
    result = parse_args(['--help', '--tts', 'piper', '--text', 'Test'])
    assert result.get('help') == True

def test_matrix_list_flags():
    
    result = parse_args(['--list-engines'])
    assert result.get('list_engines') == True
    
    result = parse_args(['--list-launchers'])
    assert result.get('list_launchers') == True

if __name__ == '__main__':
    test_matrix_help_alone()
    test_matrix_help_with_other()
    test_matrix_list_flags()
    print("OK: test_009_17_matrix")
