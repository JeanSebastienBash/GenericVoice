# Technical Documentation - Generic Voice v1.0.2

This document provides comprehensive technical information for developers and advanced users.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Modules](#core-modules)
4. [TTS Engines](#tts-engines)
5. [CLI Reference](#cli-reference)
6. [Configuration System](#configuration-system)
7. [Audio Pipeline](#audio-pipeline)
8. [Testing Framework](#testing-framework)
9. [Development Guide](#development-guide)

---

## Architecture Overview

Generic Voice follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface                      │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ CLI (gv) │  │ Interactive  │  │ GUI (gvflet)    │   │
│  │          │  │ (genericmenu)│  │                 │   │
│  └────┬─────┘  └──────┬───────┘  └────────┬────────┘   │
└───────┼───────────────┼───────────────────┼────────────┘
        │               │                   │
        └───────────────┼───────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 Configuration Layer                      │
│              (config.py, param_validator.py)             │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                Synthesis Pipeline                        │
│              (synthesis.py, audio.py)                    │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   TTS Engines                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Piper       │  │ Edge TTS    │  │ eSpeak          │  │
│  │ (offline)   │  │ (online)    │  │ (lightweight)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
src/
├── py/                          # Entry point scripts
│   ├── gv.py                         # Main CLI
│   ├── gvflet.py                     # Flet GUI interface (6 tabs)
│   ├── gvcorevoices.py               # Core voices installer (5 languages)
│   └── gvdemo.py                     # Demo script
│
├── lib/                         # Core library modules
│   ├── config.py               # Configuration dataclasses
│   ├── param_validator.py      # CLI parameter validation
│   ├── synthesis.py            # Main synthesis pipeline
│   ├── audio.py                # WAV I/O and processing
│   ├── effects.py              # Audio effects (echo, vibrato, reverb)
│   ├── melody.py               # Procedural audio generation
│   ├── player.py               # Audio playback abstraction
│   ├── errors.py               # Error handling and messages
│   ├── piper_processor.py      # Piper-specific processing
│   ├── espeak_processor.py     # eSpeak-specific processing
│   │
│   ├── tts/                    # TTS engine implementations
│   │   ├── __init__.py         # Engine factory
│   │   ├── base.py             # Abstract base class
│   │   ├── edge.py             # Microsoft Edge TTS
│   │   ├── piper.py            # Piper TTS
│   │   ├── espeak.py           # eSpeak TTS
│   │   ├── edge/               # Edge voices catalog
│   │   ├── piper/              # Piper voices and binaries
│   │   └── espeak/             # eSpeak voices catalog
│   │
│   ├── ihm/                    # User interface backends
│   │   ├── __init__.py
│   │   ├── generic.py          # Base UI class
│   │   └── genericmenu.py      # Interactive menu
│   │
│   └── system/                 # OS detection and adaptation
│       ├── detect.py           # Platform detection
│       └── adapt.py            # OS-specific adaptations
│
├── tests/                       # Test suites (~150 tests)
│   ├── run_all_tests.py        # Test runner
│   ├── test_001_cli_args/      # CLI argument tests
│   ├── test_002_config/        # Configuration tests
│   ├── test_003_player/        # Player tests
│   ├── test_004_audio/         # Audio processing tests
│   ├── test_005_effects/       # Effects tests
│   ├── test_006_melody/        # Melody generation tests
│   ├── test_007_tts/           # TTS engine tests
│   ├── test_008_integration/   # Integration tests
│   └── test_009_matrix/        # Compatibility matrix tests
│
├── output/                      # Generated audio files
│   └── .gitkeep                # Keep directory in git
│
├── doc/                         # Documentation
│   ├── USER_DOCUMENTATION.md   # User guide
│   └── TECHNICAL_DOCUMENTATION.md # This file
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project readme
└── .gitignore                   # Git exclusions
```

---

## Core Modules

### config.py

Defines configuration dataclasses for type-safe parameter handling.

**Key Classes:**
- `GVConfig`: Main configuration container
- `AudioParams`: Audio processing parameters
- `MelodyParams`: Melody generation parameters
- `VoiceEffectParams`: Voice effect parameters

### param_validator.py

Validates CLI parameters and provides error messages.

**Key Functions:**
- `validate_params()`: Main validation entry point
- `VALUE_OPTIONS`: Dictionary of valid parameter values
- `CLI_OPTIONS`: Human-readable option descriptions

### synthesis.py

Core synthesis pipeline coordinating TTS engines and audio processing.

**Key Functions:**
- `synthesize_complete()`: Main synthesis function
- `generate_melody()`: Procedural melody generation
- `apply_effects()`: Voice effect processing

### audio.py

WAV file I/O and audio processing utilities.

**Key Functions:**
- `load_wav()`: Load WAV file to numpy array
- `save_wav()`: Save numpy array to WAV file
- `normalize_audio()`: Peak normalization
- `apply_fade()`: Fade in/out processing
- `mix_layers()`: Mix multiple audio tracks

---

## TTS Engines

### Base Class (tts/base.py)

All TTS engines inherit from `BaseTTS`:

```python
class BaseTTS(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        """Check if engine is available on this system"""
        
    @abstractmethod
    def list_voices(self) -> Dict[str, Voice]:
        """Return available voices"""
        
    @abstractmethod
    def synthesize(self, text: str, voice: str, output_path: str) -> bool:
        """Synthesize text to audio file"""
```

### Piper Engine

- **Type**: Neural offline
- **Sample Rate**: 22050 Hz
- **Format**: ONNX models
- **Location**: `lib/tts/piper/`

**Key Features:**
- Fully offline operation
- Fast synthesis
- 160+ voice models
- ONNX Runtime backend

### Edge Engine

- **Type**: Cloud neural
- **Sample Rate**: 48000 Hz
- **Format**: MP3 streaming
- **Location**: `lib/tts/edge/`

**Key Features:**
- Highest quality voices
- Requires internet connection
- Supports effects and melody
- 100+ neural voices

**Note**: Features requiring 48kHz (effects, melody) only work with Edge.

### eSpeak Engine

- **Type**: Robotic offline
- **Sample Rate**: 22050 Hz
- **Format**: Native synthesis
- **Location**: `lib/tts/espeak/`

**Key Features:**
- Fully offline
- 100+ languages
- Very fast
- Lightweight

---

## CLI Reference

### Parameter Matrix

| Parameter | Type | Default | Engines | Description |
|-----------|------|---------|---------|-------------|
| `--tts` | value | piper | all | TTS engine selection |
| `--text` | value | - | all | Text to synthesize |
| `--voice` | value | auto | all | Voice identifier |
| `--output` | value | auto | all | Output filename |
| `--duration` | value | auto | all | Target duration (sec) |
| `--voice-effect` | value | none | Edge only | Audio effect |
| `--player` | value | auto | all | Audio player |
| `--wav-format` | value | 16-bit | Edge only | Bit depth |
| `--fade-in` | value | 50 | all | Fade in (ms) |
| `--fade-out` | value | 80 | all | Fade out (ms) |
| `--melody` | flag | false | Edge only | Enable melody |
| `--auto-play` | flag | false | all | Auto-play result |
| `--wait-finish` | flag | false | all | Wait for playback |
| `--normalize` | flag | false | Edge only | Normalize audio |
| `--list-engines` | flag | - | solo | List engines |
| `--list-launchers` | flag | - | solo | List UIs |
| `--auto-fix` | flag | - | solo | Fix dependencies |

### Solo Parameters

These parameters must be used alone (no other parameters):
- `--list-engines`
- `--list-launchers`
- `--auto-fix`
- `--help`

### auto-fix — Behavior and Examples

`--auto-fix` calls `adapt.auto_install_dependencies(os_name)` to resolve missing system packages. It reads `--system-os` if provided, otherwise defaults to `ubuntu`.

```bash
# Auto-detect OS
python3 py/gv.py --auto-fix

# Force OS target
python3 py/gv.py --auto-fix --system-os ubuntu
python3 py/gv.py --auto-fix --system-os debian
python3 py/gv.py --auto-fix --system-os fedora

# Elevated permissions (for system-level installs)
sudo python3 py/gv.py --auto-fix
sudo python3 py/gv.py --auto-fix --system-os ubuntu
```

> `--auto-fix` is compatible with `--system-os` as the only exception to the solo-parameter rule.

### Dependency Validation

Certain parameters require others:
- `--auto-play` requires `--tts`
- `--text` requires `--tts`
- `--voice-effect` requires Edge TTS
- `--melody` requires Edge TTS

---

## Configuration System

### Configuration Flow

```
CLI Args → parse_args() → validate_params() → GVConfig → synthesis.py
```

### Configuration Classes

```python
@dataclass
class GVConfig:
    tts: str = "piper"
    text: str = ""
    voice: str = "auto"
    output: str = "auto"
    duration: Union[int, str] = "auto"
    voice_effect: str = "none"
    player: str = "auto"
    wav_format: str = "16-bit"
    fade_in: int = 50
    fade_out: int = 80
    melody: bool = False
    auto_play: bool = False
    wait_finish: bool = False
    normalize: bool = False
```

---

## Audio Pipeline

### Synthesis Flow

```
Text Input
    ↓
TTS Engine (Piper/Edge/eSpeak)
    ↓
Voice Synthesis → WAV file
    ↓
[Optional] Voice Effects (echo, vibrato, reverb)
    ↓
[Optional] Melody Generation (chords, perc, bass)
    ↓
[Optional] Normalization
    ↓
Fade In/Out Processing
    ↓
Output Files (voice, stems, mix)
```

### Audio Specifications

**Piper:**
- Sample Rate: 22050 Hz
- Format: 16-bit PCM
- Channels: Mono

**Edge:**
- Sample Rate: 48000 Hz
- Format: 16-bit or 32-bit PCM
- Channels: Mono

**eSpeak:**
- Sample Rate: 22050 Hz
- Format: 16-bit PCM
- Channels: Mono

### File Naming

Generated files use timestamp prefix:
```
YYYYMMDD_HHMMSS_<type>.wav
```

Example: `20250408_143022_voice.wav`

### GUI Interface

**File:** `py/gvflet.py`

**Technology:** Flet 0.84 (Python Flutter framework)

**Features:**
- 6 tabs covering all CLI parameters:
  1. **TTS Tab**: Engine selection, voice selection, text input
  2. **Audio Tab**: Duration, output file, WAV format, normalize, fades
  3. **Effects Tab**: Voice effects (echo, vibrato, reverb), melody mode
  4. **Playback Tab**: Auto-play, player selection, wait-finish
  5. **Advanced Tab**: System OS override, debugging options
  6. **Tools Tab**: Voice installation, demo generation, app packaging

**Modes:**
```bash
# Desktop mode (recommended)
python3 py/gvflet.py

# Web browser mode (optional)
python3 py/gvflet.py --web --port 8555
```

**Architecture:**
- State management via `@dataclass`
- Real-time command building with `build_command()`
- Subprocess execution of `gv.py` CLI

---

## Testing Framework

### Test Structure

Tests are organized by functionality:

| Suite | Tests | Focus |
|-------|-------|-------|
| test_001_cli_args | 29 | CLI argument parsing |
| test_002_config | 24 | Configuration handling |
| test_003_player | 18 | Audio player abstraction |
| test_004_audio | 14 | Audio processing |
| test_005_effects | 9 | Voice effects |
| test_006_melody | 10 | Melody generation |
| test_007_tts | 20 | TTS engines |
| test_008_integration | 16 | Integration tests |
| test_009_matrix | 20 | Compatibility matrix |

### Running Tests

```bash
# Run all tests
python3 tests/run_all_tests.py

# Run specific suite
cd tests/test_001_cli_args
python3 run_tests.py
```

### Test Configuration

Each test suite includes:
- `conftest.py`: Test fixtures and configuration
- `run_tests.py`: Suite runner
- `test_*.py`: Individual test files

---

## Development Guide

### Adding a New CLI Parameter

1. Add to `VALUE_OPTIONS` in `param_validator.py`
2. Add validation logic in `validate_params()`
3. Add to `gv.py` argument parser
4. Add to `GVConfig` in `config.py`
5. Update documentation

### Adding a New TTS Engine

1. Create `lib/tts/newengine.py`
2. Inherit from `BaseTTS`
3. Implement required methods
4. Add to `lib/tts/__init__.py`
5. Add engine detection in `gv.py`
6. Create voices catalog if needed

### Code Style

- Follow PEP 8
- Use type hints
- Document public functions
- Keep functions focused and small

### Dependencies

Core dependencies:
```
numpy>=1.20.0      # Audio processing
scipy>=1.7.0       # Signal processing
inquirer>=2.9.0    # Interactive UI
edge-tts>=6.1.0    # Edge TTS engine
flet==0.84.0       # GUI framework (desktop)
flet-web==0.84.0   # GUI framework (web browser)
```

**Flet 0.84 Compatibility Notes:**
- `ft.app()` → `ft.run()`
- `ft.Button(text=...)` → `ft.Button(content=...)`
- `ft.Tab(text=...)` → `ft.Tab(label=...)`
- `ft.AppView.WEB_BROWSER` for web mode
- `ft.AppView.FLET_APP` for desktop mode

---

## Utility Scripts

### gvcorevoices.py

**Purpose:** Extract Core Piper voices from split ZIP archives.

**Location:** `py/gvcorevoices.py`

**Key Constants:**
```python
CORE_VOICES = [
    "fr_FR-siwis-medium",
    "en_US-amy-medium", 
    "es_ES-sharvard-medium",
    "it_IT-paola-medium",
    "de_DE-mls-medium",
]
```

**Process:**
1. Checks for `.zip.001` files for each voice
2. Extracts `.onnx` and `.onnx.json` to `lib/tts/piper/voices/`
3. Skips already extracted voices

**When to run:** After repository clone, before first synthesis.

---

### gvdemo.py

**Purpose:** Generate demo audio samples for all supported voices.

**Location:** `py/gvdemo.py`

**Voice Coverage:**
- Multiple voices available per engine

**Language Mapping:**
Uses `voices.json` to map each voice to its language code, then selects appropriate TEXT from 54 translated texts:
```python
TEXTS = {
    "fr-FR": "...", "en-US": "...", "de-DE": "...",
    # ... 54 languages total
}
```

**Process:**
1. Loads Piper `voices.json` to get language codes
2. Resolves language variants (`pt-br` → `pt-BR`, `en-gb-x-rp` → `en-GB`)
3. For each voice: synthesizes TEXT in appropriate language
4. Saves to `output/demo/demo_{engine}_{voice}.wav`
5. Logs errors to `output/demo/demo_errors.log`

**Runtime:** ~1 hour on modern hardware

**Output Structure:**
```
output/demo/
├── demo_piper_fr_FR-siwis-medium.wav
├── demo_edge_fr-FR-DeniseNeural.wav
├── demo_espeak_fr.wav
└── demo_errors.log
```

---

### gvappcorefullinstall.py

**Purpose:** Build the Core Full distribution ZIP.

**Location:** `py/gv/gvappcorefullinstall.py` (internal script, gitignored)

**Features:**
- Packages all 174 Piper `.onnx` models
- Includes complete application (lib/, py/, tests/, doc/)
- **Demo inclusion:** Checks for ≥550 WAV files in `output/demo/`
  - If threshold met: includes all demo files
  - If not met: skips demos (empty `output/demo/` placeholder only)

**Threshold Configuration:**
```python
MIN_DEMO_WAV_THRESHOLD = 550
```

**Exclusions:**
- `py/gv/` directory (internal scripts)
- `output/*` (except empty placeholders)
- `*.zip.*` split archives
- `gvvoicesinstallcore.py` (redundant in Full version)

**Output:** `py/gv/apps/gvcore_v1.0.2_allvoices.zip`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2026-03 | Initial release |
| v1.0.1 | 2026-04 | GitHub repo cleanup - EN docs, cleaned Python files |
| v1.0.2 | 2026-04 | Documentation overhaul, specs, commercial landing |

---

## License

Generic Voice Core: MIT License

Third-party components:
- Piper: MIT License
- Edge TTS: MIT License
- eSpeak: GPLv3 License

---

*Generic Voice v1.0.2 - Technical Documentation*
