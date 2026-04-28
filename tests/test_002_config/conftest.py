"""
Test: conftest.py
Suite: 002 Config
Purpose: Test Configuration and Fixtures
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import os
os.environ['__no_colors__'] = '1'

SCRIPT_NUM = "000"
