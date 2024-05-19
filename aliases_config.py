import os

current_dir = os.path.dirname(os.path.abspath(__file__))

aliases = {
    "ask": f"python3 {current_dir}/ask-app/ask.py",
    "runit": f"bash {current_dir}/ask-app/runit.sh",
    # Add more aliases as needed
    # "alias_name": "command",
}
