#!/usr/bin/env python3
"""
Module: ihm/generic.py
Purpose: Factory module re-exporting GenericMenuIHM as GenericIHM. Maintains backward compatibility.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/ihm/genericmenu.py, py/gv.py
"""

from ihm.genericmenu import GenericMenuIHM

GenericIHM = GenericMenuIHM

__all__ = ['GenericIHM', 'GenericMenuIHM']
