import os
import sys
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def load_conversation_history(ask_app_dir):
    history_file = os.path.join(ask_app_dir, 'conversation_history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def save_conversation_history(ask_app_dir, history):
    history_file = os.path.join(ask_app_dir, 'conversation_history.json')
    with open(history_file, 'w') as f:
        json.dump(history, f)

def main():
    ask_app_dir = os.path.join(os.getenv('EasyModularScriptsDir', ''), "ask-app")

    parser = argparse.ArgumentParser(description="Ask GPT-4 a question.")
    parser.add_argument('prompt', nargs='*', help="The prompt to send to GPT-4")
    parser.add_argument('-c', '--respond', action='store_true', help="Respond to the previous conversation")
    args = parser.parse_args()

    # Read the ASK_KEY environment variable
    ask_key = os.getenv('ASK_KEY')
    if not ask_key:
        print("Error: The ASK_KEY environment variable is not set.")
        sys.exit(1)
    client = OpenAI(api_key=ask_key)

    # Check if a prompt argument is provided
    if not args.prompt and not args.respond:
        print("Usage: python ask.py [-c] <prompt>")
        sys.exit(1)

    # Load conversation history if continuing
    conversation_history = load_conversation_history(ask_app_dir) if args.respond else []

    # Combine the system prompt with the user prompt
    system_prompt = "Answer in as few characters as possible. No formatting tokens such as ` or ```"
    user_prompt = ' '.join(args.prompt)

    try:
        # Prepare messages for the API call
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})

        # Make a request to OpenAI's GPT-4 model in chat mode
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        # Extract and print the response
        response_text = response.choices[0].message.content.strip()
        print(response_text)

        # Update conversation history
        if user_prompt:
            conversation_history.append({"role": "user", "content": user_prompt})
        conversation_history.append({"role": "assistant", "content": response_text})
        save_conversation_history(ask_app_dir, conversation_history)

        # Save the response to the last_output.log file in the ask_app_dir
        log_file_path = os.path.join(ask_app_dir, 'last_output.log')
        with open(log_file_path, 'w') as log_file:
            log_file.write(response_text)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
