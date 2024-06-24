import os
import glob
import shutil
from aiqs import ModelInterface
from utils import create_version_folder, save_response, log_cost, get_user_instructions_from_nvim
from system_prompt import SYSTEM_PROMPT

def gather_files(pattern, recursive):
    all_files = []
    for root, _, files in os.walk('.'):
        if '.mcoder-workspace' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    if recursive:
        matching_files = [f for f in all_files if glob.fnmatch.fnmatch(f, pattern)]
    else:
        matching_files = [f for f in all_files if glob.fnmatch.fnmatch(os.path.basename(f), pattern)]
    return matching_files

def handle_get(llm_count, pattern, recursive, user_instructions=None):
    if user_instructions is None:
        user_instructions = get_user_instructions_from_nvim()

    version_folder = create_version_folder()
    backup_folder = os.path.join(version_folder, "backup")
    response_folder = os.path.join(version_folder, "responses")
    os.makedirs(backup_folder, exist_ok=True)
    os.makedirs(response_folder, exist_ok=True)

    files = gather_files(pattern, recursive)
    for file in files:
        backup_file_path = os.path.join(backup_folder, os.path.relpath(file, '.'))
        os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
        try:
            shutil.copy(file, backup_file_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")
            continue

    prompt = SYSTEM_PROMPT + "\n" + user_instructions
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
        prompt += f'\n<file path="{file}">{content}</file>'

    modelinterface = ModelInterface()
    for i in range(llm_count):
        response = modelinterface.send_to_ai(prompt, model="sonnet3.5", max_tokens=4095)
        response_text = response[0]  # Extract the actual response text from the tuple
        save_response(response_folder, i, response_text)
        log_cost(modelinterface.cost_tracker.cost_data[-1])  # Log the latest cost data

    print(f"Responses saved in {response_folder}")