import sys
import subprocess
import time
import platform

# Set the time delay to 5 minutes (300 seconds)
TIME_DELAY = 300

HOSTS_FILE = "/etc/hosts"
BLOCKED_IP = "127.0.0.1"

# Multiline string containing site aliases
SITE_ALIASES = """
twitter=twitter.com, www.twitter.com, x.com, www.x.com
facebook=facebook.com, www.facebook.com
x=twitter.com, www.twitter.com, x.com, www.x.com
"""

def read_site_aliases():
    aliases = {}
    for line in SITE_ALIASES.strip().split('\n'):
        if line.strip() and not line.startswith('#'):
            parts = line.strip().split('=')
            if len(parts) == 2:
                key = parts[0].strip()
                values = [v.strip() for v in parts[1].split(',')]
                aliases[key] = values
    return aliases

def is_site_blocked(site):
    with open(HOSTS_FILE, 'r') as f:
        for line in f:
            if line.strip().startswith(BLOCKED_IP) and site in line:
                return True
    return False

def toggle_block_site(site):
    aliases = read_site_aliases()
    sites_to_toggle = aliases.get(site, [site, f"www.{site}"])

    with open(HOSTS_FILE, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if not any(site in line for site in sites_to_toggle):
            new_lines.append(line)

    if not is_site_blocked(sites_to_toggle[0]):
        for site in sites_to_toggle:
            new_lines.append(f"{BLOCKED_IP} {site}\n")

    with open(HOSTS_FILE, 'w') as f:
        f.writelines(new_lines)

    restart_services()

def list_blocked_sites():
    with open(HOSTS_FILE, 'r') as f:
        for line in f:
            if line.strip().startswith(BLOCKED_IP):
                print(line.strip())


def restart_services():
    system = platform.system()
    
    if system == 'Linux':
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-resolved'], check=True)
        except subprocess.CalledProcessError:
            pass

        try:
            subprocess.run(['sudo', 'service', 'NetworkManager', 'restart'], check=True)
        except subprocess.CalledProcessError:
            pass
    elif system == 'Darwin':  # macOS
        try:
            subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], check=True)
        except subprocess.CalledProcessError:
            pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python toggle_site_blocking.py <site|list>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_blocked_sites()
    else:
        aliases = read_site_aliases()
        sites_to_toggle = aliases.get(command, [command, f"www.{command}"])
        
        if is_site_blocked(sites_to_toggle[0]):
            print(f"Unblocking {command} in {TIME_DELAY // 60} minutes...")
            for remaining in range(TIME_DELAY, 0, -1):
                sys.stdout.write(f"\rTime remaining: {remaining} seconds")
                sys.stdout.flush()
                time.sleep(1)
            print("\nTime is up! Unblocking the site now.")
        else:
            print(f"Blocking {command} now.")
        
        toggle_block_site(command)

if __name__ == "__main__":
    main()

