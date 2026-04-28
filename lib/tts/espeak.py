"""
Module: tts/espeak.py
Purpose: Implements eSpeak formant TTS engine. Offline lightweight synthesis with 84 voices.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/tts/base.py, lib/espeak_processor.py
"""


import json
import os
import subprocess
from typing import List, Optional

from .base import BaseTTS, Voice, Language, TTSError

class ESpeakTTS(BaseTTS):
    
    name = "espeak"
    version = "1.0"
    description = "eSpeak open-source TTS (robotic, multilingual, offline)"
    
    def __init__(self, config=None):
        super().__init__(config)
        self._espeak_available = None
        self._espeak_ng_available = None
        self._voices_dir = os.path.join(os.path.dirname(__file__), "espeak", "voices")
        self._voices_json = os.path.join(self._voices_dir, "voices.json")
    
    def _load_json(self):
        
        if os.path.isfile(self._voices_json):
            with open(self._voices_json, encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _load_voices(self):
        
        data = self._load_json()
        return data.get("voices", {})
    
    def is_available(self) -> bool:
        
        if self._espeak_available is None:
            try:
                subprocess.run(
                    ["espeak-ng", "--version"],
                    capture_output=True,
                    check=True,
                )
                self._espeak_available = True
                self._espeak_ng_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(
                        ["espeak", "--version"],
                        capture_output=True,
                        check=True,
                    )
                    self._espeak_available = True
                    self._espeak_ng_available = False
                except (subprocess.CalledProcessError, FileNotFoundError):
                    self._espeak_available = False
                    self._espeak_ng_available = False
        
        return self._espeak_available
    
    def list_voices(self) -> List[Voice]:
        
        voices = []
        
        voices_data = self._load_voices()
        
        for lang_code, info in voices_data.items():
            voices.append(Voice(
                id=lang_code,
                name=info.get("name", lang_code),
                language=lang_code,
                model_path=info.get("model_file"),
            ))
        
        return sorted(voices, key=lambda v: v.id)
    
    def list_languages(self) -> List[Language]:
        
        voices_data = self._load_json()
        meta = voices_data.get("_meta", {})
        lang_map = meta.get("languages", {})
        
        languages = []
        for lang_code, lang_name in lang_map.items():
            count = sum(1 for v in voices_data.get("voices", {}).keys() if v.startswith(lang_code))
            languages.append(Language(
                code=lang_code,
                name=lang_name,
                voice_count=count,
            ))
        
        return sorted(languages, key=lambda l: l.code)
    
    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        output: Optional[str] = None,
        **kwargs,
    ) -> str:
        
        if not self.is_available():
            raise TTSError("eSpeak is not available")
        
        if voice is None:
            voice = "en"
        
        is_temp = output is None
        if is_temp:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                output = f.name
        
        espeak_cmd = "espeak-ng" if self._espeak_ng_available else "espeak"
        
        cmd = [espeak_cmd]
        
        cmd.extend(["-v", voice])
        
        variant = kwargs.get("variant", 1)
        if variant and self._espeak_ng_available:
            cmd.extend(["-k", str(variant)])
        
        pitch = kwargs.get("pitch", 50)
        cmd.extend(["-p", str(pitch)])
        
        speed = kwargs.get("speed", 140)
        cmd.extend(["-s", str(speed)])
        
        cmd.extend(["-w", output])
        
        cmd.extend(["--", text])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return output
        except subprocess.CalledProcessError as e:
            if is_temp and os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            raise TTSError(f"eSpeak synthesis failed: {e.stderr}")
        except FileNotFoundError:
            if is_temp and os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            raise TTSError(f"{espeak_cmd} command not found")
        except Exception as e:
            if is_temp and os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            raise TTSError(f"eSpeak synthesis failed: {e}")
