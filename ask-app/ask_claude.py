import os
import sys
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
def main():
    ask_app_dir = os.getenv('EasyModularScriptsDir') + "/ask-app/"
    ask_key = os.getenv('ASK_KEY')
    if not ask_key:
        print("Error: The ASK_KEY environment variable is not set.")
        sys.exit(1)
    client = Anthropic(api_key=ask_key)
    if len(sys.argv) < 2:
        print("Usage: python ask.py <prompt>")
        sys.exit(1)
    system_prompt = "Answer in as few characters as possible. No formatting tokens such as ` or ```"
    user_prompt = ' '.join(sys.argv[1:])
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        response_text = response.content[0].text
        print(response_text)
        if ask_app_dir:
            log_file_path = os.path.join(ask_app_dir, 'last_output.log')
            with open(log_file_path, 'w') as log_file:
                log_file.write(response_text)
        else:
            print("Error: The EasyModularScriptsDir environment variable is not set.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
if __name__ == "__main__":
    main()
