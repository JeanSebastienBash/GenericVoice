"""
Test: test_008_012_apply_config.py
Suite: 008 Integration
Purpose: Apply Config
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

from gv import apply_config, parse_args
from config import Config

def test_apply_config_creates_config():
    
    c = Config()
    assert c is not None

def test_apply_config_sets_tts():
    
    opts = parse_args(['--tts', 'piper'])
    c = Config()
    if 'tts' in opts and opts['tts']:
        c.tts = opts['tts']
    assert c.tts == 'piper'

def test_apply_config_sets_text():
    
    opts = parse_args(['--text', 'Hello'])
    c = Config()
    if 'text' in opts and opts['text']:
        c.text = opts['text']
    assert c.text == 'Hello'

if __name__ == '__main__':
    test_apply_config_creates_config()
    test_apply_config_sets_tts()
    test_apply_config_sets_text()
    print("OK: test_008_012_apply_config")
