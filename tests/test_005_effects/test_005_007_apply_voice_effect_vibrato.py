"""
Test: test_005_007_apply_voice_effect_vibrato.py
Suite: 005 Effects
Purpose: Apply Voice Effect Vibrato
Context: Unit test in test_005_effects/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/effects.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import effects
import numpy as np

def test_apply_voice_effect_vibrato():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.apply_voice_effect(data, "vibrato")
    assert isinstance(result, np.ndarray)

def test_apply_voice_effect_vibrato_params():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.apply_voice_effect(data, "vibrato", vibrato_rate=5.0, vibrato_depth=5.0)
    assert len(result) == len(data)

if __name__ == '__main__':
    test_apply_voice_effect_vibrato()
    test_apply_voice_effect_vibrato_params()
    print("OK: test_005_007_apply_voice_effect_vibrato")
