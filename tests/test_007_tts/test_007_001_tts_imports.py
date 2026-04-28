"""
Test: test_007_001_tts_imports.py
Suite: 007 Tts
Purpose: Tts Imports
Context: Unit test in test_007_tts/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/tts/
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_import_tts_module():
    
    import tts
    assert tts is not None

def test_import_base_tts():
    
    from tts import BaseTTS
    assert BaseTTS is not None

def test_import_voice():
    
    from tts import Voice
    assert Voice is not None

def test_import_language():
    
    from tts import Language
    assert Language is not None

def test_import_tts_error():
    
    from tts import TTSError
    assert TTSError is not None

def test_import_tts_engine_not_available():
    
    from tts import TTSEngineNotAvailable
    assert TTSEngineNotAvailable is not None

if __name__ == '__main__':
    test_import_tts_module()
    test_import_base_tts()
    test_import_voice()
    test_import_language()
    test_import_tts_error()
    test_import_tts_engine_not_available()
    print("OK: test_007_001_tts_imports")
