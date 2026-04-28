"""
Test: test_008_002_config_import.py
Suite: 008 Integration
Purpose: Config Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_config_import():
    import config
    assert hasattr(config, 'Config')

def test_config_singleton():
    import config
    assert hasattr(config, 'config')

if __name__ == '__main__':
    test_config_import()
    test_config_singleton()
    print("OK: test_008_002_config_import")
