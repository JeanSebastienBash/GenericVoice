"""
Module: player.py
Purpose: Abstracts audio playback across different players (vlc, cvlc, ffplay, aplay, parole). Platform-specific player detection and execution.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/system/detect.py, py/gv.py, py/gvflet.py
"""


import subprocess
import os
import sys

import sys
import os
_errors_path = os.path.join(os.path.dirname(__file__), "..")
if _errors_path not in sys.path:
    sys.path.insert(0, _errors_path)
from errors import print_warning

AVAILABLE_PLAYERS = {
    "parole": {"name": "Parole", "cmd": "parole", "os": ["ubuntu"]},
    "aplay": {"name": "ALSA", "cmd": "aplay", "os": ["ubuntu", "linux"]},
    "ffplay": {"name": "FFplay", "cmd": "ffplay", "os": ["ubuntu", "linux", "macos", "windows"]},
    "cvlc": {"name": "VLC CLI", "cmd": "cvlc", "os": ["ubuntu", "linux", "macos", "windows"]},
    "vlc": {"name": "VLC", "cmd": "vlc", "os": ["ubuntu", "linux", "macos", "windows"]},
}

DEFAULT_PLAYERS = {
    "ubuntu": "parole",
    "linux": "cvlc",
    "macos": "vlc",
    "windows": "vlc",
}

PLATFORM_OS_MAP = {
    "ubuntu": "ubuntu",
    "debian": "ubuntu",
    "linux": "linux",
    "darwin": "macos",
    "win32": "windows",
}

def get_platform_os():
    
    system = sys.platform.lower()
    return PLATFORM_OS_MAP.get(system, "linux")

def get_os_name():
    
    if hasattr(os, "uname"):
        try:
            return os.uname().sysname.lower()
        except:
            pass
    return "linux"

def get_available_players(os_name=None):
    
    if os_name is None:
        os_name = get_platform_os()
    
    players = []
    for player_id, info in AVAILABLE_PLAYERS.items():
        if os_name in info["os"]:
            players.append((player_id, info["name"]))
    
    return players

def get_default_player(os_name=None):
    
    if os_name is None:
        os_name = get_platform_os()
    
    return DEFAULT_PLAYERS.get(os_name, "cvlc")

def is_player_available(player_id):
    
    if player_id not in AVAILABLE_PLAYERS:
        return False
    
    cmd = AVAILABLE_PLAYERS[player_id]["cmd"]
    
    try:
        result = subprocess.run(
            ["which", cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def get_player_description(player_id: str) -> str:
    
    return AVAILABLE_PLAYERS.get(player_id, {}).get("name", player_id)

def play(audio_file, player_id=None, os_name=None):
    
    if not os.path.exists(audio_file):
        print_warning("Unknown Player", 
            "Fichier audio non trouve",
            f"Impossible de lire: {audio_file}",
            details=[f"Le fichier n'existe pas ou est inaccessible"],
            hint="Verifiez le chemin du fichier"
        )
        return False
    
    if player_id is None:
        player_id = get_default_player(os_name)
    
    if player_id not in AVAILABLE_PLAYERS:
        available = [p for p in AVAILABLE_PLAYERS.keys()]
        print_warning("Unknown Player", message=f"Le player '{player_id}' n'est pas un player reconnu.", details=[f"Players disponibles: {', '.join(available)}"])
        return False
    
    if not is_player_available(player_id):
        available = [p for p in AVAILABLE_PLAYERS.keys() if is_player_available(p)]
        if available:
            print_warning("Unknown Player", 
                "Player non installe",
                f"Le player '{player_id}' n'est pas installe sur ce systeme.",
                details=[
                    f"Players audio disponibles: {', '.join(available)}"
                ],
                hint=f"Essayez: python3 gv.py --auto-play --player {available[0]}"
            )
        else:
            print_warning("Unknown Player", 
                "Aucun player audio",
                "Aucun player audio n'est installe sur ce systeme.",
                details=[
                    "Installez un player: vlc, ffplay, parole, aplay...",
                    "Ou lancez: python3 gv.py --auto-fix"
                ],
                hint="Installez VLC ou FFplay pour ecouter l'audio"
            )
        return False
    
    cmd = AVAILABLE_PLAYERS[player_id]["cmd"]
    
    try:
        if player_id in ["vlc", "cvlc"]:
            subprocess.Popen(
                [cmd, "--play-and-pause", audio_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        elif player_id == "parole":
            subprocess.Popen(
                [cmd, audio_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        elif player_id == "ffplay":
            subprocess.Popen(
                [cmd, "-nodisp", "-autoexit", audio_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        elif player_id == "aplay":
            subprocess.Popen(
                [cmd, audio_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        else:
            subprocess.Popen(
                [cmd, audio_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        return True
    except Exception as e:
        print_warning("Unknown Player", 
            "Erreur de lecture",
            f"Echec de la lecture avec {player_id}: {e}",
            details=[f"Fichier: {audio_file}"],
            hint="Verifiez que le player est correctement installe"
        )
        return False

__all__ = [
    "get_platform_os",
    "get_os_name",
    "get_available_players",
    "get_default_player",
    "is_player_available",
    "play",
    "AVAILABLE_PLAYERS",
    "DEFAULT_PLAYERS",
]
