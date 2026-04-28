"""
Test: test_002_014_build_command_wait_finish.py
Suite: 002 Config
Purpose: Build Command Wait Finish
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_wait_finish():
    
    c = Config()
    c.auto_play = True
    c.audio.wait_finish = True
    cmd = c.build_command()
    assert '--wait-finish' in cmd

def test_build_command_wait_finish_without_auto_play():
    
    c = Config()
    c.auto_play = False
    c.audio.wait_finish = True
    cmd = c.build_command()
    assert '--wait-finish' not in cmd

def test_build_command_wait_finish_off():
    
    c = Config()
    cmd = c.build_command()
    assert '--wait-finish' not in cmd

def test_build_command_wait_finish_with_player():
    
    c = Config()
    c.auto_play = True
    c.player = 'cvlc'
    c.audio.wait_finish = True
    cmd = c.build_command()
    assert '--wait-finish' in cmd
    assert '--player cvlc' in cmd

if __name__ == '__main__':
    test_build_command_wait_finish()
    test_build_command_wait_finish_without_auto_play()
    test_build_command_wait_finish_off()
    test_build_command_wait_finish_with_player()
    print("✓ All test_002_014_build_command_wait_finish tests passed")
