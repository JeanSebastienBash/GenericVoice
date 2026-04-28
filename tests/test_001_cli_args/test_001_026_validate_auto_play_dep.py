"""
Test: test_001_026_validate_auto_play_dep.py
Suite: 001 Cli Args
Purpose: Validate Auto Play Dep
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
from param_validator import validate_auto_play_dependency, REQUIRE_AUTO_PLAY

def suppress_output(func):
    
    def wrapper(*args, **kwargs):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            return func(*args, **kwargs)
    return wrapper

class TestPlayerRequiresAutoPlay:
    
    @suppress_output
    def test_player_without_auto_play_invalid(self):
        
        errors = validate_auto_play_dependency({'player': 'cvlc', 'auto_play': False})
        assert len(errors) == 1, f"Expected 1 error for --player without --auto-play, got {len(errors)}"
        assert 'player' in errors[0]['title'].lower()
        assert 'auto-play' in errors[0]['title'].lower()

    @suppress_output
    def test_player_with_auto_play_valid(self):
        
        errors = validate_auto_play_dependency({'player': 'cvlc', 'auto_play': True})
        assert len(errors) == 0, f"Expected 0 errors for --player with --auto-play, got {len(errors)}"

    @suppress_output
    def test_player_without_auto_play_flag_invalid(self):
        
        errors = validate_auto_play_dependency({'player': 'cvlc'})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"

    @suppress_output
    def test_player_all_valid_values(self):
        
        valid_players = ['parole', 'cvlc', 'vlc', 'ffplay', 'aplay']
        for player in valid_players:
            errors = validate_auto_play_dependency({'player': player, 'auto_play': True})
            assert len(errors) == 0, f"Expected 0 errors for player={player} with --auto-play, got {len(errors)}"

class TestWaitFinishRequiresAutoPlay:
    
    @suppress_output
    def test_wait_finish_without_auto_play_invalid(self):
        
        errors = validate_auto_play_dependency({'wait_finish': True, 'auto_play': False})
        assert len(errors) == 1, f"Expected 1 error for --wait-finish without --auto-play, got {len(errors)}"
        assert 'wait-finish' in errors[0]['title'].lower()
        assert 'auto-play' in errors[0]['title'].lower()

    @suppress_output
    def test_wait_finish_with_auto_play_valid(self):
        
        errors = validate_auto_play_dependency({'wait_finish': True, 'auto_play': True})
        assert len(errors) == 0, f"Expected 0 errors for --wait-finish with --auto-play, got {len(errors)}"

    @suppress_output
    def test_wait_finish_without_auto_play_flag_invalid(self):
        
        errors = validate_auto_play_dependency({'wait_finish': True})
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"

    @suppress_output
    def test_wait_finish_false_valid(self):
        
        errors = validate_auto_play_dependency({'wait_finish': False, 'auto_play': False})
        assert len(errors) == 0, f"Expected 0 errors for --wait-finish False, got {len(errors)}"

class TestAutoPlayMatrix:
    
    @suppress_output
    def test_both_params_without_auto_play_invalid(self):
        
        errors = validate_auto_play_dependency({
            'player': 'cvlc',
            'wait_finish': True,
            'auto_play': False
        })
        assert len(errors) == 2, f"Expected 2 errors for both params without --auto-play, got {len(errors)}"

    @suppress_output
    def test_both_params_with_auto_play_valid(self):
        
        errors = validate_auto_play_dependency({
            'player': 'cvlc',
            'wait_finish': True,
            'auto_play': True
        })
        assert len(errors) == 0, f"Expected 0 errors for both params with --auto-play, got {len(errors)}"

    @suppress_output
    def test_empty_parsed_valid(self):
        
        errors = validate_auto_play_dependency({})
        assert len(errors) == 0, f"Expected 0 errors for empty dict, got {len(errors)}"

    @suppress_output
    def test_auto_play_alone_valid(self):
        
        errors = validate_auto_play_dependency({'auto_play': True})
        assert len(errors) == 0, f"Expected 0 errors for --auto-play alone, got {len(errors)}"

    @suppress_output
    def test_auto_play_false_valid(self):
        
        errors = validate_auto_play_dependency({'auto_play': False})
        assert len(errors) == 0, f"Expected 0 errors for --auto-play False, got {len(errors)}"

    @suppress_output
    def test_all_params_in_require_auto_play_list(self):
        
        expected_params = ['player', 'wait-finish']
        for param in expected_params:
            assert param in REQUIRE_AUTO_PLAY, f"Missing {param} in REQUIRE_AUTO_PLAY"

    @suppress_output
    def test_auto_play_with_tts_valid(self):
        
        errors = validate_auto_play_dependency({
            'tts': 'piper',
            'auto_play': True,
            'player': 'cvlc',
            'wait_finish': True
        })
        assert len(errors) == 0, f"Expected 0 errors for valid combination, got {len(errors)}"

class TestAutoPlayWithOtherParams:
    
    @suppress_output
    def test_player_with_tts_without_auto_play_still_invalid(self):
        
        errors = validate_auto_play_dependency({
            'tts': 'piper',
            'player': 'cvlc',
            'auto_play': False
        })
        assert len(errors) == 1, f"Expected 1 error for --player without --auto-play even with --tts, got {len(errors)}"

    @suppress_output
    def test_wait_finish_with_tts_without_auto_play_still_invalid(self):
        
        errors = validate_auto_play_dependency({
            'tts': 'piper',
            'text': 'hello',
            'wait_finish': True,
            'auto_play': False
        })
        assert len(errors) == 1, f"Expected 1 error for --wait-finish without --auto-play even with --tts, got {len(errors)}"

if __name__ == '__main__':
    import traceback
    
    test_classes = [
        TestPlayerRequiresAutoPlay,
        TestWaitFinishRequiresAutoPlay,
        TestAutoPlayMatrix,
        TestAutoPlayWithOtherParams,
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
        print("All test_001_026_validate_auto_play_dep tests passed")
        sys.exit(0)
