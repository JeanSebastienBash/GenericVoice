"""
Test: test_002_011_build_command_wav_format.py
Suite: 002 Config
Purpose: Build Command Wav Format
Context: Unit test in test_002_config/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/config.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from config import Config

def test_build_command_wav_format():
    
    c = Config()
    c.audio.wav_format = "32-bit"
    cmd = c.build_command()
    assert '--wav-format 32-bit' in cmd

def test_build_command_wav_format_16bit():
    
    c = Config()
    cmd = c.build_command()
    assert '--wav-format' not in cmd

def test_build_command_wav_format_with_tts():
    
    c = Config()
    c.tts = 'piper'
    c.audio.wav_format = "32-bit"
    cmd = c.build_command()
    assert '--wav-format 32-bit' in cmd
    assert '--tts piper' in cmd

if __name__ == '__main__':
    test_build_command_wav_format()
    test_build_command_wav_format_16bit()
    test_build_command_wav_format_with_tts()
    print("✓ All test_002_011_build_command_wav_format tests passed")
