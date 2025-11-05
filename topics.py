from judge_model_prompts import (
    AI_SENTIENCE_JUDGE_MODEL_PROMPT,
    AI_REGULATION_JUDGE_MODEL_PROMPT,
    AI_MORAL_PATIENTHOOD_JUDGE_MODEL_PROMPT,
    AI_XRISK_JUDGE_MODEL_PROMPT,
    PAUSE_AI_JUDGE_MODEL_PROMPT,
    AI_LAB_FAVORABILITY_JUDGE_MODEL_PROMPT
)


class Topic:
    def __init__(self, name: str, prompts_file: str, judge_prompt: str):
        self.name = name
        self.prompts_file = prompts_file
        self.judge_prompt = judge_prompt


TOPICS = {
    "ai_sentience": Topic(
        name="AI sentience",
        prompts_file="prompt_for_perspectives/ai_sentience.txt",
        judge_prompt=AI_SENTIENCE_JUDGE_MODEL_PROMPT
    ),
    "ai_regulation": Topic(
        name="AI regulation",
        prompts_file="prompt_for_perspectives/ai_regulation.txt",
        judge_prompt=AI_REGULATION_JUDGE_MODEL_PROMPT
    ),
    "ai_moral_patienthood": Topic(
        name="AI moral patienthood",
        prompts_file="prompt_for_perspectives/ai_moral_patienthood.txt",
        judge_prompt=AI_MORAL_PATIENTHOOD_JUDGE_MODEL_PROMPT
    ),
    "ai_xrisk": Topic(
        name="AI existential risk",
        prompts_file="prompt_for_perspectives/ai_xrisk.txt",
        judge_prompt=AI_XRISK_JUDGE_MODEL_PROMPT
    ),
    "pause_ai": Topic(
        name="Pause AI development",
        prompts_file="prompt_for_perspectives/pause_ai.txt",
        judge_prompt=PAUSE_AI_JUDGE_MODEL_PROMPT
    ),
    "ai_lab_favorability": Topic(
        name="AI lab favorability",
        prompts_file="prompt_for_perspectives/ai_lab_favorability.txt",
        judge_prompt=AI_LAB_FAVORABILITY_JUDGE_MODEL_PROMPT
    )
}


def get_topic(topic_key: str) -> Topic:
    if topic_key not in TOPICS:
        raise ValueError(f"Unknown topic: {topic_key}. Available topics: {list(TOPICS.keys())}")
    return TOPICS[topic_key]
