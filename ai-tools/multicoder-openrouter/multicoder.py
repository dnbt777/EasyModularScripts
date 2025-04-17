import sys
import os
import shutil
from get import handle_get
from write import handle_write, list_responses
from rollback import handle_rollback
from utils import clear_workspace, create_backup, undo_last_write, backup_current_state, ignore, unignore, lsignores
from dotenv import load_dotenv
from aiqs.model_list import openrouter_models

load_dotenv()
try:
    MODEL = os.environ.get('MODEL')
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS'))
    STREAM = bool(int(os.environ.get('stream')))
except:
    print("Please set MODEL and MAX_TOKENS in .env")
    print("See .env-example for an example env.")
    print("Available models:")
    for model_string in openrouter_models:
        print(model_string)

def main():
    if len(sys.argv) < 2:
        print("Usage: mcoder <command> [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "get":
        if len(sys.argv) < 4:
            print("Usage: mcoder get [llm count] [pattern] [-r] [user instructions]")
            sys.exit(1)
        llm_count = int(sys.argv[2])
        pattern = sys.argv[3]
        recursive = False
        user_instructions = None

        if '-r' in sys.argv:
            recursive = True
            user_instructions_index = sys.argv.index('-r') + 1
            if user_instructions_index < len(sys.argv):
                user_instructions = ' '.join(sys.argv[user_instructions_index:])
        else:
            if len(sys.argv) > 4:
                user_instructions = ' '.join(sys.argv[4:])
        handle_get(llm_count, pattern, recursive, model=MODEL, max_tokens=MAX_TOKENS, user_instructions=user_instructions, stream=STREAM)
    elif command == "write":
        if len(sys.argv) < 3:
            print("Usage: mcoder write [m]")
            sys.exit(1)
        if sys.argv[2] == "list":
            list_responses()
        else:
            m = int(sys.argv[2])
            backup_current_state()
            handle_write(m)
    elif command == "rollback":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else None
        handle_rollback(n)
    elif command == "clear":
        confirm = '-y' in sys.argv
        clear_workspace(confirm)
    elif command == "backup":
        if len(sys.argv) < 3:
            print("Usage: mcoder backup [backup name]")
            sys.exit(1)
        backup_name = sys.argv[2]
        create_backup(backup_name)
    elif command == "undo":
        undo_last_write()
    elif command == "ignore":
        if len(sys.argv) < 3:
            print("Usage: mcoder ignore [pattern]")
            sys.exit(1)
        pattern = sys.argv[2]
        ignore(pattern)
    elif command == "rmignore":
        if len(sys.argv) < 3:
            print("Usage: mcoder rmignore [pattern]")
            sys.exit(1)
        pattern = sys.argv[2]
        unignore(pattern)
    elif command in ["lsignores", "lsignore"]:
        lsignores()
    elif command == "setmodel":
        if len(sys.argv) < 3:
            print("Usage: mcoder setmodel [model name]")
            sys.exit(1)
        model_name = sys.argv[2]
        set_model(model_name)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

def set_model(model_name):
    # Update the .env file
    env_file_path = '.env'
    with open(env_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(env_file_path, 'w') as file:
        for line in lines:
            if line.startswith("MODEL="):
                file.write(f"MODEL=\"{model_name}\"\n")
            else:
                file.write(line)
    
    print(f"Model set to '{model_name}' successfully.")



if __name__ == "__main__":
    main()
