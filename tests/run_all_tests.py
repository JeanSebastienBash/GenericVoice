"""
Test: run_all_tests.py
Suite: All Test Suites
Purpose: Master Test Runner
Context: Unit test in tests/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: Generic Voice modules
"""


import sys
import os
import subprocess
import io

os.environ['__no_colors__'] = '1'
os.environ['NO_COLOR'] = '1'
os.environ['TERM'] = 'dumb'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

TEST_SUITES = [
    ('test_001_cli_args',    'CLI Arguments',    'Parsing des arguments CLI',     27),
    ('test_002_config',      'Config Class',     'Classe Config',                24),
    ('test_003_player',      'Player Module',    'Gestion deslecteurs audio',    18),
    ('test_004_audio',       'Audio Module',     'Fonctions audio',              14),
    ('test_005_effects',      'Effects Module',   'Effets vocaux',                 9),
    ('test_006_melody',       'Melody Module',    'Generation de melodie',        10),
    ('test_007_tts',          'TTS Modules',      'Moteurs TTS',                  13),
    ('test_008_integration',   'Integration',      'Integration complete',         16),
    ('test_009_matrix',       'Parameter Matrix', 'Combinaisons de parametres',   19),
]

def run_suite(suite_name, verbose=False):
    
    suite_path = os.path.join(SCRIPT_DIR, suite_name)
    runner_path = os.path.join(suite_path, "run_tests.py")
    suite_num = suite_name.split('_')[1]

    print(f"\n{'='*60}")
    print(f">>> Test {suite_num}: {suite_name}")
    print(f"{'='*60}")

    info = next((s for s in TEST_SUITES if s[0] == suite_name), None)
    if info:
        print(f"  Directory: {suite_name}/")
        print(f"  Description: {info[2]}")
        print(f"  Unit tests: {info[3]}")
        print()

    if not os.path.exists(runner_path):
        print(f"  [WARNING] Runner notfound: {runner_path}")
        return False

    env = os.environ.copy()
    env['__no_colors__'] = '1'
    env['NO_COLOR'] = '1'
    env['TERM'] = 'dumb'
    PYTHONPATH = os.path.join(PROJECT_DIR, 'lib') + ':' + os.path.join(PROJECT_DIR, 'py')
    env['PYTHONPATH'] = PYTHONPATH

    try:
        result = subprocess.run(
            [sys.executable, runner_path],
            cwd=suite_path,
            capture_output=True,
            text=True,
            env=env
        )

        def clean_output(text):
            import re
            text = re.sub(r'\x1b\[[0-9;]*[mGKH]', '', text)
            text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
            text = re.sub(r'\[\?[0-9;]*[A-Za-z]', '', text)
            text = text.replace('═', '=')
            text = text.replace('║', '|')
            text = text.replace('╔', '+')
            text = text.replace('╗', '+')
            text = text.replace('╚', '+')
            text = text.replace('╝', '+')
            text = text.replace('╠', '+')
            text = text.replace('╣', '+')
            text = text.replace('─', '-')
            text = text.replace('│', '|')
            text = text.replace('┌', '+')
            text = text.replace('┐', '+')
            text = text.replace('└', '+')
            text = text.replace('┘', '+')
            text = text.replace('├', '+')
            text = text.replace('┤', '+')
            text = text.replace('┬', '+')
            text = text.replace('┴', '+')
            text = text.replace('┼', '+')
            text = ''.join(c for c in text if ord(c) < 128 or c in '\n\r\t')
            return text

        if verbose and result.stdout:
            print(clean_output(result.stdout))

        if result.returncode == 0:
            print(f"  [OK] All tests passed")
            return True
        else:
            print(f"  [FAIL] Suite {suite_name}: code {result.returncode}")
            if result.stdout:
                print(clean_output(result.stdout))
            return False

    except Exception as e:
        print(f"  [ERROR] Execution error: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generic Voice v1.0.2 Test Runner')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--suite', type=str, default=None, help='Run specific suite')
    args = parser.parse_args()

    suites_to_run = TEST_SUITES
    if args.suite:
        suites_to_run = [s for s in TEST_SUITES if s[0] == args.suite]
        if not suites_to_run:
            print(f"[ERROR] Unknown suite: {args.suite}")
            print(f"Available suites: {', '.join(s[0] for s in TEST_SUITES)}")
            sys.exit(1)

    total_tests = sum(s[3] for s in suites_to_run)

    print(f"{'='*60}")
    print(f"GENERIC VOICE v1.0.2 - TEST SUITE")
    print(f"{'='*60}")
    print(f"Total: {total_tests} unit tests in {len(suites_to_run)} suites")
    print(f"Mode: {'VERBOSE' if args.verbose else 'NORMAL'}")
    print()

    results = []
    for suite_name, suite_label, description, test_count in suites_to_run:
        success = run_suite(suite_name, verbose=args.verbose)
        results.append((suite_label, success))

    print(f"\n{'='*60}")
    print(f"TEST RESULTS SUMMARY")
    print(f"{'='*60}")

    passed = 0
    failed = 0

    for suite_label, success in results:
        if success:
            status = "[PASSED]"
            passed += 1
        else:
            status = "[FAILED]"
            failed += 1
        print(f"  {status}: {suite_label}")

    print(f"{'='*60}")
    print(f"Total: {passed + failed} suites | Passed: {passed} | Failed: {failed}")
    print(f"{'='*60}")

    if failed > 0:
        print(f"\n[ERROR] SOME TESTS FAILED!")
        sys.exit(1)
    else:
        print(f"\n[OK] ALL TESTS PASSED!")
        sys.exit(0)

if __name__ == '__main__':
    main()
