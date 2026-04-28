"""
Test: test_001_027_validate_values.py
Suite: 001 Cli Args
Purpose: Validate Values
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
from param_validator import validate_param_values, VALUE_OPTIONS

def suppress_output(func):
    
    def wrapper(*args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            return func(*args, **kwargs)
    return wrapper

class TestTTSValues:
    
    @suppress_output
    def test_tts_piper_valid(self):
        
        errors = validate_param_values({'tts': 'piper'})
        assert len(errors) == 0, f"Expected 0 errors for --tts piper, got {len(errors)}"

    @suppress_output
    def test_tts_edge_valid(self):
        
        errors = validate_param_values({'tts': 'edge'})
        assert len(errors) == 0, f"Expected 0 errors for --tts edge, got {len(errors)}"

    @suppress_output
    def test_tts_espeak_valid(self):
        
        errors = validate_param_values({'tts': 'espeak'})
        assert len(errors) == 0, f"Expected 0 errors for --tts espeak, got {len(errors)}"

    @suppress_output
    def test_tts_invalid_engine(self):
        
        errors = validate_param_values({'tts': 'invalid_engine'})
        assert len(errors) == 1, f"Expected 1 error for invalid --tts, got {len(errors)}"
        assert 'tts' in errors[0]['title'].lower()

    @suppress_output
    def test_tts_empty_string_invalid(self):
        
        errors = validate_param_values({'tts': ''})
        assert len(errors) == 1, f"Expected 1 error for empty --tts, got {len(errors)}"

    @suppress_output
    def test_tts_numeric_invalid(self):
        
        errors = validate_param_values({'tts': '123'})
        assert len(errors) == 1, f"Expected 1 error for numeric --tts, got {len(errors)}"

class TestVoiceEffectValues:
    
    @suppress_output
    def test_voice_effect_echo_valid(self):
        
        errors = validate_param_values({'voice_effect': 'echo'})
        assert len(errors) == 0, f"Expected 0 errors for --voice-effect echo, got {len(errors)}"

    @suppress_output
    def test_voice_effect_vibrato_valid(self):
        
        errors = validate_param_values({'voice_effect': 'vibrato'})
        assert len(errors) == 0, f"Expected 0 errors for --voice-effect vibrato, got {len(errors)}"

    @suppress_output
    def test_voice_effect_reverb_valid(self):
        
        errors = validate_param_values({'voice_effect': 'reverb'})
        assert len(errors) == 0, f"Expected 0 errors for --voice-effect reverb, got {len(errors)}"

    @suppress_output
    def test_voice_effect_none_valid(self):
        
        errors = validate_param_values({'voice_effect': 'none'})
        assert len(errors) == 0, f"Expected 0 errors for --voice-effect none, got {len(errors)}"

    @suppress_output
    def test_voice_effect_invalid(self):
        
        errors = validate_param_values({'voice_effect': 'invalid_effect'})
        assert len(errors) == 1, f"Expected 1 error for invalid --voice-effect, got {len(errors)}"

    @suppress_output
    def test_voice_effect_numeric_invalid(self):
        
        errors = validate_param_values({'voice_effect': '123'})
        assert len(errors) == 1, f"Expected 1 error for numeric --voice-effect, got {len(errors)}"

class TestPlayerValues:
    
    @suppress_output
    def test_player_parole_valid(self):
        
        errors = validate_param_values({'player': 'parole'})
        assert len(errors) == 0, f"Expected 0 errors for --player parole, got {len(errors)}"

    @suppress_output
    def test_player_cvlc_valid(self):
        
        errors = validate_param_values({'player': 'cvlc'})
        assert len(errors) == 0, f"Expected 0 errors for --player cvlc, got {len(errors)}"

    @suppress_output
    def test_player_vlc_valid(self):
        
        errors = validate_param_values({'player': 'vlc'})
        assert len(errors) == 0, f"Expected 0 errors for --player vlc, got {len(errors)}"

    @suppress_output
    def test_player_ffplay_valid(self):
        
        errors = validate_param_values({'player': 'ffplay'})
        assert len(errors) == 0, f"Expected 0 errors for --player ffplay, got {len(errors)}"

    @suppress_output
    def test_player_aplay_valid(self):
        
        errors = validate_param_values({'player': 'aplay'})
        assert len(errors) == 0, f"Expected 0 errors for --player aplay, got {len(errors)}"

    @suppress_output
    def test_player_invalid(self):
        
        errors = validate_param_values({'player': 'invalid_player'})
        assert len(errors) == 1, f"Expected 1 error for invalid --player, got {len(errors)}"

    @suppress_output
    def test_player_numeric_invalid(self):
        
        errors = validate_param_values({'player': '123'})
        assert len(errors) == 1, f"Expected 1 error for numeric --player, got {len(errors)}"

class TestWavFormatValues:
    
    @suppress_output
    def test_wav_format_16bit_valid(self):
        
        errors = validate_param_values({'wav_format': '16-bit'})
        assert len(errors) == 0, f"Expected 0 errors for --wav-format 16-bit, got {len(errors)}"

    @suppress_output
    def test_wav_format_32bit_valid(self):
        
        errors = validate_param_values({'wav_format': '32-bit'})
        assert len(errors) == 0, f"Expected 0 errors for --wav-format 32-bit, got {len(errors)}"

    @suppress_output
    def test_wav_format_invalid(self):
        
        errors = validate_param_values({'wav_format': '24-bit'})
        assert len(errors) == 1, f"Expected 1 error for --wav-format 24-bit, got {len(errors)}"

    @suppress_output
    def test_wav_format_numeric_invalid(self):
        
        errors = validate_param_values({'wav_format': '32'})
        assert len(errors) == 1, f"Expected 1 error for numeric --wav-format, got {len(errors)}"

    @suppress_output
    def test_wav_format_spaces_invalid(self):
        
        errors = validate_param_values({'wav_format': ' 16-bit '})
        assert len(errors) == 1, f"Expected 1 error for --wav-format with spaces, got {len(errors)}"

class TestSystemOSValues:
    
    @suppress_output
    def test_system_os_ubuntu_valid(self):
        
        errors = validate_param_values({'system_os': 'ubuntu'})
        assert len(errors) == 0, f"Expected 0 errors for --system-os ubuntu, got {len(errors)}"

    @suppress_output
    def test_system_os_linux_valid(self):
        
        errors = validate_param_values({'system_os': 'linux'})
        assert len(errors) == 0, f"Expected 0 errors for --system-os linux, got {len(errors)}"

    @suppress_output
    def test_system_os_windows_valid(self):
        
        errors = validate_param_values({'system_os': 'windows'})
        assert len(errors) == 0, f"Expected 0 errors for --system-os windows, got {len(errors)}"

    @suppress_output
    def test_system_os_darwin_valid(self):
        
        errors = validate_param_values({'system_os': 'darwin'})
        assert len(errors) == 0, f"Expected 0 errors for --system-os darwin, got {len(errors)}"

    @suppress_output
    def test_system_os_invalid(self):
        
        errors = validate_param_values({'system_os': 'macos'})
        assert len(errors) == 1, f"Expected 1 error for --system-os macos, got {len(errors)}"

    @suppress_output
    def test_system_os_numeric_invalid(self):
        
        errors = validate_param_values({'system_os': '123'})
        assert len(errors) == 1, f"Expected 1 error for numeric --system-os, got {len(errors)}"

class TestLauncherValues:
    
    @suppress_output
    def test_launcher_genericmenu_valid(self):
        
        errors = validate_param_values({'launcher': 'genericmenu'})
        assert len(errors) == 0, f"Expected 0 errors for --launcher genericmenu, got {len(errors)}"

    @suppress_output
    def test_launcher_invalid(self):
        
        errors = validate_param_values({'launcher': 'invalid_launcher'})
        assert len(errors) == 1, f"Expected 1 error for invalid --launcher, got {len(errors)}"

    @suppress_output
    def test_launcher_numeric_invalid(self):
        
        errors = validate_param_values({'launcher': '123'})
        assert len(errors) == 1, f"Expected 1 error for numeric --launcher, got {len(errors)}"

class TestFadeInValues:
    
    @suppress_output
    def test_fade_in_positive_valid(self):
        
        errors = validate_param_values({'fade_in': '100'})
        assert len(errors) == 0, f"Expected 0 errors for --fade-in 100, got {len(errors)}"

    @suppress_output
    def test_fade_in_zero_valid(self):
        
        errors = validate_param_values({'fade_in': '0'})
        assert len(errors) == 0, f"Expected 0 errors for --fade-in 0, got {len(errors)}"

    @suppress_output
    def test_fade_in_negative_invalid(self):
        
        errors = validate_param_values({'fade_in': '-10'})
        assert len(errors) == 1, f"Expected 1 error for negative --fade-in, got {len(errors)}"

    @suppress_output
    def test_fade_in_string_invalid(self):
        
        errors = validate_param_values({'fade_in': 'abc'})
        assert len(errors) == 1, f"Expected 1 error for string --fade-in, got {len(errors)}"

    @suppress_output
    def test_fade_in_float_invalid(self):
        
        errors = validate_param_values({'fade_in': '1.5'})
        assert len(errors) == 1, f"Expected 1 error for float --fade-in, got {len(errors)}"

class TestFadeOutValues:
    
    @suppress_output
    def test_fade_out_positive_valid(self):
        
        errors = validate_param_values({'fade_out': '150'})
        assert len(errors) == 0, f"Expected 0 errors for --fade-out 150, got {len(errors)}"

    @suppress_output
    def test_fade_out_zero_valid(self):
        
        errors = validate_param_values({'fade_out': '0'})
        assert len(errors) == 0, f"Expected 0 errors for --fade-out 0, got {len(errors)}"

    @suppress_output
    def test_fade_out_negative_invalid(self):
        
        errors = validate_param_values({'fade_out': '-5'})
        assert len(errors) == 1, f"Expected 1 error for negative --fade-out, got {len(errors)}"

    @suppress_output
    def test_fade_out_string_invalid(self):
        
        errors = validate_param_values({'fade_out': 'xyz'})
        assert len(errors) == 1, f"Expected 1 error for string --fade-out, got {len(errors)}"

    @suppress_output
    def test_fade_out_float_invalid(self):
        
        errors = validate_param_values({'fade_out': '2.0'})
        assert len(errors) == 1, f"Expected 1 error for float --fade-out, got {len(errors)}"

class TestValuesMatrix:
    
    @suppress_output
    def test_empty_parsed_valid(self):
        
        errors = validate_param_values({})
        assert len(errors) == 0, f"Expected 0 errors for empty dict, got {len(errors)}"

    @suppress_output
    def test_multiple_invalid_values(self):
        
        errors = validate_param_values({
            'tts': 'invalid',
            'player': 'invalid',
            'wav_format': 'invalid'
        })
        assert len(errors) == 3, f"Expected 3 errors for multiple invalid values, got {len(errors)}"

    @suppress_output
    def test_all_valid_values(self):
        
        errors = validate_param_values({
            'tts': 'piper',
            'voice_effect': 'echo',
            'player': 'cvlc',
            'wav_format': '32-bit',
            'system_os': 'ubuntu',
            'launcher': 'genericmenu',
            'fade_in': '100',
            'fade_out': '150'
        })
        assert len(errors) == 0, f"Expected 0 errors for all valid values, got {len(errors)}"

    @suppress_output
    def test_value_options_defined(self):
        
        assert 'tts' in VALUE_OPTIONS
        assert 'voice-effect' in VALUE_OPTIONS
        assert 'player' in VALUE_OPTIONS
        assert 'wav-format' in VALUE_OPTIONS
        assert 'system-os' in VALUE_OPTIONS
        assert 'launcher' in VALUE_OPTIONS

if __name__ == '__main__':
    import traceback
    
    test_classes = [
        TestTTSValues,
        TestVoiceEffectValues,
        TestPlayerValues,
        TestWavFormatValues,
        TestSystemOSValues,
        TestLauncherValues,
        TestFadeInValues,
        TestFadeOutValues,
        TestValuesMatrix,
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
        print("All test_001_027_validate_values tests passed")
        sys.exit(0)
