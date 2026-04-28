"""
Module: errors.py
Purpose: Provides error classes, header/footer formatting for CLI output, and consistent error messaging across the application.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: py/gv.py, py/gvflet.py
"""


import sys
import os

__version__ = "1.0.2"

def _separator(width: int = 70) -> str:
    
    return "=" * width

def _thin_separator(width: int = 70) -> str:
    
    return "-" * width

def _double_separator(width: int = 70) -> str:
    
    return "+" + "=" * (width - 2) + "+"

def print_header():
    
    print()
    print(_double_separator(70))
    print("|" + " " * 68 + "|")
    print("|" + " " * 20 + "G E N E R I C   V O I C E" + " " * 23 + "|")
    print("|" + " " * 24 + f"Menu Launcher v{__version__}" + " " * (68 - 24 - len(f"Menu Launcher v{__version__}")) + "|")
    print("|" + " " * 68 + "|")
    print(_double_separator(70))
    print()

def print_footer():
    
    print()
    print(_double_separator(70))
    print("|" + " " * 68 + "|")
    print("|  Aide:" + " " * 62 + "|")
    print("|    python3 gv.py --help                    Afficher l'aide complete" + " " * (68 - 61 - len("Afficher l'aide complete")) + "|")
    print("|    python3 gv.py                           Lancer le menu interactif" + " " * (68 - 60 - len("Lancer le menu interactif")) + "|")
    print("|    python3 gv.py --launcher genericmenu    Lancer le Generic Menu" + " " * (68 - 59 - len("Lancer le Generic Menu")) + "|")
    print("|" + " " * 68 + "|")
    print("|  Documentation:" + " " * 53 + "|")
    print("|    https://github.com/JeanSebastienBash/GenericVoice" + " " * 29+ "|")
    print("|" + " " * 68 + "|")
    print("|  Contact:" + " " * 58 + "|")
    print("|    DreamprojectAI - https://dreamproject.online" + " " * 18 + "|")
    print("|" + " " * 68 + "|")
    print(_double_separator(70))
    print()

def print_error(title: str, message: str, details: list = None, example: str = None, hint: str = None, width: int = 70):
    
    print_header()
    print(_separator(width))
    print(f"  ERREUR: {title}")
    print(_separator(width))
    print(f"  {message}")
    print()

    if details:
        for detail in details:
            print(f"    {detail}")
        print()

    if example:
        print(f"  Exemple:")
        print(f"    {example}")
        print()

    if hint:
        print(f"  [CONSEIL] {hint}")
        print()

    print(_separator(width))
    print_footer()

def print_warning(title: str, message: str, details: list = None, width: int = 70, hint: str = None):
    
    print()
    print(_thin_separator(width))
    print(f"  ATTENTION: {title}")
    print(_thin_separator(width))
    print(f"  {message}")
    print()

    if details:
        for detail in details:
            print(f"    {detail}")
        print()

    if hint:
        print(f"  [CONSEIL] {hint}")
        print()

    print(_thin_separator(width))
    print()

def print_info(title: str, message: str, details: list = None, width: int = 70):
    
    print()
    print(_thin_separator(width))
    print(f"  INFO: {title}")
    print(_thin_separator(width))
    print(f"  {message}")
    print()

    if details:
        for detail in details:
            print(f"    {detail}")
        print()

    print(_thin_separator(width))
    print()

def error_missing_option_value(option: str, valid_values: list = None, default: str = None, example: str = None):
    
    print_header()
    print(_separator())
    print(f"  ERREUR: L'option {option} necessite une valeur")
    print(_separator())
    print(f"  Vous avez utilise l'option {option} sans fournir de valeur.")
    print()
    print("  Cette option attend un parametre pour fonctionner correctement.")
    print()

    if valid_values:
        print("  Valeurs valides pour cette option:")
        for v in valid_values:
            print(f"    - {v}")
        print()

    if default:
        print(f"  Valeur par defaut: {default}")
        print()

    if example:
        print("  Exemple d'utilisation correcte:")
        print(f"    {example}")
        print()

    print("  [CONSEIL] Specifiez une valeur apres l'option")
    print(_separator())
    print_footer()

def error_unknown_option(option: str, all_options: list = None):
    
    print_header()
    print(_separator())
    print(f"  ERREUR: Option inconnue: {option}")
    print(_separator())
    print(f"  L'option '{option}' n'est pas reconnue par Generic Voice.")
    print()
    print("  Vous avez probablement fait une faute de frappe ou utilise")
    print("une option qui n'existe pas dans cette version.")
    print()

    if all_options:
        print("  Toutes les options disponibles:")
        max_per_line = 5
        for i in range(0, len(all_options), max_per_line):
            line_opts = all_options[i:i+max_per_line]
            print(f"    {'  '.join(line_opts)}")
        print()

    print("  [CONSEIL] Consultez l'aide avec --help pour voir toutes les options")
    print(_separator())
    print_footer()

def error_missing_tts_engine(engine: str, available_engines: dict):
    
    print_header()
    print(_separator())
    print(f"  ERREUR: Moteur TTS '{engine}' non disponible")
    print(_separator())
    print(f"  Le moteur TTS '{engine}' n'est pas installe ou accessible.")
    print()
    print("  Un moteur TTS (Text-to-Speech) est necessaire pour synthetiser")
    print("  du texte en audio. Verifiez que le moteur est bien installe.")
    print()

    print("  Moteurs TTS disponibles sur ce systeme:")
    for name, status in available_engines.items():
        status_text = "DISPONIBLE" if status else "NON DISPONIBLE"
        status_icon = "[OK]" if status else "[--]"
        print(f"    {status_icon} {name:15} {status_text}")
    print()

    print("  [CONSEIL] Utilisez --list-engines pour voir les moteurs disponibles")
    print(_separator())
    print_footer()

def error_missing_dependencies(missing: dict, install_command: str = None):
    
    print_header()
    print(_separator())
    print("  ERREUR: Dependances manquantes")
    print(_separator())
    print("  Des dependances requises sont absentes de votre systeme.")
    print()
    print("  Generic Voice a besoin de certains paquets pour fonctionner.")
    print("  Voici ce qui manque:")
    print()

    if missing.get("core"):
        print(f"    Core: {', '.join(missing['core'])}")
    if missing.get("ihm"):
        print(f"    IHM: {', '.join(missing['ihm'])}")
    if missing.get("python"):
        print(f"    Python: {', '.join(missing['python'])}")
    print()

    print("  [CONSEIL] Executez --auto-fix pour installer automatiquement")
    print(_separator())
    print_footer()

def error_invalid_os(os_value: str, valid_values: list):
    
    print_header()
    print(_separator())
    print(f"  ERREUR: Systeme d'exploitation invalide: '{os_value}'")
    print(_separator())
    print(f"  '{os_value}' n'est pas un systeme d'exploitation reconnu.")
    print()
    print("  L'option --system-os permet de forcer le type de systeme")
    print("  pour l'installation des dependances specifiques.")
    print()

    print("  Systemes d'exploitation valides:")
    for v in valid_values:
        print(f"    - {v}")
    print()

    print("  [CONSEIL] Ubuntu est recommande pour une experience optimale")
    print(_separator())
    print_footer()

def error_player_not_available(player: str, available_players: list):
    
    print_header()
    print(_separator())
    print(f"  ERREUR: Lecteur audio '{player}' non disponible")
    print(_separator())
    print(f"  Le lecteur audio '{player}' n'est pas installe sur ce systeme.")
    print()
    print("  Pour utiliser l'option --player avec --auto-play, vous devez")
    print("  avoir un lecteur audio installe sur votre systeme.")
    print()

    print("  Lecteurs audio disponibles sur ce systeme:")
    for p in available_players:
        print(f"    - {p}")
    print()

    print("  [CONSEIL] Installez un lecteur audio ou utilisez --auto-fix")
    print(_separator())
    print_footer()

def error_invalid_parameter(param: str, reason: str, valid_values: list = None, example: str = None):
    
    print_header()
    print(_separator())
    print(f"  ERREUR: Parametre invalide: {param}")
    print(_separator())
    print(f"  {reason}")
    print()

    if valid_values:
        print("  Valeurs valides pour ce parametre:")
        for v in valid_values:
            print(f"    - {v}")
        print()

    if example:
        print("  Exemple d'utilisation correcte:")
        print(f"    {example}")
        print()

    print("  [CONSEIL] Verifiez la valeur du parametre et reessayez")
    print(_separator())
    print_footer()

def error_file_not_found(file_path: str, search_locations: list = None):
    
    print_header()
    print(_separator())
    print("  ERREUR: Fichier non trouve")
    print(_separator())
    print(f"  Le fichier requis n'a pas ete trouve: {file_path}")
    print()

    if search_locations:
        print("  Emplacements recherches:")
        for loc in search_locations:
            print(f"    - {loc}")
        print()

    print("  [CONSEIL] Verifiez que le fichier existe ou reinstallez l'application")
    print(_separator())
    print_footer()

def error_permission_denied(action: str, item: str = None):
    
    print_header()
    print(_separator())
    print("  ERREUR: Permission refusee")
    print(_separator())
    print("  Vous n'avez pas la permission d'effectuer cette action.")
    print()

    if item:
        print(f"  Element: {item}")
    print(f"  Action: {action}")
    print()

    print("  [CONSEIL] Verifiez les permissions du fichier ou utilisez sudo")
    print(_separator())
    print_footer()

CLI_OPTIONS = {
    "tts": {"values": ["piper", "edge", "espeak"], "default": "piper", "desc": "Moteur TTS"},
    "text": {"values": None, "default": None, "desc": "Texte a synthetiser"},
    "voice": {"values": None, "default": "auto", "desc": "Voix a utiliser"},
    "duration": {"values": None, "default": "auto", "desc": "Duree en secondes ou 'auto'"},
    "output": {"values": None, "default": "auto", "desc": "Chemin du fichier WAV de sortie"},
    "melody": {"values": None, "default": False, "desc": "Activer la generation de melodie"},
    "voice-effect": {"values": ["echo", "vibrato", "reverb", "none"], "default": None, "desc": "Effet vocal"},
    "player": {"values": ["parole", "cvlc", "vlc", "ffplay", "aplay"], "default": "auto", "desc": "Player audio"},
    "auto-play": {"values": None, "default": False, "desc": "Lecture auto apres generation"},
    "wait-finish": {"values": None, "default": False, "desc": "Attendre fin lecture"},
    "normalize": {"values": None, "default": False, "desc": "Normaliser le volume audio"},
    "wav-format": {"values": ["16-bit", "32-bit"], "default": "16-bit", "desc": "Format WAV"},
    "fade-in": {"values": None, "default": "50", "desc": "Duree fade-in en ms"},
    "fade-out": {"values": None, "default": "80", "desc": "Duree fade-out en ms"},
    "system-os": {"values": ["ubuntu", "linux", "windows", "darwin"], "default": "auto", "desc": "Systeme d'exploitation force"},
    "launcher": {"values": ["genericmenu"], "default": "genericmenu", "desc": "Backend IHM"},
    "auto-fix": {"values": None, "default": False, "desc": "Auto-installer les dependances"},
    "list-engines": {"values": None, "default": False, "desc": "Lister les moteurs TTS"},
    "list-launchers": {"values": None, "default": False, "desc": "Lister les backends IHM"},
    "help": {"values": None, "default": False, "desc": "Afficher l'aide"},
}

FLAG_OPTIONS = ["melody", "auto-play", "wait-finish", "normalize", "auto-fix", "list-engines", "list-launchers", "help"]

def get_all_cli_options() -> list:
    
    return [f"--{opt}" for opt in CLI_OPTIONS.keys()]

def get_option_info(option: str) -> dict:
    
    return CLI_OPTIONS.get(option, {})

def suggest_similar_option(option: str) -> str:
    
    option_clean = option.lstrip('-')

    if option_clean in CLI_OPTIONS:
        return f"--{option_clean}"

    for opt in CLI_OPTIONS.keys():
        if option_clean in opt or opt in option_clean:
            return f"--{opt}"

    return None

__all__ = [
    "print_header",
    "print_footer",
    "print_error",
    "print_warning",
    "print_info",
    "error_missing_option_value",
    "error_unknown_option",
    "error_missing_tts_engine",
    "error_missing_dependencies",
    "error_invalid_os",
    "error_player_not_available",
    "error_invalid_parameter",
    "error_file_not_found",
    "error_permission_denied",
    "CLI_OPTIONS",
    "FLAG_OPTIONS",
    "get_all_cli_options",
    "get_option_info",
    "suggest_similar_option",
]
