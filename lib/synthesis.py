"""
Module: synthesis.py
Purpose: Core synthesis coordinator. Orchestrates TTS engine calls, audio processing, effects application, and melody generation.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/tts/__init__.py, lib/audio.py, lib/effects.py, lib/melody.py, lib/player.py
"""


import os
import numpy as np
from scipy import signal as sp_signal
import scipy

import audio
import effects
import melody

SAMPLE_RATE = 48000

def resample_audio(data, orig_sr, target_sr):
    
    if orig_sr == target_sr:
        return data
    
    from math import gcd
    g = gcd(orig_sr, target_sr)
    up = target_sr // g
    down = orig_sr // g
    
    return sp_signal.resample_poly(data, up, down).astype(np.float32)

def synthesize_complete(
    tts_engine,
    text: str,
    voice: str = None,
    output_dir: str = "output",
    base_name: str = None,
    voice_effect: str = None,
    voice_effect_params: dict = None,
    melody_enabled: bool = False,
    melody_params: dict = None,
    percussion_params: dict = None,
    bass_params: dict = None,
    mix_params: dict = None,
    normalize: bool = False,
    fade_in_ms: int = 50,
    fade_out_ms: int = 80,
):
    
    os.makedirs(output_dir, exist_ok=True)
    
    if base_name is None:
        import time
        base_name = f"gv_{time.strftime('%Y%m%d_%H%M%S')}"
    
    tts_name = getattr(tts_engine, 'name', 'unknown')
    
    if tts_name == 'piper':
        import piper_processor
        wav_file = tts_engine.synthesize(text=text, voice=voice, output=None)
        return piper_processor.process_piper_audio(
            wav_file,
            output_dir=output_dir,
            base_name=base_name,
            fade_in_ms=fade_in_ms,
            fade_out_ms=fade_out_ms,
        )
    
    if tts_name == 'espeak':
        import espeak_processor
        wav_file = tts_engine.synthesize(text=text, voice=voice, output=None)
        return espeak_processor.process_espeak_audio(
            wav_file,
            output_dir=output_dir,
            base_name=base_name,
            fade_in_ms=fade_in_ms,
            fade_out_ms=fade_out_ms,
        )
    
    voice_effect_params = voice_effect_params or {}
    melody_params = melody_params or {}
    percussion_params = percussion_params or {}
    bass_params = bass_params or {}
    mix_params = mix_params or {}
    
    wav_file = tts_engine.synthesize(text=text, voice=voice, output=None)
    
    sr, voice_data = audio.load_wav(wav_file)
    if voice_data is None:
        raise RuntimeError(f"Failed to load voice audio: {wav_file}")
    
    if sr != SAMPLE_RATE:
        voice_data = resample_audio(voice_data, sr, SAMPLE_RATE)
    
    if len(voice_data.shape) > 1:
        voice_data = voice_data.mean(axis=1)
    
    voice_data = voice_data.astype(np.float32)
    
    if np.max(np.abs(voice_data)) > 0:
        voice_data = voice_data / np.max(np.abs(voice_data)) * 0.9
    
    duration = len(voice_data) / SAMPLE_RATE
    
    if voice_effect and voice_effect != "none":
        voice_data = effects.apply_voice_effect(
            voice_data,
            effect_name=voice_effect,
            delay_ms=voice_effect_params.get("delay_ms", 120),
            decay=voice_effect_params.get("decay", 0.35),
            count=voice_effect_params.get("count", 3),
            vibrato_rate=voice_effect_params.get("vibrato_rate", 5.0),
            vibrato_depth=voice_effect_params.get("vibrato_depth", 5.0),
        )
    
    voice_data = effects.fade_in_out(voice_data, fade_in_ms, fade_out_ms)
    
    stems = {}
    stems["voice"] = voice_data
    
    if melody_enabled:
        root_note = melody_params.get("root_note", "C")
        chord_type = melody_params.get("chord_type", "major")
        chord_voicing = melody_params.get("chord_voicing", "close")
        pad_waveform = melody_params.get("pad_waveform", "sine")
        
        note_freqs = {
            "C": 261.63, "D": 293.66, "E": 329.63, "F": 349.23,
            "G": 392.00, "A": 440.00, "B": 493.88
        }
        root_freq = note_freqs.get(root_note, 261.63)
        
        chord_data = melody.generate_chord_layer(
            root_freq=root_freq,
            chord_type=chord_type,
            duration=duration,
            waveform=pad_waveform,
        )
        chord_data = chord_data[:len(voice_data)] if len(chord_data) > len(voice_data) else np.pad(chord_data, (0, len(voice_data) - len(chord_data)))
        stems["chord"] = chord_data.astype(np.float32)
        
        timpani_main = percussion_params.get("timpani_main", 70)
        hihat_density = percussion_params.get("hihat_density", 0.5)
        perc_pattern = percussion_params.get("perc_pattern", "straight")
        
        perc_data = melody.generate_percussion_layer(
            duration=duration,
            timpani_main=timpani_main,
            hihat_density=hihat_density,
            pattern=perc_pattern,
        )
        perc_data = perc_data[:len(voice_data)] if len(perc_data) > len(voice_data) else np.pad(perc_data, (0, len(voice_data) - len(perc_data)))
        stems["perc"] = perc_data.astype(np.float32)
        
        bass_type = bass_params.get("bass_type", "sine")
        bass_note_style = bass_params.get("bass_note_style", "root")
        
        bass_data = melody.generate_bass_layer(
            root_freq=root_freq,
            duration=duration,
            bass_type=bass_type,
            note_style=bass_note_style,
        )
        bass_data = bass_data[:len(voice_data)] if len(bass_data) > len(voice_data) else np.pad(bass_data, (0, len(voice_data) - len(bass_data)))
        stems["bass"] = bass_data.astype(np.float32)
    
    voice_level = mix_params.get("voice", 0.6)
    chord_level = mix_params.get("chord", 0.25)
    perc_level = mix_params.get("perc", 0.30)
    bass_level = mix_params.get("bass", 0.20)
    
    mix = voice_data * voice_level
    
    if "chord" in stems:
        mix += stems["chord"] * chord_level
    if "perc" in stems:
        mix += stems["perc"] * perc_level
    if "bass" in stems:
        mix += stems["bass"] * bass_level
    
    if normalize:
        mix = audio.normalize(mix)
    
    peak = np.max(np.abs(mix))
    if peak > 0.95:
        mix = mix / peak * 0.95
    
    paths = {}
    
    mix_path = os.path.join(output_dir, f"{base_name}_mix.wav")
    audio.save_wav_16bit(mix_path, mix, SAMPLE_RATE)
    paths["mix"] = mix_path
    
    for stem_name, stem_data in stems.items():
        if normalize:
            stem_data = audio.normalize(stem_data)
        stem_path = os.path.join(output_dir, f"{base_name}_{stem_name}.wav")
        audio.save_wav_16bit(stem_path, stem_data, SAMPLE_RATE)
        paths[stem_name] = stem_path
    
    try:
        os.remove(wav_file)
    except:
        pass
    
    return paths
