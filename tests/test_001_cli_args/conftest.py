"""
Test: conftest.py
Suite: 001 Cli Args
Purpose: Test Configuration and Fixtures
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import os
os.environ['__no_colors__'] = '1'

SCRIPT_NUM = "000"
