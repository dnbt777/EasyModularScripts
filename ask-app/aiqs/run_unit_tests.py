
import os
from dotenv import load_dotenv
from aiqs.ModelInterface import ModelInterface

def run_unit_tests():
    load_dotenv()

    model_interface = ModelInterface()

    models = [
        "bedrock-haiku",
        "bedrock-sonnet",
        "bedrock-opus",
        "bedrock-sonnet3.5",
        "bedrock-sonnet3.7"
        "gpt-4o",
        "gpt-3.5-turbo",
        "anthropic-haiku",
        "anthropic-sonnet",
        "anthropic-opus",
        "anthropic-sonnet3.5",
        "anthropic-sonnet3.7",
    ]

    test_prompt = "Say your name, then the capital of France, then a prime number"

    print("Running unit tests for each model:")
    for model in models:
        print(f"\nTesting {model}:")
        try:
            response, metrics = model_interface.send_to_ai(test_prompt, model, max_tokens=50)
            print(f"Response: {response.strip()}")
            print(f"Metrics: {metrics}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_unit_tests()
