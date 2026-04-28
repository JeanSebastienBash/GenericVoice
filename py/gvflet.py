#!/usr/bin/env python3
"""
Module: gvflet.py
Purpose: Provides graphical interface mirroring CLI functionality. Organized into tabs for TTS, Audio, Effects, Playback, and Advanced settings.
Context: Entry point script in py/. Part of Generic Voice v1.0.2 TTS suite.
Impact: Direct user-facing tool. Changes affect user workflow and voice installation.
Related: lib/config.py, lib/synthesis.py, lib/player.py, lib/param_validator.py, py/gv.py
"""


import flet as ft
import subprocess
import os
import sys
import json
from dataclasses import dataclass
from typing import List

print("=" * 60)
print("GVFLET.PY - STARTING")
print("=" * 60)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PIPER_VOICES_DIR = os.path.join(PROJECT_ROOT, "lib", "tts", "piper", "voices")

print(f"[LOG] SCRIPT_DIR: {SCRIPT_DIR}")
print(f"[LOG] PROJECT_ROOT: {PROJECT_ROOT}")
print(f"[LOG] PIPER_VOICES_DIR: {PIPER_VOICES_DIR}")

PRIMARY = "#6366F1"
PRIMARY_DARK = "#4F46E5"
DARK = "#1F2937"
DARK_LIGHT = "#374151"
WHITE = "#FFFFFF"
TEXT_SECONDARY = "#9CA3AF"
WARNING = "#F59E0B"
ERROR = "#EF4444"
SUCCESS = "#10B981"

SOLO_PARAMS = ["help", "list-engines", "list-launchers", "auto-fix", "launcher"]
REQUIRE_TTS = ["text", "voice", "duration", "output", "melody", "voice-effect", "auto-play", "player", "wait-finish", "normalize", "wav-format", "fade-in", "fade-out"]
REQUIRE_AUTO_PLAY = ["player", "wait-finish"]
EDGE_ONLY_PARAMS = {
    "melody": {"reason": "Requires 48kHz sample rate (Edge only)", "supported_tts": ["edge"]},
    "voice-effect": {"reason": "Effects need 48kHz sample rate (Edge only)", "supported_tts": ["edge"]},
    "normalize": {"reason": "Degrades 22kHz quality on non-Edge engines", "supported_tts": ["edge"]},
    "wav-format-32bit": {"reason": "32-bit float format (Edge only)", "supported_tts": ["edge"]},
}

VALUE_OPTIONS = {
    "tts": {"values": ["piper", "edge", "espeak"], "default": "piper", "desc": "TTS Engine"},
    "voice": {"values": None, "default": "auto", "desc": "Voice to use"},
    "text": {"values": None, "default": None, "desc": "Text to synthesize"},
    "duration": {"values": None, "default": "auto", "desc": "Duration in seconds or 'auto'"},
    "output": {"values": None, "default": "auto", "desc": "Output WAV file path"},
    "voice-effect": {"values": ["echo", "vibrato", "reverb", "none"], "default": "none", "desc": "Voice effect"},
    "player": {"values": ["parole", "cvlc", "vlc", "ffplay", "aplay"], "default": "auto", "desc": "Audio player"},
    "wav-format": {"values": ["16-bit", "32-bit"], "default": "16-bit", "desc": "WAV format"},
    "fade-in": {"values": None, "default": "50", "desc": "Fade-in duration (ms)"},
    "fade-out": {"values": None, "default": "80", "desc": "Fade-out duration (ms)"},
    "system-os": {"values": ["ubuntu", "linux", "windows", "darwin"], "default": "auto", "desc": "Operating system"},
}

FLAG_OPTIONS = ["melody", "auto-play", "wait-finish", "normalize"]

print("[LOG] Colors and constants defined")

@dataclass
class State:
    tts: str = "piper"
    voice: str = "auto"
    text: str = ""
    duration: str = "auto"
    output: str = "auto"
    voice_effect: str = "none"
    player: str = "auto"
    wav_format: str = "16-bit"
    fade_in: int = 50
    fade_out: int = 80
    system_os: str = "auto"
    melody: bool = False
    auto_play: bool = False
    wait_finish: bool = False
    normalize: bool = False

print("[LOG] State dataclass defined")

state = State()
print("[LOG] State instance created")

def load_voices_for_tts(tts_engine: str) -> dict:
    print(f"[LOG] load_voices_for_tts called with: {tts_engine}")
    voices_file = os.path.join(PROJECT_ROOT, "lib", "tts", tts_engine, "voices", "voices.json")
    print(f"[LOG] voices_file path: {voices_file}")
    
    if not os.path.exists(voices_file):
        print(f"[LOG] voices_file NOT found: {voices_file}")
        if tts_engine == "espeak":
            print("[LOG] Returning default espeak voices")
            return {
                "fr": {"name": "Français"},
                "en": {"name": "Anglais"},
                "de": {"name": "Allemand"},
                "es": {"name": "Espagnol"},
                "it": {"name": "Italien"},
                "pt": {"name": "Portugais"},
            }
        return {}
    
    try:
        print(f"[LOG] Loading voices from: {voices_file}")
        with open(voices_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        voices = data.get("voices", {})
        print(f"[LOG] Loaded {len(voices)} voices for {tts_engine}")
        return voices
    except Exception as e:
        print(f"[ERROR] Failed to load voices for {tts_engine}: {e}")
        return {}

def get_voice_options(tts_engine: str) -> list:
    print(f"[LOG] get_voice_options called for: {tts_engine}")
    voices = load_voices_for_tts(tts_engine)
    options = [ft.dropdown.Option("auto", "auto - Détection automatique")]
    
    for voice_id, voice_data in sorted(voices.items()):
        lang_name = voice_data.get("language_name", voice_data.get("name", voice_id))
        options.append(ft.dropdown.Option(voice_id, f"{voice_id} - {lang_name}"))
    
    print(f"[LOG] Created {len(options)} voice options")
    return options

def is_edge_only_param(param: str) -> bool:
    return param in EDGE_ONLY_PARAMS

def validate_constraints() -> List[str]:
    warnings = []
    
    if state.tts != "edge":
        if state.melody:
            warnings.append("⚠️ --melody requires Edge TTS (48kHz)")
        if state.voice_effect and state.voice_effect != "none":
            warnings.append(f"⚠️ --voice-effect requires Edge TTS (48kHz)")
        if state.normalize:
            warnings.append("⚠️ --normalize may degrade quality with non-Edge engines")
        if state.wav_format == "32-bit":
            warnings.append("⚠️ --wav-format 32-bit requires Edge TTS")
    
    if not state.auto_play:
        if state.player and state.player != "auto":
            warnings.append("⚠️ --player requires --auto-play")
        if state.wait_finish:
            warnings.append("⚠️ --wait-finish requires --auto-play")
    
    if not state.text and state.tts:
        warnings.append("⚠️ --text is required for synthesis")
    
    return warnings

def build_command() -> List[str]:
    print("[LOG] build_command called")
    cmd = ["python3", os.path.join(SCRIPT_DIR, "gv.py")]
    
    cmd.extend(["--tts", state.tts])
    if state.text:
        cmd.extend(["--text", state.text])
    if state.voice and state.voice != "auto":
        cmd.extend(["--voice", state.voice])
    if state.duration and state.duration != "auto":
        cmd.extend(["--duration", str(state.duration)])
    if state.output and state.output != "auto":
        cmd.extend(["--output", state.output])
    if state.voice_effect and state.voice_effect != "none":
        cmd.extend(["--voice-effect", state.voice_effect])
    if state.player and state.player != "auto":
        cmd.extend(["--player", state.player])
    if state.wav_format and state.wav_format != "16-bit":
        cmd.extend(["--wav-format", state.wav_format])
    if state.fade_in:
        cmd.extend(["--fade-in", str(state.fade_in)])
    if state.fade_out:
        cmd.extend(["--fade-out", str(state.fade_out)])
    if state.system_os and state.system_os != "auto":
        cmd.extend(["--system-os", state.system_os])
    if state.melody:
        cmd.append("--melody")
    if state.auto_play:
        cmd.append("--auto-play")
    if state.wait_finish:
        cmd.append("--wait-finish")
    if state.normalize:
        cmd.append("--normalize")
    
    print(f"[LOG] Command built: {' '.join(cmd)}")
    return cmd

def build_solo_command(solo_param: str) -> List[str]:
    print(f"[LOG] build_solo_command called for: {solo_param}")
    cmd = ["python3", os.path.join(SCRIPT_DIR, "gv.py")]
    
    if solo_param == "help":
        cmd.append("--help")
    elif solo_param == "list-engines":
        cmd.append("--list-engines")
    elif solo_param == "list-launchers":
        cmd.append("--list-launchers")
    elif solo_param == "auto-fix":
        cmd.append("--auto-fix")
    elif solo_param == "launcher":
        cmd.extend(["--launcher", "genericmenu"])
    
    print(f"[LOG] Solo command built: {' '.join(cmd)}")
    return cmd

print("[LOG] Functions defined")

def main(page: ft.Page):
    print("=" * 60)
    print("[LOG] main() function called")
    print("=" * 60)
    
    print("[LOG] Setting page properties...")
    page.title = "Generic Voice v1.0.2"
    print("[LOG] page.title set")
    
    page.window.width = 1000
    print("[LOG] page.window.width set")
    
    page.window.height = 750
    print("[LOG] page.window.height set")
    
    page.theme_mode = ft.ThemeMode.DARK
    print("[LOG] page.theme_mode set")
    
    page.bgcolor = DARK
    print("[LOG] page.bgcolor set")
    
    print("[LOG] Creating result_text...")
    result_text = ft.Text(value="", size=11, color=PRIMARY, font_family="monospace", selectable=True)
    print("[LOG] result_text created")
    
    warning_text = ft.Text(value="", size=10, color=WARNING, font_family="monospace")
    command_preview = ft.Text(value="", size=10, color=TEXT_SECONDARY, font_family="monospace", selectable=True)
    
    print("[LOG] Creating TTS tab content...")
    
    print("[LOG] Creating tts_dropdown...")
    tts_dropdown = ft.Dropdown(
        label="Moteur TTS",
        value=state.tts,
        options=[
            ft.dropdown.Option("piper", "Piper - Offline (22kHz)"),
            ft.dropdown.Option("edge", "Edge - Microsoft Cloud (48kHz)"),
            ft.dropdown.Option("espeak", "eSpeak - Open Source (22kHz)"),
        ],
        width=400,
    )
    print("[LOG] tts_dropdown created")
    
    print("[LOG] Creating voice_dropdown...")
    voice_dropdown = ft.Dropdown(
        label="Voix",
        value=state.voice,
        options=get_voice_options(state.tts),
        width=400,
    )
    print("[LOG] voice_dropdown created")
    
    print("[LOG] Creating text_field...")
    text_field = ft.TextField(
        label="Texte à synthétiser",
        value=state.text,
        multiline=True,
        min_lines=3,
        max_lines=6,
        width=600,
    )
    print("[LOG] text_field created")
    
    print("[LOG] Creating Audio tab content...")
    
    duration_dropdown = ft.Dropdown(
        label="Durée",
        value=state.duration,
        options=[
            ft.dropdown.Option("auto", "auto - Détection automatique"),
            ft.dropdown.Option("5", "5 secondes"),
            ft.dropdown.Option("10", "10 secondes"),
            ft.dropdown.Option("30", "30 secondes"),
            ft.dropdown.Option("60", "60 secondes"),
        ],
        width=200,
    )
    print("[LOG] duration_dropdown created")
    
    output_field = ft.TextField(
        label="Fichier de sortie",
        value=state.output,
        hint_text="auto ou /chemin/vers/fichier.wav",
        width=400,
    )
    print("[LOG] output_field created")
    
    wav_format_dropdown = ft.Dropdown(
        label="Format WAV",
        value=state.wav_format,
        options=[
            ft.dropdown.Option("16-bit", "16-bit PCM (Standard)"),
            ft.dropdown.Option("32-bit", "32-bit Float (Edge uniquement)"),
        ],
        width=200,
    )
    print("[LOG] wav_format_dropdown created")
    
    normalize_switch = ft.Switch(label="Normalize - Normalisation audio", value=state.normalize)
    print("[LOG] normalize_switch created")
    
    fade_in_field = ft.TextField(label="Fade-in (ms)", value=str(state.fade_in), width=100)
    fade_out_field = ft.TextField(label="Fade-out (ms)", value=str(state.fade_out), width=100)
    print("[LOG] fade fields created")
    
    print("[LOG] Creating Effects tab content...")
    
    voice_effect_dropdown = ft.Dropdown(
        label="Effet vocal",
        value=state.voice_effect,
        options=[
            ft.dropdown.Option("none", "Aucun"),
            ft.dropdown.Option("echo", "Echo - Écho multi-tap"),
            ft.dropdown.Option("vibrato", "Vibrato - Modulation de fréquence"),
            ft.dropdown.Option("reverb", "Reverb - Réverbération"),
        ],
        width=300,
    )
    
    melody_switch = ft.Switch(label="Melody - Génération mélodique", value=state.melody)
    
    effects_info_text = ft.Text(
        "ℹ️ melody et voice-effect sont optimisés avec Edge TTS (48kHz) — compatibilité vérifiée à l'exécution",
        size=11,
        color=TEXT_SECONDARY,
    )
    
    effects_tab_content = ft.Column([
        ft.Text("Effets Vocaux", size=18, weight=ft.FontWeight.BOLD, color=WHITE),
        effects_info_text,
        ft.Container(height=10),
        voice_effect_dropdown,
        ft.Container(height=10),
        melody_switch,
    ], scroll=ft.ScrollMode.AUTO)
    print("[LOG] effects_tab_content created")
    
    print("[LOG] Creating Playback tab content...")
    
    auto_play_switch = ft.Switch(label="Auto-play - Lecture automatique", value=state.auto_play)
    
    player_dropdown = ft.Dropdown(
        label="Lecteur audio",
        value=state.player,
        options=[
            ft.dropdown.Option("auto", "auto - Détection automatique"),
            ft.dropdown.Option("parole", "parole - Ubuntu"),
            ft.dropdown.Option("cvlc", "cvlc - VLC CLI"),
            ft.dropdown.Option("vlc", "vlc - VLC GUI"),
            ft.dropdown.Option("ffplay", "ffplay - FFmpeg"),
            ft.dropdown.Option("aplay", "aplay - ALSA"),
        ],
        width=300,
    )
    
    wait_finish_switch = ft.Switch(label="Wait-finish - Attendre la fin", value=state.wait_finish)
    
    playback_info_text = ft.Text(
        "ℹ️ player et wait-finish nécessitent auto-play — compatibilité vérifiée à l'exécution",
        size=11,
        color=TEXT_SECONDARY,
    )
    
    playback_tab_content = ft.Column([
        ft.Text("Lecture Audio", size=18, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Text("Configuration de la lecture audio", size=12, color=TEXT_SECONDARY),
        ft.Container(height=10),
        auto_play_switch,
        ft.Container(height=10),
        playback_info_text,
        ft.Container(height=10),
        player_dropdown,
        ft.Container(height=10),
        wait_finish_switch,
    ], scroll=ft.ScrollMode.AUTO)
    print("[LOG] playback_tab_content created")
    
    print("[LOG] Creating Advanced tab content...")
    
    system_os_dropdown = ft.Dropdown(
        label="Système d'exploitation",
        value=state.system_os,
        options=[
            ft.dropdown.Option("auto", "auto - Détection automatique"),
            ft.dropdown.Option("ubuntu", "Ubuntu"),
            ft.dropdown.Option("linux", "Linux générique"),
            ft.dropdown.Option("windows", "Windows"),
            ft.dropdown.Option("darwin", "macOS"),
        ],
        width=300,
    )
    
    advanced_tab_content = ft.Column([
        ft.Text("Paramètres Avancés", size=18, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Text("Configuration système et debugging", size=12, color=TEXT_SECONDARY),
        ft.Container(height=10),
        system_os_dropdown,
    ], scroll=ft.ScrollMode.AUTO)
    print("[LOG] advanced_tab_content created")
    
    print("[LOG] Creating Tools tab content...")
    
    tools_result_text = ft.Text(value="", size=11, color=PRIMARY, font_family="monospace", selectable=True)
    
    list_engines_btn = ft.Button(
        content="📋 Lister les moteurs TTS",
        on_click=lambda e: run_solo_command("list-engines", tools_result_text),
        style=ft.ButtonStyle(bgcolor=PRIMARY_DARK, color=WHITE, padding=10),
    )
    
    list_launchers_btn = ft.Button(
        content="🖥️ Lister les interfaces",
        on_click=lambda e: run_solo_command("list-launchers", tools_result_text),
        style=ft.ButtonStyle(bgcolor=PRIMARY_DARK, color=WHITE, padding=10),
    )
    
    auto_fix_btn = ft.Button(
        content="🔧 Installer les dépendances",
        on_click=lambda e: run_solo_command("auto-fix", tools_result_text),
        style=ft.ButtonStyle(bgcolor=SUCCESS, color=WHITE, padding=10),
    )
    
    help_btn = ft.Button(
        content="❓ Afficher l'aide",
        on_click=lambda e: run_solo_command("help", tools_result_text),
        style=ft.ButtonStyle(bgcolor=DARK_LIGHT, color=WHITE, padding=10),
    )
    
    launcher_btn = ft.Button(
        content="🚀 Lancer GenericMenu",
        on_click=lambda e: run_solo_command("launcher", tools_result_text),
        style=ft.ButtonStyle(bgcolor=WARNING, color=DARK, padding=10),
    )
    
    tools_tab_content = ft.Column([
        ft.Text("Outils & Actions", size=18, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Text("Commandes autonomes (sans paramètres supplémentaires)", size=12, color=TEXT_SECONDARY),
        ft.Container(height=20),
        ft.Text("Actions disponibles:", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Container(height=10),
        ft.Row([list_engines_btn, list_launchers_btn]),
        ft.Container(height=10),
        ft.Row([auto_fix_btn, help_btn]),
        ft.Container(height=10),
        launcher_btn,
        ft.Container(height=20),
        ft.Text("Résultat:", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Container(height=10),
        tools_result_text,
    ], scroll=ft.ScrollMode.AUTO)
    print("[LOG] tools_tab_content created")
    
    def update_constraints():
        page.update()
    
    def run_solo_command(solo_param: str, result_control: ft.Text):
        print(f"[LOG] Running solo command: {solo_param}")
        cmd = build_solo_command(solo_param)
        result_control.value = f"Exécution: {' '.join(cmd)}\n\nEn cours..."
        page.update()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            print(f"[LOG] Solo command completed with returncode: {result.returncode}")
            output = result.stdout if result.returncode == 0 else result.stderr
            if len(output) > 3000:
                output = output[-3000:]
            result_control.value = output
            print("[LOG] Solo command result displayed")
        except subprocess.TimeoutExpired:
            result_control.value = f"✗ Timeout (>120s)\n\nCommande: {' '.join(cmd)}"
            print("[ERROR] Solo command timeout")
        except Exception as ex:
            result_control.value = f"✗ Exception: {ex}\n\nCommande: {' '.join(cmd)}"
            print(f"[ERROR] Solo command exception: {ex}")
        
        page.update()
    
    def on_tts_change(e):
        print(f"[LOG] on_tts_change called with value: {e.control.value}")
        voice_dropdown.options = get_voice_options(e.control.value)
        voice_dropdown.value = "auto"
        state.tts = e.control.value
        update_constraints()
        on_param_change()
        print("[LOG] on_tts_change complete")
    
    tts_dropdown.on_change = on_tts_change
    print("[LOG] tts_dropdown.on_change assigned")
    
    def on_auto_play_change(e):
        print(f"[LOG] on_auto_play_change called with value: {e.control.value}")
        state.auto_play = e.control.value
        update_constraints()
        on_param_change()
        print("[LOG] on_auto_play_change complete")
    
    auto_play_switch.on_change = on_auto_play_change
    
    def on_param_change(e=None):
        state.tts = tts_dropdown.value
        state.voice = voice_dropdown.value
        state.text = text_field.value
        state.duration = duration_dropdown.value
        state.output = output_field.value
        state.wav_format = wav_format_dropdown.value
        state.normalize = normalize_switch.value
        state.fade_in = int(fade_in_field.value) if fade_in_field.value.isdigit() else 50
        state.fade_out = int(fade_out_field.value) if fade_out_field.value.isdigit() else 80
        state.voice_effect = voice_effect_dropdown.value
        state.melody = melody_switch.value
        state.auto_play = auto_play_switch.value
        state.player = player_dropdown.value
        state.wait_finish = wait_finish_switch.value
        state.system_os = system_os_dropdown.value
        
        warnings = validate_constraints()
        if warnings:
            warning_text.value = "\n".join(warnings)
        else:
            warning_text.value = ""
        
        cmd = build_command()
        command_preview.value = f"Commande: {' '.join(cmd)}"
        page.update()
    
    tts_tab_content = ft.Column([
        ft.Text("Moteur TTS", size=18, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Text("Sélectionnez le moteur de synthèse vocale", size=12, color=TEXT_SECONDARY),
        ft.Container(height=10),
        tts_dropdown,
        ft.Container(height=10),
        ft.Text("Voix", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
        voice_dropdown,
        ft.Container(height=10),
        ft.Text("Texte", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
        text_field,
    ], scroll=ft.ScrollMode.AUTO)
    print("[LOG] tts_tab_content created")
    
    audio_tab_content = ft.Column([
        ft.Text("Paramètres Audio", size=18, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Text("Configuration de la sortie audio", size=12, color=TEXT_SECONDARY),
        ft.Container(height=10),
        ft.Row([duration_dropdown, wav_format_dropdown]),
        ft.Container(height=10),
        output_field,
        ft.Container(height=10),
        normalize_switch,
        ft.Container(height=10),
        ft.Text("Fades", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
        ft.Row([fade_in_field, fade_out_field]),
    ], scroll=ft.ScrollMode.AUTO)
    print("[LOG] audio_tab_content created")
    
    print("[LOG] Creating generate button and callback...")
    
    def on_generate(e):
        print("[LOG] on_generate called")
        print(f"[LOG] TTS: {tts_dropdown.value}")
        print(f"[LOG] Voice: {voice_dropdown.value}")
        
        state.tts = tts_dropdown.value
        state.voice = voice_dropdown.value
        state.text = text_field.value
        state.duration = duration_dropdown.value
        state.output = output_field.value
        state.wav_format = wav_format_dropdown.value
        state.normalize = normalize_switch.value
        state.fade_in = int(fade_in_field.value) if fade_in_field.value.isdigit() else 50
        state.fade_out = int(fade_out_field.value) if fade_out_field.value.isdigit() else 80
        state.voice_effect = voice_effect_dropdown.value
        state.melody = melody_switch.value
        state.auto_play = auto_play_switch.value
        state.player = player_dropdown.value
        state.wait_finish = wait_finish_switch.value
        state.system_os = system_os_dropdown.value
        
        warnings = validate_constraints()
        if warnings:
            warning_text.value = "\n".join(warnings)
        
        cmd = build_command()
        
        result_text.value = f"Commande:\n{' '.join(cmd)}\n\nExécution..."
        print("[LOG] Updating page with initial result...")
        page.update()
        
        print(f"[LOG] Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            print(f"[LOG] Command completed with returncode: {result.returncode}")
            if result.returncode == 0:
                output = result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout
                result_text.value = f"✓ Succès\n\nCommande:\n{' '.join(cmd)}\n\nOutput:\n{output}"
                print("[LOG] Success!")
            else:
                result_text.value = f"✗ Erreur (code {result.returncode})\n\nCommande:\n{' '.join(cmd)}\n\nError:\n{result.stderr}"
                print(f"[ERROR] Command failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            result_text.value = f"✗ Timeout (>60s)\n\nCommande:\n{' '.join(cmd)}"
            print("[ERROR] Command timeout")
        except Exception as ex:
            result_text.value = f"✗ Exception: {ex}\n\nCommande:\n{' '.join(cmd)}"
            print(f"[ERROR] Exception: {ex}")
        
        page.update()
        print("[LOG] on_generate complete")
    
    generate_btn = ft.Button(
        content="Générer",
        on_click=on_generate,
        style=ft.ButtonStyle(bgcolor=PRIMARY, color=WHITE, padding=15),
    )
    print("[LOG] generate_btn created")
    
    print("[LOG] Building main layout with Tabs...")
    
    print("[LOG] Creating TabBar...")
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="TTS"),
            ft.Tab(label="Audio"),
            ft.Tab(label="Effects"),
            ft.Tab(label="Playback"),
            ft.Tab(label="Advanced"),
            ft.Tab(label="Tools"),
        ],
    )
    print("[LOG] TabBar created")
    
    print("[LOG] Creating TabBarView...")
    tab_bar_view = ft.TabBarView(
        expand=True,
        controls=[
            ft.Container(content=tts_tab_content, padding=10),
            ft.Container(content=audio_tab_content, padding=10),
            ft.Container(content=effects_tab_content, padding=10),
            ft.Container(content=playback_tab_content, padding=10),
            ft.Container(content=advanced_tab_content, padding=10),
            ft.Container(content=tools_tab_content, padding=10),
        ],
    )
    print("[LOG] TabBarView created")
    
    print("[LOG] Creating Tabs Column...")
    tabs_column = ft.Column(
        expand=True,
        controls=[
            tab_bar,
            ft.Container(
                content=ft.Text("🎤 Generic Voice v1.0.2 - TTS Synthesis", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY),
                padding=10,
            ),
            tab_bar_view,
        ],
    )
    print("[LOG] Tabs Column created")
    
    print("[LOG] Creating Tabs...")
    tabs = ft.Tabs(
        length=6,
        selected_index=0,
        expand=True,
        content=tabs_column,
    )
    print("[LOG] Tabs created")
    
    print("[LOG] Creating SafeArea...")
    safe_area = ft.SafeArea(
        expand=True,
        content=tabs,
    )
    print("[LOG] SafeArea created")
    
    print("[LOG] Adding SafeArea to page...")
    page.add(safe_area)
    print("[LOG] SafeArea added to page")
    
    print("[LOG] Adding warnings and command preview...")
    page.add(ft.Container(content=warning_text, padding=5))
    page.add(ft.Container(content=command_preview, padding=5))
    print("[LOG] Warnings and preview added to page")
    
    print("[LOG] Adding generate button to page...")
    page.add(ft.Container(content=generate_btn, padding=10))
    print("[LOG] Generate button added to page")
    
    print("[LOG] Adding result section to page...")
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Résultat", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
                ft.Container(height=5),
                result_text,
            ]),
            padding=10,
        )
    )
    print("[LOG] Result section added to page")
    
    update_constraints()
    
    print("=" * 60)
    print("[LOG] main() function COMPLETE - UI READY")
    print("=" * 60)

if __name__ == "__main__":
    print("[LOG] Script started")
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--web", action="store_true", help="Run in web browser mode")
    parser.add_argument("--port", type=int, default=8555, help="Port")
    args, _ = parser.parse_known_args()
    
    print("🚀 Lancement gvflet...")
    if args.web:
        print(f"   Mode: Web Browser")
        print(f"   URL: http://localhost:{args.port}")
        print("[LOG] Calling ft.run with WEB_BROWSER view")
        ft.run(main, port=args.port, view=ft.AppView.WEB_BROWSER)
    else:
        print("   Mode: Desktop App")
        print("[LOG] Calling ft.run with default view (desktop)")
        ft.run(main, port=args.port)