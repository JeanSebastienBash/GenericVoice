#!/usr/bin/env python3
"""
Module: gv.py
Purpose: Main CLI entry point and controller for Generic Voice v1.0.2.
    Provides command-line interface for TTS synthesis and interactive
    text-based menu system organized into tabs (TTS, Audio, Effects, Playback, Advanced).
Context: Top-level launcher in py/. Imports and orchestrates lib/ modules
    including config, synthesis, player, param_validator, ihm, and TTS engines.
    Called directly by users or via interactive menu launcher.
Impact: Core application interface. Changes affect all CLI interactions,
    menu workflows, and synthesis pipeline initialization.
Related: lib/config.py, lib/synthesis.py, lib/player.py, lib/param_validator.py,
    lib/ihm/generic.py, lib/tts/__init__.py, lib/system/detect.py, lib/errors.py,
    lib/adapt.py, py/gvflet.py (GUI counterpart)
"""


import sys
import os
import time
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
LIB_DIR = os.path.join(PROJECT_ROOT, "lib")
sys.path.insert(0, LIB_DIR)
sys.path.insert(0, PROJECT_ROOT)

__version__ = "1.0.2"

PIPER_VOICES_DIR = os.path.join(PROJECT_ROOT, "lib", "tts", "piper", "voices")
PIPER_CORE_VOICES = [
    "fr_FR-siwis-medium",
    "en_US-amy-medium",
    "es_ES-sharvard-medium",
    "it_IT-paola-medium",
    "de_DE-mls-medium",
]


try:
    from ihm.generic import GenericIHM
except ImportError:
    GenericIHM = None

try:
    from param_validator import (
        VALUE_OPTIONS, FLAG_OPTIONS,
        validate_all_params, print_validation_errors,
    )
except ImportError:
    VALUE_OPTIONS = {}
    FLAG_OPTIONS = []
    def validate_all_params(p): return []
    def print_validation_errors(e): pass

try:
    import config as config_module
    config = config_module.config
except ImportError:
    config = None

try:
    from system import adapt
except ImportError:
    adapt = None

try:
    import player
except ImportError:
    player = None

try:
    import synthesis
except ImportError:
    synthesis = None

try:
    from tts import get_tts_engine, TTSEngineNotAvailable
except ImportError:
    get_tts_engine = None
    TTSEngineNotAvailable = Exception

try:
    from system import detect
except ImportError:
    detect = None

try:
    from errors import print_header, print_footer
except ImportError:
    def print_header():
        print("=" * 70)
        print("  G E N E R I C   V O I C E  v1.0.2")
        print("=" * 70)
    def print_footer():
        print("=" * 70)
        print("  Aide: python3 gv.py --help")
        print("  Docs: https://github.com/JeanSebastienBash/GenericVoice")
        print("=" * 70)


def get_all_cli_options():
    opts = [f"--{k}" for k in VALUE_OPTIONS.keys()]
    opts += [f"--{f}" for f in FLAG_OPTIONS]
    opts += ["-h"]
    return opts


def has_zip_archives():
    """Retourne True seulement si des archives zip sont presentes
    mais que le .onnx correspondant n'est pas encore extrait."""
    zip_pattern = os.path.join(PIPER_VOICES_DIR, "*.zip*")
    for f in glob.glob(zip_pattern):
        if f.endswith(".zip") or ".zip." in f:
            base = f.split(".zip")[0]
            if not os.path.exists(base + ".onnx"):
                return True  # zip present MAIS .onnx absent
    return False  # zip present mais .onnx aussi present -> voix OK


def check_piper_voices_installed():
    missing = []
    for voice in PIPER_CORE_VOICES:
        onnx_file = os.path.join(PIPER_VOICES_DIR, f"{voice}.onnx")
        if not os.path.exists(onnx_file):
            missing.append(voice)
    return len(missing) == 0, missing


def load_ihm():
    """Charge et retourne le module IHM."""
    if GenericIHM:
        return GenericIHM()
    return None


def load_voices_for_tts(tts_engine):
    voices_file = os.path.join(PROJECT_ROOT, "lib", "tts", tts_engine, "voices", "voices.json")
    if not os.path.exists(voices_file):
        if tts_engine == "espeak":
            return {"fr": {"name": "Francais"}, "en": {"name": "Anglais"},
                    "de": {"name": "Allemand"}, "es": {"name": "Espagnol"},
                    "it": {"name": "Italien"},  "pt": {"name": "Portugais"}}
        return {}
    try:
        import json
        with open(voices_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("voices", {})
    except Exception:
        return {}


def error_missing_option_value(opt, valid_values=None, default=None, example=None):
    print_header()
    print(f"  ERREUR: Valeur manquante pour {opt}")
    print()
    if default:
        print(f"  Valeur par defaut: {default}")
    if valid_values:
        print("  Valeurs valides:")
        for v in valid_values:
            print(f"    - {v}")
    if example:
        print(f"  Exemple: {example}")
    print()
    print_footer()


def error_unknown_option(opt, all_options=None):
    print_header()
    print(f"  ERREUR: Option inconnue: {opt}")
    print()
    if all_options:
        print("  Options disponibles:")
        for o in sorted(all_options):
            print(f"    {o}")
    print()
    print_footer()


def print_piper_installation_error():
    print_header()
    print("  ERREUR: VOIX PIPER NON INSTALLEES")
    print()
    if has_zip_archives():
        print("  Archives ZIP presentes. Executez:")
        print("    python3 gvzipvoicesinstallcore.py")
    else:
        print("  Executez: python3 gvzipvoicesinstallcore.py")
    print()
    print_footer()


def usage():
    print_header()
    print("""
  USAGE:
    python3 gv.py [OPTIONS]

  SYNTHESE DIRECTE:
    python3 gv.py --tts piper --text "Bonjour"
    python3 gv.py --tts edge --voice fr-FR-DeniseNeural --text "Bonjour"
    python3 gv.py --tts piper --text "Test" --auto-play --player cvlc

  MENU INTERACTIF:
    python3 gv.py
    python3 gv.py --launcher genericmenu

  PARAMETRES VALEUR (--param VALEUR):
    --tts         piper | edge | espeak          (defaut: piper)
    --voice       ID voix                        (defaut: auto)
    --text        "texte a synthetiser"
    --duration    secondes | auto               (defaut: auto)
    --output      /chemin/fichier.wav            (defaut: auto)
    --voice-effect  echo | vibrato | reverb | none
    --player      parole | cvlc | vlc | ffplay | aplay
    --wav-format  16-bit | 32-bit               (defaut: 16-bit)
    --fade-in     ms >= 0                       (defaut: 50)
    --fade-out    ms >= 0                       (defaut: 80)
    --system-os   ubuntu | linux | windows | darwin | auto
    --launcher    genericmenu

  FLAGS (--param):
    --melody          Generation melodique
    --auto-play       Lecture automatique apres synthese
    --wait-finish     Attendre fin de lecture
    --normalize       Normalisation audio
    --auto-fix        Installer les dependances
    --list-engines    Lister les moteurs TTS
    --list-launchers  Lister les interfaces disponibles
    --help, -h        Afficher cette aide

  CONTRAINTES (validees par param_validator.py):
    SOLO: --help, --list-engines, --list-launchers, --auto-fix, --launcher
    REQUIRE --tts: --text, --voice, --duration, --output, --melody,
                   --voice-effect, --auto-play, --player, --wait-finish,
                   --normalize, --wav-format, --fade-in, --fade-out
    REQUIRE --auto-play: --player, --wait-finish

  EXEMPLES:
    python3 gv.py --tts piper --text "Bonjour le monde"
    python3 gv.py --tts edge --text "Jingle" --melody --voice-effect echo
    python3 gv.py --tts piper --text "Test" --auto-play --wait-finish
    python3 gv.py --list-engines
    python3 gv.py --auto-fix
""")
    print_footer()


def list_engines():
    print_header()
    print("  MOTEURS TTS DISPONIBLES")
    print()
    engines = [
        ("piper",  "Piper  - Offline neural TTS (22kHz)"),
        ("edge",   "Edge   - Microsoft Cloud TTS (48kHz)"),
        ("espeak", "eSpeak - Open Source TTS (22kHz)"),
    ]
    for name, desc in engines:
        if get_tts_engine:
            try:
                get_tts_engine(name)
                status = "[OK] DISPONIBLE  "
            except Exception:
                status = "[NA] INDISPONIBLE"
        else:
            status = "[??] INCONNU     "
        print(f"  {status}  {name:8}  {desc}")
    print()
    print("  Exemple: python3 gv.py --tts piper --text \"Bonjour\"")
    print()
    print_footer()


def list_launchers():
    print_header()
    print("  INTERFACES IHM DISPONIBLES")
    print()
    print("  [OK] DISPONIBLE  genericmenu  Interface texte interactive [DEFAULT]")
    print("  [OK] DISPONIBLE  gvflet       Interface graphique Flet (GUI)")
    print()
    print("  Utilisation:")
    print("    python3 gv.py                         # Lance genericmenu")
    print("    python3 gv.py --launcher genericmenu  # Equivalent")
    print("    python3 py/gvflet.py                  # Interface graphique")
    print()
    print_footer()


def run_auto_fix():
    print_header()
    print("  AUTO-FIX: Installation des dependances")
    print()
    if adapt:
        os_name = (config.system_os if config else None) or "ubuntu"
        try:
            adapt.auto_install_dependencies(os_name)
            print("  Installation terminee.")
        except Exception as e:
            print(f"  Erreur: {e}")
            print("  Essayez: sudo python3 gv.py --auto-fix")
    else:
        print("  Module adapt non disponible.")
    print()
    print_footer()


def parse_args(args):
    parsed = {
        "tts": None,        "text": None,       "voice": None,
        "duration": None,   "output": None,     "voice_effect": None,
        "player": None,     "wav_format": None, "fade_in": None,
        "fade_out": None,   "system_os": None,  "launcher": None,
        "melody": False,    "auto_play": False, "wait_finish": False,
        "normalize": False, "auto_fix": False,
        "list_engines": False, "list_launchers": False, "help": False,
    }

    all_opts = get_all_cli_options()
    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ("--help", "-h"):
            parsed["help"] = True; i += 1
        elif arg == "--list-engines":
            parsed["list_engines"] = True; i += 1
        elif arg == "--list-launchers":
            parsed["list_launchers"] = True; i += 1
        elif arg == "--auto-fix":
            parsed["auto_fix"] = True; i += 1
        elif arg == "--melody":
            parsed["melody"] = True; i += 1
        elif arg == "--auto-play":
            parsed["auto_play"] = True; i += 1
        elif arg == "--wait-finish":
            parsed["wait_finish"] = True; i += 1
        elif arg == "--normalize":
            parsed["normalize"] = True; i += 1
        elif arg == "--tts":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--tts", ["piper", "edge", "espeak"], "piper",
                    "python3 gv.py --tts piper --text \"Bonjour\"")
                sys.exit(1)
            parsed["tts"] = args[i+1]; i += 2
        elif arg == "--text":
            if i + 1 >= len(args) or (args[i+1].startswith("--") and args[i+1] in all_opts):
                error_missing_option_value("--text", default="(aucun)",
                    example="python3 gv.py --text \"Bonjour le monde\"")
                sys.exit(1)
            parsed["text"] = args[i+1]; i += 2
        elif arg == "--voice":
            if i + 1 >= len(args) or args[i+1].startswith("--"):
                error_missing_option_value("--voice", default="auto",
                    example="python3 gv.py --tts piper --voice fr_FR-siwis-medium --text \"Hi\"")
                sys.exit(1)
            parsed["voice"] = args[i+1]; i += 2
        elif arg == "--duration":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--duration", default="auto",
                    example="python3 gv.py --duration 10")
                sys.exit(1)
            parsed["duration"] = args[i+1]; i += 2
        elif arg == "--output":
            if i + 1 >= len(args) or (args[i+1].startswith("--") and args[i+1] in all_opts):
                error_missing_option_value("--output", default="auto",
                    example="python3 gv.py --output /chemin/fichier.wav")
                sys.exit(1)
            parsed["output"] = args[i+1]; i += 2
        elif arg == "--voice-effect":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--voice-effect",
                    ["echo", "vibrato", "reverb", "none"],
                    example="python3 gv.py --voice-effect echo")
                sys.exit(1)
            parsed["voice_effect"] = args[i+1]; i += 2
        elif arg == "--player":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--player",
                    ["parole", "cvlc", "vlc", "ffplay", "aplay"], "auto",
                    example="python3 gv.py --auto-play --player cvlc")
                sys.exit(1)
            parsed["player"] = args[i+1]; i += 2
        elif arg == "--wav-format":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--wav-format", ["16-bit", "32-bit"], "16-bit",
                    example="python3 gv.py --wav-format 32-bit")
                sys.exit(1)
            parsed["wav_format"] = args[i+1]; i += 2
        elif arg == "--fade-in":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--fade-in", default="50 ms",
                    example="python3 gv.py --fade-in 100")
                sys.exit(1)
            parsed["fade_in"] = args[i+1]; i += 2
        elif arg == "--fade-out":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--fade-out", default="80 ms",
                    example="python3 gv.py --fade-out 150")
                sys.exit(1)
            parsed["fade_out"] = args[i+1]; i += 2
        elif arg == "--system-os":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--system-os",
                    ["ubuntu", "linux", "windows", "darwin", "auto"], "auto",
                    example="python3 gv.py --system-os ubuntu")
                sys.exit(1)
            parsed["system_os"] = args[i+1]; i += 2
        elif arg == "--launcher":
            if i + 1 >= len(args) or args[i+1].startswith("-"):
                error_missing_option_value("--launcher", ["genericmenu"], "genericmenu",
                    example="python3 gv.py --launcher genericmenu")
                sys.exit(1)
            parsed["launcher"] = args[i+1]; i += 2
        else:
            error_unknown_option(arg, all_opts)
            sys.exit(1)

    if parsed.get("text") and not parsed.get("tts"):
        parsed["tts"] = "piper"

    return parsed


def validate_params(opts):
    errors = validate_all_params(opts)
    if errors:
        print_validation_errors(errors)
        sys.exit(1)


def apply_config(opts):
    if not config:
        return
    if opts["tts"]:          config.tts = opts["tts"]
    if opts["text"]:         config.text = opts["text"]
    if opts["voice"]:        config.voice = opts["voice"]
    if opts["duration"]:     config.duration = opts["duration"]
    if opts["output"]:       config.output = opts["output"]
    if opts["melody"]:       config.melody_toggle = True
    if opts["voice_effect"]:
        config.voice_toggle = True
        config.voice_effect_name = opts["voice_effect"]
    if opts["system_os"]:    config.system_os = opts["system_os"]
    if opts["launcher"]:     config.launcher = opts["launcher"]
    if opts["auto_fix"]:     config.auto_fix = True
    if opts["player"]:       config.player = opts["player"]
    if opts["auto_play"]:    config.auto_play = True
    if opts["wait_finish"]:  config.audio.wait_finish = True
    if opts["normalize"]:    config.audio.normalize = True
    if opts["wav_format"]:   config.audio.wav_format = opts["wav_format"]
    if opts["fade_in"]:      config.audio.fade_in_ms = int(opts["fade_in"])
    if opts["fade_out"]:     config.audio.fade_out_ms = int(opts["fade_out"])


def handle_tts_submenu(ihm):
    """Tab TTS : engine / voice / text."""
    while True:
        info = config.get_display_info()
        items = [
            ("1", f"Moteur TTS     : {info['tts']}"),
            ("2", f"Voix           : {info['voice']}"),
            ("3", f"Texte          : {info['text']}"),
            ("R", "Retour"),
        ]
        choice = ihm.menu(
            title="Generic Voice v1.0.2 - TTS",
            text=f"Command: {config.build_command()}",
            height=12, width=70, choice_height=4, items=items,
        )
        if choice is None or choice == "R":
            break
        elif choice == "1":
            engines = [
                ("piper",  "Piper  - Offline neural TTS (22kHz)", config.tts == "piper"),
                ("edge",   "Edge   - Microsoft Cloud TTS (48kHz)", config.tts == "edge"),
                ("espeak", "eSpeak - Open Source TTS (22kHz)",    config.tts == "espeak"),
            ]
            sel = ihm.radiolist("Moteur TTS", "Choisir le moteur:", 11, 55, 3, engines)
            if sel:
                config.tts = sel
                config.voice = ""
        elif choice == "2":
            voices = load_voices_for_tts(config.tts)
            if voices:
                current = config.voice or "auto"
                items_v = [("auto", "auto - Detection automatique", current == "auto")]
                for vid, vdata in sorted(voices.items()):
                    name = vdata.get("language_name", vdata.get("name", vid))
                    items_v.append((vid, f"{vid} - {name}", current == vid))
                sel = ihm.radiolist("Voix", f"Voix pour {config.tts}:",
                                   min(len(items_v) + 4, 20), 65,
                                   min(len(items_v), 15), items_v)
                if sel:
                    config.voice = "" if sel == "auto" else sel
            else:
                val = ihm.inputbox("Voix", "ID de voix (vide = auto):", 7, 55,
                                  config.voice or "auto")
                if val is not None:
                    config.voice = "" if val == "auto" else val
        elif choice == "3":
            val = ihm.inputbox("Texte", "Texte a synthetiser:", 9, 65,
                              config.text or "")
            if val is not None:
                config.text = val


def handle_audio_submenu(ihm):
    """Tab Audio : duration / output / wav-format / normalize / fade-in / fade-out."""
    while True:
        info = config.get_display_info()
        items = [
            ("1", f"Duree          : {info['duration']}"),
            ("2", f"Sortie         : {info['output']}"),
            ("3", f"Format WAV     : {info['wav_format']}"),
            ("4", f"Normalize      : {info['normalize']}"),
            ("5", f"Fade-in        : {info['fade_in']}"),
            ("6", f"Fade-out       : {info['fade_out']}"),
            ("R", "Retour"),
        ]
        choice = ihm.menu(
            title="Generic Voice v1.0.2 - Audio",
            text=f"Command: {config.build_command()}",
            height=16, width=70, choice_height=7, items=items,
        )
        if choice is None or choice == "R":
            break
        elif choice == "1":
            durations = [
                ("auto", "auto - Detection automatique", config.duration == "auto"),
                ("5",  "5 secondes",  config.duration == "5"),
                ("10", "10 secondes", config.duration == "10"),
                ("30", "30 secondes", config.duration == "30"),
                ("60", "60 secondes", config.duration == "60"),
            ]
            sel = ihm.radiolist("Duree", "Duree de la synthese:", 10, 40, 5, durations)
            if sel:
                config.duration = sel
        elif choice == "2":
            val = ihm.inputbox("Sortie", "Chemin WAV (vide = auto):",
                              7, 60, config.output or "auto")
            if val is not None:
                config.output = "" if val == "auto" else val
        elif choice == "3":
            formats = [
                ("16-bit", "16-bit PCM (standard)", config.audio.wav_format == "16-bit"),
                ("32-bit", "32-bit Float (Edge TTS)", config.audio.wav_format == "32-bit"),
            ]
            sel = ihm.radiolist("Format WAV", "Format audio:", 8, 50, 2, formats)
            if sel:
                config.audio.wav_format = sel
        elif choice == "4":
            config.audio.normalize = not config.audio.normalize
        elif choice == "5":
            val = ihm.inputbox("Fade-in", "Fade-in en ms (>= 0):",
                              7, 40, str(config.audio.fade_in_ms))
            if val and val.isdigit():
                config.audio.fade_in_ms = int(val)
        elif choice == "6":
            val = ihm.inputbox("Fade-out", "Fade-out en ms (>= 0):",
                              7, 40, str(config.audio.fade_out_ms))
            if val and val.isdigit():
                config.audio.fade_out_ms = int(val)


def handle_effects_submenu(ihm):
    """Tab Effects : voice-effect / melody."""
    while True:
        info = config.get_display_info()
        items = [
            ("1", f"Voice-effect   : {info['voice_effect']}"),
            ("2", f"Melody         : {info['melody_info']}"),
            ("R", "Retour"),
        ]
        choice = ihm.menu(
            title="Generic Voice v1.0.2 - Effects",
            text=f"Command: {config.build_command()}",
            height=11, width=70, choice_height=3, items=items,
        )
        if choice is None or choice == "R":
            break
        elif choice == "1":
            cur = config.voice_effect_name or "none"
            effects = [
                ("none",    "Aucun effet",                      cur == "none" or not cur),
                ("echo",    "Echo    - Echo multi-tap",         cur == "echo"),
                ("vibrato", "Vibrato - Modulation de frequence", cur == "vibrato"),
                ("reverb",  "Reverb  - Reverberation",          cur == "reverb"),
            ]
            sel = ihm.radiolist("Voice Effect",
                               "Effet vocal (voir matrice compat.):",
                               11, 60, 4, effects)
            if sel:
                if sel == "none":
                    config.voice_toggle = False
                    config.voice_effect_name = ""
                else:
                    config.voice_toggle = True
                    config.voice_effect_name = sel
        elif choice == "2":
            config.melody_toggle = not config.melody_toggle


def handle_playback_submenu(ihm):
    """Tab Playback : auto-play / player / wait-finish."""
    while True:
        info = config.get_display_info()
        items = [
            ("1", f"Auto-play      : {info['auto_play']}"),
            ("2", f"Player         : {info['player']}"),
            ("3", f"Wait-finish    : {info['wait_finish']}"),
            ("R", "Retour"),
        ]
        choice = ihm.menu(
            title="Generic Voice v1.0.2 - Playback",
            text=f"Command: {config.build_command()}",
            height=12, width=70, choice_height=4, items=items,
        )
        if choice is None or choice == "R":
            break
        elif choice == "1":
            config.auto_play = not config.auto_play
        elif choice == "2":
            cur = config.player or "auto"
            players = [
                ("auto",   "auto   - Detection automatique", cur == "auto"),
                ("parole", "parole - Ubuntu gnome-speech",   cur == "parole"),
                ("cvlc",   "cvlc   - VLC ligne de commande", cur == "cvlc"),
                ("vlc",    "vlc    - VLC interface graphique", cur == "vlc"),
                ("ffplay", "ffplay - FFmpeg player",          cur == "ffplay"),
                ("aplay",  "aplay  - ALSA player",           cur == "aplay"),
            ]
            sel = ihm.radiolist("Player", "Lecteur audio:", 13, 60, 6, players)
            if sel:
                config.player = "" if sel == "auto" else sel
        elif choice == "3":
            config.audio.wait_finish = not config.audio.wait_finish


def handle_advanced_submenu(ihm):
    """Tab Advanced : system-os."""
    while True:
        items = [
            ("1", f"System OS      : {config.system_os or 'auto'}"),
            ("R", "Retour"),
        ]
        choice = ihm.menu(
            title="Generic Voice v1.0.2 - Advanced",
            text=f"Command: {config.build_command()}",
            height=10, width=70, choice_height=2, items=items,
        )
        if choice is None or choice == "R":
            break
        elif choice == "1":
            cur = config.system_os or "auto"
            systems = [
                ("auto",    "auto    - Detection automatique", cur == "auto"),
                ("ubuntu",  "ubuntu  - Ubuntu / Debian",       cur == "ubuntu"),
                ("linux",   "linux   - Linux generique",       cur == "linux"),
                ("windows", "windows - Microsoft Windows",     cur == "windows"),
                ("darwin",  "darwin  - macOS",                 cur == "darwin"),
            ]
            sel = ihm.radiolist("System OS", "Forcer le systeme:", 12, 55, 5, systems)
            if sel:
                config.system_os = "" if sel == "auto" else sel


def handle_execute(ihm):
    cmd = config.build_command()
    if not config.text:
        ihm.msgbox("Erreur", "Aucun texte.\nUtilisez [T] > [3] pour saisir le texte.", 8, 50)
        return
    if ihm.yesno("Confirmer", f"Executer la synthese ?\n\n{cmd}", 13, 65):
        print(f"\nExecution: {cmd}")
        try:
            import subprocess
            result = subprocess.run(cmd, shell=True, text=True)
            msg = "Synthese terminee." if result.returncode == 0 else f"Erreur (code {result.returncode})."
            input(f"\n{msg} Appuyez sur Entree...")
        except Exception as e:
            input(f"\nException: {e}. Appuyez sur Entree...")


def handle_help(ihm):
    help_text = """
  PARAMETRES VALEUR:
    --tts         piper | edge | espeak
    --voice       ID de voix (auto = defaut)
    --text        Texte a synthetiser
    --duration    secondes | auto
    --output      Chemin WAV
    --voice-effect  echo | vibrato | reverb | none
    --player      parole | cvlc | vlc | ffplay | aplay
    --wav-format  16-bit | 32-bit
    --fade-in     ms >= 0 (defaut: 50)
    --fade-out    ms >= 0 (defaut: 80)
    --system-os   ubuntu | linux | windows | darwin | auto

  FLAGS:
    --melody        Generation melodique
    --auto-play     Lecture automatique
    --wait-finish   Attendre fin lecture
    --normalize     Normalisation audio

  COMMANDES SOLO:
    --help            Aide
    --list-engines    Moteurs TTS
    --list-launchers  Interfaces
    --auto-fix        Installer deps
    --launcher genericmenu  Ce menu

  EXEMPLES:
    python3 gv.py --tts piper --text "Bonjour"
    python3 gv.py --tts edge --text "Hi" --melody --voice-effect echo
    python3 gv.py --tts piper --text "Test" --auto-play --player cvlc
"""
    ihm.msgbox("AIDE - Generic Voice v1.0.2", help_text, 35, 70)



def main_menu(ihm):
    while True:
        info = config.get_display_info()

        items = [
            ("T", f"[TTS]      Moteur: {info['tts']}  |  Voix: {info['voice']}  |  Texte: {info['text']}"),
            ("A", f"[Audio]    Format: {info['wav_format']}  |  Norm: {info['normalize']}  |  Fades: {info['fade_in']}/{info['fade_out']}"),
            ("E", f"[Effects]  Effect: {info['voice_effect']}  |  Melody: {info['melody_info']}"),
            ("P", f"[Playback] Auto-play: {info['auto_play']}  |  Player: {info['player']}  |  Wait: {info['wait_finish']}"),
            ("D", f"[Advanced] System OS: {config.system_os or 'auto'}"),
            ("X", "EXECUTER la synthese"),
            ("H", "Aide"),
            ("Q", "Quitter"),
        ]

        choice = ihm.menu(
            title="Generic Voice v1.0.2 - Menu Principal",
            text=f"Command: {config.build_command()}",
            height=20, width=78, choice_height=8, items=items,
        )

        if choice is None or choice == "Q":
            break
        elif choice == "T": handle_tts_submenu(ihm)
        elif choice == "A": handle_audio_submenu(ihm)
        elif choice == "E": handle_effects_submenu(ihm)
        elif choice == "P": handle_playback_submenu(ihm)
        elif choice == "D": handle_advanced_submenu(ihm)
        elif choice == "X": handle_execute(ihm)
        elif choice == "H": handle_help(ihm)



def main():
    opts = parse_args(sys.argv[1:])
    validate_params(opts)

    if opts["help"]:
        usage(); sys.exit(0)

    if opts["list_engines"]:
        list_engines(); sys.exit(0)

    if opts["list_launchers"]:
        list_launchers(); sys.exit(0)

    if opts["auto_fix"]:
        run_auto_fix()
        if not any([opts["tts"], opts["text"], opts["launcher"]]):
            sys.exit(0)

    apply_config(opts)

    if opts["system_os"] and detect:
        try:
            config.system_os = detect.get_effective_os(opts["system_os"])
        except Exception:
            pass

    if opts["tts"] and opts["text"]:
        if opts["tts"] == "piper":
            if has_zip_archives() or not check_piper_voices_installed()[0]:
                print_piper_installation_error(); sys.exit(1)

        if not get_tts_engine:
            print("Module TTS non disponible."); sys.exit(1)

        try:
            engine = get_tts_engine(opts["tts"])
        except TTSEngineNotAvailable as e:
            print(f"Moteur TTS indisponible: {e}"); sys.exit(1)

        voice = opts.get("voice")
        if not voice and opts["tts"] == "piper":
            for core_voice in PIPER_CORE_VOICES:
                voice_path = os.path.join(PIPER_VOICES_DIR, f"{core_voice}.onnx")
                if os.path.isfile(voice_path):
                    voice = core_voice
                    break
        if not voice:
            voice = engine.get_default_voice()
        if voice:
            print(f"Voix: {voice}")

        output_path = opts.get("output")
        if output_path and output_path != "auto":
            output_dir = os.path.dirname(output_path) or "."
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(output_path))[0]
        else:
            output_dir = os.path.join(PROJECT_ROOT, "output")
            os.makedirs(output_dir, exist_ok=True)
            base_name = f"gv_{time.strftime('%Y%m%d_%H%M%S')}"

        if not synthesis:
            print("Module synthesis non disponible."); sys.exit(1)

        try:
            print(f"Synthese [{opts['tts']}]: {opts['text']}")
            voice_effect_name = config.voice_effect_name if config.voice_toggle else None
            paths = synthesis.synthesize_complete(
                tts_engine=engine,
                text=opts["text"],
                voice=voice,
                output_dir=output_dir,
                base_name=base_name,
                voice_effect=voice_effect_name,
                voice_effect_params={
                    "delay_ms": config.voice_effect.delay_ms,
                    "decay": config.voice_effect.decay,
                    "count": config.voice_effect.count,
                    "vibrato_rate": config.voice_effect.vibrato_rate,
                    "vibrato_depth": config.voice_effect.vibrato_depth,
                    "reverb_room": config.voice_effect.reverb_room,
                    "reverb_damping": config.voice_effect.reverb_damping,
                },
                melody_enabled=config.melody_toggle,
                melody_params={
                    "root_note": config.melody.root_note,
                    "chord_type": config.melody.chord_type,
                    "chord_voicing": config.melody.chord_voicing,
                    "pad_waveform": config.melody.pad_waveform,
                },
                percussion_params={
                    "timpani_main": config.percussion.timpani_main,
                    "hihat_density": config.percussion.hihat_density,
                    "perc_pattern": config.percussion.perc_pattern,
                },
                bass_params={
                    "bass_type": config.bass.bass_type,
                    "bass_note_style": config.bass.bass_note_style,
                },
                mix_params={
                    "voice": config.mix.voice,
                    "chord": config.mix.chord,
                    "perc": config.mix.perc,
                    "bass": config.mix.bass,
                },
                normalize=config.audio.normalize,
                fade_in_ms=config.audio.fade_in_ms,
                fade_out_ms=config.audio.fade_out_ms,
            )
            for key, path in paths.items():
                print(f"  {key}: {path}")

            if opts.get("auto_play") and player:
                player_name = opts.get("player") or player.get_default_player()
                if player_name and player.is_player_available(player_name):
                    print(f"Lecture avec {player_name}...")
                    player.play(paths.get("mix", ""), player_name)

        except Exception as e:
            print(f"Erreur synthese: {e}"); sys.exit(1)

        sys.exit(0)

    if not GenericIHM:
        print("Module IHM non disponible.")
        print("Utilisez: python3 py/gvflet.py")
        sys.exit(1)

    ihm = GenericIHM()
    main_menu(ihm)


if __name__ == "__main__":
    main()
