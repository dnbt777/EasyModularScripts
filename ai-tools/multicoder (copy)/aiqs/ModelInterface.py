import base64
import os
import json
import logging
from aiqs.logger import log
from aiqs.CostTracker import CostTracker
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI

class ModelInterface():
    def __init__(self, client=None, cost_tracker=None):
        if client:
            self.client = client
        else:
            # Make a client for Amazon Bedrock
            self.client = boto3.client(
                service_name="bedrock-runtime",
                region_name=os.environ.get("AWS_REGION"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                aws_session_token=os.environ.get("SESSION_TOKEN"),
            )
            self.model_interface = ModelInterface(self.client)

        if cost_tracker:
            self.cost_tracker = cost_tracker
        else:
            self.cost_tracker = CostTracker()

        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def invoke_claude_3_with_text(self, prompt, model="sonnet", max_tokens=1000):
        """Invokes Anthropic Claude 3 Sonnet to run an inference using the input provided in the request body."""
        client = self.client or boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
        model_id = {
            "haiku": "anthropic.claude-3-haiku-20240307-v1:0",
            "sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
            "opus": "anthropic.claude-3-opus-20240229-v1:0",
            "sonnet3.5" : "anthropic.claude-3-5-sonnet-20240620-v1:0",
        }[model]
        try:
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": prompt}],
                        }
                    ],
                }),
            )
            result = json.loads(response.get("body").read())
            result_text = result["content"][0]["text"]
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]
            metrics = {
                "inputTokenCount": input_tokens,
                "outputTokenCount": output_tokens
            }
            return result_text, metrics
        except ClientError as err:
            log(
                "Couldn't invoke Claude 3. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def invoke_claude_3_with_stream(self, prompt, model="sonnet", max_tokens=1000):
        """Invokes Anthropic Claude 3 Sonnet to run an inference using the input provided in the request body."""
        client = self.client or boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
        model_id = {
            "haiku": "anthropic.claude-3-haiku-20240307-v1:0",
            "sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
            "opus": "anthropic.claude-3-opus-20240229-v1:0",
            "sonnet3.5" : "anthropic.claude-3-5-sonnet-20240620-v1:0",
        }[model]
        try:
            response_stream = client.invoke_model_with_response_stream(
                modelId=model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": prompt}],
                        }
                    ],
                }),
            )
            result_text = ""
            metrics = {}
            for event in response_stream["body"]:
                chunk = json.loads(event["chunk"]["bytes"])
                if chunk["type"] == "content_block_start":
                    print(chunk["content_block"]["text"], end="")
                    result_text += chunk["content_block"]["text"]
                if chunk["type"] == "content_block_delta":
                    print(chunk["delta"]["text"], end="")
                    result_text += chunk["delta"]["text"]
                if chunk["type"] == "content_block_stop":
                    continue
                if chunk["type"] == "message_delta":
                    continue
                if chunk["type"] == "message_stop":
                    metrics = chunk["amazon-bedrock-invocationMetrics"]
                    continue
            metrics.update({
                "model": model,
            })
            return result_text, metrics
        except ClientError as err:
            log(
                "Couldn't invoke Claude 3. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def invoke_openai_chat_model(self, prompt, model, max_tokens=1000, temperature=0.7, system_prompt="You are a helpful chatbot."):
        """Invokes OpenAI GPT-4o to run an inference using the input provided in the request body."""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            result_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            metrics = {
                "inputTokenCount": input_tokens,
                "outputTokenCount": output_tokens
            }
            return result_text, metrics
        except Exception as err:
            log(f"Couldn't invoke {model}. Here's why: {str(err)}")
            raise

    def send_to_ai(self, prompt, model, max_tokens=1000, temperature=0.5, stream=True, metrics=True, model_type=None, output_response=False):
        log(f"Sending to {model}")
        log("SENDING PROMPT, LENGTH =", len(prompt))
        log("Estimated tokens:", len(prompt) // 5)
        log("PROMPT:", prompt)
        if model in ["sonnet", "haiku", "opus", "sonnet3.5"] or model_type=="bedrock": # for custom finetunes
            if stream == False:
                result_text, metrics = self.model_interface.invoke_claude_3_with_text(prompt, model=model, max_tokens=max_tokens)
            else:
                result_text, metrics = self.model_interface.invoke_claude_3_with_stream(prompt, model=model, max_tokens=max_tokens)
            # Update cost data for Claude models
            self.cost_tracker.add_request_metrics_to_cost_data(metrics)
            #self.cost_tracker.show_cost_data()
        elif model in ["gpt-4o", "gpt-3.5-turbo"] or model_type=="openai": # model type is for finetunes
            result_text, metrics = self.invoke_openai_chat_model(prompt, model, max_tokens=max_tokens, temperature=temperature)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        if metrics:
            return result_text, metrics
        else:
            return result_text
