"""
Test: test_001_024_validate_solo_params.py
Suite: 001 Cli Args
Purpose: Validate Solo Params
Context: Unit test in test_001_cli_args/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: py/gv.py, lib/param_validator.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import io
import contextlib
from param_validator import validate_solo_params, SOLO_PARAMS

def suppress_output(func):
    
    def wrapper(*args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            return func(*args, **kwargs)
    return wrapper

class TestSoloParamsHelp:
    
    @suppress_output
    def test_help_alone_valid(self):
        
        errors = validate_solo_params({'help': True})
        assert len(errors) == 0, f"Expected 0 errors for --help alone, got {len(errors)}"

    @suppress_output
    def test_help_with_tts_invalid(self):
        
        errors = validate_solo_params({'help': True, 'tts': 'piper'})
        assert len(errors) == 1, f"Expected 1 error for --help with --tts, got {len(errors)}"
        assert 'help' in errors[0]['title'].lower()

    @suppress_output
    def test_help_with_text_invalid(self):
        
        errors = validate_solo_params({'help': True, 'text': 'hello'})
        assert len(errors) == 1, f"Expected 1 error for --help with --text, got {len(errors)}"

    @suppress_output
    def test_help_with_multiple_params_invalid(self):
        
        errors = validate_solo_params({'help': True, 'tts': 'piper', 'text': 'hello'})
        assert len(errors) == 1, f"Expected 1 error for --help with multiple params, got {len(errors)}"

class TestSoloParamsListEngines:
    
    @suppress_output
    def test_list_engines_alone_valid(self):
        
        errors = validate_solo_params({'list_engines': True})
        assert len(errors) == 0, f"Expected 0 errors for --list-engines alone, got {len(errors)}"

    @suppress_output
    def test_list_engines_with_tts_invalid(self):
        
        errors = validate_solo_params({'list_engines': True, 'tts': 'piper'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'list-engines' in errors[0]['title'].lower()

    @suppress_output
    def test_list_engines_with_text_invalid(self):
        
        errors = validate_solo_params({'list_engines': True, 'text': 'hello'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"

class TestSoloParamsListLaunchers:
    
    @suppress_output
    def test_list_launchers_alone_valid(self):
        
        errors = validate_solo_params({'list_launchers': True})
        assert len(errors) == 0, f"Expected 0 errors for --list-launchers alone, got {len(errors)}"

    @suppress_output
    def test_list_launchers_with_tts_invalid(self):
        
        errors = validate_solo_params({'list_launchers': True, 'tts': 'piper'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'list-launchers' in errors[0]['title'].lower()

class TestSoloParamsAutoFix:
    
    @suppress_output
    def test_auto_fix_alone_valid(self):
        
        errors = validate_solo_params({'auto_fix': True})
        assert len(errors) == 0, f"Expected 0 errors for --auto-fix alone, got {len(errors)}"

    @suppress_output
    def test_auto_fix_with_tts_invalid(self):
        
        errors = validate_solo_params({'auto_fix': True, 'tts': 'piper'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'auto-fix' in errors[0]['title'].lower()

    @suppress_output
    def test_auto_fix_with_text_invalid(self):
        
        errors = validate_solo_params({'auto_fix': True, 'text': 'hello'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"

class TestSoloParamsLauncher:
    
    @suppress_output
    def test_launcher_alone_valid(self):
        
        errors = validate_solo_params({'launcher': 'genericmenu'})
        assert len(errors) == 0, f"Expected 0 errors for --launcher alone, got {len(errors)}"

    @suppress_output
    def test_launcher_with_tts_invalid(self):
        
        errors = validate_solo_params({'launcher': 'genericmenu', 'tts': 'piper'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'launcher' in errors[0]['title'].lower()

    @suppress_output
    def test_launcher_with_multiple_params_invalid(self):
        
        errors = validate_solo_params({'launcher': 'genericmenu', 'tts': 'piper', 'text': 'hello'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"

class TestSoloParamsMatrix:
    
    @suppress_output
    def test_all_solo_params_in_list(self):
        
        expected_solo = ['help', 'list-engines', 'list-launchers', 'auto-fix', 'launcher']
        for param in expected_solo:
            assert param in SOLO_PARAMS, f"Missing {param} in SOLO_PARAMS"

    @suppress_output
    def test_empty_parsed_valid(self):
        
        errors = validate_solo_params({})
        assert len(errors) == 0, f"Expected 0 errors for empty dict, got {len(errors)}"

    @suppress_output
    def test_non_solo_params_only_valid(self):
        
        errors = validate_solo_params({'tts': 'piper', 'text': 'hello', 'auto_play': True})
        assert len(errors) == 0, f"Expected 0 errors for non-solo params, got {len(errors)}"

    @suppress_output
    def test_multiple_solo_params_invalid(self):
        
        errors = validate_solo_params({'help': True, 'list_engines': True})
        assert len(errors) >= 1, f"Expected at least 1 error for multiple solo params, got {len(errors)}"

if __name__ == '__main__':
    import traceback
    
    test_classes = [
        TestSoloParamsHelp,
        TestSoloParamsListEngines,
        TestSoloParamsListLaunchers,
        TestSoloParamsAutoFix,
        TestSoloParamsLauncher,
        TestSoloParamsMatrix,
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                method = getattr(instance, method_name)
                try:
                    method()
                    print(f"  [OK] {test_class.__name__}::{method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  [FAIL] {test_class.__name__}::{method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  [ERROR] {test_class.__name__}::{method_name}: {type(e).__name__}: {e}")
                    failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("All test_001_024_validate_solo_params tests passed")
        sys.exit(0)
