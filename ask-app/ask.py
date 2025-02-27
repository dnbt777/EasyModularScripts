import os
import sys
import json
import argparse
from dotenv import load_dotenv
from aiqs.ModelInterface import ModelInterface

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

    parser = argparse.ArgumentParser(description="Ask AI a question.")
    parser.add_argument('prompt', nargs='*', help="The prompt to send to the AI model")
    parser.add_argument('-c', '--respond', action='store_true', help="Respond to the previous conversation")
    args = parser.parse_args()

    # Initialize the ModelInterface
    model_interface = ModelInterface()
    
    # Get model settings from environment variables
    model = os.getenv('MODEL', 'gpt-4o')
    max_tokens = int(os.getenv('MAX_TOKENS', '8192'))
    stream = int(os.getenv('stream', '0')) == 1

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
        # Prepare combined prompt
        combined_prompt = system_prompt + "\n\n"
        
        # Add conversation history
        for msg in conversation_history:
            if msg["role"] == "user":
                combined_prompt += f"User: {msg['content']}\n\n"
            elif msg["role"] == "assistant":
                combined_prompt += f"Assistant: {msg['content']}\n\n"
        
        # Add the current user prompt
        if user_prompt:
            combined_prompt += f"User: {user_prompt}\n\nAssistant: "
        
        # Make a request using the model_interface
        if stream:
            response_text, metrics = model_interface.send_to_ai(
                combined_prompt, 
                model=model, 
                max_tokens=max_tokens,
                stream=True,
                logging=False
            )
            print()
        else:
            response_text, metrics = model_interface.send_to_ai(
                combined_prompt, 
                model=model, 
                max_tokens=max_tokens,
                logging=False
            )
            print(response_text)
            print()

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
