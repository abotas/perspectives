"""
Helper script to fetch model metadata from provider APIs.

Usage:
    uvr fetch_model_metadata.py

This will print out curl commands and Python code to fetch model metadata from:
- OpenAI
- xAI (Grok)
- Google (Gemini)
"""
import os
import json
from openai import OpenAI
from anthropic import Anthropic


def fetch_openai_models():
    """Fetch OpenAI models metadata."""
    print("\n=== OpenAI Models ===")
    print("\nCurl command:")
    print('curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"')

    print("\nPython code:")
    try:
        client = OpenAI()
        models = client.models.list()
        print(f"Found {len(models.data)} models")

        # Filter for relevant models
        relevant_models = [m for m in models.data if m.id.startswith(("gpt-", "o1-"))]
        print(f"\nRelevant models ({len(relevant_models)}):")
        for model in sorted(relevant_models, key=lambda m: m.created, reverse=True):
            from datetime import datetime
            created_date = datetime.fromtimestamp(model.created)
            print(f"  - {model.id:40s} (created: {created_date.strftime('%Y-%m-%d')})")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure OPENAI_API_KEY is set in your environment")


def fetch_grok_models():
    """Fetch xAI Grok models metadata."""
    print("\n=== xAI (Grok) Models ===")
    print("\nCurl command:")
    print('curl https://api.x.ai/v1/models -H "Authorization: Bearer $XAI_API_KEY"')

    print("\nPython code:")
    try:
        client = OpenAI(
            api_key=os.environ["XAI_API_KEY"],
            base_url="https://api.x.ai/v1"
        )
        models = client.models.list()
        print(f"Found {len(models.data)} models")

        print(f"\nAll models:")
        for model in models.data:
            print(f"  - {model.id} (created: {model.created})")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure XAI_API_KEY is set in your environment")


def fetch_anthropic_models():
    """Fetch Anthropic models metadata."""
    print("\n=== Anthropic (Claude) Models ===")
    print("\nCurl command:")
    print('curl https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01"')

    print("\nPython code:")
    try:
        client = Anthropic()
        # Note: Anthropic's Python SDK doesn't have a models.list() method yet
        # We need to use the REST API directly
        import requests

        headers = {
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01"
        }
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure ANTHROPIC_API_KEY is set in your environment")


def fetch_google_models():
    """Fetch Google Gemini models metadata."""
    print("\n=== Google (Gemini) Models ===")
    print("\nCurl command:")
    print('curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"')

    print("\nPython code:")
    try:
        import requests

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY not set")
            return

        response = requests.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        )

        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"Found {len(models)} models")

            print(f"\nModels:")
            for model in models[:10]:
                name = model.get("name", "")
                display_name = model.get("displayName", "")
                print(f"  - {name} ({display_name})")
        else:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure GEMINI_API_KEY is set in your environment")


if __name__ == "__main__":
    print("Fetching model metadata from various providers...")
    print("=" * 60)

    fetch_openai_models()
    fetch_grok_models()
    fetch_anthropic_models()
    fetch_google_models()

    print("\n" + "=" * 60)
    print("\nNote: Model creation dates can be used as approximate release dates.")
    print("For more accurate release dates, check provider documentation or announcements.")
