"""
Module: tts/piper.py
Purpose: Implements Piper neural TTS engine. Offline synthesis using ONNX models. 174 voices supported.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/tts/base.py, lib/piper_processor.py
"""


import json
import os
import subprocess
import sys
from typing import List, Optional

from .base import BaseTTS, Voice, Language, TTSError

class PiperTTS(BaseTTS):
    
    name = "piper"
    version = "1.0"
    description = "Neural offline TTS (160+ voices)"
    
    def __init__(self, config=None):
        super().__init__(config)
        piper_file = __file__
        if piper_file.endswith('.pyc'):
            piper_file = piper_file.replace('.pyc', '.py')
        piper_dir = os.path.dirname(piper_file)
        
        self._voices_dir = os.path.join(piper_dir, "piper", "voices")
        self._bin_dir = os.path.join(piper_dir, "piper", "bin")
        self._piper_bin = os.path.join(self._bin_dir, "piper")
        
        self._project_dir = os.path.dirname(os.path.dirname(piper_dir))
    
    def _load_voices_json(self):
        
        voices_json = os.path.join(self._voices_dir, "voices.json")
        if os.path.isfile(voices_json):
            with open(voices_json, encoding="utf-8") as f:
                return json.load(f)
        return {"voices": {}, "_meta": {"languages": {}}}
    
    def is_available(self) -> bool:
        
        if os.path.isfile(self._piper_bin) and os.access(self._piper_bin, os.X_OK):
            return True
        
        try:
            subprocess.run(["piper", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def list_voices(self) -> List[Voice]:
        
        voices = []
        voices_dir = self._voices_dir
        
        if not os.path.isdir(voices_dir):
            return voices
        
        voices_json = os.path.join(voices_dir, "voices.json")
        if os.path.isfile(voices_json):
            with open(voices_json) as f:
                data = json.load(f)
                for voice_id, info in data.get("voices", {}).items():
                    model_file = info.get("model_file", f"{voice_id}.onnx")
                    model_path = os.path.join(voices_dir, model_file)
                    if os.path.isfile(model_path):
                        voices.append(Voice(
                            id=voice_id,
                            name=info.get("name", voice_id.replace("_", " ").title()),
                            language=info.get("language", "en"),
                            model_path=model_path,
                        ))
        else:
            for item in os.listdir(voices_dir):
                item_path = os.path.join(voices_dir, item)
                
                if os.path.isdir(item_path):
                    voice_id = item
                    parts = item.split("-")
                    language = parts[0] if parts else "en"
                    
                    voices.append(Voice(
                        id=voice_id,
                        name=item.replace("_", " ").title(),
                        language=language,
                        model_path=item_path,
                    ))
                elif item.endswith(".onnx"):
                    voice_id = item.replace(".onnx", "")
                    parts = item.split("_")
                    language = parts[0] if parts else "en"
                    
                    voices.append(Voice(
                        id=voice_id,
                        name=voice_id.replace("_", " ").title(),
                        language=language,
                        model_path=item_path,
                    ))
        
        return sorted(voices, key=lambda v: v.id)
    
    def list_languages(self) -> List[Language]:
        
        voices = self.list_voices()
        data = self._load_voices_json()
        lang_map = data.get("_meta", {}).get("languages", {})
        languages = {}
        
        for voice in voices:
            if voice.language not in languages:
                languages[voice.language] = Language(
                    code=voice.language,
                    name=lang_map.get(voice.language, voice.language.title()),
                    voice_count=1,
                )
            else:
                languages[voice.language].voice_count += 1
        
        return sorted(languages.values(), key=lambda l: l.code)
    
    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        output: Optional[str] = None,
        **kwargs,
    ) -> str:
        
        if not self.is_available():
            raise TTSError("Piper is not available")
        
        model_path = None
        if voice:
            if os.path.isfile(voice):
                model_path = voice
            else:
                voice_onnx = os.path.join(self._voices_dir, f"{voice}.onnx")
                if os.path.isfile(voice_onnx):
                    model_path = voice_onnx
                else:
                    voice_dir = os.path.join(self._voices_dir, voice)
                    if os.path.isdir(voice_dir):
                        for f in os.listdir(voice_dir):
                            if f.endswith(".onnx"):
                                model_path = os.path.join(voice_dir, f)
                                break
        
        if model_path is None:
            voices = self.list_voices()
            if voices:
                model_path = voices[0].model_path
            else:
                raise TTSError(
                    "Aucune voix Piper installee. "
                    "Executez: python3 py/gvzipvoicesinstallcore.py"
                )
        
        if not os.path.isfile(model_path):
            raise TTSError(
                f"Fichier modele introuvable: {model_path}\n"
                "Executez: python3 py/gvzipvoicesinstallcore.py"
            )
        
        is_temp = output is None
        if is_temp:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                output = f.name
        
        cmd = [self._piper_bin, "--model", model_path, "--output_file", output]
        
        espeak_paths = [
            os.path.join(self._bin_dir, "espeak-ng-data"),  # Local bundled
            "/usr/lib/x86_64-linux-gnu/espeak-ng-data",
            "/usr/share/espeak-ng-data",
            "/usr/local/share/espeak-ng-data",
        ]
        for path in espeak_paths:
            if os.path.isdir(path):
                cmd.extend(["--espeak_data", path])
                break
        
        try:
            result = subprocess.run(
                cmd,
                input=text,
                capture_output=True,
                text=True,
                check=True,
            )
            return output
        except subprocess.CalledProcessError as e:
            if is_temp and os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            raise TTSError(f"Piper synthesis failed: {e.stderr}")
        except FileNotFoundError:
            if is_temp and os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            raise TTSError(f"Piper binary not found at {self._piper_bin}")
        except Exception as e:
            if is_temp and os.path.exists(output):
                try:
                    os.remove(output)
                except:
                    pass
            raise TTSError(f"Piper synthesis failed: {e}")
