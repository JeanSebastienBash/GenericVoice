"""
Test: test_001_029_validate_tts_compat.py
Suite: 001 Cli Args
Purpose: Validate Tts Compat
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
from param_validator import validate_tts_compatibility, EDGE_ONLY_PARAMS

def suppress_output(func):
    
    def wrapper(*args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            return func(*args, **kwargs)
    return wrapper

class TestMelodyCompatibility:
    
    @suppress_output
    def test_melody_with_edge_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'edge', 'melody': True})
        assert len(errors) == 0, f"Expected 0 errors for --melody with edge, got {len(errors)}"

    @suppress_output
    def test_melody_with_piper_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'melody': True})
        assert len(errors) == 1, f"Expected 1 error for --melody with piper, got {len(errors)}"
        assert 'melody' in errors[0]['title'].lower()
        assert 'piper' in errors[0]['title'].lower()

    @suppress_output
    def test_melody_with_espeak_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'espeak', 'melody': True})
        assert len(errors) == 1, f"Expected 1 error for --melody with espeak, got {len(errors)}"
        assert 'melody' in errors[0]['title'].lower()

class TestVoiceEffectCompatibility:
    
    @suppress_output
    def test_voice_effect_with_edge_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'edge', 'voice_effect': 'reverb'})
        assert len(errors) == 0, f"Expected 0 errors for --voice-effect with edge, got {len(errors)}"

    @suppress_output
    def test_voice_effect_echo_with_piper_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'voice_effect': 'echo'})
        assert len(errors) == 1, f"Expected 1 error for --voice-effect echo with piper, got {len(errors)}"

    @suppress_output
    def test_voice_effect_vibrato_with_espeak_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'espeak', 'voice_effect': 'vibrato'})
        assert len(errors) == 1, f"Expected 1 error for --voice-effect vibrato with espeak, got {len(errors)}"

    @suppress_output
    def test_voice_effect_none_with_piper_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'voice_effect': 'none'})
        assert len(errors) == 0, f"Expected 0 errors for --voice-effect none with piper, got {len(errors)}"

class TestNormalizeCompatibility:
    
    @suppress_output
    def test_normalize_with_edge_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'edge', 'normalize': True})
        assert len(errors) == 0, f"Expected 0 errors for --normalize with edge, got {len(errors)}"

    @suppress_output
    def test_normalize_with_piper_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'normalize': True})
        assert len(errors) == 1, f"Expected 1 error for --normalize with piper, got {len(errors)}"

    @suppress_output
    def test_normalize_with_espeak_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'espeak', 'normalize': True})
        assert len(errors) == 1, f"Expected 1 error for --normalize with espeak, got {len(errors)}"

class TestWavFormatCompatibility:
    
    @suppress_output
    def test_wav_format_16bit_with_edge_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'edge', 'wav_format': '16-bit'})
        assert len(errors) == 0, f"Expected 0 errors for --wav-format 16-bit with edge, got {len(errors)}"

    @suppress_output
    def test_wav_format_32bit_with_edge_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'edge', 'wav_format': '32-bit'})
        assert len(errors) == 0, f"Expected 0 errors for --wav-format 32-bit with edge, got {len(errors)}"

    @suppress_output
    def test_wav_format_16bit_with_piper_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'wav_format': '16-bit'})
        assert len(errors) == 0, f"Expected 0 errors for --wav-format 16-bit with piper, got {len(errors)}"

    @suppress_output
    def test_wav_format_32bit_with_piper_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'wav_format': '32-bit'})
        assert len(errors) == 1, f"Expected 1 error for --wav-format 32-bit with piper, got {len(errors)}"
        assert '32-bit' in errors[0]['title']
        assert 'piper' in errors[0]['title'].lower()

    @suppress_output
    def test_wav_format_32bit_with_espeak_invalid(self):
        
        errors = validate_tts_compatibility({'tts': 'espeak', 'wav_format': '32-bit'})
        assert len(errors) == 1, f"Expected 1 error for --wav-format 32-bit with espeak, got {len(errors)}"

class TestMultipleIncompatibleParams:
    
    @suppress_output
    def test_multiple_params_with_piper(self):
        
        errors = validate_tts_compatibility({
            'tts': 'piper',
            'melody': True,
            'voice_effect': 'reverb',
            'normalize': True,
        })
        assert len(errors) == 3, f"Expected 3 errors, got {len(errors)}"

    @suppress_output
    def test_multiple_params_with_espeak(self):
        
        errors = validate_tts_compatibility({
            'tts': 'espeak',
            'melody': True,
            'wav_format': '32-bit',
        })
        assert len(errors) == 2, f"Expected 2 errors, got {len(errors)}"

class TestValidCombinations:
    
    @suppress_output
    def test_piper_fade_in_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'fade_in': '100'})
        assert len(errors) == 0, f"Expected 0 errors for --fade-in with piper, got {len(errors)}"

    @suppress_output
    def test_piper_fade_out_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'piper', 'fade_out': '150'})
        assert len(errors) == 0, f"Expected 0 errors for --fade-out with piper, got {len(errors)}"

    @suppress_output
    def test_espeak_voice_valid(self):
        
        errors = validate_tts_compatibility({'tts': 'espeak', 'voice': 'fr'})
        assert len(errors) == 0, f"Expected 0 errors for --voice with espeak, got {len(errors)}"

    @suppress_output
    def test_edge_all_features_valid(self):
        
        errors = validate_tts_compatibility({
            'tts': 'edge',
            'melody': True,
            'voice_effect': 'reverb',
            'normalize': True,
            'wav_format': '32-bit',
        })
        assert len(errors) == 0, f"Expected 0 errors for all features with edge, got {len(errors)}"

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
