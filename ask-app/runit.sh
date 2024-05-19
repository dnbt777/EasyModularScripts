#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read the command from last_output.log in the script's directory
COMMAND=$(cat "$SCRIPT_DIR/last_output.log")

# Execute the command in the current working directory
eval "$COMMAND"
