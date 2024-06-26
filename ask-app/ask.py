import os
import sys
from dotenv import load_dotenv
import subprocess

def main():
    # Load environment variables
    load_dotenv()

    # Check LAB_TO_USE
    lab_to_use = os.getenv('LAB_TO_USE')

    if not lab_to_use:
        print("Error: LAB_TO_USE is not set in the .env file.")
        sys.exit(1)

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get command line arguments (excluding the script name)
    args = sys.argv[1:]

    if lab_to_use.lower() == 'openai':
        script_path = os.path.join(current_dir, 'ask_gpt.py')
    elif lab_to_use.lower() == 'anthropic':
        script_path = os.path.join(current_dir, 'ask_claude.py')
    else:
        print(f"Error: Unknown LAB_TO_USE value: {lab_to_use}")
        sys.exit(1)

    # Run the appropriate script
    try:
        result = subprocess.run([sys.executable, script_path] + args, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
