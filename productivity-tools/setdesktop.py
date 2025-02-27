
#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
import sys

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Set custom desktop directory')
    parser.add_argument('n', nargs='?', type=int, default=0,
                       help='Desktop number (0 for default)')
    args = parser.parse_args()

    # Define paths
    config_path = Path.home() / '.config' / 'user-dirs.dirs'
    
    # Determine new desktop path
    if args.n == 0:
        new_desktop = Path.home() / 'Desktop'
        new_desktop_str = '"$HOME/Desktop"'
    else:
        new_desktop = Path.home() / f'Desktop{args.n}'
        new_desktop_str = f'"$HOME/Desktop{args.n}"'

    # Create the directory if it doesn't exist
    new_desktop.mkdir(parents=True, exist_ok=True)

    try:
        # Read current config
        with open(config_path, 'r') as f:
            content = f.read()

        # Replace the desktop directory line
        pattern = r'(XDG_DESKTOP_DIR=).*'
        new_content = re.sub(pattern, fr'\1{new_desktop_str}', content)

        # Write back to file
        with open(config_path, 'w') as f:
            f.write(new_content)

        print(f"Desktop directory set to: {new_desktop_str}")

    except FileNotFoundError:
        print(f"Error: Could not find config file at {config_path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when accessing {config_path}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
