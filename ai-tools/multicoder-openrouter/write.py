import os
import re
from utils import (
    get_latest_version_folder, read_response_file, apply_mcdiff,
    extract_patch_files, apply_patch
)



def handle_write(m):
    version_folder = get_latest_version_folder()
    response_file = os.path.join(version_folder, "responses", f"response{m}.txt")
    response_content = read_response_file(response_file)

    # Handle complete file creation
    file_pattern = re.compile(r'<file path="([^"]+)">(.*?)</file>', re.DOTALL)
    files = file_pattern.findall(response_content)

    for file_path, file_content in files:
        if file_path:  # Ensure file_path is not empty
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(file_content)
            print(f"File created: {file_path}")

    # Handle legacy mcdiff blocks
    mcdiff_pattern = re.compile(r'<mcdiff file="([^"]+)">(.*?)</mcdiff>', re.DOTALL)
    diffs = mcdiff_pattern.findall(response_content)

    for file_path, diff_content in diffs:
        if file_path:
            apply_mcdiff(file_path, diff_content)

    # Handle unified diff patch blocks
    patch_files = extract_patch_files(response_content)
    print(f"Processing {len(patch_files)} patch files")
    for _patch_name, patch_content in patch_files:
        print(patch_content)
        apply_patch(patch_content)

    print(f"Changes applied from {response_file}")


def list_responses():
    version_folder = get_latest_version_folder()
    response_folder = os.path.join(version_folder, "responses")
    response_files = [f for f in os.listdir(response_folder) if f.startswith("response") and f.endswith(".txt")]
    for response_file in response_files:
        print(response_file)
