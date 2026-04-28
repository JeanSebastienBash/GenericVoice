"""
Module: effects.py
Purpose: Implements echo, vibrato, and reverb voice effects using scipy signal processing. Applied to synthesized voice output.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/audio.py, lib/synthesis.py
"""


import numpy as np
from scipy import signal

SAMPLE_RATE = 48000

def add_echo(audio, delay_ms=120, decay=0.35, count=3):
    delay_samples = int(SAMPLE_RATE * delay_ms / 1000)
    total_length = len(audio) + delay_samples * count
    result = np.zeros(total_length, dtype=np.float32)
    
    for i in range(count + 1):
        offset = delay_samples * i
        gain = decay ** i
        end = min(offset + len(audio), total_length)
        result[offset:end] += audio[:end - offset] * gain
    
    return result[:len(audio)]

def add_vibrato(audio, rate=5.0, depth=5.0):
    t = np.arange(len(audio)) / SAMPLE_RATE
    modulation_ms = depth + depth * np.sin(2 * np.pi * rate * t)
    delay_samples = (modulation_ms * SAMPLE_RATE / 1000).astype(int)
    delay_samples = np.clip(delay_samples, 1, len(audio) - 1)
    
    result = np.zeros_like(audio)
    for i in range(len(audio)):
        delay = delay_samples[i]
        if i >= delay:
            result[i] = audio[i - delay]
        else:
            result[i] = audio[i]
    return result

def add_reverb(audio, room_size=0.5, damping=0.5):
    delays = [0.0297, 0.0371, 0.0411, 0.0437]
    delays = [int(d * SAMPLE_RATE * room_size) for d in delays]
    
    result = audio.copy()
    for delay in delays:
        if delay > 0 and delay < len(audio):
            delayed = np.zeros_like(audio)
            delayed[delay:] = audio[:-delay]
            b, a = signal.butter(2, damping, btype='low')
            delayed = signal.lfilter(b, a, delayed)
            result += delayed * 0.3
    
    result /= 1.0 + 0.3 * len(delays)
    return result

def apply_voice_effect(audio, effect_name="echo", delay_ms=120, decay=0.35, count=3,
                       vibrato_rate=5.0, vibrato_depth=5.0, reverb_room=0.5, reverb_damping=0.5):
    if effect_name == "none" or effect_name == "":
        return audio
    
    if effect_name == "echo":
        return add_echo(audio, delay_ms, decay, count)
    if effect_name == "vibrato":
        return add_vibrato(audio, vibrato_rate, vibrato_depth)
    if effect_name == "reverb":
        return add_reverb(audio, reverb_room, reverb_damping)
    return audio

def fade_in_out(audio, fade_in_ms=30, fade_out_ms=150):
    result = audio.copy()
    fade_in_samples = int(SAMPLE_RATE * fade_in_ms / 1000)
    if fade_in_samples > 0 and fade_in_samples < len(result):
        result[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    
    fade_out_samples = int(SAMPLE_RATE * fade_out_ms / 1000)
    if fade_out_samples > 0 and fade_out_samples < len(result):
        result[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    return result
