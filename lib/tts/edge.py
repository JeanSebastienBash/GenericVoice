"""
Module: tts/edge.py
Purpose: Implements Microsoft Edge TTS engine via edge-tts library. Online/cloud synthesis with 318 voices.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/tts/base.py
"""


import json
import os
import subprocess
from typing import List, Optional

from .base import BaseTTS, Voice, Language, TTSError

class EdgeTTS(BaseTTS):
    
    name = "edge"
    version = "1.0"
    description = "Microsoft Edge cloud TTS (internet required)"
    
    def __init__(self, config=None):
        super().__init__(config)
        self._edge_tts_available = None
        self._voices_dir = os.path.join(os.path.dirname(__file__), "edge", "voices")
        self._voices_json = os.path.join(self._voices_dir, "voices.json")
    
    def _load_voices(self):
        
        voices = {}
        if os.path.isfile(self._voices_json):
            with open(self._voices_json, encoding="utf-8") as f:
                data = json.load(f)
                voices = data.get("voices", {})
        return voices
    
    def is_available(self) -> bool:
        
        if self._edge_tts_available is None:
            try:
                subprocess.run(
                    ["edge-tts", "--version"],
                    capture_output=True,
                    check=True,
                )
                self._edge_tts_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    import edge_tts
                    self._edge_tts_available = True
                except ImportError:
                    self._edge_tts_available = False
        return self._edge_tts_available
    
    def list_voices(self) -> List[Voice]:
        
        voices = []
        
        voices_data = self._load_voices()
        
        for voice_id, info in voices_data.items():
            voices.append(Voice(
                id=voice_id,
                name=info.get("name", voice_id),
                language=info.get("language", "en"),
                model_path=None,
            ))
        
        return sorted(voices, key=lambda v: v.id)
    
    def list_languages(self) -> List[Language]:
        
        voices = self.list_voices()
        languages = {}
        
        for voice in voices:
            if voice.language not in languages:
                languages[voice.language] = Language(
                    code=voice.language,
                    name=voice.language.split("-")[0].upper(),
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
            raise TTSError("Edge TTS is not available. Install: pip install edge-tts")
        
        if voice is None:
            voice = "en-US-AriaNeural"
        
        import tempfile
        
        is_temp = output is None
        if is_temp:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                output = f.name
        
        base_output = output
        if output.endswith(".wav"):
            base_output = output[:-4]
        
        mp3_path = base_output + ".mp3"
        wav_path = base_output + ".wav"
        
        rate = kwargs.get("rate", "+0%")
        pitch = kwargs.get("pitch", "+0Hz")
        volume = kwargs.get("volume", "+0%")
        
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", rate,
            "--pitch", pitch,
            "--volume", volume,
            "--write-media", mp3_path,
            "--text", text,
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            convert_cmd = [
                "ffmpeg", "-y", "-i", mp3_path,
                "-acodec", "pcm_s16le",
                "-ar", "48000",
                "-ac", "1",
                wav_path
            ]
            subprocess.run(convert_cmd, capture_output=True, check=True)
            
            return wav_path
            
        except subprocess.CalledProcessError as e:
            if is_temp and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except:
                    pass
            raise TTSError(f"Edge TTS synthesis failed: {e.stderr}")
        except FileNotFoundError:
            if is_temp and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except:
                    pass
            raise TTSError("edge-tts command not found. Install: pip install edge-tts")
        except Exception as e:
            if is_temp and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except:
                    pass
            raise TTSError(f"Edge TTS synthesis failed: {e}")
        finally:
            if os.path.exists(mp3_path):
                try:
                    os.remove(mp3_path)
                except:
                    pass
