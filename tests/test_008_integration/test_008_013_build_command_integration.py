"""
Test: test_008_013_build_command_integration.py
Suite: 008 Integration
Purpose: Build Command Integration
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: All lib/ modules
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_integration():
    c = Config()
    c.tts = 'piper'
    c.text = 'Hello'
    cmd = c.build_command()
    assert 'piper' in cmd
    assert 'Hello' in cmd

if __name__ == '__main__':
    test_build_command_integration()
    print("OK: test_008_013_build_command_integration")
