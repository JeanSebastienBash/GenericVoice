"""
Test: test_005_002_echo_effect_real.py
Suite: 005 Effects
Purpose: Echo Effect Real
Context: Unit test in test_005_effects/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/effects.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import effects
import numpy as np

def test_add_echo_defined():
    assert hasattr(effects, 'add_echo')

def test_add_echo_returns_array():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.add_echo(data, delay_ms=100, decay=0.3, count=2)
    assert isinstance(result, np.ndarray)

def test_add_echo_same_length():
    data = np.random.rand(4800).astype(np.float32)
    result = effects.add_echo(data, delay_ms=100, decay=0.3, count=2)
    assert len(result) == len(data)

if __name__ == '__main__':
    test_add_echo_defined()
    test_add_echo_returns_array()
    test_add_echo_same_length()
    print("OK: test_005_002_echo_effect_real")
