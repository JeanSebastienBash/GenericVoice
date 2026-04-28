"""
Module: system/detect.py
Purpose: Detects platform (Linux, macOS, Windows) and distribution (Ubuntu, Debian, Fedora). Provides OS-specific information.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/player.py, lib/system/adapt.py
"""


import platform
import sys
from typing import Optional

class OSDetectionError(Exception):
    
    pass

class OSType:
    UBUNTU = "ubuntu"    # Debian/Ubuntu - apt available
    LINUX = "linux"       # Generic Linux - no apt
    WINDOWS = "windows"   # Windows - not yet implemented
    MACOS = "darwin"      # macOS - for future use

def get_os() -> str:
    
    return platform.system().lower()

def detect_system_os() -> str:
    
    system = platform.system().lower()
    
    if system == "windows":
        return OSType.WINDOWS
    elif system == "darwin":
        return OSType.MACOS
    else:
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content or "debian" in content:
                    return OSType.UBUNTU
        except (FileNotFoundError, PermissionError):
            pass
        return OSType.LINUX

def validate_system_os(system_os: str) -> bool:
    
    valid_values = {OSType.UBUNTU, OSType.LINUX, OSType.WINDOWS, OSType.MACOS}
    return system_os.lower() in valid_values

def get_effective_os(system_os: Optional[str] = None) -> str:
    
    if system_os is None:
        return detect_system_os()
    
    system_os = system_os.lower()
    
    if not validate_system_os(system_os):
        raise OSDetectionError(
            f"Invalid --system-os value: '{system_os}'. "
            f"Valid values: ubuntu, linux, windows"
        )
    
    return system_os

def is_linux() -> bool:
    
    return get_os() == "linux"

def is_windows() -> bool:
    
    return get_os() == "windows"

def is_macos() -> bool:
    
    return get_os() == "darwin"

def is_ubuntu() -> bool:
    
    return detect_system_os() == OSType.UBUNTU

def requires_apt() -> bool:
    
    return detect_system_os() == OSType.UBUNTU
