from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, validator
from evals.data_models.hashable import HashableBaseModel


class LLMParams(HashableBaseModel):
    model: Union[str, List[str]]
    temperature: float = 0.2
    top_p: float = 1.0
    n: int = 1
    num_candidates_per_completion: int = 1
    insufficient_valids_behaviour: Literal["error", "continue", "pad_invalids"] = "error"
    max_tokens: Optional[int] = None
    logprobs: Optional[int] = None


class StopReason(Enum):
    MAX_TOKENS = "max_tokens"
    STOP_SEQUENCE = "stop_sequence"

    def __str__(self):
        return self.value


class LLMResponse(BaseModel):
    model_id: str
    completion: str
    stop_reason: StopReason
    cost: float
    duration: Optional[float] = None
    api_duration: Optional[float] = None
    logprobs: Optional[List[dict[str, float]]] = None

    @validator("stop_reason", pre=True)
    def parse_stop_reason(cls, v):
        if v in ["length", "max_tokens"]:
            return StopReason.MAX_TOKENS
        elif v in ["stop", "stop_sequence"]:
            return StopReason.STOP_SEQUENCE
        raise ValueError(f"Invalid stop reason: {v}")

    def to_dict(self):
        return {**self.dict(), "stop_reason": str(self.stop_reason)}
