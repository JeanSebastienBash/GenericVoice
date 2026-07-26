"""
Test: test_002_013_build_command_fade.py
Suite: 002 Config
Purpose: Build Command Fade
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_fade_in():
    
    c = Config()
    c.audio.fade_in_ms = 100
    cmd = c.build_command()
    assert cmd[cmd.index('--fade-in') + 1] == '100'

def test_build_command_fade_out():
    
    c = Config()
    c.audio.fade_out_ms = 150
    cmd = c.build_command()
    assert cmd[cmd.index('--fade-out') + 1] == '150'

def test_build_command_fade_both():
    
    c = Config()
    c.audio.fade_in_ms = 75
    c.audio.fade_out_ms = 120
    cmd = c.build_command()
    assert cmd[cmd.index('--fade-in') + 1] == '75'
    assert cmd[cmd.index('--fade-out') + 1] == '120'

def test_build_command_fade_default():
    
    c = Config()
    cmd = c.build_command()
    assert '--fade-in' not in cmd
    assert '--fade-out' not in cmd

if __name__ == '__main__':
    test_build_command_fade_in()
    test_build_command_fade_out()
    test_build_command_fade_both()
    test_build_command_fade_default()
    print("✓ All test_002_013_build_command_fade tests passed")
