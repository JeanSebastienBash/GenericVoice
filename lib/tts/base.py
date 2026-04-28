"""
Module: tts/base.py
Purpose: Defines BaseTTS abstract interface, Voice and Language dataclasses, and TTSError exceptions. Contract for all TTS implementations.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/tts/piper.py, lib/tts/edge.py, lib/tts/espeak.py
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import os

class TTSError(Exception):
    
    pass

class TTSEngineNotAvailable(TTSError):
    
    pass

@dataclass
class Voice:
    
    id: str
    name: str
    language: str
    model_path: Optional[str] = None

@dataclass
class Language:
    
    code: str
    name: str
    voice_count: int = 0

class BaseTTS(ABC):
    
    name: str = "base"
    version: str = "1.0"
    description: str = "Base TTS class"
    
    _engines: Dict[str, type] = {}
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        
        self.config = config or {}
        self._project_dir = self._find_project_dir()
    
    def _find_project_dir(self) -> str:
        
        tts_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.dirname(os.path.dirname(os.path.dirname(tts_dir)))
    
    @abstractmethod
    def is_available(self) -> bool:
        
        pass
    
    @abstractmethod
    def list_voices(self) -> List[Voice]:
        
        pass
    
    @abstractmethod
    def list_languages(self) -> List[Language]:
        
        pass
    
    @abstractmethod
    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        output: Optional[str] = None,
        **kwargs,
    ) -> str:
        
        pass
    
    def get_default_voice(self) -> Optional[str]:
        
        voices = self.list_voices()
        return voices[0].id if voices else None
    
    def info(self) -> str:
        
        voice_count = len(self.list_voices())
        return f"{self.name} v{self.version} - {self.description} ({voice_count} voices)"

def get_tts_engine(name: str) -> BaseTTS:
    
    from .piper import PiperTTS
    from .edge import EdgeTTS
    from .espeak import ESpeakTTS
    
    engines = {
        "piper": PiperTTS,
        "edge": EdgeTTS,
        "espeak": ESpeakTTS,
    }
    
    if name not in engines:
        raise ValueError(
            f"Unknown TTS engine: '{name}'. "
            f"Valid engines: piper, edge, espeak. "
            f"Use --list-engines to see available engines."
        )
    
    engine = engines[name]()
    if not engine.is_available():
        raise TTSEngineNotAvailable(
            f"TTS engine '{name}' is not available. "
            f"Install it or use --auto-fix to install dependencies."
        )
    
    return engine

def auto_detect_tts() -> Optional[BaseTTS]:
    
    preferred_order = ["piper", "edge", "espeak"]
    
    for name in preferred_order:
        try:
            engine = get_tts_engine(name)
            if engine.is_available():
                return engine
        except (TTSEngineNotAvailable, ValueError):
            continue
    
    return None
