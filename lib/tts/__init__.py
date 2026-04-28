"""
Module: tts/__init__.py
Purpose: Factory module for TTS engine instantiation. Exports BaseTTS, PiperTTS, EdgeTTS, ESpeakTTS, and helper functions.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/tts/base.py, lib/tts/piper.py, lib/tts/edge.py, lib/tts/espeak.py, lib/synthesis.py
"""


from .base import BaseTTS, Voice, Language, TTSError, TTSEngineNotAvailable, get_tts_engine, auto_detect_tts
from .piper import PiperTTS
from .edge import EdgeTTS
from .espeak import ESpeakTTS

__all__ = [
    "BaseTTS",
    "Voice",
    "Language", 
    "TTSError",
    "TTSEngineNotAvailable",
    "get_tts_engine",
    "auto_detect_tts",
    "PiperTTS",
    "EdgeTTS",
    "ESpeakTTS",
]

def get_tts_engine_status() -> dict:
    
    status = {}
    for engine_name in ["piper", "edge", "espeak"]:
        try:
            engine = get_tts_engine(engine_name)
            status[engine_name] = True
        except TTSEngineNotAvailable:
            status[engine_name] = False
        except ValueError:
            status[engine_name] = False
    return status
