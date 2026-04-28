"""
Module: piper_processor.py
Purpose: Post-processing for Piper TTS output. Handles audio format conversion and normalization specific to Piper engine.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/tts/piper.py, lib/audio.py
"""


import os
import numpy as np
from scipy.io import wavfile

PIPER_SAMPLE_RATE = 22050

def process_piper_audio(wav_file, output_dir="output", base_name=None,
                         fade_in_ms=50, fade_out_ms=80):
    
    os.makedirs(output_dir, exist_ok=True)
    
    if base_name is None:
        import time
        base_name = f"gv_{time.strftime('%Y%m%d_%H%M%S')}"
    
    sr, data = wavfile.read(wav_file)
    
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val * 0.9
    
    fade_in_samples = int(fade_in_ms * sr / 1000)
    fade_out_samples = int(fade_out_ms * sr / 1000)
    
    if fade_in_samples > 0 and fade_in_samples < len(data):
        data[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    if fade_out_samples > 0 and fade_out_samples < len(data):
        data[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    
    voice_path = os.path.join(output_dir, f"{base_name}_voice.wav")
    data_16 = (data * 32767).astype(np.int16)
    
    import wave
    with wave.open(voice_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(data_16.tobytes())
    
    mix_path = os.path.join(output_dir, f"{base_name}_mix.wav")
    with wave.open(mix_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(data_16.tobytes())
    
    return {
        "voice": voice_path,
        "mix": mix_path,
        "sample_rate": sr,
        "duration": len(data) / sr,
    }
