"""
Test: test_002_012_build_command_normalize.py
Suite: 002 Config
Purpose: Build Command Normalize
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_normalize():
    
    c = Config()
    c.audio.normalize = True
    cmd = c.build_command()
    assert '--normalize' in cmd

def test_build_command_normalize_off():
    
    c = Config()
    cmd = c.build_command()
    assert '--normalize' not in cmd

def test_build_command_normalize_with_tts():
    
    c = Config()
    c.tts = 'piper'
    c.audio.normalize = True
    cmd = c.build_command()
    assert '--normalize' in cmd
    assert '--tts piper' in cmd

if __name__ == '__main__':
    test_build_command_normalize()
    test_build_command_normalize_off()
    test_build_command_normalize_with_tts()
    print("✓ All test_002_012_build_command_normalize tests passed")
