# OpenRouter models with provider prefixes
openrouter_models = [
    # OpenAI models
    "openai/gpt-4o",
    "openai/gpt-4-turbo",
    "openai/gpt-4",
    "openai/gpt-3.5-turbo",
    "openai/gpt-4o-mini",
    
    # Anthropic models
    "anthropic/claude-3-opus",
    "anthropic/claude-3-sonnet",
    "anthropic/claude-3-haiku",
    "anthropic/claude-3-5-sonnet",
    "anthropic/claude-3-7-sonnet",
    
    # Google models
    "google/gemini-1.5-pro",
    "google/gemini-1.5-flash",
    
    # Other models
    "mistral/mixtral-8x7b",
    "mistral/mistral-large",
    "meta/llama-3-70b",
    "meta/llama-3-8b"
]

# Model pricing information for cost tracking
model_pricing = {
    "openai/gpt-4o": {
        "input": 0.005,  # per 1000 tokens
        "output": 0.015   # per 1000 tokens
    },
    "openai/gpt-3.5-turbo": {
        "input": 0.0005,
        "output": 0.0015
    },
    # Add other models as needed
}

