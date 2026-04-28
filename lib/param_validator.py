"""
Module: param_validator.py
Purpose: Validates command-line arguments, checks parameter dependencies, and provides validation error reporting.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect synthesis pipeline, audio quality, or CLI behavior.
Related: lib/config.py, py/gv.py
"""


import sys
from typing import Dict, List, Optional, Tuple

try:
    from errors import print_header, print_footer
except ImportError:
    def print_header():
        print("=" * 70)
        print("  G E N E R I C   V O I C E")
        print("  Menu Launcher v1.0.2")
        print("=" * 70)
        print()

    def print_footer():
        print("=" * 70)
        print("  Aide: python3 gv.py --help | python3 gv.py")
        print("  Documentation: https://github.com/JeanSebastienBash/GenericVoice")
        print("  Contact: DreamprojectAI - https://dreamproject.online")
        print("=" * 70)
        print()

VALUE_OPTIONS = {
    "tts": {
        "values": ["piper", "edge", "espeak"],
        "default": "piper",
        "desc": "Moteur TTS",
        "long_desc": "Le moteur TTS (Text-to-Speech) est le coeur de la synthese vocale.",
    },
    "voice": {
        "values": None,
        "default": "auto",
        "desc": "Voix a utiliser",
    },
    "text": {
        "values": None,
        "default": None,
        "desc": "Texte a synthetiser",
    },
    "duration": {
        "values": None,
        "default": "auto",
        "desc": "Duree en secondes ou 'auto'",
    },
    "output": {
        "values": None,
        "default": "auto",
        "desc": "Chemin du fichier WAV de sortie",
    },
    "voice-effect": {
        "values": ["echo", "vibrato", "reverb", "none"],
        "default": None,
        "desc": "Effet vocal",
    },
    "player": {
        "values": ["parole", "cvlc", "vlc", "ffplay", "aplay"],
        "default": "auto",
        "desc": "Player audio",
    },
    "wav-format": {
        "values": ["16-bit", "32-bit"],
        "default": "16-bit",
        "desc": "Format WAV",
    },
    "fade-in": {
        "values": None,
        "default": "50",
        "desc": "Duree fade-in en ms (entier >= 0)",
    },
    "fade-out": {
        "values": None,
        "default": "80",
        "desc": "Duree fade-out en ms (entier >= 0)",
    },
    "system-os": {
        "values": ["ubuntu", "linux", "windows", "darwin"],
        "default": "auto",
        "desc": "Systeme d'exploitation force",
    },
    "launcher": {
        "values": ["genericmenu"],
        "default": "genericmenu",
        "desc": "Backend IHM",
    },
}

FLAG_OPTIONS = [
    "melody",
    "auto-play",
    "wait-finish",
    "normalize",
    "auto-fix",
    "list-engines",
    "list-launchers",
    "help",
]

ALL_CLI_OPTIONS = [f"--{opt}" for opt in list(VALUE_OPTIONS.keys()) + FLAG_OPTIONS]

SOLO_PARAMS = ["help", "list-engines", "list-launchers", "auto-fix", "launcher"]

REQUIRE_TTS = [
    "text",
    "voice",
    "duration",
    "output",
    "melody",
    "voice-effect",
    "auto-play",
    "player",
    "wait-finish",
    "normalize",
    "wav-format",
    "fade-in",
    "fade-out",
]

REQUIRE_AUTO_PLAY = ["player", "wait-finish"]

EDGE_ONLY_PARAMS = {
    "melody": {
        "reason": "La generation de melodie necessite un sample rate de 48000 Hz",
        "supported_tts": ["edge"],
    },
    "voice-effect": {
        "reason": "Les effets vocaux (echo, reverb, vibrato) necessitent un sample rate de 48000 Hz",
        "supported_tts": ["edge"],
    },
    "normalize": {
        "reason": "La normalisation aggressive peut degrader la qualite des moteurs 22050 Hz",
        "supported_tts": ["edge"],
    },
    "wav-format": {
        "reason": "Le format 32-bit n'est supporte que par Edge TTS",
        "supported_tts": ["edge"],
        "valid_value": "32-bit",
    },
}

def print_validation_error(error: Dict) -> None:
    
    print_header()

    print("=" * 70)
    print(f"  ERREUR: {error['title']}")
    print("=" * 70)

    print(f"  {error['message']}")
    print()

    if error.get("explanation"):
        for line in error["explanation"]:
            print(f"  {line}")
        print()

    if error.get("params_found"):
        print("  Parametres trouves dans votre commande:")
        for p in error["params_found"]:
            print(f"    {p} (= incorrect avec --{error.get('solo_param', 'help')})")
        print()

    if error.get("valid_values"):
        print("  Valeurs valides pour cette option:")
        for v in error["valid_values"]:
            print(f"    - {v}")
        print()

    if error.get("example"):
        print("  Exemple d'utilisation correcte:")
        print(f"    {error['example']}")
        print()

    if error.get("hint"):
        print(f"  [CONSEIL] {error['hint']}")
        print()

    print("=" * 70)
    print_footer()

def print_validation_errors(errors: List[Dict]) -> None:
    
    for error in errors:
        print_validation_error(error)

def validate_solo_params(parsed: Dict) -> List[Dict]:
    
    errors = []

    for solo_param in SOLO_PARAMS:
        key = solo_param.replace("-", "_")
        if parsed.get(key):
            other_params = []
            for k, v in parsed.items():
                if k != key and v:
                    if k in VALUE_OPTIONS and v:
                        other_params.append(f"--{k.replace('_', '-')}")
                    elif k in [f.replace("-", "_") for f in FLAG_OPTIONS] and v:
                        other_params.append(f"--{k.replace('_', '-')}")

            if other_params:
                errors.append(
                    {
                        "title": f"--{solo_param} doit etre utilise seul",
                        "message": f"L'option --{solo_param} ne peut pas etre combinee avec d'autres options.",
                        "explanation": [
                            f"L'option --{solo_param} est une commande autonome.",
                            "Elle doit etre utilisee seule, sans autres parametres.",
                        ],
                        "params_found": other_params,
                        "solo_param": solo_param,
                        "example": f"python3 gv.py --{solo_param}",
                        "hint": f"Executez 'python3 gv.py --{solo_param}' seul",
                    }
                )

    return errors

def validate_tts_dependency(parsed: Dict) -> List[Dict]:
    
    errors = []

    if not parsed.get("tts"):
        for param in REQUIRE_TTS:
            key = param.replace("-", "_")
            value = parsed.get(key)
            if value:
                if isinstance(value, bool) and value:
                    errors.append(
                        {
                            "title": f"--{param} necessite --tts",
                            "message": f"L'option --{param} ne peut etre utilisee que si --tts est specifie.",
                            "explanation": [
                                f"--{param} est un parametre de synthese.",
                                "Il necessite qu'un moteur TTS soit selectionne.",
                                "Le moteur TTS (Text-to-Speech) est le coeur de la synthese vocale.",
                            ],
                            "example": f"python3 gv.py --tts piper --{param}",
                            "hint": f"Ajoutez --tts ENGINE avant --{param}",
                            "valid_values": ["piper", "edge", "espeak"],
                        }
                    )
                elif not isinstance(value, bool) and value:
                    errors.append(
                        {
                            "title": f"--{param} necessite --tts",
                            "message": f"L'option --{param} ne peut etre utilisee que si --tts est specifie.",
                            "explanation": [
                                f"--{param} est un parametre de synthese.",
                                "Il necessite qu'un moteur TTS soit selectionne.",
                                "Le moteur TTS (Text-to-Speech) est le coeur de la synthese vocale.",
                            ],
                            "example": f"python3 gv.py --tts piper --{param} {value}",
                            "hint": f"Ajoutez --tts <moteur> avant --{param}",
                            "valid_values": ["piper", "edge", "espeak"],
                        }
                    )

    return errors

def validate_auto_play_dependency(parsed: Dict) -> List[Dict]:
    
    errors = []

    if not parsed.get("auto_play"):
        if parsed.get("player"):
            errors.append(
                {
                    "title": "--player necessite --auto-play",
                    "message": "L'option --player ne peut etre utilisee que si --auto-play est active.",
                    "explanation": [
                        "Le lecteur audio (--player) permet de lire le fichier genere.",
                        "Il ne peut etre utilise que si la lecture automatique (--auto-play) est activee.",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour\" --auto-play --player cvlc",
                    "hint": "Ajoutez --auto-play avant --player",
                    "valid_values": ["parole", "cvlc", "vlc", "ffplay", "aplay"],
                }
            )

        if parsed.get("wait_finish"):
            errors.append(
                {
                    "title": "--wait-finish necessite --auto-play",
                    "message": "L'option --wait-finish ne peut etre utilisee que si --auto-play est active.",
                    "explanation": [
                        "L'option --wait-finish permet d'attendre la fin de la lecture.",
                        "Elle ne peut etre utilisee que si la lecture automatique (--auto-play) est activee.",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour\" --auto-play --wait-finish",
                    "hint": "Ajoutez --auto-play avant --wait-finish",
                }
            )

    return errors

def validate_param_values(parsed: Dict) -> List[Dict]:
    
    errors = []

    if parsed.get("tts") is not None and parsed["tts"] != "":
        valid = VALUE_OPTIONS["tts"]["values"]
        if parsed["tts"] not in valid:
            errors.append(
                {
                    "title": f"Valeur invalide pour --tts: '{parsed['tts']}'",
                    "message": f"Le moteur TTS '{parsed['tts']}' n'est pas reconnu.",
                    "explanation": [
                        "Le moteur TTS (Text-to-Speech) est le coeur de la synthese vocale.",
                        "Generic Voice supporte plusieurs moteurs differents.",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour le monde\"",
                    "hint": "Choisissez un moteur parmi les valeurs valides",
                    "valid_values": valid,
                }
            )
    elif parsed.get("tts") == "":
        errors.append(
            {
                "title": "Valeur vide pour --tts",
                "message": "L'option --tts necessite une valeur non vide.",
                "explanation": [
                    "Le moteur TTS (Text-to-Speech) est le coeur de la synthese vocale.",
                    "Vous devez specifier un moteur valide.",
                ],
                "example": "python3 gv.py --tts piper --text \"Bonjour le monde\"",
                "hint": "Choisissez un moteur parmi les valeurs valides",
                "valid_values": VALUE_OPTIONS["tts"]["values"],
            }
        )

    if parsed.get("voice_effect"):
        valid = VALUE_OPTIONS["voice-effect"]["values"]
        if parsed["voice_effect"] not in valid:
            errors.append(
                {
                    "title": f"Valeur invalide pour --voice-effect: '{parsed['voice_effect']}'",
                    "message": f"L'effet vocal '{parsed['voice_effect']}' n'est pas reconnu.",
                    "explanation": [
                        "Les effets vocaux permettent de modifier le son de la voix generee.",
                        "Generic Voice supporte plusieurs effets predefinis.",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Hi\" --voice-effect echo",
                    "hint": "Choisissez un effet parmi les valeurs valides",
                    "valid_values": valid,
                }
            )

    if parsed.get("player"):
        valid = VALUE_OPTIONS["player"]["values"]
        if parsed["player"] not in valid:
            errors.append(
                {
                    "title": f"Valeur invalide pour --player: '{parsed['player']}'",
                    "message": f"Le lecteur audio '{parsed['player']}' n'est pas reconnu.",
                    "explanation": [
                        "Le lecteur audio permet de lire le fichier WAV genere.",
                        "Il doit etre installe sur votre systeme pour fonctionner.",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour\" --auto-play --player cvlc",
                    "hint": "Choisissez un lecteur parmi les valeurs valides",
                    "valid_values": valid,
                }
            )

    if parsed.get("wav_format"):
        valid = VALUE_OPTIONS["wav-format"]["values"]
        if parsed["wav_format"] not in valid:
            errors.append(
                {
                    "title": f"Valeur invalide pour --wav-format: '{parsed['wav_format']}'",
                    "message": f"Le format WAV '{parsed['wav_format']}' n'est pas reconnu.",
                    "explanation": [
                        "Le format WAV determine la qualite et la taille du fichier audio.",
                        "Generic Voice supporte deux formats standards.",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour\" --wav-format 32-bit",
                    "hint": "Choisissez un format parmi les valeurs valides",
                    "valid_values": valid,
                }
            )

    if parsed.get("system_os"):
        valid = VALUE_OPTIONS["system-os"]["values"]
        if parsed["system_os"] not in valid:
            errors.append(
                {
                    "title": f"Valeur invalide pour --system-os: '{parsed['system_os']}'",
                    "message": f"Le systeme '{parsed['system_os']}' n'est pas reconnu.",
                    "explanation": [
                        "L'option --system-os permet de forcer le type de systeme.",
                        "Cela aide Generic Voice a installer les bonnes dependances.",
                    ],
                    "example": "python3 gv.py --system-os ubuntu",
                    "hint": "Choisissez un systeme parmi les valeurs valides",
                    "valid_values": valid,
                }
            )

    if parsed.get("fade_in"):
        try:
            val = int(parsed["fade_in"])
            if val < 0:
                errors.append(
                    {
                        "title": f"Valeur invalide pour --fade-in: '{parsed['fade_in']}'",
                        "message": "La duree de fade-in doit etre un entier positif ou nul.",
                        "explanation": [
                            "Le fade-in permet d'augmenter progressivement le volume au debut.",
                            "La duree doit etre exprimee en millisecondes (ms).",
                        ],
                        "example": "python3 gv.py --tts piper --text \"Bonjour\" --fade-in 100",
                        "hint": "Utilisez une valeur entiere positive ou nulle (ex: 100)",
                    }
                )
        except ValueError:
            errors.append(
                {
                    "title": f"Valeur invalide pour --fade-in: '{parsed['fade_in']}'",
                    "message": "La duree de fade-in doit etre un entier.",
                    "explanation": [
                        "Le fade-in permet d'augmenter progressivement le volume au debut.",
                        "La duree doit etre exprimee en millisecondes (ms).",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour\" --fade-in 100",
                    "hint": "Utilisez une valeur entiere (ex: 100)",
                }
            )

    if parsed.get("fade_out"):
        try:
            val = int(parsed["fade_out"])
            if val < 0:
                errors.append(
                    {
                        "title": f"Valeur invalide pour --fade-out: '{parsed['fade_out']}'",
                        "message": "La duree de fade-out doit etre un entier positif ou nul.",
                        "explanation": [
                            "Le fade-out permet de diminuer progressivement le volume a la fin.",
                            "La duree doit etre exprimee en millisecondes (ms).",
                        ],
                        "example": "python3 gv.py --tts piper --text \"Bonjour\" --fade-out 150",
                        "hint": "Utilisez une valeur entiere positive ou nulle (ex: 150)",
                    }
                )
        except ValueError:
            errors.append(
                {
                    "title": f"Valeur invalide pour --fade-out: '{parsed['fade_out']}'",
                    "message": "La duree de fade-out doit etre un entier.",
                    "explanation": [
                        "Le fade-out permet de diminuer progressivement le volume a la fin.",
                        "La duree doit etre exprimee en millisecondes (ms).",
                    ],
                    "example": "python3 gv.py --tts piper --text \"Bonjour\" --fade-out 150",
                    "hint": "Utilisez une valeur entiere (ex: 150)",
                }
            )

    if parsed.get("launcher"):
        valid = VALUE_OPTIONS["launcher"]["values"]
        if parsed["launcher"] not in valid:
            errors.append(
                {
                    "title": f"Valeur invalide pour --launcher: '{parsed['launcher']}'",
                    "message": f"Le backend IHM '{parsed['launcher']}' n'est pas reconnu.",
                    "explanation": [
                        "Le lanceur (ou backend IHM) est l'interface utilisateur.",
                        "Generic Voice supporte actuellement un seul lanceur.",
                    ],
                    "example": "python3 gv.py --launcher genericmenu",
                    "hint": "Utilisez 'genericmenu' comme valeur",
                    "valid_values": valid,
                }
            )

    return errors

def validate_tts_compatibility(parsed: Dict) -> List[Dict]:
    
    errors = []
    
    tts = parsed.get("tts", "piper")
    
    if not tts or tts == "auto":
        return errors
    
    for param, info in EDGE_ONLY_PARAMS.items():
        param_key = param.replace("-", "_")
        
        if parsed.get(param_key):
            supported = info["supported_tts"]
            
            if param == "wav-format":
                if parsed.get(param_key) == info.get("valid_value"):
                    if tts not in supported:
                        errors.append({
                            "title": f"--{param} incompatible avec --tts {tts}",
                            "message": f"Le format WAV 32-bit n'est pas compatible avec {tts}.",
                            "explanation": [
                                info["reason"],
                                f"Le moteur {tts} utilise une resolution native de 16-bit.",
                                "Seul Edge TTS supporte le format 32-bit.",
                            ],
                            "example": f"python3 gv.py --tts {tts} --text \"Bonjour\"",
                            "hint": "Utilisez --wav-format 16-bit ou supprimez l'option",
                            "valid_values": ["16-bit"],
                        })
            else:
                if tts not in supported:
                    errors.append({
                        "title": f"--{param} incompatible avec --tts {tts}",
                        "message": f"--{param} n'est pas compatible avec {tts}.",
                        "explanation": [
                            info["reason"],
                            f"Le moteur {tts} genere a 22050 Hz pour preserver la qualite.",
                            f"Seul{'s' if len(supported) > 1 else ''} {', '.join(supported)} supporte{'nt' if len(supported) > 1 else ''} cette option.",
                        ],
                        "example": f"python3 gv.py --tts edge --{param} --text \"Bonjour\"",
                        "hint": f"Utilisez --tts edge pour activer --{param}",
                        "valid_values": supported,
                    })
    
    return errors

def validate_all_params(parsed: Dict) -> List[Dict]:
    
    all_errors = []

    all_errors.extend(validate_solo_params(parsed))
    all_errors.extend(validate_tts_dependency(parsed))
    all_errors.extend(validate_auto_play_dependency(parsed))
    all_errors.extend(validate_param_values(parsed))
    all_errors.extend(validate_tts_compatibility(parsed))

    return all_errors

def get_param_info(param: str) -> Optional[Dict]:
    
    param_clean = param.lstrip("-").replace("_", "-")
    if param_clean in VALUE_OPTIONS:
        return VALUE_OPTIONS[param_clean]
    elif param_clean in FLAG_OPTIONS:
        return {"values": None, "default": False, "desc": f"Flag: --{param_clean}"}
    return None

def is_valid_combination(params: List[str]) -> Tuple[bool, List[str]]:
    
    reasons = []

    has_tts = "tts" in params
    has_auto_play = "auto-play" in params or "auto_play" in params

    for solo in SOLO_PARAMS:
        if solo in params and len(params) > 1:
            reasons.append(f"--{solo} doit etre utilise seul")

    if not has_tts:
        for param in REQUIRE_TTS:
            if param in params:
                reasons.append(f"--{param} necessite --tts")

    if not has_auto_play:
        if "player" in params:
            reasons.append("--player necessite --auto-play")
        if "wait-finish" in params or "wait_finish" in params:
            reasons.append("--wait-finish necessite --auto-play")

    return len(reasons) == 0, reasons

__all__ = [
    "VALUE_OPTIONS",
    "FLAG_OPTIONS",
    "ALL_CLI_OPTIONS",
    "SOLO_PARAMS",
    "REQUIRE_TTS",
    "REQUIRE_AUTO_PLAY",
    "validate_solo_params",
    "validate_tts_dependency",
    "validate_auto_play_dependency",
    "validate_param_values",
    "validate_all_params",
    "print_validation_error",
    "print_validation_errors",
    "get_param_info",
    "is_valid_combination",
]
