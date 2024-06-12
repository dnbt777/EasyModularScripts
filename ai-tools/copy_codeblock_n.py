import re
import pyperclip
import argparse

def get_code_block_from_clipboard(n):
    # Get the current clipboard content
    clipboard_content = pyperclip.paste()
    
    # Find all code blocks in the clipboard content
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', clipboard_content, re.DOTALL)
    
    # If no code blocks are found, return an empty string
    if not code_blocks:
        return ""
    
    # Handle the case where n is out of range
    if n >= len(code_blocks) or n < -len(code_blocks):
        return ""
    
    # Select the nth code block
    selected_code_block = code_blocks[n]
    
    return selected_code_block

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Copy the nth code block from the clipboard to the clipboard.')
    parser.add_argument('n', type=int, nargs='?', default=-1, help='The index of the code block to copy (default: -1 for the last code block)')
    args = parser.parse_args()
    
    # Get the nth code block from the clipboard
    code_block = get_code_block_from_clipboard(args.n)
    
    # Copy the selected code block back to the clipboard
    pyperclip.copy(code_block)
    
    print("Copied code block to clipboard:")
    print(code_block)

if __name__ == "__main__":
    main()
