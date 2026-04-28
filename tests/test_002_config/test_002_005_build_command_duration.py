"""
Test: test_002_005_build_command_duration.py
Suite: 002 Config
Purpose: Build Command Duration
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_duration():
    c = Config()
    c.duration = '5'
    cmd = c.build_command()
    assert '--duration 5' in cmd
if __name__ == '__main__':
    test_build_command_duration()
