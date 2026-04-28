"""
Module: ihm/genericmenu.py
Purpose: Implements interactive CLI menu system with tabs (TTS, Audio, Effects, Playback, Advanced). Mirrors gvflet.py GUI structure.
Context: Core library module in lib/. Imported by scripts and other lib modules.
Impact: Changes affect TTS engine behavior, menu interactions, or OS compatibility.
Related: py/gv.py
"""


import sys
import os
from typing import List, Tuple, Optional

def clear_screen():
    
    print("\n" + "=" * 60 + "\n")

def loading(message: str = "Loading"):
    
    print(f"{message}...")

class GenericMenuIHM:
    
    name = "genericmenu"
    version = "2.0"
    description = "Enhanced GenericMenu with detailed descriptions"
    priority = 10
    
    def is_available(self) -> bool:
        return True
    
    def is_interactive(self) -> bool:
        return True
    
    def _print_header(self, title: str, subtitle: str = ""):
        
        clear_screen()
        width = 70
        print()
        print("=" * width)
        print(f"  {title}")
        if subtitle:
            print(f"  {subtitle}")
        print("=" * width)
        print()
    
    def _print_menu_item(self, num: int, tag: str, desc: str, help_text: str = ""):
        
        print(f"  [{num}]  {desc}")
        
        if help_text:
            print(f"       -> {help_text}")
    
    def _print_box(self, title: str, content: str, width: int = 60):
        
        print()
        print("+" + "-" * (width - 2) + "+")
        print(f"| {title} |")
        print("+" + "-" * (width - 2) + "+")
        
        lines = content.split('\n')
        for line in lines:
            print(f"| {line}")
        
        print("+" + "-" * (width - 2) + "+")
        print()
    
    def _yes_no(self, prompt: str) -> bool:
        
        while True:
            try:
                ans = input(f"  {prompt} [Y/n]: ").strip().lower()
                if not ans or ans == 'y':
                    return True
                elif ans == 'n':
                    return False
            except (EOFError, KeyboardInterrupt):
                return False
    
    def menu(
        self,
        title: str,
        text: str,
        height: int,
        width: int,
        choice_height: int,
        items: List[Tuple[str, str]],
    ) -> Optional[str]:
        
        cmd_line = ""
        if "Command:" in text:
            for line in text.split("\n"):
                if "Command:" in line:
                    cmd_line = line.strip().replace("Command: ", "")
                    break
        
        self._print_header(title, f"Command: {cmd_line}" if cmd_line else "")
        
        menu_help = {}
        
        for i, (tag, desc) in enumerate(items, 1):
            help_text = menu_help.get(tag, "")
            self._print_menu_item(i, tag, desc, help_text)
        
        print()
        print("  " + "-" * 50)
        print("  Tip: Enter number (1-17) or letter to select")
        print()
        
        while True:
            try:
                choice = input("  > ").strip()
                if not choice:
                    continue
                
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(items):
                        return items[idx][0]
                except ValueError:
                    pass
                
                choice_upper = choice.upper()
                for tag, desc in items:
                    if choice_upper == tag.upper():
                        return tag
                
                print("  *** Invalid choice!")
                print("  Try a number (1-{}) or letter".format(len(items)))
                
            except EOFError:
                return None
            except KeyboardInterrupt:
                return None
    
    def msgbox(self, title: str, text: str, height: int, width: int) -> bool:
        
        self._print_box(title, text)
        try:
            input("  Press Enter to continue...")
        except (KeyboardInterrupt, EOFError):
            pass
        return True
    
    def inputbox(
        self,
        title: str,
        text: str,
        height: int,
        width: int,
        default: str = "",
    ) -> Optional[str]:
        
        self._print_box(title, text)
        
        default_str = f"[{default}]" if default else ""
        
        try:
            ans = input(f"  > {default_str} ").strip()
            return ans if ans else default
        except (EOFError, KeyboardInterrupt):
            return None
    
    def radiolist(
        self,
        title: str,
        text: str,
        height: int,
        width: int,
        choice_height: int,
        items: List[Tuple[str, str, bool]],
    ) -> Optional[str]:
        
        self._print_header(title)
        print(f"  {text}\n")
        
        for i, (tag, desc, selected) in enumerate(items, 1):
            marker = "[*]" if selected else "[ ]"
            print(f"  [{i}]  {marker} {desc}")
        
        print()
        
        while True:
            try:
                choice = input("  > ").strip()
                if not choice:
                    return None
                
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(items):
                        return items[idx][0]
                except ValueError:
                    pass
                
                for tag, desc, _ in items:
                    if choice.upper() == tag.upper():
                        return tag
                        
            except (EOFError, KeyboardInterrupt):
                return None
    
    def yesno(self, title: str, text: str, height: int, width: int) -> bool:
        
        self._print_box(title, text)
        return self._yes_no("Confirm?")
    
    def scrolltext(
        self,
        title: str,
        text: str,
        height: int,
        width: int,
        items: Optional[List[str]] = None,
    ) -> bool:
        
        content = "\n".join(items) if items else text
        self._print_box(title, content)
        try:
            input("  Press Enter to continue...")
        except (KeyboardInterrupt, EOFError):
            pass
        return True
