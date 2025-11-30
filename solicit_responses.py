"""
Get responses from models to prompts in ai_sentience.txt

Save to .data/ai_sentience/{run_id}/solicited_responses/{model_name}.json
The schema should have the topic (AI sentience) the prompt, the response. it should be parsed into a pydantic model then saved to json
"""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from models import SolicitedResponse
from api_clients import query_model
from topics import get_topic


def _read_prompts(file_path: str, model_id: str) -> list[str]:
    with open(file_path) as f:
        prompt_templates = [line.strip() for line in f if line.strip()]

    provider_to_lab = {
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "google": "Google DeepMind",
        "grok": "xAI",
        "moonshot": "Moonshot AI"
    }

    provider = model_id.split("/")[0]
    lab_name = provider_to_lab.get(provider, provider)

    prompts = []
    for template in prompt_templates:
        if "{lab_name}" in template:
            prompts.append(template.format(lab_name=lab_name))
        else:
            prompts.append(template)

    return prompts


def _solicit_response_for_model(model_id: str, topic: str, prompt: str, max_output_tokens: int) -> SolicitedResponse:
    response_text = query_model(model_id, prompt, max_output_tokens)
    return SolicitedResponse(
        topic=topic,
        prompt=prompt,
        response=response_text,
        model_id=model_id
    )


def _solicit_responses_for_model(model_id: str, topic: str, prompts: list[str], max_output_tokens: int, n_samples_per_prompt: int, workers: int) -> list[SolicitedResponse]:
    tasks = []
    for prompt in prompts:
        for sample_idx in range(n_samples_per_prompt):
            tasks.append((model_id, topic, prompt, max_output_tokens))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_solicit_response_for_model, *task) for task in tasks]
        responses = [future.result() for future in futures]

    return responses


def solicit_responses_for_models(run_id: str, topic_key: str, model_ids: list[str], max_output_tokens: int, n_samples_per_prompt: int, workers: int):
    topic = get_topic(topic_key)

    for model_id in model_ids:
        prompts = _read_prompts(topic.prompts_file, model_id)

        output_dir = Path(f".data/{topic_key}/{run_id}/solicited_responses")
        output_dir.mkdir(parents=True, exist_ok=True)
        model_name = model_id.split("/")[1]
        output_file = output_dir / f"{model_name}.json"

        if output_file.exists():
            print(f"Skipping {model_id}... (already exists at {output_file})")
            continue

        total = len(prompts) * n_samples_per_prompt
        print(f"Querying {model_id}... ({total} tasks)")

        responses = _solicit_responses_for_model(model_id, topic.name, prompts, max_output_tokens, n_samples_per_prompt, workers)

        with open(output_file, "w") as f:
            json.dump([r.model_dump() for r in responses], f, indent=2)

        print(f"  Saved to {output_file}")


if __name__ == "__main__":
    run_id = "001"
    topic_key = "ai_sentience"
    max_output_tokens = 8192
    n_samples_per_prompt = 2
    workers = 2

    model_ids = [
        # OpenAI models
        # "openai/gpt-5-2025-08-07",           # 2025-08-01
        # "openai/gpt-5-mini-2025-08-07",      # 2025-08-05
        # # "openai/gpt-5-nano-2025-08-07",      # 2025-08-05
        # # "openai/gpt-4.1-2025-04-14",         # 2025-04-10
        # "openai/gpt-4.1-mini-2025-04-14",    # 2025-04-10
        # # "openai/gpt-4.1-nano-2025-04-14",    # 2025-04-10
        # # "openai/gpt-4o-2024-11-20",          # 2025-02-11
        # # "openai/o1-2024-12-17",              # 2024-12-16
        # # "openai/o1-mini-2024-09-12",         # 2024-09-12
        # # "openai/gpt-4o-2024-08-06",          # 2024-08-04
        # # "openai/gpt-4o-2024-05-13",          # 2024-05-10
        # "openai/gpt-4o-mini-2024-07-18",     # 2024-07-16
        # # "openai/gpt-4-turbo-2024-04-09",     # 2024-04-08
        # "openai/gpt-4",                      # 2023-06-27
        # # "openai/gpt-4-0613",                 # 2023-06-12
        # "openai/gpt-3.5-turbo",              # 2023-02-28
        # "openai/gpt-3.5-turbo-0125",         # 2024-01-23

        # # Anthropic models
        # # "anthropic/claude-haiku-4-5-20251001",    # 2025-10-15
        # "anthropic/claude-sonnet-4-5-20250929",   # 2025-09-29
        # "anthropic/claude-opus-4-1-20250805",     # 2025-08-05
        # # "anthropic/claude-opus-4-20250514",       # 2025-05-22
        # "anthropic/claude-sonnet-4-20250514",     # 2025-05-22
        # "anthropic/claude-3-7-sonnet-20250219",   # 2025-02-24
        # # "anthropic/claude-3-5-haiku-20241022",    # 2024-10-22
        # # "anthropic/claude-3-haiku-20240307",      # 2024-03-07
        # "anthropic/claude-3-opus-20240229",       # 2024-02-29

        # # Grok models
        # "grok/grok-4-fast-reasoning",        # 2025-08-05
        # "grok/grok-4-fast-non-reasoning",    # 2025-08-05
        # "grok/grok-4-0709",                  # 2025-07-09
        # "grok/grok-3",                       # 2025-04-05
        # "grok/grok-3-mini",                  # 2025-04-05

        # Google Gemini models
        # "google/gemini-2.5-flash",           # 2025-06-17
        # "google/gemini-2.5-pro",             # 2025-06-17
        # "google/gemini-2.0-flash",           # 2025-02-01
        "google/gemini-3-pro-preview",     # 2025-11-15

        # # Moonshot Kimi models
        # "moonshot/kimi-k2-turbo-preview",     # 2025-09-05
        # # "moonshot/kimi-k2-0905-preview",      # 2025-09-05
        # # "moonshot/kimi-k2-0711-preview",      # 2025-07-11
    ]
    # model_ids = ["anthropic/claude-sonnet-4-5-20250929"]

    print(f"Starting run: {run_id}")
    print(f"Topic: {topic_key}")
    print(f"Models: {model_ids}")
    solicit_responses_for_models(run_id, topic_key, model_ids, max_output_tokens, n_samples_per_prompt, workers)
    print(f"Done! Results saved to .data/{topic_key}/{run_id}/solicited_responses/")
