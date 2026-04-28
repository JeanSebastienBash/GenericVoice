"""
Module: system/adapt.py
Purpose: Installs missing system dependencies based on detected OS. Auto-fix command implementation.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: py/gv.py, lib/system/detect.py
"""


import importlib.util
import os
import subprocess
import sys
from typing import List, Optional, Dict, Any

from .detect import (
    get_effective_os,
    OSType,
    is_linux,
    is_windows,
    is_macos,
    is_ubuntu,
    requires_apt,
)

import sys
import os
_errors_path = os.path.join(os.path.dirname(__file__), "..")
if _errors_path not in sys.path:
    sys.path.insert(0, _errors_path)
from errors import print_warning, print_info

class DependencyError(Exception):
    
    pass

REQUIRED_PACKAGES: Dict[str, Dict[str, List[str]]] = {
    OSType.UBUNTU: {
        "core": ["python3", "python3-pip"],
        "ihm": ["whiptail"],
        "optional": [],  # gum installed via npm or apt
    },
    OSType.LINUX: {
        "core": ["python3", "python3-pip"],
        "ihm": ["whiptail"],
        "optional": [],  # gum installed via npm or package manager
    },
    OSType.MACOS: {
        "core": ["python3"],
        "ihm": [],  # whiptail not available on macOS
        "optional": [],  # gum via brew
    },
    OSType.WINDOWS: {
        "core": ["python3"],
        "ihm": [],  # whiptail/gum need WSL
        "optional": [],
    },
}

PIP_PACKAGES: Dict[str, List[str]] = {
    "core": ["inquirer", "numpy", "scipy"],
    "optional": [],
}

GUM_INSTALL_COMMANDS: Dict[str, List[List[str]]] = {
    OSType.UBUNTU: [
        ["sudo", "apt-get", "update"],
        ["sudo", "apt-get", "install", "-y", "gum"],  # may not be available
    ],
    OSType.LINUX: [
    ],
    OSType.MACOS: [
        ["brew", "install", "gum"],
    ],
}

def check_command_exists(command: str) -> bool:
    
    try:
        subprocess.run(
            ["which", command],
            capture_output=True,
            check=False,
        )
        return True
    except FileNotFoundError:
        return False

def check_python_module(module_name: str) -> bool:
    
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def get_missing_core_dependencies(system_os: Optional[str] = None) -> List[str]:
    
    os_type = get_effective_os(system_os)
    missing = []
    
    for pkg in REQUIRED_PACKAGES.get(os_type, {}).get("core", []):
        if not check_command_exists(pkg):
            missing.append(pkg)
    
    return missing

def get_missing_ihm_dependencies(system_os: Optional[str] = None) -> List[str]:
    
    os_type = get_effective_os(system_os)
    missing = []
    
    for pkg in REQUIRED_PACKAGES.get(os_type, {}).get("ihm", []):
        if not check_command_exists(pkg):
            missing.append(pkg)
    
    return missing

def get_missing_python_dependencies() -> List[str]:
    
    missing = []
    
    for module in PIP_PACKAGES.get("core", []):
        if not check_python_module(module):
            missing.append(module)
    
    return missing

def check_python_deps() -> List[str]:
    
    missing = []
    for pkg in PIP_PACKAGES.get("core", []):
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    return missing

def install_apt_packages(packages: List[str], sudo: bool = True) -> bool:
    
    if not packages:
        return True
    
    cmd = ["apt-get", "install", "-y"]
    if sudo:
        cmd = ["sudo"] + cmd
    
    try:
        subprocess.run(cmd + list(packages), check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_pip_packages(packages: List[str], user: bool = True, verbose: bool = True) -> bool:
    
    if not packages:
        return True
    
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    cmd = [sys.executable, "-m", "pip", "install"]
    if user and not in_venv:
        cmd.append("--user")
    
    for package in packages:
        if verbose:
            print(f"Installing {package}...", end=" ", flush=True)
        
        try:
            subprocess.run(cmd + [package], check=True, capture_output=True)
            if verbose:
                print("OK")
        except subprocess.CalledProcessError as e:
            if verbose:
                print(f"FAILED")
            return False
    
    return True

def auto_install_dependencies(system_os: Optional[str] = None) -> bool:
    
    os_type = get_effective_os(system_os)
    success = True
    
    if os_type == OSType.UBUNTU or (os_type == OSType.LINUX and check_command_exists("apt-get")):
        missing_apt = get_missing_core_dependencies(os_type) + get_missing_ihm_dependencies(os_type)
        if missing_apt:
            success = success and install_apt_packages(missing_apt)
    
    missing_pip = get_missing_python_dependencies()
    if missing_pip:
        success = success and install_pip_packages(missing_pip)
    
    if os_type in (OSType.UBUNTU, OSType.LINUX, OSType.MACOS):
        if not check_command_exists("gum"):
            success = success and install_gum(os_type)
    
    return success

def install_gum(os_type: str) -> bool:
    
    import os
    
    if os_type == OSType.UBUNTU or (os_type == OSType.LINUX and check_command_exists("apt-get")):
        try:
            can_sudo = os.geteuid() == 0 or \
                       subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode == 0
            
            if not can_sudo:
                print_warning(
                    "Installation gum necessite sudo",
                    "L'installation de gum necessite un mot de passe sudo.",
                    details=[
                        "Pour installer manuellement, executez:",
                        "  sudo apt-get update && sudo apt-get install gum",
                        "",
                        "Ou ajoutez le depot Charm:",
                        "  curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg",
                        "  echo 'deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *' | sudo tee /etc/apt/sources.list.d/charm.list",
                        "  sudo apt-get update && sudo apt-get install gum",
                    ],
                    hint="Executez cette commande manuellement avec sudo"
                )
                return False
            
            subprocess.run(["sudo", "mkdir", "-p", "/etc/apt/keyrings"], check=True)
            subprocess.run(
                ["curl", "-fsSL", "https://repo.charm.sh/apt/gpg.key"],
                stdout=subprocess.PIPE,
                check=True,
            )
            subprocess.run(
                ["sudo", "gpg", "--dearmor", "-o", "/etc/apt/keyrings/charm.gpg"],
                stdin=subprocess.PIPE,
                check=True,
            )
            subprocess.run(
                ["sudo", "sh", "-c", 
                 "echo 'deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *' "
                 "| sudo tee /etc/apt/sources.list.d/charm.list"],
                check=True,
            )
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "gum"], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    if os_type == OSType.MACOS:
        try:
            subprocess.run(
                ["brew", "install", "gum"],
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            pass
    
    if check_command_exists("go"):
        try:
            go_path = subprocess.run(["go", "env", "GOPATH"], capture_output=True, text=True).stdout.strip()
            if go_path:
                gum_bin = os.path.join(go_path, "bin", "gum")
                subprocess.run(
                    ["go", "install", "github.com/charmbracelet/gum@latest"],
                    capture_output=True,
                    check=True,
                )
                if os.path.exists(gum_bin) or check_command_exists("gum"):
                    return True
        except subprocess.CalledProcessError:
            pass
    
    return False

def ensure_dependencies(system_os: Optional[str] = None, auto_fix: bool = False) -> bool:
    
    os_type = get_effective_os(system_os)
    
    missing_core = get_missing_core_dependencies(os_type)
    missing_ihm = get_missing_ihm_dependencies(os_type)
    missing_python = get_missing_python_dependencies()
    
    missing_all = missing_core + missing_ihm + missing_python
    
    if not missing_all:
        return True
    
    if auto_fix:
        return auto_install_dependencies(system_os)
    
    raise DependencyError(
        f"Missing dependencies: {', '.join(missing_all)}. "
        f"Run with --auto-fix to install automatically."
    )

def get_ihm_backend() -> str:
    
    if check_python_module("inquirer"):
        return "inquirer"
    
    if check_command_exists("whiptail"):
        return "whiptail"
    
    if check_command_exists("gum"):
        return "gum"
    
    return "none"

def format_missing_report(system_os: Optional[str] = None) -> str:
    
    os_type = get_effective_os(system_os)
    
    missing_core = get_missing_core_dependencies(os_type)
    missing_ihm = get_missing_ihm_dependencies(os_type)
    missing_python = get_missing_python_dependencies()
    
    lines = ["Missing dependencies:"]
    
    if missing_core:
        lines.append(f"  Core: {', '.join(missing_core)}")
    if missing_ihm:
        lines.append(f"  IHM: {', '.join(missing_ihm)}")
    if missing_python:
        lines.append(f"  Python: {', '.join(missing_python)}")
    
    if os_type == OSType.UBUNTU:
        lines.append("  Run with --auto-fix to install automatically.")
    elif os_type == OSType.LINUX:
        lines.append("  Install manually using your package manager.")
    else:
        lines.append("  Please install manually.")
    
    return "\n".join(lines)
