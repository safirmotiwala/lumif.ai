from typing import Any, Literal, Optional
from uuid import UUID
from pydantic import BaseModel
from pydantic import (
    Field,
    root_validator,
)

class LLMConfig(BaseModel):

    model: Optional[str] = Field(
        title="Model",
        default=None,
        description="Model to use (e.g., 'gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo')."
    )

    temperature: Optional[float] = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Controls randomness: 0.0 (deterministic) to 1.0 (creative)."
    )

    top_p: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Limits token sampling to top cumulative probability (nucleus sampling)."
    )

    frequency_penalty: Optional[float] = Field(
        default=None,
        ge=-2.0,
        le=2.0,
        description="Penalizes token frequency to reduce repetition."
    )

    presence_penalty: Optional[float] = Field(
        default=None,
        ge=-2.0,
        le=2.0,
        description="Penalizes tokens that already appear to encourage new topics."
    )

    max_tokens: Optional[int] = Field(
        default=None,
        gt=0,
        description="Maximum number of tokens to generate."
    )

    stop_sequences: Optional[list[str]] = Field(
        default=None,
        description="List of sequences where generation will stop."
    )

    n: Optional[int] = Field(
        default=None,
        gt=0,
        description="Number of completions to generate per prompt."
    )

    streaming: Optional[bool] = Field(
        default=False,
        description="Whether to stream tokens as they are generated."
    )

    class Config:
        frozen=True

    @root_validator(pre=True)
    def validate_response_tuning(cls, values):
        """Check that the temperature, top_p, and top_k values are within their acceptable ranges."""
        # Extract values
        temperature = values.get('temperature')
        top_p = values.get('top_p')
        top_k = values.get('top_k')

        # Validate temperature
        if temperature is not None and not (0.0 <= temperature <= 1.0):
            raise ValueError('temperature must be between 0 and 1')

        # Validate top_p
        if top_p is not None and not (0.0 <= top_p <= 1.0):
            raise ValueError('top_p must be between 0 and 1')

        # Validate top_k
        if top_k is not None and not (1 <= top_k <= 100):
            raise ValueError('top_k must be between 1 and 100')

        return values

class BuildAgent(BaseModel):
    name: str
    prompt: str = None
    tools: Optional[list] = []
    llm_config: LLMConfig = LLMConfig()
    
class BuildRunnableConfig(BaseModel):
    thread_id: str = None
    run_id: UUID
    model: str
    
class BuildInputMessage(BaseModel):
    query: str
    
class ExecuteAgentInput(BaseModel):
    agent: Any
    mode: Literal["invoke", "ainvoke", "astream"]
    input: dict
    config: Any