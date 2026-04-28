"""
Test: test_002_017_get_display_info.py
Suite: 002 Config
Purpose: Get Display Info
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_get_display_info():
    c = Config()
    info = c.get_display_info()
    assert 'tts' in info
    assert 'mode' in info
if __name__ == '__main__':
    test_get_display_info()
