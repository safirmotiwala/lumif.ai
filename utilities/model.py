from functools import cache
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from agents.model import LLMConfig
from config import settings
from .utils import remove_empty_values_from_object
from config.llm import (
    GoogleModelName,
    OpenAIModelName,
    _MODEL_TABLE
)

from .logger import get_logger
logger = get_logger(__name__)

ModelT: Any = (
    ChatOpenAI | ChatGoogleGenerativeAI
)

def get_llm_model_name(config: LLMConfig):
    model_name = config.model
    api_model_name = _MODEL_TABLE.get(model_name)
    if not api_model_name:
        raise ValueError(f"Unsupported model: {model_name}")
    return api_model_name

def get_llm_provider(model_name: str) -> str:
    """
    Identify the provider based on the model name.
    """
    if model_name in OpenAIModelName:
        return "OpenAI"
    elif model_name in GoogleModelName:
        return "Google"
    else:
        raise ValueError(f"Unsupported model: {model_name}")

@cache
def get_model(config: LLMConfig, /) -> ModelT:

    model_name = get_llm_model_name(config)
    config_dict = config.model_dump()
    config_dict["model"] = model_name

    if config.streaming:
        config_dict["stream"] = True
        config_dict["streaming"] = True
        config_dict["stream_options"] = {"include_usage": True}

    config_dict = remove_empty_values_from_object(config_dict)

    logger.info(f">>> ### >> Using model: {model_name} with config: {config_dict}")

    model_provider = get_llm_provider(model_name)

    if model_provider == "OpenAI":
        return ChatOpenAI(**config_dict)

    elif model_provider == "Google":
        return ChatGoogleGenerativeAI(**config_dict, api_key=settings.GOOGLE_API_KEY)