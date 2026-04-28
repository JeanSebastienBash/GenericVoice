"""
Test: test_005_008_apply_voice_effect_reverb.py
Suite: 005 Effects
Purpose: Apply Voice Effect Reverb
Context: Unit test in test_005_effects/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/effects.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import effects
import numpy as np

def test_apply_voice_effect_reverb():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.apply_voice_effect(data, "reverb")
    assert isinstance(result, np.ndarray)

def test_apply_voice_effect_reverb_params():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.apply_voice_effect(data, "reverb", reverb_room=0.5)
    assert len(result) == len(data)

if __name__ == '__main__':
    test_apply_voice_effect_reverb()
    test_apply_voice_effect_reverb_params()
    print("OK: test_005_008_apply_voice_effect_reverb")
