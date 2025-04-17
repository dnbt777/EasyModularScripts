
import requests
from threading import Event, Thread
import os
import json

def stream_with_cancellation(prompt: str, cancel_event: Event, system_prompt="You are a helpful chatbot.", max_tokens=1000, temperature=0.7):
    """
    Stream responses from OpenRouter with support for cancellation.
    
    Args:
        prompt: The user's input prompt
        cancel_event: An Event that can be set to cancel streaming
        system_prompt: Optional system instruction
        max_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature for generation
        
    Returns:
        None - output is printed directly to console
    """
    model = os.environ.get("MODEL", "openai/gpt-4o")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True
    }
    
    with requests.Session() as session:
        response = session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            stream=True
        )
        
        try:
            for line in response.iter_lines():
                if cancel_event.is_set():
                    response.close()
                    return
                
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]  # Remove 'data: ' prefix
                        if data_str.strip() == '[DONE]':
                            break
                        
                        try:
                            data = json.loads(data_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    print(content, end='', flush=True)
                        except json.JSONDecodeError:
                            continue
        finally:
            response.close()

# Example usage demonstration
def example_streaming():
    """Example of how to use the stream_with_cancellation function"""
    cancel_event = Event()
    stream_thread = Thread(
        target=lambda: stream_with_cancellation("Write a short story about AI", cancel_event)
    )
    stream_thread.start()
    
    # To cancel the stream after 5 seconds:
    # import time
    # time.sleep(5)
    # cancel_event.set()
    
    stream_thread.join()  # Wait for streaming to complete
