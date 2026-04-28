"""
Test: test_002_010_build_command_auto_play.py
Suite: 002 Config
Purpose: Build Command Auto Play
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_auto_play():
    c = Config()
    c.auto_play = True
    cmd = c.build_command()
    assert '--auto-play' in cmd
if __name__ == '__main__':
    test_build_command_auto_play()
