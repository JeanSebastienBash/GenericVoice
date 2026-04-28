"""
Test: test_002_007_build_command_melody.py
Suite: 002 Config
Purpose: Build Command Melody
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_melody():
    
    c = Config()
    c.melody_toggle = True
    cmd = c.build_command()
    assert '--melody' in cmd

def test_build_command_melody_off():
    
    c = Config()
    c.melody_toggle = False
    cmd = c.build_command()
    assert '--melody' not in cmd

def test_build_command_melody_with_tts():
    
    c = Config()
    c.tts = 'piper'
    c.melody_toggle = True
    cmd = c.build_command()
    assert '--melody' in cmd
    assert '--tts piper' in cmd

if __name__ == '__main__':
    test_build_command_melody()
    test_build_command_melody_off()
    test_build_command_melody_with_tts()
    print("✓ All test_002_007_build_command_melody tests passed")
