import os
import sys
import pyperclip
import re

def create_files_from_clipboard(folder_name=None):
    # Get clipboard contents
    clipboard_content = pyperclip.paste()
    
    # Regular expression to match code blocks with headers
    code_block_pattern = re.compile(r'```(.*?)\n(.*?)```', re.DOTALL)
    
    # Find all code blocks with headers
    code_blocks = code_block_pattern.findall(clipboard_content)
    
    # Determine the base directory
    base_dir = os.getcwd() if folder_name is None else os.path.join(os.getcwd(), folder_name)
    
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Create files from code blocks
    for header, code in code_blocks:
        # Skip code blocks with empty headers
        if not header.strip():
            continue
        
        # Clean up the header to use it as a file path
        file_path = os.path.join(base_dir, header.strip())
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the code to the file
        with open(file_path, 'w') as file:
            file.write(code.strip())
        
        print(f"Created file: {file_path}")

if __name__ == "__main__":
    # Get the folder name from command line arguments
    folder_name = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Create files from clipboard contents
    create_files_from_clipboard(folder_name)
