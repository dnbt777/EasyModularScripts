import os

current_dir = os.path.dirname(os.path.abspath(__file__))

aliases = {
    # ask-app
    "ask": f"python3 {current_dir}/ask-app/ask.py",
    "runit": f"bash {current_dir}/ask-app/runit.sh",

    # media-tools
    "mts-zipvids": f"python3 {current_dir}/media-tools/zipvids.py",
    "zipvids": f"mts-zipvids",

    # ai tools
    "gmfp": f"bash {current_dir}/ai-tools/get_multifile_prompt.sh",

    # Add more aliases as needed
    # "alias_name": "command",
}
