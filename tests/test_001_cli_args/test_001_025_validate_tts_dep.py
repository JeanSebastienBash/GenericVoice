"""
Test: test_001_025_validate_tts_dep.py
Suite: 001 Cli Args
Purpose: Validate Tts Dep
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
from param_validator import validate_tts_dependency, REQUIRE_TTS

def suppress_output(func):
    
    def wrapper(*args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            return func(*args, **kwargs)
    return wrapper

class TestTextRequiresTTS:
    
    @suppress_output
    def test_text_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'text': 'hello', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error for --text without --tts, got {len(errors)}"
        assert 'text' in errors[0]['title'].lower()
        assert 'tts' in errors[0]['title'].lower()

    @suppress_output
    def test_text_with_tts_valid(self):
        
        errors = validate_tts_dependency({'text': 'hello', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors for --text with --tts, got {len(errors)}"

class TestVoiceRequiresTTS:
    
    @suppress_output
    def test_voice_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'voice': 'en_US-ljspeech', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'voice' in errors[0]['title'].lower()

    @suppress_output
    def test_voice_with_tts_valid(self):
        
        errors = validate_tts_dependency({'voice': 'en_US-ljspeech', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestDurationRequiresTTS:
    
    @suppress_output
    def test_duration_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'duration': '10', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'duration' in errors[0]['title'].lower()

    @suppress_output
    def test_duration_with_tts_valid(self):
        
        errors = validate_tts_dependency({'duration': '10', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestOutputRequiresTTS:
    
    @suppress_output
    def test_output_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'output': '/tmp/test.wav', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'output' in errors[0]['title'].lower()

    @suppress_output
    def test_output_with_tts_valid(self):
        
        errors = validate_tts_dependency({'output': '/tmp/test.wav', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestMelodyRequiresTTS:
    
    @suppress_output
    def test_melody_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'melody': True, 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'melody' in errors[0]['title'].lower()

    @suppress_output
    def test_melody_with_tts_valid(self):
        
        errors = validate_tts_dependency({'melody': True, 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestVoiceEffectRequiresTTS:
    
    @suppress_output
    def test_voice_effect_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'voice_effect': 'echo', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'voice-effect' in errors[0]['title'].lower()

    @suppress_output
    def test_voice_effect_with_tts_valid(self):
        
        errors = validate_tts_dependency({'voice_effect': 'echo', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestAutoPlayRequiresTTS:
    
    @suppress_output
    def test_auto_play_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'auto_play': True, 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'auto-play' in errors[0]['title'].lower()

    @suppress_output
    def test_auto_play_with_tts_valid(self):
        
        errors = validate_tts_dependency({'auto_play': True, 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestPlayerRequiresTTS:
    
    @suppress_output
    def test_player_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'player': 'cvlc', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'player' in errors[0]['title'].lower()

    @suppress_output
    def test_player_with_tts_valid(self):
        
        errors = validate_tts_dependency({'player': 'cvlc', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestWaitFinishRequiresTTS:
    
    @suppress_output
    def test_wait_finish_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'wait_finish': True, 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'wait-finish' in errors[0]['title'].lower()

    @suppress_output
    def test_wait_finish_with_tts_valid(self):
        
        errors = validate_tts_dependency({'wait_finish': True, 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestNormalizeRequiresTTS:
    
    @suppress_output
    def test_normalize_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'normalize': True, 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'normalize' in errors[0]['title'].lower()

    @suppress_output
    def test_normalize_with_tts_valid(self):
        
        errors = validate_tts_dependency({'normalize': True, 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestWavFormatRequiresTTS:
    
    @suppress_output
    def test_wav_format_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'wav_format': '32-bit', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'wav-format' in errors[0]['title'].lower()

    @suppress_output
    def test_wav_format_with_tts_valid(self):
        
        errors = validate_tts_dependency({'wav_format': '32-bit', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestFadeInRequiresTTS:
    
    @suppress_output
    def test_fade_in_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'fade_in': '100', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'fade-in' in errors[0]['title'].lower()

    @suppress_output
    def test_fade_in_with_tts_valid(self):
        
        errors = validate_tts_dependency({'fade_in': '100', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestFadeOutRequiresTTS:
    
    @suppress_output
    def test_fade_out_without_tts_invalid(self):
        
        errors = validate_tts_dependency({'fade_out': '150', 'tts': None})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"
        assert 'fade-out' in errors[0]['title'].lower()

    @suppress_output
    def test_fade_out_with_tts_valid(self):
        
        errors = validate_tts_dependency({'fade_out': '150', 'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}"

class TestTTSMatrix:
    
    @suppress_output
    def test_all_params_in_require_tts_list(self):
        
        expected_params = [
            'text', 'voice', 'duration', 'output', 'melody',
            'voice-effect', 'auto-play', 'player', 'wait-finish',
            'normalize', 'wav-format', 'fade-in', 'fade-out'
        ]
        for param in expected_params:
            param_key = param.replace('-', '_')
            assert param in REQUIRE_TTS or param_key in [p.replace('-', '_') for p in REQUIRE_TTS], \
                f"Missing {param} in REQUIRE_TTS"

    @suppress_output
    def test_multiple_params_without_tts_invalid(self):
        
        errors = validate_tts_dependency({
            'text': 'hello',
            'voice': 'test',
            'melody': True,
            'tts': None
        })
        assert len(errors) == 3, f"Expected 3 errors for multiple params without --tts, got {len(errors)}"

    @suppress_output
    def test_empty_parsed_valid(self):
        
        errors = validate_tts_dependency({})
        assert len(errors) == 0, f"Expected 0 errors for empty dict, got {len(errors)}"

    @suppress_output
    def test_tts_only_valid(self):
        
        errors = validate_tts_dependency({'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors for --tts alone, got {len(errors)}"

    @suppress_output
    def test_complete_valid_combination(self):
        
        errors = validate_tts_dependency({
            'tts': 'piper',
            'text': 'hello',
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
        assert len(errors) == 0, f"Expected 0 errors for valid combination, got {len(errors)}"

if __name__ == '__main__':
    import traceback
    
    test_classes = [
        TestTextRequiresTTS,
        TestVoiceRequiresTTS,
        TestDurationRequiresTTS,
        TestOutputRequiresTTS,
        TestMelodyRequiresTTS,
        TestVoiceEffectRequiresTTS,
        TestAutoPlayRequiresTTS,
        TestPlayerRequiresTTS,
        TestWaitFinishRequiresTTS,
        TestNormalizeRequiresTTS,
        TestWavFormatRequiresTTS,
        TestFadeInRequiresTTS,
        TestFadeOutRequiresTTS,
        TestTTSMatrix,
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
        print("All test_001_025_validate_tts_dep tests passed")
        sys.exit(0)
