"""
Module: config.py
Purpose: Defines GVConfig, AudioParams, MelodyParams, VoiceEffectParams dataclasses. Manages CLI parameter conversion, validation, and configuration state.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/param_validator.py, lib/player.py, lib/synthesis.py
"""


import os
from dataclasses import dataclass, field
from typing import Optional
import player as player_lib

DEFAULT_TTS = "piper"
DEFAULT_MODE = "generate"
DEFAULT_LAUNCHER = "genericmenu"
DEFAULT_SYSTEM_OS = "ubuntu"

CORE_PIPER_VOICES = [
    "fr_FR-siwis-medium",
    "en_US-amy-medium",
    "es_ES-sharvard-medium",
    "it_IT-paola-medium",
    "de_DE-mls-medium"
]

def get_default_player():
    return player_lib.get_default_player()

def get_available_players():
    return player_lib.get_available_players()

@dataclass
class VoiceEffectParams:
    delay_ms: int = 120
    decay: float = 0.35
    count: int = 3
    vibrato_rate: float = 5.0
    vibrato_depth: float = 5.0
    reverb_room: float = 0.5
    reverb_damping: float = 0.5

@dataclass
class MelodyParams:
    root_note: str = "C"
    chord_type: str = "major"
    chord_voicing: str = "close"
    chord_filter: int = 3000
    pad_waveform: str = "sine"
    pad_harmonics: int = 3

@dataclass
class PercussionParams:
    timpani_main: int = 70
    timpani_mid: int = 80
    timpani_intro: int = 90
    timpani_decay: float = 5.0
    timpani_noise: float = 0.3
    hihat_density: float = 0.5
    hihat_cutoff: int = 8000
    perc_pattern: str = "straight"
    final_hit_delay: float = 0.82

@dataclass
class BassParams:
    bass_type: str = "sine"
    bass_filter: int = 300
    bass_saturation: float = 1.5
    bass_note_style: str = "root"

@dataclass
class MixParams:
    voice: float = 0.6
    chord: float = 0.25
    perc: float = 0.30
    bass: float = 0.20
    ascend_curve: float = 1.5
    ascend_start: float = 0.30
    compression_drive: float = 1.4

@dataclass
class eSpeakParams:
    variant: int = 1
    pitch: int = 50
    speed: int = 140

@dataclass
class AudioParams:
    wav_format: str = "16-bit"
    normalize: bool = False
    normalize_peak: float = 0.85
    center_start_time: float = 0.5
    fade_in_ms: int = 50
    fade_out_ms: int = 80
    wait_finish: bool = False

class Config:
    def __init__(self):
        self.tts = DEFAULT_TTS
        self.mode = DEFAULT_MODE
        self.launcher = DEFAULT_LAUNCHER
        self.system_os = DEFAULT_SYSTEM_OS
        self.auto_fix = False
        
        self.text = ""
        self.voice = ""
        self.duration = "auto"
        self.output = ""
        
        self.voice_toggle = False
        self.voice_effect_name = ""
        self.melody_toggle = False
        
        self.player = get_default_player()
        self.auto_play = False
        self.wait_finish = False
        
        self.demo_lang = "FR"
        
        self.voice_effect = VoiceEffectParams()
        self.melody = MelodyParams()
        self.percussion = PercussionParams()
        self.bass = BassParams()
        self.mix = MixParams()
        self.espeak = eSpeakParams()
        self.audio = AudioParams()
    
    def is_blocked(self) -> bool:
        return self.mode != "generate"
    
    def reset_to_defaults(self):
        
        self.tts = DEFAULT_TTS
        self.mode = DEFAULT_MODE
        self.launcher = DEFAULT_LAUNCHER
        self.system_os = DEFAULT_SYSTEM_OS
        self.auto_fix = False
        self.text = ""
        self.voice = ""
        self.duration = "auto"
        self.output = ""
        self.voice_toggle = False
        self.voice_effect_name = ""
        self.melody_toggle = False
        self.player = get_default_player()
        self.auto_play = False
        self.demo_lang = "FR"
        self.voice_effect = VoiceEffectParams()
        self.melody = MelodyParams()
        self.percussion = PercussionParams()
        self.bass = BassParams()
        self.mix = MixParams()
        self.espeak = eSpeakParams()
        self.audio = AudioParams()
    
    def get_display_info(self) -> dict:
        tts_display = self.tts
        if not self.tts:
            tts_display = "piper (default)"
        
        mode_display = self.mode
        if self.is_blocked():
            mode_display += " [BLOCKED]"
        
        voice_toggle = "ON" if self.voice_toggle else "off"
        
        effect_display = self.voice_effect_name if self.voice_effect_name else "none"
        
        melody_info = "ON" if self.melody_toggle else "OFF"
        
        text_display = self.text if self.text else "default"
        if len(text_display) > 30:
            text_display = text_display[:27] + "..."
        
        voice_display = self.voice if self.voice else "auto"
        
        duration_display = self.duration if self.duration else "auto"
        
        output_display = self.output if self.output else "auto"
        
        player_display = self.player
        if not self.player:
            player_display = get_default_player()
        
        auto_play_display = "ON" if self.auto_play else "off"
        
        wait_finish_display = "ON" if self.audio.wait_finish else "off"
        
        normalize_display = "ON" if self.audio.normalize else "off"
        
        fade_in_display = f"{self.audio.fade_in_ms}ms"
        fade_out_display = f"{self.audio.fade_out_ms}ms"
        
        wav_format_display = self.audio.wav_format
        
        return {
            "tts": tts_display,
            "mode": mode_display,
            "voice_toggle": voice_toggle,
            "voice_effect": effect_display,
            "melody_info": melody_info,
            "text": text_display,
            "voice": voice_display,
            "duration": duration_display,
            "output": output_display,
            "player": player_display,
            "auto_play": auto_play_display,
            "wait_finish": wait_finish_display,
            "normalize": normalize_display,
            "fade_in": fade_in_display,
            "fade_out": fade_out_display,
            "wav_format": wav_format_display,
            "blocked": self.is_blocked(),
        }
    
    def build_command(self) -> str:
        cmd = f"python3 gv.py --mode {self.mode} --tts {self.tts}"
        
        if self.voice_toggle:
            cmd += " --voice-effect"
            if self.voice_effect_name:
                cmd += f" {self.voice_effect_name}"
        
        if self.melody_toggle:
            cmd += " --melody"
        
        if self.text:
            cmd += f' --text "{self.text}"'
        
        if self.voice:
            cmd += f" --voice {self.voice}"
        
        if self.duration and self.duration != "auto":
            cmd += f" --duration {self.duration}"
        
        if self.output:
            cmd += f" --output {self.output}"
        
        if self.auto_play:
            cmd += " --auto-play"
            if self.player:
                cmd += f" --player {self.player}"
        
        if self.audio.wav_format and self.audio.wav_format != "16-bit":
            cmd += f" --wav-format {self.audio.wav_format}"
        
        if self.audio.normalize:
            cmd += " --normalize"
        
        if self.auto_play and self.audio.wait_finish:
            cmd += " --wait-finish"
        
        if self.audio.fade_in_ms != 50:
            cmd += f" --fade-in {self.audio.fade_in_ms}"
        
        if self.audio.fade_out_ms != 80:
            cmd += f" --fade-out {self.audio.fade_out_ms}"
        
        return cmd

config = Config()
