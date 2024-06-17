#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
  echo "Error: No commit message provided."
  echo "Usage: $0 \"commit message\""
  exit 1
fi

# Assign the first argument to the commit message
commit_message="$1"

# Run the git commit and push commands
git add .
git commit -am "$commit_message" && git push

# Check if the commands were successful
if [ $? -eq 0 ]; then
  echo "Commit and push were successful."
else
  echo "An error occurred during commit or push."
fi

