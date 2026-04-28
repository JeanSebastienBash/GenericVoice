"""
Test: test_008_006_melody_import.py
Suite: 008 Integration
Purpose: Melody Import
Context: Unit test in test_008_integration/. Validates specific functionality.
Impact: Failures indicate bugs in related modules.
Related: lib/melody.py
"""


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

def test_melody_import():
    import melody
    assert hasattr(melody, 'generate_chord_layer')

def test_melody_functions():
    import melody
    assert hasattr(melody, 'generate_percussion_layer')
    assert hasattr(melody, 'generate_bass_layer')

if __name__ == '__main__':
    test_melody_import()
    test_melody_functions()
    print("OK: test_008_006_melody_import")
