"""
Test: test_007_003_tts_error.py
Suite: 007 Tts
Purpose: Tts Error
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tts import TTSError

def test_tts_error_defined():
    assert TTSError is not None

def test_tts_error_is_exception():
    assert issubclass(TTSError, Exception)

if __name__ == '__main__':
    test_tts_error_defined()
    test_tts_error_is_exception()
    print("OK: test_007_003_tts_error")
