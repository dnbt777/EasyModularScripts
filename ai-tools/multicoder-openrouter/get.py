import os
import glob
import shutil
from aiqs.ModelInterface import ModelInterface
from utils import create_version_folder, save_response, log_cost, get_user_instructions_from_nvim, read_mcignore, gather_files
from system_prompt import SYSTEM_PROMPT

def handle_get(llm_count, pattern, recursive, model=None, max_tokens=4095, user_instructions=None, stream=False):
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

    prompt = SYSTEM_PROMPT + "\n"
    prompt += f'<user instructions>\n{user_instructions}\n</user instructions>\n'
    prompt += '<project files>\n'
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            prompt += f'<file path="{file}">{content}</file>\n'
        except UnicodeDecodeError as e:
            print(f"Error reading file {file}: {e}")
            print(f"Suggestion: Run 'mc ignore {file}' to ignore this file in future operations.")
            continue
    prompt += '</project files>'

    modelinterface = ModelInterface()
    for i in range(llm_count):
        response = modelinterface.send_to_ai(prompt, model=model, max_tokens=max_tokens, stream=stream)
        response_text = response[0]  # Extract the actual response text from the tuple
        save_response(response_folder, i, response_text)
        log_cost(modelinterface.cost_tracker.cost_data[-1])  # Log the latest cost data

    print(f"Responses saved in {response_folder}")
