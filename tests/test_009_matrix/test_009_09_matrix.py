"""
Test: test_009_09_matrix.py
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

def test_matrix_list_engines():
    
    result = parse_args(['--list-engines'])
    assert result.get('list_engines') == True

def test_matrix_list_launchers():
    
    result = parse_args(['--list-launchers'])
    assert result.get('list_launchers') == True

def test_matrix_list_both():
    
    result = parse_args(['--list-engines', '--list-launchers'])
    assert result.get('list_engines') == True
    assert result.get('list_launchers') == True

if __name__ == '__main__':
    test_matrix_list_engines()
    test_matrix_list_launchers()
    test_matrix_list_both()
    print("OK: test_009_09_matrix")
