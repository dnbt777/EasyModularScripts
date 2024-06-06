#!/bin/bash

# Array of file names
file_names=("$@")

# Initialize the string s
s=""

# Loop through each file name
for file_name in "${file_names[@]}"; do
    if [[ -f "$file_name" ]]; then
        # Read the file contents
        file_contents=$(cat "$file_name")
        
        # Append the formatted string to s
        s+="\`\`\`${file_name}\n${file_contents}\`\`\`\n"
    else
        echo "File not found: $file_name"
    fi
done

# Copy the string s to the clipboard
if command -v xclip &> /dev/null; then
    echo -e "$s" | xclip -selection clipboard
elif command -v pbcopy &> /dev/null; then
    echo -e "$s" | pbcopy
else
    echo "No clipboard utility found. Please install xclip or pbcopy."
fi
