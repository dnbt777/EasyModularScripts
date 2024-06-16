#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <repository-name>"
  exit 1
fi

# Get the current logged-in Git user's username
GIT_USER=$(git config user.name)

# Check if the username is retrieved
if [ -z "$GIT_USER" ]; then
  echo "Error: Could not retrieve Git username. Make sure you have configured Git."
  exit 1
fi

# Print the Git username
echo "Logged in Git user: $GIT_USER"

# Construct the Git clone URL
REPO_NAME=$1
CLONE_URL="git@github.com:${GIT_USER}/${REPO_NAME}.git"

# Clone the repository
echo "Cloning repository from $CLONE_URL"
git clone "$CLONE_URL"
