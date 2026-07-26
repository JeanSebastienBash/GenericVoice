"""
Test: test_002_001_build_command_basic.py
Suite: 002 Config
Purpose: Build Command Basic
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_basic():
    c = Config()
    c.tts = 'espeak'
    c.mode = 'generate'
    cmd = c.build_command()
    assert isinstance(cmd, list)
    assert cmd[cmd.index('--tts') + 1] == 'espeak'

def test_build_command_default_tts():
    c = Config()
    cmd = c.build_command()
    assert cmd[cmd.index('--tts') + 1] == 'piper'

def test_build_command_contains_python():
    c = Config()
    cmd = c.build_command()
    assert cmd[0] == 'python3'
    assert 'gv.py' in cmd[1]

def test_build_command_empty_config():
    c = Config()
    cmd = c.build_command()
    assert '--mode' not in cmd
    assert '--tts' in cmd

def test_build_command_tts_edge():
    c = Config()
    c.tts = 'edge'
    cmd = c.build_command()
    assert cmd[cmd.index('--tts') + 1] == 'edge'

def test_build_command_format():
    c = Config()
    c.tts = 'piper'
    cmd = c.build_command()
    assert cmd[0] == 'python3'
    assert '--tts' in cmd

if __name__ == '__main__':
    test_build_command_basic()
    test_build_command_default_tts()
    test_build_command_contains_python()
    test_build_command_empty_config()
    test_build_command_tts_edge()
    test_build_command_format()
    print("✓ All test_002_001_build_command_basic tests passed")
