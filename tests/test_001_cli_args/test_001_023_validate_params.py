"""
Test: test_001_023_validate_params.py
Suite: 001 Cli Args
Purpose: Validate Params
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import validate_params

def test_validate_params_empty():
    
    validate_params({})
    assert True

def test_validate_params_player_without_auto_play():
    
    try:
        validate_params({'player': 'cvlc', 'auto_play': False})
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass

def test_validate_params_player_with_auto_play():
    
    validate_params({'player': 'cvlc', 'auto_play': True})
    assert True

def test_validate_wait_finish_without_auto_play():
    
    try:
        validate_params({'wait_finish': True, 'auto_play': False})
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass

def test_validate_wait_finish_with_auto_play():
    
    validate_params({'wait_finish': True, 'auto_play': True})
    assert True

def test_validate_params_auto_play_alone():
    
    validate_params({'auto_play': True})
    assert True

def test_validate_params_player_auto_play_wait_finish():
    
    validate_params({'player': 'cvlc', 'auto_play': True, 'wait_finish': True})
    assert True

def test_validate_params_no_errors():
    
    validate_params({
        'tts': 'piper',
        'text': 'Hello',
        'auto_play': True,
        'player': 'cvlc',
        'wait_finish': True
    })
    assert True

def test_validate_params_multiple_errors():
    
    try:
        validate_params({
            'player': 'cvlc',
            'wait_finish': True,
            'auto_play': False
        })
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass

if __name__ == '__main__':
    test_validate_params_empty()
    test_validate_params_player_without_auto_play()
    test_validate_params_player_with_auto_play()
    test_validate_wait_finish_without_auto_play()
    test_validate_wait_finish_with_auto_play()
    test_validate_params_auto_play_alone()
    test_validate_params_player_auto_play_wait_finish()
    test_validate_params_no_errors()
    test_validate_params_multiple_errors()
    print("✓ All test_001_023_validate_params tests passed")
