# Generic Voice

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flet 0.84](https://img.shields.io/badge/flet-0.84-purple.svg)](https://flet.dev/)
[![Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()

Text-to-speech synthesis tool providing unified access to multiple TTS engines with CLI and GUI interfaces.

## Overview

Generic Voice is a text-to-speech synthesis platform with command-line and graphical interfaces. It supports three TTS engines:
- **Piper**: Neural synthesis, offline operation, high quality (22kHz)
- **Edge TTS**: Cloud-based neural synthesis, requires internet, excellent quality (48kHz)
- **eSpeak**: Formant synthesis, offline operation, lightweight (22kHz)

## Features

- Multiple TTS engine support (Piper, Edge, eSpeak)
- Audio effects and processing (echo, vibrato, reverb) - Edge TTS only
- Melody and music generation - Edge TTS only
- Multi-track export (stems separation)
- **GUI Interface** (Flet 0.84) with full CLI parameter support
- Interactive CLI mode
- Cross-platform (Linux primary)

## Quick Start

```bash
# Clone repository
git clone https://github.com/JeanSebastienBash/GenericVoice.git
cd GenericVoice

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Auto-install missing system dependencies (requires sudo)
sudo python3 py/gv.py --auto-fix

# With explicit OS target
sudo python3 py/gv.py --auto-fix --system-os ubuntu
sudo python3 py/gv.py --auto-fix --system-os debian

# Install voice models (5 Core voices: FR, EN, DE, ES, IT)
python3 py/gvcorevoices.py

# Generate audio (CLI)
python3 py/gv.py --tts piper --text "Hello world"

# Launch GUI
python3 py/gvflet.py

# Launch GUI in web browser mode
python3 py/gvflet.py --web --port 8555
```

## Usage

```bash
# List available engines
python3 py/gv.py --list-engines

# Simple synthesis
python3 py/gv.py --tts piper --text "Hello world"

# With specific voice
python3 py/gv.py --tts piper --voice fr_FR-siwis-medium --text "Bonjour"

# Using Edge TTS (online)
python3 py/gv.py --tts edge --voice fr-FR-DeniseNeural --text "Bonjour"

# With effects (Edge TTS only)
python3 py/gv.py --tts edge --text "Hello" --voice-effect echo

# With melody generation (Edge TTS only)
python3 py/gv.py --tts edge --text "Welcome" --melody

# Auto-play after generation
python3 py/gv.py --tts piper --text "Hello" --auto-play --player cvlc
```

## Interactive Mode

```bash
python3 py/gv.py
```

## GUI Mode (Flet 0.84)

The GUI provides a graphical interface with 6 tabs covering all CLI parameters:

```bash
# Desktop mode
python3 py/gvflet.py

# Web browser mode
python3 py/gvflet.py --web --port 8555
```

**GUI Tabs:**
1. **TTS Tab**: Engine selection, voice selection, text input
2. **Audio Tab**: Duration, output file, WAV format, normalize, fades
3. **Effects Tab**: Voice effects (echo, vibrato, reverb), melody mode
4. **Playback Tab**: Auto-play, player selection, wait-finish
5. **Advanced Tab**: System OS override, debugging options
6. **Tools Tab**: Voice installation, demo generation, app packaging

## System Requirements

- Linux (Ubuntu/Debian recommended)
- Python 3.8+
- Flet 0.84+ (for GUI)
- 500MB disk space (for voice models)
- Internet connection (for Edge TTS and initial voice downloads)

## Project Structure

```
GenericVoice/
├── py/                        # Entry point scripts
│   ├── gv.py                 # Main CLI
│   ├── gvflet.py             # GUI interface (Flet 0.84)
│   ├── gvcorevoices.py       # Core voices installer (5 languages)
│   └── gvdemo.py             # Demo script
├── lib/                      # Core libraries
│   ├── tts/                  # TTS engine implementations
│   │   ├── piper/           # Piper TTS
│   │   ├── edge/            # Edge TTS
│   │   └── espeak/          # eSpeak TTS
│   ├── audio.py              # Audio processing
│   ├── effects.py            # Voice effects
│   └── ...
├── tests/                    # Test suites
├── output/                   # Generated audio files
├── doc/                      # Documentation
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## TTS Engines

| Engine | Type | Quality | Latency | Voices | Offline |
|--------|------|---------|---------|--------|---------|
| Piper | Neural | High (22kHz) | Fast | Multiple | Yes |
| Edge | Neural | Excellent (48kHz) | Medium | Multiple | No |
| eSpeak | Formant | Robotic (22kHz) | Instant | Multiple | Yes |

## Documentation

- [User Guide](doc/USER_DOCUMENTATION.md) - Complete usage guide
- [Technical Documentation](doc/TECHNICAL_DOCUMENTATION.md) - API and architecture

## License

Generic Voice Core: MIT License

Third-party components:
- Edge TTS: MIT License
- Piper: MIT License
- eSpeak: GPLv3 License

---

Made by [DreamprojectAI](https://dreamproject.online)

[Website](https://dreamproject.online/prj/genericvoice) •
[Documentation](doc/USER_DOCUMENTATION.md) •
[Issues](https://github.com/JeanSebastienBash/GenericVoice/issues)