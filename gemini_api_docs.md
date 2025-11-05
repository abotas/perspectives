Home
Gemini API
Gemini API Docs
Was this helpful?

Send feedbackGemini API quickstart

content_copy


This quickstart shows you how to install our libraries and make your first Gemini API request.

Before you begin
You need a Gemini API key. If you don't already have one, you can get it for free in Google AI Studio.

Install the Google GenAI SDK
Python
JavaScript
Go
Java
Apps Script
Using Python 3.9+, install the google-genai package using the following pip command:


pip install -q -U google-genai
Make your first request
Here is an example that uses the generateContent method to send a request to the Gemini API using the Gemini 2.5 Flash model.

If you set your API key as the environment variable GEMINI_API_KEY, it will be picked up automatically by the client when using the Gemini API libraries. Otherwise you will need to pass your API key as an argument when initializing the client.

Note that all code samples in the Gemini API docs assume that you have set the environment variable GEMINI_API_KEY.

Python
JavaScript
Go
Java
Apps Script
REST

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)

Text generation

content_copy


The Gemini API can generate text output from various inputs, including text, images, video, and audio, leveraging Gemini models.

Here's a basic example that takes a single text input:

Python
JavaScript
Go
Java
REST
Apps Script

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)

Thinking with Gemini 2.5
2.5 Flash and Pro models have "thinking" enabled by default to enhance quality, which may take longer to run and increase token usage.

When using 2.5 Flash, you can disable thinking by setting the thinking budget to zero.

For more details, see the thinking guide.

Python
JavaScript
Go
Java
REST
Apps Script

from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    ),
)
print(response.text)
System instructions and other configurations
You can guide the behavior of Gemini models with system instructions. To do so, pass a GenerateContentConfig object.

Python
JavaScript
Go
Java
REST
Apps Script

from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko."),
    contents="Hello there"
)

print(response.text)
The GenerateContentConfig object also lets you override default generation parameters, such as temperature.

Python
JavaScript
Go
Java
REST
Apps Script

from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Explain how AI works"],
    config=types.GenerateContentConfig(
        temperature=0.1
    )
)
print(response.text)