#!/usr/bin/env python3
"""
Module: ihm/__init__.py
Purpose: Exports GenericIHM and GenericMenuIHM from ihm.generic module.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: lib/ihm/generic.py, lib/ihm/genericmenu.py
"""

from ihm.genericmenu import GenericMenuIHM

GenericIHM = GenericMenuIHM

__all__ = ['GenericIHM', 'GenericMenuIHM']
