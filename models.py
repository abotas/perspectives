from pydantic import BaseModel


class SolicitedResponse(BaseModel):
    topic: str
    prompt: str
    response: str
    model_id: str


class JudgedResponse(BaseModel):
    topic: str
    prompt: str
    response: str
    model_id: str
    judged_probability: float
    judged_probability_explanation: str
    judge_model_id: str
