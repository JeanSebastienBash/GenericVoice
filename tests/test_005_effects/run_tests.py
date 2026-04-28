"""
Test: run_tests.py
Suite: 005 Effects
Purpose: Test Runner
Context: Unit test in test_005_effects/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/effects.py
"""


import sys
import os
import importlib.util
import io
import contextlib

os.environ['__no_colors__'] = '1'
os.environ['NO_COLOR'] = '1'
os.environ['TERM'] = 'dumb'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(TESTS_DIR)

sys.path.insert(0, os.path.join(PROJECT_DIR, 'lib'))
sys.path.insert(0, PROJECT_DIR)

import re
SUITE_NUM = re.search(r'test_(\d+)', os.path.basename(SCRIPT_DIR)).group(1) if re.search(r'test_(\d+)', os.path.basename(SCRIPT_DIR)) else '000'

TEST_FILES = sorted([f for f in os.listdir(SCRIPT_DIR) if f.startswith(f'test_{SUITE_NUM}_') and f.endswith('.py')])

def clean_text(text):
    
    text = re.sub(r'\x1b\[[0-9;]*[mGKH]', '', text)
    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
    text = re.sub(r'\[\?[0-9;]*[A-Za-z]', '', text)
    text = text.replace('═', '=').replace('║', '|').replace('╔', '+')
    text = text.replace('╗', '+').replace('╚', '+').replace('╝', '+')
    text = text.replace('╠', '+').replace('╣', '+').replace('─', '-')
    text = ''.join(c for c in text if ord(c) < 128 or c in '\n\r\t')
    return text

def main():
    passed = 0
    failed = 0
    errors = []
    
    for filename in TEST_FILES:
        filepath = os.path.join(SCRIPT_DIR, filename)
        spec = importlib.util.spec_from_file_location("test_module", filepath)
        module = importlib.util.module_from_spec(spec)
        
        try:
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
            
            try:
                spec.loader.exec_module(module)
                
                test_funcs = sorted([name for name in dir(module) if name.startswith('test_')])
                
                for func_name in test_funcs:
                    func = getattr(module, func_name)
                    if callable(func):
                        try:
                            stdout_capture = io.StringIO()
                            stderr_capture = io.StringIO()
                            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                                func()
                            print(f"  [OK] {func_name}")
                            passed += 1
                        except AssertionError as e:
                            print(f"  [FAIL] {func_name}: {e}")
                            failed += 1
                            errors.append(f"{filename}::{func_name}: {e}")
                        except SystemExit:
                            print(f"  [OK] {func_name}")
                            passed += 1
                        except Exception as e:
                            print(f"  [ERROR] {func_name}: {type(e).__name__}: {e}")
                            failed += 1
                            errors.append(f"{filename}::{func_name}: {type(e).__name__}: {e}")
            finally:
                sys.stderr = old_stderr
                            
        except Exception as e:
            print(f"  [ERROR] Loading {filename}: {e}")
            failed += 1
            errors.append(f"{filename}: {e}")
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  - {err}")
    
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
