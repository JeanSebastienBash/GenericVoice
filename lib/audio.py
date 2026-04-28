"""
Module: audio.py
Purpose: Handles WAV file reading/writing, audio normalization, fading, mixing, and format conversion. Core audio utilities for synthesis pipeline.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/effects.py, lib/melody.py, lib/synthesis.py
"""


import numpy as np
from scipy import signal
from scipy.io import wavfile
from pathlib import Path
import wave

SAMPLE_RATE = 48000

def envelope_ascending(duration, start_level=0.15, end_level=1.0, curve_exp=1.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    env = start_level + (end_level - start_level) * (t / duration) ** curve_exp
    return env

def soft_clip(x, drive=1.5):
    return np.tanh(x * drive)

def load_wav(wav_path):
    if not Path(wav_path).exists():
        return SAMPLE_RATE, None
    
    try:
        sr, data = wavfile.read(wav_path)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {wav_path}: {e}")
        return SAMPLE_RATE, None
        
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    if sr != SAMPLE_RATE:
        from math import gcd
        g = gcd(sr, SAMPLE_RATE)
        up = SAMPLE_RATE // g
        down = sr // g
        data = signal.resample_poly(data, up, down).astype(np.float32)
    return sr, data

def save_wav_32bit(filepath, data, sample_rate=SAMPLE_RATE):
    
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        data = np.clip(data.astype(np.float32), -1.0, 1.0)
        wavfile.write(str(filepath), sample_rate, data)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde (32-bit): {e}")

def save_wav_16bit(filepath, data, sample_rate=SAMPLE_RATE):
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        data = np.clip(data.astype(np.float32), -1.0, 1.0)
        data_16 = (data * 32767).astype(np.int16)
        with wave.open(str(filepath), 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(data_16.tobytes())
    except Exception as e:
        print(f"Erreur lors de la sauvegarde (16-bit): {e}")

def mix_layers(layers, levels, duration, ascend_start=0.3, ascend_curve=1.5, compression_drive=1.4):
    target_length = int(SAMPLE_RATE * duration)
    padded_layers = []
    for layer in layers:
        if len(layer) < target_length:
            padded = np.zeros(target_length, dtype=np.float32)
            padded[:len(layer)] = layer
            padded_layers.append(padded)
        else:
            padded_layers.append(layer[:target_length])
    
    mix = np.zeros(target_length, dtype=np.float32)
    for layer, level in zip(padded_layers, levels):
        mix += layer * level
    
    final_env = envelope_ascending(duration, ascend_start, 1.0, ascend_curve)
    mix *= final_env
    mix = soft_clip(mix, compression_drive) * 0.85
    
    peak = np.max(np.abs(mix))
    if peak > 0.95:
        mix = mix / peak * 0.95
    
    fade_samples = int(0.05 * SAMPLE_RATE)
    fade_samples = min(fade_samples, len(mix))
    if fade_samples > 0:
        mix[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return mix

def center_audio(audio, target_duration, start_time, fade_in_ms=50, fade_out_ms=80):
    target_length = int(SAMPLE_RATE * target_duration)
    centered = np.zeros(target_length, dtype=np.float32)
    start_pos = int(start_time * SAMPLE_RATE)
    if start_pos >= target_length:
        return centered
        
    end_pos = min(start_pos + len(audio), target_length)
    audio_trimmed = audio[:end_pos - start_pos]
    if len(audio_trimmed) == 0:
        return centered
        
    fade_in_samples = int(fade_in_ms * SAMPLE_RATE / 1000)
    fade_out_samples = int(fade_out_ms * SAMPLE_RATE / 1000)
    
    if fade_in_samples > 0 and fade_in_samples < len(audio_trimmed):
        audio_trimmed[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    if fade_out_samples > 0 and fade_out_samples < len(audio_trimmed):
        audio_trimmed[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    
    centered[start_pos:end_pos] = audio_trimmed
    return centered

def normalize(audio, target_peak=0.85):
    peak = np.max(np.abs(audio))
    if peak > 0:
        return audio / peak * target_peak
    return audio

def time_array(duration):
    return np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
