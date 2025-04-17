
import os
import json
import requests
from aiqs.logger import log
from aiqs.CostTracker import CostTracker

class ModelInterface():
    def __init__(self, cost_tracker=None):
        if cost_tracker:
            self.cost_tracker = cost_tracker
        else:
            self.cost_tracker = CostTracker()

        # Initialize OpenRouter client
        self.openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        if not self.openrouter_api_key:
            log("WARNING: OPENROUTER_API_KEY not found in environment variables")
            
    def invoke_openrouter_chat_model(self, prompt, model, max_tokens=1000, temperature=0.7, system_prompt="You are a helpful chatbot.", stream=False):
        """Invokes OpenRouter API to run an inference using the input provided in the request body."""
        model_name = os.environ.get("MODEL", model)
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream
        }
        
        if stream:
            # Create a capture list to store aggregated response
            response_data = {"text": "", "input_tokens": 0, "output_tokens": 0}
            
            with requests.Session() as session:
                response = session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    stream=True
                )
                
                try:
                    for line in response.iter_lines():
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
                                            response_data["text"] += content
                                    
                                    # Capture usage info if available
                                    if 'usage' in data:
                                        if 'prompt_tokens' in data['usage']:
                                            response_data["input_tokens"] = data['usage']['prompt_tokens']
                                        if 'completion_tokens' in data['usage']:
                                            response_data["output_tokens"] = data['usage']['completion_tokens']
                                except json.JSONDecodeError:
                                    continue
                finally:
                    response.close()
            
            metrics = {
                "inputTokenCount": response_data["input_tokens"],
                "outputTokenCount": response_data["output_tokens"],
                "model": model_name,
            }
            
            return response_data["text"], metrics
        else:
            # Non-streaming request
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                result_text = result["choices"][0]["message"]["content"]
                
                input_tokens = 0
                output_tokens = 0
                if "usage" in result:
                    input_tokens = result["usage"].get("prompt_tokens", 0)
                    output_tokens = result["usage"].get("completion_tokens", 0)
                
                metrics = {
                    "inputTokenCount": input_tokens,
                    "outputTokenCount": output_tokens,
                    "model": model_name,
                }
                
                return result_text, metrics
            else:
                error_message = f"OpenRouter API call failed with status code {response.status_code}: {response.text}"
                log(error_message)
                raise Exception(error_message)

    def send_to_ai(self, prompt, model, max_tokens=1000, temperature=0.5, stream=False, metrics=True, logging=True):
        if logging:
            log(f"Sending to {model}")
            log("SENDING PROMPT, LENGTH =", len(prompt))
            log("Estimated tokens:", len(prompt) // 5)
            log("PROMPT:", prompt)
            
        result_text, metrics_data = self.invoke_openrouter_chat_model(
            prompt, 
            model, 
            max_tokens=max_tokens, 
            temperature=temperature, 
            stream=stream
        )
        self.cost_tracker.add_request_metrics_to_cost_data(metrics_data)
        
        if metrics:
            return result_text, metrics_data
        else:
            return result_text
