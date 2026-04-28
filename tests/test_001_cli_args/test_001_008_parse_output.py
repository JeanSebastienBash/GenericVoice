"""
Test: test_001_008_parse_output.py
Suite: 001 Cli Args
Purpose: Parse Output
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_output_simple():
    
    result = parse_args(['--output', '/tmp/test.wav'])
    assert result.get('output') == '/tmp/test.wav'

def test_parse_output_default_none():
    
    result = parse_args([])
    assert result.get('output') is None

def test_parse_output_relative():
    
    result = parse_args(['--output', 'output/my_audio.wav'])
    assert result.get('output') == 'output/my_audio.wav'

def test_parse_output_with_spaces():
    
    result = parse_args(['--output', '/path/with spaces/audio.wav'])
    assert 'spaces' in result.get('output', '')

def test_parse_output_with_tts():
    
    result = parse_args(['--tts', 'piper', '--output', '/tmp/result.wav'])
    assert result.get('output') == '/tmp/result.wav'
    assert result.get('tts') == 'piper'

def test_parse_output_extension():
    
    result = parse_args(['--output', '/tmp/audio.mp3'])
    assert result.get('output') == '/tmp/audio.mp3'

def test_parse_output_full_flags():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test', '--output', 'out.wav'])
    assert result.get('output') == 'out.wav'
    assert result.get('tts') == 'piper'
    assert result.get('text') == 'Test'

def test_parse_output_absolute_path():
    
    result = parse_args(['--output', '/home/user/audio/output.wav'])
    assert result.get('output') == '/home/user/audio/output.wav'

def test_parse_output_current_dir():
    
    result = parse_args(['--output', './output.wav'])
    assert result.get('output') == './output.wav'

def test_parse_output_filename_only():
    
    result = parse_args(['--output', 'test_output.wav'])
    assert result.get('output') == 'test_output.wav'

if __name__ == '__main__':
    test_parse_output_simple()
    test_parse_output_default_none()
    test_parse_output_relative()
    test_parse_output_with_spaces()
    test_parse_output_with_tts()
    test_parse_output_extension()
    test_parse_output_full_flags()
    test_parse_output_absolute_path()
    test_parse_output_current_dir()
    test_parse_output_filename_only()
    print("✓ All test_001_008_parse_output tests passed")
