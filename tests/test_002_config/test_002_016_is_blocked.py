"""
Test: test_002_016_is_blocked.py
Suite: 002 Config
Purpose: Is Blocked
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_is_blocked_generate():
    
    c = Config()
    c.mode = 'generate'
    assert c.is_blocked() == False

def test_is_blocked_list_voices():
    
    c = Config()
    c.mode = 'list-voices'
    assert c.is_blocked() == True

def test_is_blocked_list_languages():
    
    c = Config()
    c.mode = 'list-languages'
    assert c.is_blocked() == True

def test_is_blocked_demo():
    
    c = Config()
    c.mode = 'demo'
    assert c.is_blocked() == True

def test_is_blocked_demo_lang():
    
    c = Config()
    c.mode = 'demo-lang'
    assert c.is_blocked() == True

def test_is_blocked_default():
    
    c = Config()
    assert c.is_blocked() == False

def test_is_blocked_after_mode_change():
    
    c = Config()
    assert c.is_blocked() == False
    c.mode = 'list-voices'
    assert c.is_blocked() == True
    c.mode = 'generate'
    assert c.is_blocked() == False

def test_is_blocked_multiple_changes():
    
    c = Config()
    modes = ['generate', 'list-voices', 'generate', 'demo', 'generate']
    expected = [False, True, False, True, False]
    for mode, exp in zip(modes, expected):
        c.mode = mode
        assert c.is_blocked() == exp, f"Failed for mode {mode}"

if __name__ == '__main__':
    test_is_blocked_generate()
    test_is_blocked_list_voices()
    test_is_blocked_list_languages()
    test_is_blocked_demo()
    test_is_blocked_demo_lang()
    test_is_blocked_default()
    test_is_blocked_after_mode_change()
    test_is_blocked_multiple_changes()
    print("✓ All test_002_016_is_blocked tests passed")
