
import os
import argparse
import pyperclip

def get_file_list(directory, recursive=False):
    file_list = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
    else:
        for item in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, item)):
                file_list.append(item)
    return file_list

def main():
    parser = argparse.ArgumentParser(description="List files in the current directory and copy to clipboard.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Include subdirectories recursively")
    args = parser.parse_args()

    current_dir = os.getcwd()
    file_list = get_file_list(current_dir, args.recursive)
    
    # Format the list as a string representation
    formatted_list = str(file_list)
    
    # Copy to clipboard
    pyperclip.copy(formatted_list)
    
    print(f"File list copied to clipboard: {formatted_list}")

if __name__ == "__main__":
    main()
