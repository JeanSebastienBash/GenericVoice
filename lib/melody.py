"""
Module: melody.py
Purpose: Generates procedural background music with chord progressions, percussion, and bass layers. Complements voice synthesis with melody.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/audio.py, lib/synthesis.py
"""


import numpy as np
from scipy import signal

SAMPLE_RATE = 48000
DURATION = 5.0

def make_waveform(freq, duration, waveform='sine', harmonics=3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    wave = np.zeros_like(t)
    harmonics = max(1, int(harmonics))
    for h in range(1, harmonics + 1):
        amp = 1.0 / h
        h_freq = freq * h
        if waveform == 'sine':
            wave += np.sin(2 * np.pi * h_freq * t) * amp
        elif waveform == 'triangle':
            wave += signal.sawtooth(2 * np.pi * h_freq * t, width=0.5) * amp
        elif waveform == 'saw':
            wave += signal.sawtooth(2 * np.pi * h_freq * t, width=1.0) * amp
        else:
            wave += np.sin(2 * np.pi * h_freq * t) * amp
    peak = np.max(np.abs(wave))
    if peak > 0:
        wave = wave / peak
    return wave

def build_chord(root, chord_type, duration, waveform='sine', harmonics=3):
    intervals = {'major': [1.0, 5/4, 3/2], 'minor': [1.0, 6/5, 3/2],
                 'sus2': [1.0, 9/8, 3/2], 'sus4': [1.0, 4/3, 3/2]}
    ratios = intervals.get(chord_type, intervals['major'])
    chord = np.zeros(int(SAMPLE_RATE * duration), dtype=np.float32)
    
    for i, ratio in enumerate(ratios):
        freq = root * ratio
        amp = 1.0 / (i + 1)
        tone = make_waveform(freq, duration, waveform, harmonics)
        chord[:len(tone)] += tone[:len(chord)] * amp
    return chord

def generate_chord_layer(root_freq=261.63, chord_type="major", duration=DURATION,
                        waveform="sine", harmonics=3, chorus_depth_ms=3.0,
                        filter_cutoff=3000, ascend_start=0.3, ascend_curve=1.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    env = ascend_start + (1.0 - ascend_start) * (t / duration) ** ascend_curve
    
    chords = np.zeros(int(SAMPLE_RATE * duration), dtype=np.float32)
    chord1_dur = duration / 2
    chord1 = build_chord(root_freq, chord_type, chord1_dur, waveform, harmonics)
    second_root = root_freq * 3/2
    chord2_dur = duration / 2
    chord2 = build_chord(second_root, chord_type, chord2_dur, waveform, harmonics)
    
    chords[:len(chord1)] = chord1
    chords[len(chord1):len(chord1) + len(chord2)] = chord2
    chords *= env
    
    detuned = np.zeros_like(chords)
    shift = int(chorus_depth_ms / 1000 * SAMPLE_RATE)
    shift = max(1, shift)
    detuned[shift:] = chords[:-shift] * 0.3
    chords += detuned
    
    cutoff = filter_cutoff / (SAMPLE_RATE / 2)
    cutoff = min(cutoff, 0.99)
    b, a = signal.butter(4, cutoff, btype='low')
    chords = signal.lfilter(b, a, chords)
    
    peak = np.max(np.abs(chords))
    if peak > 0:
        chords = chords / peak * 0.45
    return chords.astype(np.float32)

def generate_timpani_hit(start_time, duration, freq, decay_rate, noise_amount, target_duration=None):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    hit = (1.0 * np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2 * t) +
           0.2 * np.sin(2 * np.pi * freq * 3 * t) + 0.1 * np.sin(2 * np.pi * freq * 4 * t))
    noise = np.random.randn(len(t)) * noise_amount
    b, a = signal.butter(6, 500 / (SAMPLE_RATE / 2), btype='low')
    noise = signal.lfilter(b, a, noise)
    hit += noise
    env = np.exp(-decay_rate * t / duration)
    hit *= env
    
    if target_duration is None:
        target_duration = duration
    result = np.zeros(int(SAMPLE_RATE * target_duration), dtype=np.float32)
    start_sample = int(start_time * SAMPLE_RATE)
    if start_sample >= len(result):
        return result
    end_sample = min(start_sample + len(hit), len(result))
    copy_len = min(len(hit), end_sample - start_sample)
    if copy_len > 0:
        result[start_sample:start_sample + copy_len] = hit[:copy_len]
    return result

def generate_hihat(start_time, duration, cutoff, target_duration=None):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.randn(len(t))
    cutoff_norm = cutoff / (SAMPLE_RATE / 2)
    cutoff_norm = min(cutoff_norm, 0.99)
    b, a = signal.butter(4, cutoff_norm, btype='high')
    noise = signal.lfilter(b, a, noise)
    env = np.exp(-50 * t / duration)
    noise *= env
    
    if target_duration is None:
        target_duration = duration
    result = np.zeros(int(SAMPLE_RATE * target_duration), dtype=np.float32)
    start_sample = int(start_time * SAMPLE_RATE)
    if start_sample >= len(result):
        return result
    end_sample = min(start_sample + len(noise), len(result))
    copy_len = min(len(noise), end_sample - start_sample)
    if copy_len > 0:
        result[start_sample:start_sample + copy_len] = noise[:copy_len]
    return result

def generate_percussion_layer(duration=DURATION, timpani_main=70, timpani_mid=80,
                             timpani_intro=90, timpani_decay=5.0, timpani_noise=0.3,
                             hihat_density=0.5, hihat_cutoff=8000, pattern="straight",
                             final_hit_delay=0.82, rng=None):
    if rng is None:
        rng = np.random.RandomState()
    
    perc = np.zeros(int(SAMPLE_RATE * duration), dtype=np.float32)
    timpani_final = generate_timpani_hit(final_hit_delay, 0.8, timpani_main, timpani_decay, timpani_noise, target_duration=duration)
    perc += timpani_final * 1.0
    
    mid_time = rng.uniform(0.3, 0.5) * duration
    timpani_mid = generate_timpani_hit(mid_time, 0.6, timpani_mid, timpani_decay * 0.8, timpani_noise, target_duration=duration)
    perc += timpani_mid * 0.5
    
    intro_time = rng.uniform(0.02, 0.12) * duration
    timpani_intro = generate_timpani_hit(intro_time, 0.4, timpani_intro, timpani_decay * 0.6, timpani_noise, target_duration=duration)
    perc += timpani_intro * 0.3
    
    if hihat_density <= 0:
        beats = []
    elif pattern == 'straight':
        beats = np.arange(0, duration, hihat_density)
    elif pattern == 'syncopated':
        beats = np.arange(0.125, duration, hihat_density)
    else:
        beats = np.arange(0, duration, hihat_density * 2)
    
    for beat_time in beats:
        if beat_time < duration:
            hihat_dur = rng.uniform(0.03, 0.07)
            hi_hat = generate_hihat(beat_time, hihat_dur, hihat_cutoff, target_duration=duration)
            perc[:len(hi_hat)] += hi_hat[:len(perc)] * rng.uniform(0.08, 0.20)
    return perc.astype(np.float32)

def generate_bass_note(freq, duration, waveform='sine'):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    if waveform == 'sine':
        return (0.6 * np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t) +
                0.15 * np.sin(2 * np.pi * freq * 3 * t))
    elif waveform == 'triangle':
        return signal.sawtooth(2 * np.pi * freq * t, width=0.5) * 0.8
    elif waveform == 'square_soft':
        sq = signal.square(2 * np.pi * freq * t)
        b, a = signal.butter(4, 400 / (SAMPLE_RATE / 2), btype='low')
        return signal.lfilter(b, a, sq) * 0.7
    return np.sin(2 * np.pi * freq * t)

def generate_bass_layer(root_freq=261.63, duration=DURATION, bass_type="sine",
                       filter_cutoff=300, saturation=1.5, note_style="root",
                       ascend_start=0.08, ascend_curve=1.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    env = ascend_start + (0.9 - ascend_start) * (t / duration) ** ascend_curve
    
    bass = np.zeros(int(SAMPLE_RATE * duration), dtype=np.float32)
    bass_root = root_freq / 2
    bass_fifth = bass_root * 3/2
    
    dur1 = duration / 2
    dur2 = duration / 2
    
    if note_style == 'root':
        bass_note1 = generate_bass_note(bass_root, dur1, bass_type)
        bass_note2 = generate_bass_note(bass_fifth, dur2, bass_type)
    elif note_style == 'walking':
        bass_note1 = generate_bass_note(bass_root, dur1, bass_type)
        bass_note2 = generate_bass_note(bass_root * 4/3, dur2, bass_type)
    else:
        bass_note1 = generate_bass_note(bass_root, dur1, bass_type)
        bass_note2 = generate_bass_note(bass_root, dur2, bass_type)
    
    bass[:len(bass_note1)] = bass_note1
    bass[len(bass_note1):len(bass_note1) + len(bass_note2)] = bass_note2
    bass *= env
    
    cutoff = filter_cutoff / (SAMPLE_RATE / 2)
    cutoff = min(cutoff, 0.99)
    b, a = signal.butter(6, cutoff, btype='low')
    bass = signal.lfilter(b, a, bass)
    bass = np.tanh(bass * saturation) * 0.6
    
    peak = np.max(np.abs(bass))
    if peak > 0:
        bass = bass / peak * 0.5
    return bass.astype(np.float32)
