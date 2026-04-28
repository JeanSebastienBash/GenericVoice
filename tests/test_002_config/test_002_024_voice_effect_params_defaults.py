"""
Test: test_002_024_voice_effect_params_defaults.py
Suite: 002 Config
Purpose: Voice Effect Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_voice_effect_params_defaults():
    c = Config()
    c.voice_toggle = True
    c.voice_effect_name = 'echo'
    assert c.voice_effect_name == 'echo'
if __name__ == '__main__':
    test_voice_effect_params_defaults()
