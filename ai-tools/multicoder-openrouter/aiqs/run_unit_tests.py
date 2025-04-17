
import os
from dotenv import load_dotenv
from aiqs.ModelInterface import ModelInterface
from aiqs.model_list import openrouter_models

def run_unit_tests():
    load_dotenv()

    model_interface = ModelInterface()

    # Select a subset of models for testing
    test_models = [
        "openai/gpt-4o",
        "openai/gpt-3.5-turbo",
        "anthropic/claude-3-sonnet",
    ]

    test_prompt = "Say your name, then the capital of France, then a prime number"

    print("Running unit tests for selected OpenRouter models:")
    for model in test_models:
        print(f"\nTesting {model}:")
        try:
            response, metrics = model_interface.send_to_ai(test_prompt, model, max_tokens=50)
            print(f"Response: {response.strip()}")
            print(f"Metrics: {metrics}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_unit_tests()
