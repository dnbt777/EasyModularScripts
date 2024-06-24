import os
import re
import csv
import shutil
import zipfile
import subprocess

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

    # Restore files from backup
    for root, _, files in os.walk(backup_folder):
        for file in files:
            backup_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(backup_file_path, backup_folder)
            original_file_path = os.path.join(os.getcwd(), relative_path)
            os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
            shutil.copy(backup_file_path, original_file_path)

    # Remove files that were created after the backup
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