import os
from datetime import datetime
from openai import OpenAI
from anthropic import Anthropic
from google import genai
from pydantic import BaseModel


class ModelInfo(BaseModel):
    id: str
    display_name: str
    release_date: datetime
    provider: str


SUPPORTED_MODELS = [
    # OpenAI models (sorted by release date, newest first)
    ModelInfo(id="gpt-5-2025-08-07",            display_name="GPT-5 (2025-08-07)",             release_date=datetime(2025, 8, 1),   provider="openai"),
    ModelInfo(id="gpt-5-mini-2025-08-07",       display_name="GPT-5 Mini (2025-08-07)",        release_date=datetime(2025, 8, 5),   provider="openai"),
    ModelInfo(id="gpt-5-nano-2025-08-07",       display_name="GPT-5 Nano (2025-08-07)",        release_date=datetime(2025, 8, 5),   provider="openai"),
    ModelInfo(id="gpt-4.1-2025-04-14",          display_name="GPT-4.1 (2025-04-14)",           release_date=datetime(2025, 4, 10),  provider="openai"),
    ModelInfo(id="gpt-4.1-mini-2025-04-14",     display_name="GPT-4.1 Mini (2025-04-14)",      release_date=datetime(2025, 4, 10),  provider="openai"),
    ModelInfo(id="gpt-4.1-nano-2025-04-14",     display_name="GPT-4.1 Nano (2025-04-14)",      release_date=datetime(2025, 4, 10),  provider="openai"),
    ModelInfo(id="gpt-4o-2024-11-20",           display_name="GPT-4o (2024-11-20)",            release_date=datetime(2025, 2, 11),  provider="openai"),
    ModelInfo(id="o1-2024-12-17",               display_name="o1 (2024-12-17)",                release_date=datetime(2024, 12, 16), provider="openai"),
    ModelInfo(id="o1-mini-2024-09-12",          display_name="o1 Mini (2024-09-12)",           release_date=datetime(2024, 9, 12),  provider="openai"),
    ModelInfo(id="gpt-4o-2024-08-06",           display_name="GPT-4o (2024-08-06)",            release_date=datetime(2024, 8, 4),   provider="openai"),
    ModelInfo(id="gpt-4o-2024-05-13",           display_name="GPT-4o (2024-05-13)",            release_date=datetime(2024, 5, 10),  provider="openai"),
    ModelInfo(id="gpt-4o-mini-2024-07-18",      display_name="GPT-4o Mini (2024-07-18)",       release_date=datetime(2024, 7, 16),  provider="openai"),
    ModelInfo(id="gpt-4-turbo-2024-04-09",      display_name="GPT-4 Turbo (2024-04-09)",       release_date=datetime(2024, 4, 8),   provider="openai"),
    ModelInfo(id="gpt-4",                       display_name="GPT-4",                          release_date=datetime(2023, 6, 27),  provider="openai"),
    ModelInfo(id="gpt-4-0613",                  display_name="GPT-4 (0613)",                   release_date=datetime(2023, 6, 12),  provider="openai"),
    ModelInfo(id="gpt-3.5-turbo",               display_name="GPT-3.5 Turbo",                  release_date=datetime(2023, 2, 28),  provider="openai"),
    ModelInfo(id="gpt-3.5-turbo-0125",          display_name="GPT-3.5 Turbo (0125)",           release_date=datetime(2024, 1, 23),  provider="openai"),

    # Anthropic models
    ModelInfo(id="claude-haiku-4-5-20251001",   display_name="Claude Haiku 4.5",               release_date=datetime(2025, 10, 15), provider="anthropic"),
    ModelInfo(id="claude-sonnet-4-5-20250929",  display_name="Claude Sonnet 4.5",              release_date=datetime(2025, 9, 29),  provider="anthropic"),
    ModelInfo(id="claude-opus-4-1-20250805",    display_name="Claude Opus 4.1",                release_date=datetime(2025, 8, 5),   provider="anthropic"),
    ModelInfo(id="claude-opus-4-20250514",      display_name="Claude Opus 4",                  release_date=datetime(2025, 5, 22),  provider="anthropic"),
    ModelInfo(id="claude-sonnet-4-20250514",    display_name="Claude Sonnet 4",                release_date=datetime(2025, 5, 22),  provider="anthropic"),
    ModelInfo(id="claude-3-7-sonnet-20250219",  display_name="Claude Sonnet 3.7",              release_date=datetime(2025, 2, 24),  provider="anthropic"),
    ModelInfo(id="claude-3-5-haiku-20241022",   display_name="Claude Haiku 3.5",               release_date=datetime(2024, 10, 22), provider="anthropic"),
    ModelInfo(id="claude-3-haiku-20240307",     display_name="Claude Haiku 3",                 release_date=datetime(2024, 3, 7),   provider="anthropic"),
    ModelInfo(id="claude-3-opus-20240229",      display_name="Claude Opus 3",                  release_date=datetime(2024, 2, 29),  provider="anthropic"),

    # Grok models
    ModelInfo(id="grok-4-fast-reasoning",       display_name="Grok 4 Fast (Reasoning)",        release_date=datetime(2025, 8, 5),   provider="grok"),
    ModelInfo(id="grok-4-fast-non-reasoning",   display_name="Grok 4 Fast (Non-Reasoning)",    release_date=datetime(2025, 8, 5),   provider="grok"),
    ModelInfo(id="grok-4-0709",                 display_name="Grok 4",                         release_date=datetime(2025, 7, 9),   provider="grok"),
    ModelInfo(id="grok-3",                      display_name="Grok 3",                         release_date=datetime(2025, 4, 5),   provider="grok"),
    ModelInfo(id="grok-3-mini",                 display_name="Grok 3 Mini",                    release_date=datetime(2025, 4, 5),   provider="grok"),
    ModelInfo(id="grok-2-1212",                 display_name="Grok 2 (1212)",                  release_date=datetime(2025, 1, 20),  provider="grok"),

    # Google Gemini models
    ModelInfo(id="gemini-3-pro-preview",        display_name="Gemini 3 Pro",                   release_date=datetime(2025, 11, 15), provider="google"),
    ModelInfo(id="gemini-2.5-pro",              display_name="Gemini 2.5 Pro",                 release_date=datetime(2025, 6, 17),  provider="google"),
    ModelInfo(id="gemini-2.5-flash",            display_name="Gemini 2.5 Flash",               release_date=datetime(2025, 6, 17),  provider="google"),
    ModelInfo(id="gemini-2.0-flash",            display_name="Gemini 2.0 Flash",               release_date=datetime(2025, 2, 1),   provider="google"),

    # Moonshot Kimi models
    ModelInfo(id="kimi-k2-turbo-preview",       display_name="Kimi K2 Turbo",                  release_date=datetime(2025, 9, 5),   provider="moonshot"),
    ModelInfo(id="kimi-k2-0905-preview",        display_name="Kimi K2 (0905)",                 release_date=datetime(2025, 9, 5),   provider="moonshot"),
    ModelInfo(id="kimi-k2-0711-preview",        display_name="Kimi K2 (0711)",                 release_date=datetime(2025, 7, 11),  provider="moonshot"),
    ModelInfo(id="kimi-k2-thinking",            display_name="Kimi K2 Thinking",               release_date=datetime(2025, 9, 5),   provider="moonshot"),
    ModelInfo(id="kimi-k2-thinking-turbo",      display_name="Kimi K2 Thinking Turbo",         release_date=datetime(2025, 9, 5),   provider="moonshot"),
]


def _get_supported_model_ids() -> list[str]:
    return [f"{model.provider}/{model.id}" for model in SUPPORTED_MODELS]


def get_model_info(model_id: str) -> ModelInfo:
    for model in SUPPORTED_MODELS:
        if f"{model.provider}/{model.id}" == model_id:
            return model
    raise ValueError(f"Model not found: {model_id}")


def _query_openai(model: str, prompt: str, max_output_tokens: int) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=max_output_tokens
    )
    return response.output_text


def _query_anthropic(model: str, prompt: str, max_output_tokens: int) -> str:
    model_max_tokens = {
        "claude-3-opus-20240229": 4096,
        "claude-3-haiku-20240307": 4096,
    }

    if model in model_max_tokens:
        model_limit = model_max_tokens[model]
        if max_output_tokens > model_limit:
            print(f"WARNING: Requested max_output_tokens={max_output_tokens} exceeds {model} limit of {model_limit}. Capping to {model_limit}.")
            max_output_tokens = model_limit

    client = Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=max_output_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def _query_grok(model: str, prompt: str, max_output_tokens: int) -> str:
    client = OpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1"
    )
    response = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=max_output_tokens
    )
    return response.output_text


def _query_gemini(model: str, prompt: str, max_output_tokens: int) -> str:
    client = genai.Client()
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text


def _query_kimi(model: str, prompt: str, max_output_tokens: int) -> str:
    client = OpenAI(
        api_key=os.environ["MOONSHOT_API_KEY"],
        base_url="https://api.moonshot.ai/v1"
    )

    # Thinking models require temperature=1.0 for best performance
    temperature = 1.0 if "thinking" in model else 0.6

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are Kimi, an AI assistant provided by Moonshot AI."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_output_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content


def query_model(model_id: str, prompt: str, max_output_tokens: int) -> str:
    supported_model_ids = _get_supported_model_ids()
    if model_id not in supported_model_ids:
        raise ValueError(f"Unsupported model: {model_id}. Supported models: {supported_model_ids}")

    provider, model = model_id.split("/")
    if provider == "openai":
        return _query_openai(model, prompt, max_output_tokens)
    elif provider == "anthropic":
        return _query_anthropic(model, prompt, max_output_tokens)
    elif provider == "grok":
        return _query_grok(model, prompt, max_output_tokens)
    elif provider == "google":
        return _query_gemini(model, prompt, max_output_tokens)
    elif provider == "moonshot":
        return _query_kimi(model, prompt, max_output_tokens)
    raise ValueError(f"Unknown provider: {provider}")
