"""
Test: test_005_006_apply_voice_effect_echo.py
Suite: 005 Effects
Purpose: Apply Voice Effect Echo
Context: Unit test in test_005_effects/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/effects.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import effects
import numpy as np

def test_apply_voice_effect_echo():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.apply_voice_effect(data, "echo")
    assert isinstance(result, np.ndarray)

def test_apply_voice_effect_echo_params():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.apply_voice_effect(data, "echo", delay_ms=100, decay=0.3, count=3)
    assert len(result) == len(data)

if __name__ == '__main__':
    test_apply_voice_effect_echo()
    test_apply_voice_effect_echo_params()
    print("OK: test_005_006_apply_voice_effect_echo")
