"""
Test: test_009_03_matrix.py
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

def test_matrix_melody_voice_effect():
    
    result = parse_args(['--melody', '--voice-effect', 'echo'])
    assert result.get('melody') == True
    assert result.get('voice_effect') == 'echo'

def test_matrix_melody_full():
    
    result = parse_args(['--melody', '--voice-effect', 'reverb', '--normalize'])
    assert result.get('melody') == True
    assert result.get('voice_effect') == 'reverb'
    assert result.get('normalize') == True

def test_matrix_voice_effects():
    
    for effect in ['echo', 'vibrato', 'reverb', 'none']:
        result = parse_args(['--voice-effect', effect])
        assert result.get('voice_effect') == effect

if __name__ == '__main__':
    test_matrix_melody_voice_effect()
    test_matrix_melody_full()
    test_matrix_voice_effects()
    print("OK: test_009_03_matrix")
