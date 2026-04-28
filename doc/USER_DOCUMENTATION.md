# User Guide - Generic Voice v1.0.2

Complete guide for using Generic Voice text-to-speech system.

## Table of Contents

1. [What is Generic Voice?](#what-is-generic-voice)
2. [Installation](#installation)
3. [Understanding TTS Engines](#understanding-tts-engines)
4. [Basic Usage](#basic-usage)
5. [Command Reference](#command-reference)
6. [Advanced Features](#advanced-features)
7. [Output Files](#output-files)
8. [Troubleshooting](#troubleshooting)

---

## What is Generic Voice?

Generic Voice is a command-line tool that provides unified access to multiple Text-to-Speech (TTS) engines. It allows you to convert text into speech using different synthesis technologies from a single interface.

**Key Features:**
- Support for 3 TTS engines: Piper (offline), Edge TTS (online), eSpeak (offline)
- Batch processing capabilities
- Audio effects and melody generation (Edge TTS only)
- Multi-track export (stems)
- Cross-platform support (Linux primary)

---

## Installation

### System Requirements

- Operating System: Linux (Ubuntu/Debian recommended)
- Python: Version 3.8 or higher
- Disk Space: 500MB minimum (for Core version)
- Internet: Required only for Edge TTS engine

### Step-by-Step Setup

1. **Download the repository:**
```bash
git clone https://github.com/JeanSebastienBash/GenericVoice.git
cd GenericVoice
```

2. **Create a Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install required packages:**
```bash
pip install -r requirements.txt
```

**Fix missing system dependencies:**
```bash
sudo python3 py/gv.py --auto-fix
```

**Note for GUI (Flet 0.84):** The GUI requires `flet==0.84.0` and `flet-web==0.84.0` which are included in requirements.txt. To run the GUI:
```bash
# Desktop mode
python3 py/gvflet.py

# Web browser mode (optional)
python3 py/gvflet.py --web --port 8555
```

4. **Install voice models:**
```bash
python3 py/gvcorevoices.py
```

5. **Verify installation:**
```bash
python3 py/gv.py --list-engines
```

---

## Understanding TTS Engines

Generic Voice provides access to three different TTS engines, each with specific characteristics:

### Piper
- **Type**: Neural network synthesis
- **Connection**: Offline (no internet required)
- **Quality**: High-quality natural speech
- **Speed**: Fast
- **Use case**: Production work, consistent output
- **Voice count**: 174 models available (Core includes 5, Full includes all 174)

### Edge TTS
- **Type**: Cloud-based neural synthesis (Microsoft Azure)
- **Connection**: Online (internet required)
- **Quality**: Excellent quality, most natural voices
- **Speed**: Network-dependent
- **Use case**: High-quality productions, effects, melody
- **Voice count**: 100+ voices in multiple languages

### eSpeak
- **Type**: Formant synthesis
- **Connection**: Offline (no internet required)
- **Quality**: Robotic/mechanical sound
- **Speed**: Very fast
- **Use case**: Testing, quick previews, 100+ languages
- **Voice count**: 100+ languages supported

---

## Basic Usage

### Simple Synthesis

Generate speech with default settings:

```bash
python3 py/gv.py --tts piper --text "Hello, this is a test."
```

Output files are created in the `output/` directory.

### Selecting a Specific Voice

```bash
python3 py/gv.py --tts piper --voice fr_FR-siwis-medium --text "Bonjour le monde"
```

### Using Different Engines

**Piper (offline):**
```bash
python3 py/gv.py --tts piper --text "Hello world"
```

**Edge TTS (online):**
```bash
python3 py/gv.py --tts edge --voice fr-FR-DeniseNeural --text "Bonjour le monde"
```

**eSpeak (offline):**
```bash
python3 py/gv.py --tts espeak --text "Quick test"
```

---

## Command Reference

### Core Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--tts` | Select TTS engine | `--tts piper` |
| `--text` | Text to synthesize | `--text "Hello world"` |
| `--voice` | Voice identifier | `--voice fr_FR-siwis-medium` |
| `--output` | Output filename | `--output audio.wav` |

### Audio Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `--duration` | Target duration (seconds) | auto | integer or "auto" |
| `--wav-format` | Audio bit depth | 16-bit | 16-bit, 32-bit (Edge only) |
| `--fade-in` | Fade in duration (ms) | 50 | integer |
| `--fade-out` | Fade out duration (ms) | 80 | integer |
| `--normalize` | Normalize audio levels | disabled | flag (Edge only) |

### Playback Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--auto-play` | Play audio after generation | `--auto-play` |
| `--player` | Audio player to use | `--player cvlc` |
| `--wait-finish` | Wait for playback to complete | `--wait-finish` |

**Available players:** parole, cvlc, vlc, ffplay, aplay, auto

### Utility Commands

| Command | Description |
|---------|-------------|
| `--list-engines` | List available TTS engines and status |
| `--list-launchers` | List available interface backends |
| `--auto-fix` | Install missing dependencies |
| `--help` | Display help information |

### Usage Examples

**Basic synthesis:**
```bash
python3 py/gv.py --tts piper --text "Hello world"
```

**With specific voice:**
```bash
python3 py/gv.py --tts piper --voice en_US-amy-medium --text "Hello"
```

**With playback:**
```bash
python3 py/gv.py --tts piper --text "Hello" --auto-play --player cvlc
```

**With effects (Edge TTS only):**
```bash
python3 py/gv.py --tts edge --text "Hello" --voice-effect echo
```

**With melody (Edge TTS only):**
```bash
python3 py/gv.py --tts edge --text "Welcome" --melody --duration 30
```

**Full production example:**
```bash
python3 py/gv.py \
  --tts edge \
  --voice en-US-JennyNeural \
  --text "Welcome to our show" \
  --melody \
  --duration 15 \
  --voice-effect reverb \
  --normalize \
  --fade-in 100 \
  --fade-out 200 \
  --auto-play \
  --player cvlc
```

---

## Advanced Features

### Voice Effects (Edge TTS Only)

Available effects:

| Effect | Description |
|--------|-------------|
| `echo` | Adds echo/reverb |
| `vibrato` | Adds pitch modulation |
| `reverb` | Adds room reverberation |

**Usage:**
```bash
python3 py/gv.py --tts edge --text "Test" --voice-effect echo
```

### Melody Generation (Edge TTS Only)

Generate procedural background music with voice:

```bash
python3 py/gv.py --tts edge --text "Intro" --melody --duration 30
```

This creates 5 audio files:
- `*_voice.wav` - Voice track
- `*_chord.wav` - Chord/harmony track
- `*_perc.wav` - Percussion track
- `*_bass.wav` - Bass track
- `*_mix.wav` - Combined mix

### Interactive Mode

Launch the interactive menu:

```bash
python3 py/gv.py
```

or explicitly:

```bash
python3 py/gv.py --launcher genericmenu
```

### GUI Interface

Launch the graphical interface:

```bash
python3 py/gvflet.py
```

---

## Output Files

### File Locations

All generated audio files are saved to the `output/` directory.

### Naming Convention

Files use timestamp prefix: `YYYYMMDD_HHMMSS_<type>.wav`

Example: `20250408_143022_voice.wav`

### File Types

| Suffix | Description | Generated When |
|--------|-------------|----------------|
| `*_voice.wav` | Voice synthesis only | Always |
| `*_mix.wav` | Final mix with melody | With `--melody` |
| `*_chord.wav` | Chord track | With `--melody` |
| `*_perc.wav` | Percussion track | With `--melody` |
| `*_bass.wav` | Bass track | With `--melody` |

### Audio Specifications

- **Format**: WAV (RIFF/WAVE)
- **Sample rate**: 22050 Hz (Piper, eSpeak) or 48000 Hz (Edge)
- **Channels**: Mono
- **Bit depth**: 16-bit (default) or 32-bit (Edge only)

---

## Troubleshooting

### Missing System Dependencies

If Generic Voice fails to start or reports missing libraries, use `--auto-fix`:

```bash
# Auto-fix (detects OS automatically)
sudo python3 py/gv.py --auto-fix

# Specify OS explicitly
sudo python3 py/gv.py --auto-fix --system-os ubuntu
sudo python3 py/gv.py --auto-fix --system-os debian
sudo python3 py/gv.py --auto-fix --system-os fedora
```

> `--auto-fix` is a solo command — it installs system-level packages and exits.
> Run it once after installation, or any time a dependency error occurs.

### Piper Voices Not Installed

**Error:** Voice files not found

**Solution:**
```bash
python3 py/gvcorevoices.py
```

Verify installation:
```bash
ls lib/tts/piper/voices/*.onnx
```

### Edge TTS Connection Error

**Error:** Network or connection errors

**Solution:**
- Verify internet connection
- Check firewall settings
- Use Piper or eSpeak for offline operation

### No Audio Playback

**Error:** Audio generates but doesn't play

**Solution:**

1. Install a media player:
```bash
sudo apt-get install vlc
```

2. Specify player:
```bash
python3 py/gv.py --tts piper --text "Test" --auto-play --player cvlc
```

3. Check audio system:
```bash
aplay -l
```

### Permission Errors

**Solution:**
```bash
chmod +x py/gv.py
chmod +x py/gvflet.py
```

### Python Import Errors

**Solution:**
1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Output Directory Issues

Ensure the `output/` directory exists and is writable:
```bash
mkdir -p output
chmod 755 output
```

---

## Utility Scripts

Generic Voice includes additional utility scripts in the `py/` directory:

### gvcorevoices.py — Core Voices Installer

Installs the 5 Core Piper voices from split ZIP archives.

**Usage:**
```bash
python3 py/gvcorevoices.py
```

**What it does:**
- Extracts `fr_FR-siwis-medium`, `en_US-amy-medium`, `es_ES-sharvard-medium`, `it_IT-paola-medium`, `de_DE-mls-medium`
- Places `.onnx` and `.onnx.json` files in `lib/tts/piper/voices/`
- Archives must be present (downloaded separately or via Git LFS)

**When to use:** After cloning the repository, before first use.

---

### gvdemo.py — Demo Generation Script

Generates sample audio files for available voices.

**Usage:**
```bash
python3 py/gvdemo.py
```

**What it does:**
- Synthesizes a demo text in the appropriate language for each voice
- Generates sample WAV files in `output/demo/`
- Creates `output/demo/demo_errors.log` with any failed voices
- Uses 54 translated TEXTS to match each voice's language
- Takes approximately **1 hour on a good machine**

**Output:**
- `output/demo/demo_piper_*.wav` — Piper voice samples
- `output/demo/demo_edge_*.wav` — Edge voice samples  
- `output/demo/demo_espeak_*.wav` — eSpeak voice samples
- `output/demo/demo_errors.log` — Log of failed syntheses

**When to use:** To generate demo files for the Core Full ZIP package. The ZIP builder checks for ≥550 demo files and includes them if present.

---

### gvappcorefullinstall.py — Core Full ZIP Builder

Creates the `gvcore_v1.0.2_allvoices.zip` distribution package.

**Location:** `py/gv/gvappcorefullinstall.py` (internal script)

**What it does:**
- Packages all 174 Piper voices (`.onnx` + `.onnx.json`)
- Includes all application files (lib/, py/, tests/, doc/)
- **Checks for demo files:** If ≥550 WAV files exist in `output/demo/`, includes them
- Creates empty `output/` and `output/demo/` placeholders

**When to use:** When preparing the Core Full distribution for users.

---

## Quick Reference

```bash
# List engines
python3 py/gv.py --list-engines

# Basic synthesis
python3 py/gv.py --tts piper --text "Hello"

# With voice selection
python3 py/gv.py --tts piper --voice fr_FR-siwis-medium --text "Bonjour"

# With effects
python3 py/gv.py --tts edge --text "Hello" --voice-effect echo

# With melody
python3 py/gv.py --tts edge --text "Hello" --melody

# With playback
python3 py/gv.py --tts piper --text "Hello" --auto-play --player cvlc

# Interactive mode
python3 py/gv.py

# GUI mode
python3 py/gvflet.py
```

---

## Core Full — All 174 Piper Voices

The standard Core installation includes 5 Piper voices (FR, EN, DE, ES, IT).

---

## Additional Resources

- [Technical Documentation](TECHNICAL_DOCUMENTATION.md)

---

*Generic Voice v1.0.2 - User Guide*
*DreamprojectAI - https://dreamproject.online/prj/genericvoice*
