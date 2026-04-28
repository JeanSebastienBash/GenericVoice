#!/usr/bin/env python3
"""
Module: gvcorevoices.py
Purpose: Installs the 5 Core Piper voice models from split ZIP archives. Extracts ONNX models for FR, EN, ES, IT, DE languages.
Context: Entry point script in py/. Part of Generic Voice v1.0.2 TTS suite.
Impact: Direct user-facing tool. Changes affect user workflow and voice installation.
Related: lib/tts/piper/voices/
"""


import os
import sys
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent
PIPER_VOICES_DIR = PROJECT_ROOT / "lib" / "tts" / "piper" / "voices"

CORE_VOICES = [
    "fr_FR-siwis-medium",
    "en_US-amy-medium",
    "es_ES-sharvard-medium",
    "it_IT-paola-medium",
    "de_DE-mls-medium",
]

def check_voice_installed(voice_name: str) -> bool:
    
    onnx_file = PIPER_VOICES_DIR / f"{voice_name}.onnx"
    return onnx_file.exists()

def find_zip_archives(voice_name: str) -> list:
    
    archives = []
    
    single_zip = PIPER_VOICES_DIR / f"{voice_name}.zip"
    if single_zip.exists():
        return [single_zip]
    
    chunk_idx = 1
    while True:
        chunk_file = PIPER_VOICES_DIR / f"{voice_name}.zip.{chunk_idx:03d}"
        if chunk_file.exists():
            archives.append(chunk_file)
            chunk_idx += 1
        else:
            break
    
    return archives

def has_any_zip_archives() -> bool:
    
    for f in PIPER_VOICES_DIR.glob("*.zip*"):
        return True
    return False

def install_voice(voice_name: str) -> bool:
    
    print(f"  [{voice_name}]", end=" ")
    
    if check_voice_installed(voice_name):
        print("DEJA INSTALLEE")
        return True
    
    archives = find_zip_archives(voice_name)
    
    if not archives:
        print("ERREUR: Aucune archive ZIP trouvee")
        return False
    
    if len(archives) > 1:
        print(f"Reconstruction ({len(archives)} chunks)...", end=" ")
        combined_file = PIPER_VOICES_DIR / f"{voice_name}_combined.zip"
        
        with open(combined_file, 'wb') as outfile:
            for chunk_file in sorted(archives):
                with open(chunk_file, 'rb') as infile:
                    outfile.write(infile.read())
        
        archive_to_extract = combined_file
    else:
        print(f"Extraction...", end=" ")
        archive_to_extract = archives[0]
    
    try:
        with zipfile.ZipFile(archive_to_extract, 'r') as zf:
            zf.extractall(PIPER_VOICES_DIR)
        
        if len(archives) > 1:
            combined_file.unlink()
        
        print("OK")
        return True
        
    except Exception as e:
        print(f"ERREUR: {e}")
        return False

def cleanup_archives():
    
    print()
    print("Suppression des archives ZIP...")
    
    deleted = 0
    for f in PIPER_VOICES_DIR.glob("*.zip*"):
        try:
            f.unlink()
            deleted += 1
            print(f"  Supprime: {f.name}")
        except Exception as e:
            print(f"  Erreur suppression {f.name}: {e}")
    
    return deleted

def main():
    print("=" * 70)
    print("     GENERIC VOICE - Installation des voix Piper Core")
    print("=" * 70)
    print()
    
    if not PIPER_VOICES_DIR.exists():
        print(f"ERREUR: Repertoire introuvable: {PIPER_VOICES_DIR}")
        sys.exit(1)
    
    print(f"Voix a installer: {len(CORE_VOICES)}")
    print(f"  - FR: fr_FR-siwis-medium")
    print(f"  - EN: en_US-amy-medium")
    print(f"  - ES: es_ES-sharvard-medium")
    print(f"  - IT: it_IT-paola-medium")
    print(f"  - DE: de_DE-mls-medium")
    print()
    
    installed = 0
    for voice_name in CORE_VOICES:
        if install_voice(voice_name):
            installed += 1
    
    print()
    print("=" * 70)
    print(f"INSTALLATION: {installed}/{len(CORE_VOICES)} voix installees")
    print("=" * 70)
    
    if installed == len(CORE_VOICES):
        cleanup_archives()
        print()
        print("Installation terminee avec succes!")
        print()
        print("Vous pouvez maintenant utiliser Generic Voice:")
        print("  python3 gv.py --tts piper --text \"Bonjour\"")
        sys.exit(0)
    else:
        print()
        print("ERREUR: Installation incomplete")
        sys.exit(1)

if __name__ == "__main__":
    main()
