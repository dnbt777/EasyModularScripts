
import base64
import os
import json
import logging
from aiqs.logger import log
from aiqs.CostTracker import CostTracker
from aiqs.model_list import bedrock_models, anthropic_models, openai_models
import boto3
import botocore
from botocore.exceptions import ClientError
from openai import OpenAI
import anthropic

class ModelInterface():
    def __init__(self, client=None, cost_tracker=None):
        if client:
            self.client = client
        else:
            # Make a client for Amazon Bedrock
            config = botocore.config.Config(
                read_timeout=900,
                connect_timeout=900,
                retries={"max_attempts": 0}
            )
            self.client = boto3.client(
                service_name="bedrock-runtime",
                region_name=os.environ.get("AWS_REGION"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                aws_session_token=os.environ.get("SESSION_TOKEN"),
                config=config,
            )

        if cost_tracker:
            self.cost_tracker = cost_tracker
        else:
            self.cost_tracker = CostTracker()

        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Initialize Anthropic client
        self.anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def invoke_claude_3_with_text(self, prompt, model="bedrock-haiku3.5", max_tokens=1024):
        """Invokes Anthropic Claude 3 Sonnet to run an inference using the input provided in the request body."""
        client = self.client or boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
        model_id = bedrock_models[model]
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
                "outputTokenCount": output_tokens,
                "model": model,
            }
            return result_text, metrics
        except ClientError as err:
            log(
                "Couldn't invoke Claude 3. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def invoke_claude_3_with_stream(self, prompt, model="bedrock-sonnet", max_tokens=1000):
        """Invokes Anthropic Claude 3 Sonnet to run an inference using the input provided in the request body."""
        client = self.client or boto3.client(service_name="bedrock-runtime", region_name="us-west-2") # todo - dont hardcode this
        model_id = bedrock_models[model]
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
            print(response)
            result_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            metrics = {
                "inputTokenCount": input_tokens,
                "outputTokenCount": output_tokens,
                "model": model,
            }
            return result_text, metrics
        except Exception as err:
            log(f"Couldn't invoke {model}. Here's why: {str(err)}")
            raise

    def invoke_anthropic_chat_model(self, prompt, model, max_tokens=1000, temperature=0.7, system_prompt="You are a helpful chatbot."):
        """Invokes Anthropic API to run an inference using the input provided in the request body."""
        model = anthropic_models[model_id]
        try:
            response = self.anthropic_client.messages.create(
                model=model.replace("anthropic-", ""),
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result_text = response.content[0].text
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            metrics = {
                "inputTokenCount": input_tokens,
                "outputTokenCount": output_tokens,
                "model": model
            }
            return result_text, metrics
        except Exception as err:
            log(f"Couldn't invoke Anthropic {model}. Here's why: {str(err)}")
            raise

    def send_to_ai(self, prompt, model, max_tokens=1000, temperature=0.5, stream=False, metrics=True, logging=True):
        if logging:
            log(f"Sending to {model}")
            log("SENDING PROMPT, LENGTH =", len(prompt))
            log("Estimated tokens:", len(prompt) // 5)
            log("PROMPT:", prompt)
        if model.startswith("bedrock-"):
            if not stream:
                result_text, metrics = self.invoke_claude_3_with_text(prompt, model=model, max_tokens=max_tokens)
            else:
                result_text, metrics = self.invoke_claude_3_with_stream(prompt, model=model, max_tokens=max_tokens)
            # Update cost data for Claude models
            self.cost_tracker.add_request_metrics_to_cost_data(metrics)
        elif model in openai_models:
            result_text, metrics = self.invoke_openai_chat_model(prompt, model, max_tokens=max_tokens, temperature=temperature)
            self.cost_tracker.add_request_metrics_to_cost_data(metrics)
        elif model.startswith("anthropic-"):
            result_text, metrics = self.invoke_anthropic_chat_model(prompt, model, max_tokens=max_tokens, temperature=temperature)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        if metrics:
            return result_text, metrics
        else:
            return result_text
