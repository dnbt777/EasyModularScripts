# initializes loading of dotenv and stuff
from aiqs import ModelInterface
from aiqs.streaming_utils import stream_with_cancellation
from threading import Event
import os
from dotenv import load_dotenv

load_dotenv()

# initialize the model interface with OpenRouter
modelinterface = ModelInterface()

prompt = "Introduce yourself, with enthusiasm! Keep it short though and use emojis!"

# Example 1: Basic OpenRouter call
if os.environ.get("OPENROUTER_API_KEY"):
    # Get responses from OpenRouter
    for model in ["openai/gpt-4o", "openai/gpt-3.5-turbo"]:
        print(f"\n--- Testing {model} ---")
        try:
            response = modelinterface.send_to_ai(prompt, model=model, max_tokens=500, temperature=1.0)
            print(f"Response: {response[0]}\n")
            modelinterface.cost_tracker.show_cost_data()
        except Exception as e:
            print(f"Error with {model}: {str(e)}")

# Example 2: OpenRouter streaming example
if os.environ.get("OPENROUTER_API_KEY"):
    print("\n--- OpenRouter Streaming Example ---")
    # Example without cancellation
    response = modelinterface.send_to_ai(
        "Write a short poem about AI", 
        model=os.environ.get("MODEL", "openai/gpt-4o"), 
        max_tokens=200, 
        stream=True
    )
    print("\n\n")
    
    # Example with cancellation
    print("--- Streaming with Cancellation (will stop after a few words) ---")
    cancel_event = Event()
    import threading
    import time
    
    # Start streaming in a separate thread
    stream_thread = threading.Thread(
        target=lambda: stream_with_cancellation(
            "Write a paragraph about the future of AI", 
            cancel_event
        )
    )
    stream_thread.start()
    
    # Wait for 2 seconds and then cancel
    time.sleep(2)
    cancel_event.set()
    stream_thread.join()
    print("\n[Stream was cancelled]")