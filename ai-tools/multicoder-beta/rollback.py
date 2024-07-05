import os
import shutil
from utils import get_version_folder

def handle_rollback(n=None):
    version_folder = get_version_folder(n)
    backup_folder = os.path.join(version_folder, "backup")

    for root, _, files in os.walk(backup_folder):
        for file in files:
            backup_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(backup_file_path, backup_folder)
            original_file_path = os.path.join(os.getcwd(), relative_path)
            shutil.copy(backup_file_path, original_file_path)

    print(f"Rolled back to version {n if n is not None else 'latest'}")