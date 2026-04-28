"""
Test: test_001_005_parse_text.py
Suite: 001 Cli Args
Purpose: Parse Text
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gv import parse_args

def test_parse_text_simple():
    
    result = parse_args(['--text', 'Hello'])
    assert result.get('text') == 'Hello'

def test_parse_text_with_spaces():
    
    result = parse_args(['--text', 'Hello World'])
    assert result.get('text') == 'Hello World'

def test_parse_text_with_special_chars():
    
    result = parse_args(['--text', 'Hello! How are you?'])
    assert result.get('text') == 'Hello! How are you?'

def test_parse_text_with_accents():
    
    result = parse_args(['--text', 'Rencontré élément àççents'])
    assert 'Rencontré' in result.get('text', '')

def test_parse_text_default_none():
    
    result = parse_args([])
    assert result.get('text') is None

def test_parse_text_with_tts():
    
    result = parse_args(['--tts', 'piper', '--text', 'Test message'])
    assert result.get('text') == 'Test message'
    assert result.get('tts') == 'piper'

def test_parse_text_empty():
    
    result = parse_args(['--text', ''])
    assert result.get('text') == ''

def test_parse_text_long():
    
    long_text = "This is a very long text message that contains multiple words and sentences. " * 5
    result = parse_args(['--text', long_text])
    assert result.get('text') == long_text

def test_parse_text_unicode():
    
    result = parse_args(['--text', '日本語テキスト'])
    assert result.get('text') == '日本語テキスト'

def test_parse_text_numbers():
    
    result = parse_args(['--text', 'Testing 123 numbers'])
    assert result.get('text') == 'Testing 123 numbers'

if __name__ == '__main__':
    test_parse_text_simple()
    test_parse_text_with_spaces()
    test_parse_text_with_special_chars()
    test_parse_text_with_accents()
    test_parse_text_default_none()
    test_parse_text_with_tts()
    test_parse_text_empty()
    test_parse_text_long()
    test_parse_text_unicode()
    test_parse_text_numbers()
    print("✓ All test_001_005_parse_text tests passed")
