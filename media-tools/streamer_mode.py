#!/usr/bin/env python3

import subprocess

def get_desktop_icons_status():
    """Get the current status of desktop icons visibility."""
    result = subprocess.run(
        ['dconf', 'read', '/org/nemo/desktop/show-desktop-icons'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

def toggle_desktop_icons():
    """Toggle the desktop icons visibility."""
    current_status = get_desktop_icons_status()
    if current_status == 'true':
        subprocess.run(['dconf', 'write', '/org/nemo/desktop/show-desktop-icons', 'false'])
        print("Desktop icons are now hidden.")
    else:
        subprocess.run(['dconf', 'write', '/org/nemo/desktop/show-desktop-icons', 'true'])
        print("Desktop icons are now visible.")

if __name__ == "__main__":
    toggle_desktop_icons()

