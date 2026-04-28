"""
Test: test_001_028_validate_integration.py
Suite: 001 Cli Args
Purpose: Validate Integration
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
from param_validator import validate_all_params

def suppress_output(func):
    
    def wrapper(*args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            return func(*args, **kwargs)
    return wrapper

class TestSoloParamsIntegration:
    
    @suppress_output
    def test_help_alone_valid(self):
        
        errors = validate_all_params({'help': True})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_help_with_other_params_invalid(self):
        
        errors = validate_all_params({'help': True, 'tts': 'piper'})
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_list_engines_alone_valid(self):
        
        errors = validate_all_params({'list_engines': True})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_list_launchers_alone_valid(self):
        
        errors = validate_all_params({'list_launchers': True})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_auto_fix_alone_valid(self):
        
        errors = validate_all_params({'auto_fix': True})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_launcher_alone_valid(self):
        
        errors = validate_all_params({'launcher': 'genericmenu'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestTTSDependencyIntegration:
    
    @suppress_output
    def test_tts_with_text_valid(self):
        
        errors = validate_all_params({'tts': 'piper', 'text': 'hello'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_text_without_tts_invalid(self):
        
        errors = validate_all_params({'text': 'hello'})
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_complete_valid_combination(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello world',
            'voice': 'en_US-ljspeech',
            'duration': '10',
            'output': '/tmp/test.wav',
            'melody': True,
            'voice_effect': 'echo',
            'auto_play': True,
            'player': 'cvlc',
            'wait_finish': True,
            'normalize': True,
            'wav_format': '32-bit',
            'fade_in': '100',
            'fade_out': '150'
        })
        assert len(errors) == 0, f"Expected 0 errors for complete valid combination, got {len(errors)}"

    @suppress_output
    def test_multiple_params_without_tts_invalid(self):
        
        errors = validate_all_params({
            'text': 'hello',
            'voice': 'test',
            'melody': True,
            'auto_play': True
        })
        assert len(errors) >= 3, f"Expected at least 3 errors, got {len(errors)}"

class TestAutoPlayDependencyIntegration:
    
    @suppress_output
    def test_player_with_auto_play_valid(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'auto_play': True,
            'player': 'cvlc'
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_player_without_auto_play_invalid(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'player': 'cvlc'
        })
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_wait_finish_with_auto_play_valid(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'auto_play': True,
            'wait_finish': True
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_wait_finish_without_auto_play_invalid(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'wait_finish': True
        })
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

class TestValueValidationIntegration:
    
    @suppress_output
    def test_invalid_tts_value(self):
        
        errors = validate_all_params({'tts': 'invalid_engine'})
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_invalid_player_value(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'auto_play': True,
            'player': 'invalid_player'
        })
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_invalid_wav_format_value(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'wav_format': '24-bit'
        })
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_negative_fade_in_value(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'fade_in': '-10'
        })
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

class TestMultipleErrorsIntegration:
    
    @suppress_output
    def test_solo_param_with_tts_dep_error(self):
        
        errors = validate_all_params({
            'help': True,
            'text': 'hello'
        })
        assert len(errors) >= 2, f"Expected at least 2 errors, got {len(errors)}"

    @suppress_output
    def test_all_error_types_combined(self):
        
        errors = validate_all_params({
            'help': True,
            'text': 'hello',
            'player': 'cvlc',
            'tts': 'invalid'
        })
        assert len(errors) >= 3, f"Expected at least 3 errors, got {len(errors)}"

    @suppress_output
    def test_empty_dict_valid(self):
        
        errors = validate_all_params({})
        assert len(errors) == 0, f"Expected 0 errors for empty dict, got {len(errors)}"

class TestEdgeCasesIntegration:
    
    @suppress_output
    def test_tts_only_valid(self):
        
        errors = validate_all_params({'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_system_os_alone_valid(self):
        
        errors = validate_all_params({'system_os': 'ubuntu'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_melody_without_tts_invalid(self):
        
        errors = validate_all_params({'melody': True})
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_voice_effect_without_tts_invalid(self):
        
        errors = validate_all_params({'voice_effect': 'echo'})
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_normalize_without_tts_invalid(self):
        
        errors = validate_all_params({'normalize': True})
        assert len(errors) >= 1, f"Expected at least 1 error, got {len(errors)}"

    @suppress_output
    def test_all_flags_with_tts_valid(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'melody': True,
            'auto_play': True,
            'normalize': True,
            'wait_finish': True,
            'player': 'cvlc',
            'voice_effect': 'echo',
            'wav_format': '32-bit',
            'fade_in': '100',
            'fade_out': '150'
        })
        assert len(errors) == 0, f"Expected 0 errors for all flags with --tts, got {len(errors)}"

class TestValidCombinationsIntegration:
    
    @suppress_output
    def test_minimal_valid_synthesis(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello'
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_synthesis_with_player(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'auto_play': True,
            'player': 'cvlc'
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_synthesis_with_melody(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'melody': True
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_synthesis_with_all_audio_options(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'normalize': True,
            'wav_format': '32-bit',
            'fade_in': '100',
            'fade_out': '150'
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

    @suppress_output
    def test_synthesis_with_voice_effect(self):
        
        errors = validate_all_params({
            'tts': 'piper',
            'text': 'hello',
            'voice_effect': 'echo'
        })
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

if __name__ == '__main__':
    import traceback
    
    test_classes = [
        TestSoloParamsIntegration,
        TestTTSDependencyIntegration,
        TestAutoPlayDependencyIntegration,
        TestValueValidationIntegration,
        TestMultipleErrorsIntegration,
        TestEdgeCasesIntegration,
        TestValidCombinationsIntegration,
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
        print("All test_001_028_validate_integration tests passed")
        sys.exit(0)
