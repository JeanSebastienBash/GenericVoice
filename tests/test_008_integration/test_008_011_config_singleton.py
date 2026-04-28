"""
Test: test_008_011_config_singleton.py
Suite: 008 Integration
Purpose: Config Singleton
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
import config

def test_config_is_singleton():
    c1 = config.config
    c2 = config.config
    assert c1 is c2

if __name__ == '__main__':
    test_config_is_singleton()
    print("OK: test_008_011_config_singleton")
