
import os
import re
import csv
import shutil
import zipfile
import subprocess
import glob
import fnmatch


def create_version_folder():
    workspace = ".mcoder-workspace"
    versions = os.path.join(workspace, "versions")
    os.makedirs(versions, exist_ok=True)
    version_folders = [d for d in os.listdir(versions) if os.path.isdir(os.path.join(versions, d))]
    version_numbers = [int(re.search(r'\d+', d).group()) for d in version_folders]
    new_version_number = max(version_numbers, default=-1) + 1
    new_version_folder = os.path.join(versions, f"version{new_version_number}")
    os.makedirs(new_version_folder, exist_ok=True)
    return new_version_folder

def save_response(response_folder, index, response):
    response_file = os.path.join(response_folder, f"response{index}.txt")
    with open(response_file, 'w') as f:
        f.write(response)

def get_latest_version_folder():
    workspace = ".mcoder-workspace"
    versions = os.path.join(workspace, "versions")
    version_folders = [d for d in os.listdir(versions) if os.path.isdir(os.path.join(versions, d))]
    version_numbers = [int(re.search(r'\d+', d).group()) for d in version_folders]
    latest_version_number = max(version_numbers)
    latest_version_folder = os.path.join(versions, f"version{latest_version_number}")
    return latest_version_folder

def read_response_file(response_file):
    with open(response_file, 'r') as f:
        return f.read()

def get_version_folder(n):
    workspace = ".mcoder-workspace"
    versions = os.path.join(workspace, "versions")
    if n is None:
        return get_latest_version_folder()
    else:
        return os.path.join(versions, f"version{n}")

def log_cost(cost_data):
    workspace = ".mcoder-workspace"
    os.makedirs(workspace, exist_ok=True)
    cost_file = os.path.join(workspace, "costs.csv")
    file_exists = os.path.isfile(cost_file)

    with open(cost_file, 'a', newline='') as csvfile:
        cost_writer = csv.writer(csvfile)
        if not file_exists:
            cost_writer.writerow(["model", "input_cost", "output_cost", "total_cost"])
        cost_writer.writerow([cost_data['model'], cost_data['input_cost'], cost_data['output_cost'], cost_data['total_cost']])

def clear_workspace(confirm):
    workspace = ".mcoder-workspace"
    if not confirm:
        user_input = input("THIS WILL DELETE ALL MCODER WORKSPACE FILES. PROCEED? Y/n: ")
        if user_input.lower() != 'y':
            print("Operation cancelled.")
            return
    shutil.rmtree(workspace)
    print(f"{workspace} has been cleared.")

def create_backup(backup_name):
    workspace = ".mcoder-workspace"
    backup_folder = os.path.join(workspace, "manual-backups")
    os.makedirs(backup_folder, exist_ok=True)
    backup_path = os.path.join(backup_folder, f"{backup_name}.zip")

    with zipfile.ZipFile(backup_path, 'w') as backup_zip:
        for root, _, files in os.walk('.'):
            if '.mcoder-workspace' in root:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                backup_zip.write(file_path, os.path.relpath(file_path, '.'))

    print(f"Backup created at {backup_path}")

def backup_current_state():
    workspace = ".mcoder-workspace"
    backup_folder = os.path.join(workspace, "last-write-backup")
    if os.path.exists(backup_folder):
        shutil.rmtree(backup_folder)
    os.makedirs(backup_folder, exist_ok=True)

    for root, _, files in os.walk('.'):
        if '.mcoder-workspace' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            backup_path = os.path.join(backup_folder, os.path.relpath(file_path, '.'))
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy(file_path, backup_path)

    print(f"Current state backed up to {backup_folder}")

def undo_last_write():
    workspace = ".mcoder-workspace"
    backup_folder = os.path.join(workspace, "last-write-backup")

    if not os.path.exists(backup_folder):
        print("No backup found to undo.")
        return

    for root, _, files in os.walk(backup_folder):
        for file in files:
            backup_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(backup_file_path, backup_folder)
            original_file_path = os.path.join(os.getcwd(), relative_path)
            os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
            shutil.copy(backup_file_path, original_file_path)

    for root, _, files in os.walk('.'):
        if '.mcoder-workspace' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, '.')
            backup_file_path = os.path.join(backup_folder, relative_path)
            if not os.path.exists(backup_file_path):
                os.remove(file_path)

    print(f"Undo completed. Files restored from {backup_folder}")

def get_user_instructions_from_nvim():
    workspace = ".mcoder-workspace"
    os.makedirs(workspace, exist_ok=True)
    temp_file = os.path.join(workspace, "temp_instructions.txt")
    subprocess.run(["nvim", temp_file])
    with open(temp_file, 'r') as f:
        user_instructions = f.read()
    os.remove(temp_file)
    return user_instructions

def read_mcignore():
    workspace = ".mcoder-workspace"
    mcignore_path = os.path.join(workspace, ".mcignore")
    if not os.path.exists(mcignore_path):
        # Create default .mcignore with __pycache__
        with open(mcignore_path, 'w') as f:
            f.write("__pycache__\n")
    with open(mcignore_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def ignore(pattern):
    workspace = ".mcoder-workspace"
    mcignore_path = os.path.join(workspace, ".mcignore")
    os.makedirs(workspace, exist_ok=True)
    
    # Create .mcignore file if it doesn't exist
    if not os.path.exists(mcignore_path):
        with open(mcignore_path, 'w') as f:
            f.write("__pycache__\n")
    
    with open(mcignore_path, 'r') as f:
        patterns = f.read().splitlines()
    
    if pattern not in patterns:
        with open(mcignore_path, 'a') as f:
            f.write(f"\n{pattern}")
        print(f"Added '{pattern}' to .mcignore")
    else:
        print(f"'{pattern}' is already in .mcignore")


def unignore(pattern):
    workspace = ".mcoder-workspace"
    mcignore_path = os.path.join(workspace, ".mcignore")
    if not os.path.exists(mcignore_path):
        print("No .mcignore file found.")
        return
    with open(mcignore_path, 'r') as f:
        lines = f.readlines()
    with open(mcignore_path, 'w') as f:
        removed = False
        for line in lines:
            if line.strip() != pattern:
                f.write(line)
            else:
                removed = True
    if removed:
        print(f"Removed '{pattern}' from .mcignore")
    else:
        print(f"Pattern '{pattern}' not found in .mcignore")

def lsignores():
    workspace = ".mcoder-workspace"
    mcignore_path = os.path.join(workspace, ".mcignore")
    if not os.path.exists(mcignore_path):
        print("No .mcignore file found.")
        return
    with open(mcignore_path, 'r') as f:
        ignores = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    if ignores:
        print("Current ignore patterns:")
        for ignore in ignores:
            print(f"- {ignore}")
    else:
        print("No ignore patterns found.")

def should_ignore(file_path, ignore_patterns):
    normalized_path = os.path.normpath(file_path)
    for pattern in ignore_patterns:
        # Check for exact match
        if fnmatch.fnmatch(normalized_path, pattern):
            return True
        
        # Check for directory match (e.g., "dir" should match "dir/*")
        if os.path.isdir(normalized_path) and fnmatch.fnmatch(normalized_path + '/*', pattern):
            return True
        
        # Check for file in directory match (e.g., "dir" should match "./dir/file.txt")
        if fnmatch.fnmatch(os.path.dirname(normalized_path), pattern):
            return True
        
        # Check for pattern without leading "./" (e.g., "dir/file.txt" should match "./dir/file.txt")
        if normalized_path.startswith('./') and fnmatch.fnmatch(normalized_path[2:], pattern):
            return True
        
        # Check for subdirectory match (e.g., "wandb" should match "path/to/wandb/file.txt")
        path_parts = normalized_path.split(os.sep)
        if any(part == pattern for part in path_parts):
            return True
    
    return False

def gather_files(pattern, recursive):
    all_files = []
    ignore_patterns = read_mcignore()
    for root, dirs, files in os.walk('.'):
        if '.mcoder-workspace' in root or should_ignore(root, ignore_patterns):
            dirs[:] = []  # Skip this directory
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_patterns):
                all_files.append(file_path)
    if recursive:
        matching_files = [f for f in all_files if glob.fnmatch.fnmatch(f, pattern)]
    else:
        matching_files = [f for f in all_files if glob.fnmatch.fnmatch(os.path.basename(f), pattern)]
    return matching_files
