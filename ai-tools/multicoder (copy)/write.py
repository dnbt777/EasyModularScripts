import os
import re
from utils import get_latest_version_folder, read_response_file

def handle_write(m):
    version_folder = get_latest_version_folder()
    response_file = os.path.join(version_folder, "responses", f"response{m}.txt")
    response_content = read_response_file(response_file)

    file_pattern = re.compile(r'<file path="([^"]+)">(.+?)</file>', re.DOTALL)
    files = file_pattern.findall(response_content)

    for file_path, file_content in files:
        if file_path:  # Ensure file_path is not empty
            dir_path = os.path.dirname(file_path)
            if dir_path:  # Ensure dir_path is not empty
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(file_content)
            print(f"File written: {file_path}")

    print(f"Files written from {response_file}")

def list_responses():
    version_folder = get_latest_version_folder()
    response_folder = os.path.join(version_folder, "responses")
    response_files = [f for f in os.listdir(response_folder) if f.startswith("response") and f.endswith(".txt")]
    for response_file in response_files:
        print(response_file)