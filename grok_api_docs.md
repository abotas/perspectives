# Grok API Documentation

## Overview
The xAI Grok API is compatible with OpenAI SDK but uses a different base URL and API key.

## Setup

### API Key
Create an API key via the [API Keys Page](https://console.x.ai/) in the xAI API Console.

Export it as an environment variable:
```bash
export XAI_API_KEY="your_api_key"
```

## API Endpoint
**Base URL**: `https://api.x.ai/v1`

## Making Requests

### Using OpenAI Responses API (Recommended)
Grok is fully compatible with the OpenAI Responses API:

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

response = client.responses.create(
    model="grok-4",
    input="What is the meaning of life?"
)

print(response.output_text)
```

With reasoning effort control:

```python
response = client.responses.create(
    model="grok-4",
    reasoning={"effort": "low"},
    input="What is the meaning of life?"
)

print(response.output_text)
```

### Using Chat Completions API (Legacy)
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {
            "role": "system",
            "content": "You are Grok, a highly intelligent, helpful AI assistant."
        },
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
)

print(response.choices[0].message.content)
```

### Using Native xAI SDK
```python
from xai_sdk import Client
from xai_sdk.chat import user, system
import os

client = Client(
    api_key=os.getenv("XAI_API_KEY"),
    timeout=3600  # Override default timeout for reasoning models
)

chat = client.chat.create(model="grok-4")
chat.append(system("You are Grok, a highly intelligent, helpful AI assistant."))
chat.append(user("What is the meaning of life?"))

response = chat.sample()
print(response.content)
```

## Available Models
- `grok-4` - Latest Grok model
- `grok-4-fast-non-reasoning` - Fast, non-reasoning variant
- `grok-3` - Previous generation

## Key Differences from OpenAI
1. **Base URL**: Must use `https://api.x.ai/v1` instead of OpenAI's default
2. **API Key**: Uses `XAI_API_KEY` environment variable
3. **Timeout**: Reasoning models may need longer timeout (3600s recommended)
4. **Structured Outputs**: Supported on certain models

## Vision Support
Certain Grok models can accept both text and images:

```python
from xai_sdk import Client
from xai_sdk.chat import user, image

client = Client(api_key=os.getenv("XAI_API_KEY"))

chat = client.chat.create(model="grok-4")
chat.append(
    user(
        "What's in this image?",
        image("https://example.com/image.png")
    )
)

response = chat.sample()
print(response.content)
```
