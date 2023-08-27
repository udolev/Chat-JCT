from enum import Enum
from typing import List, Literal

from pydantic import BaseModel, Field


class LlmEngine(str, Enum):
    '''Enum class to represent different llm engins'''
    OPEN_AI = 'openAI'


class QueryMessage(BaseModel):
    role: Literal['user', 'system', 'assistant']
    content: str = Field(max_length=100_000)


class Query(BaseModel):
    '''An object representing a query with its essential parameters'''
    temperature: float = Field(ge=0, le=1, default=0)
    llm_engine: LlmEngine = LlmEngine.OPEN_AI
    model: str = "gpt-3.5-turbo"
    context: List[QueryMessage] = []

    class Config:
        use_enum_values = True
