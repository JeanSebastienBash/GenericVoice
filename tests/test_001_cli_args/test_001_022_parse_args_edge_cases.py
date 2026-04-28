"""
Test: test_001_022_parse_args_edge_cases.py
Suite: 001 Cli Args
Purpose: Parse Args Edge Cases
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_empty_args():
    
    result = parse_args([])
    assert isinstance(result, dict)
    assert len(result) > 0

def test_parse_args_dict_keys():
    
    result = parse_args([])
    expected_keys = ['tts', 'text', 'voice', 'duration', 'output', 'melody',
                     'voice_effect', 'system_os', 'launcher', 'auto_fix',
                     'player', 'auto_play', 'wait_finish', 'normalize',
                     'wav_format', 'fade_in', 'fade_out',
                     'list_engines', 'list_launchers', 'help']
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"

def test_parse_args_default_values():
    
    result = parse_args([])
    assert result.get('melody') == False
    assert result.get('auto_play') == False
    assert result.get('wait_finish') == False
    assert result.get('normalize') == False
    assert result.get('auto_fix') == False
    assert result.get('list_engines') == False
    assert result.get('list_launchers') == False
    assert result.get('help') == False

def test_parse_args_none_defaults():
    
    result = parse_args([])
    assert result.get('tts') is None
    assert result.get('text') is None
    assert result.get('voice') is None
    assert result.get('duration') is None
    assert result.get('output') is None
    assert result.get('voice_effect') is None
    assert result.get('system_os') is None
    assert result.get('launcher') is None
    assert result.get('player') is None
    assert result.get('wav_format') is None
    assert result.get('fade_in') is None
    assert result.get('fade_out') is None

def test_parse_unknown_option_handling():
    
    try:
        result = parse_args(['--unknown-option'])
        assert False, "Should have raised SystemExit"
    except SystemExit:
        pass

def test_parse_case_sensitivity():
    
    result = parse_args(['--tts', 'Piper'])
    assert result.get('tts') == 'Piper'

def test_parse_whitespace_in_values():
    
    result = parse_args(['--text', 'Multiple   spaces   here'])
    assert result.get('text') == 'Multiple   spaces   here'

def test_parse_empty_value_handling():
    
    result = parse_args(['--text', ''])
    assert result.get('text') == ''

def test_parse_result_type():
    
    result = parse_args(['--tts', 'piper'])
    assert isinstance(result, dict)

if __name__ == '__main__':
    test_parse_empty_args()
    test_parse_args_dict_keys()
    test_parse_args_default_values()
    test_parse_args_none_defaults()
    test_parse_unknown_option_handling()
    test_parse_case_sensitivity()
    test_parse_whitespace_in_values()
    test_parse_empty_value_handling()
    test_parse_result_type()
    print("✓ All test_001_022_parse_args_edge_cases tests passed")
