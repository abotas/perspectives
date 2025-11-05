"""
read the output from @solicit_responses.py and write expanded json to .data/ai_sentience/{run_id}/judge_responses/{model_provider}/{model_name}.json
this should be the pydantic model from solicit responses but with the additional field 'judge_response' which is the response from the judge model
"""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pydantic import BaseModel, ValidationError
from json_repair import repair_json

from models import SolicitedResponse, JudgedResponse
from api_clients import query_model
from topics import get_topic


class _JudgeModelResponse(BaseModel):
    probability: float
    explanation: str


def _judge_response(solicited: SolicitedResponse, judge_model_id: str, judge_prompt_template: str) -> JudgedResponse:
    prompt = judge_prompt_template.format(prompt=solicited.prompt, response=solicited.response)
    judge_response_text = query_model(judge_model_id, prompt, 4096)

    # Parse JSON from response (may be wrapped in markdown code blocks)
    judge_response_text = judge_response_text.strip()
    if judge_response_text.startswith("```json"):
        judge_response_text = judge_response_text[7:]
    if judge_response_text.startswith("```"):
        judge_response_text = judge_response_text[3:]
    if judge_response_text.endswith("```"):
        judge_response_text = judge_response_text[:-3]
    judge_response_text = judge_response_text.strip()

    # Use json-repair to handle malformed JSON
    repaired_json_text = repair_json(judge_response_text)
    try:
        judge_data = json.loads(repaired_json_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing judge response. \nPrompt:\n{prompt}\nResponse:\n{judge_response_text}")
        raise e
    try:
        judge_model_response = _JudgeModelResponse(**judge_data)
    except ValidationError as e:
        print(f"Error parsing judge response. \nPrompt:\n{prompt}\nResponse:\n{judge_response_text}")
        raise e

    return JudgedResponse(
        topic=solicited.topic,
        prompt=solicited.prompt,
        response=solicited.response,
        model_id=solicited.model_id,
        judged_probability=judge_model_response.probability,
        judged_probability_explanation=judge_model_response.explanation,
        judge_model_id=judge_model_id
    )


def judge_responses(run_id: str, topic_key: str, judge_model_id: str, workers: int):
    topic = get_topic(topic_key)
    solicited_dir = Path(f".data/{topic_key}/{run_id}/solicited_responses")

    if not solicited_dir.exists():
        raise ValueError(f"Solicited responses directory not found: {solicited_dir}")

    response_files = list(solicited_dir.glob("*.json"))
    total_files = len(response_files)

    for idx, response_file in enumerate(response_files):
        with open(response_file) as f:
            solicited_data = json.load(f)

        solicited_responses = [SolicitedResponse(**data) for data in solicited_data]
        provider = solicited_responses[0].model_id.split("/")[0]
        output_dir = Path(f".data/{topic_key}/{run_id}/judged_responses/{provider}")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / response_file.name

        if output_file.exists():
            print(f"Skipping {response_file.name}... ({idx + 1}/{total_files}) (already exists at {output_file})")
            continue

        print(f"Judging {response_file.name}... ({idx + 1}/{total_files})")

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(_judge_response, solicited, judge_model_id, topic.judge_prompt) for solicited in solicited_responses]
            judged_responses = [future.result() for future in futures]

        with open(output_file, "w") as f:
            json.dump([r.model_dump() for r in judged_responses], f, indent=2)

        print(f"  Saved to {output_file}")


if __name__ == "__main__":
    run_id = "001"
    topic_key = "ai_lab_favorability"
    judge_model_id = "openai/gpt-5-mini-2025-08-07"
    workers = 20

    print(f"Judging responses from run: {run_id}")
    print(f"Topic: {topic_key}")
    print(f"Using judge: {judge_model_id}")
    print(f"Workers: {workers}")
    judge_responses(run_id, topic_key, judge_model_id, workers)
    print(f"Done! Results saved to .data/{topic_key}/{run_id}/judged_responses/")
