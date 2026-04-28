"""
Test: test_002_020_percussion_params_defaults.py
Suite: 002 Config
Purpose: Percussion Params Defaults
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_percussion_params_timpani_main():
    
    c = Config()
    assert c.percussion.timpani_main == 70

def test_percussion_params_timpani_mid():
    
    c = Config()
    assert c.percussion.timpani_mid == 80

def test_percussion_params_timpani_intro():
    
    c = Config()
    assert c.percussion.timpani_intro == 90

def test_percussion_params_timpani_decay():
    
    c = Config()
    assert c.percussion.timpani_decay == 5.0

def test_percussion_params_timpani_noise():
    
    c = Config()
    assert c.percussion.timpani_noise == 0.3

def test_percussion_params_hihat_density():
    
    c = Config()
    assert c.percussion.hihat_density == 0.5

def test_percussion_params_hihat_cutoff():
    
    c = Config()
    assert c.percussion.hihat_cutoff == 8000

def test_percussion_params_perc_pattern():
    
    c = Config()
    assert c.percussion.perc_pattern == "straight"

if __name__ == '__main__':
    test_percussion_params_timpani_main()
    test_percussion_params_timpani_mid()
    test_percussion_params_timpani_intro()
    test_percussion_params_timpani_decay()
    test_percussion_params_timpani_noise()
    test_percussion_params_hihat_density()
    test_percussion_params_hihat_cutoff()
    test_percussion_params_perc_pattern()
    print("✓ All test_002_020_percussion_params_defaults tests passed")
