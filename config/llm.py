from enum import StrEnum, auto
from typing import TypeAlias


class Provider(StrEnum):
    OPENAI = auto()
    AZURE_OPENAI = auto()
    DEEPSEEK = auto()
    ANTHROPIC = auto()
    GOOGLE = auto()
    GROQ = auto()
    AWS = auto()
    OLLAMA = auto()
    FAKE = auto()

class OpenAIModelName(StrEnum):
    """https://platform.openai.com/docs/models/gpt-4o"""

    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    GPT_41 = "gpt-4.1"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"
    GPT_45_PREVIEW = "gpt-4.5-preview"
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_NANO = "gpt-5-nano"

class AzureOpenAIModelName(StrEnum):
    """Azure OpenAI model names"""

    AZURE_GPT_4O = "azure-gpt-4o"
    AZURE_GPT_4O_MINI = "azure-gpt-4o-mini"

class DeepseekModelName(StrEnum):
    """https://api-docs.deepseek.com/quick_start/pricing"""

    DEEPSEEK_CHAT = "deepseek-chat"

class AnthropicModelName(StrEnum):
    """https://docs.anthropic.com/en/docs/about-claude/models#model-names"""

    HAIKU_3 = "claude-3-haiku"
    HAIKU_35 = "claude-3.5-haiku"
    SONNET_35 = "claude-3.5-sonnet"

class GoogleModelName(StrEnum):
    """https://ai.google.dev/gemini-api/docs/models/gemini"""

    GEMINI_15_FLASH = "gemini-1.5-flash"
    GEMINI_15_PRO = "gemini-1.5-pro"
    GEMINI_20_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_20_FLASH = "gemini-2.0-flash"
    GEMINI_25_FLASH_LITE = "gemini-2.5-flash-lite"
    GEMINI_25_FLASH = "gemini-2.5-flash"
    GEMINI_25_PRO = "gemini-2.5-pro"

class GroqModelName(StrEnum):
    """https://console.groq.com/docs/models"""

    LLAMA_31_8B = "groq-llama-3.1-8b"
    LLAMA_33_70B = "groq-llama-3.3-70b"

    LLAMA_GUARD_3_8B = "groq-llama-guard-3-8b"

class AWSModelName(StrEnum):
    """https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html"""

    BEDROCK_HAIKU = "bedrock-3.5-haiku"
    BEDROCK_SONNET = "bedrock-3.5-sonnet"

class OllamaModelName(StrEnum):
    """https://ollama.com/search"""

    OLLAMA_GENERIC = "ollama"

class FakeModelName(StrEnum):
    """Fake model for testing."""

    FAKE = "fake"

AllModelEnum: TypeAlias = (
    OpenAIModelName
    | AzureOpenAIModelName
    | DeepseekModelName
    | AnthropicModelName
    | GoogleModelName
    | GroqModelName
    | AWSModelName
    | FakeModelName
)

_MODEL_TABLE = {
    OpenAIModelName.GPT_4O_MINI: "gpt-4o-mini",
    OpenAIModelName.GPT_4O: "gpt-4o",
    OpenAIModelName.GPT_41: "gpt-4.1",
    OpenAIModelName.GPT_41_MINI: "gpt-4.1-mini",
    OpenAIModelName.GPT_41_NANO: "gpt-4.1-nano",
    OpenAIModelName.GPT_45_PREVIEW: "gpt-4.5-preview",
    OpenAIModelName.GPT_5: "gpt-5",
    OpenAIModelName.GPT_5_MINI: "gpt-5-mini",
    OpenAIModelName.GPT_5_NANO: "gpt-5-nano",
    DeepseekModelName.DEEPSEEK_CHAT: "deepseek-chat",
    AnthropicModelName.HAIKU_3: "claude-3-haiku-20240307",
    AnthropicModelName.HAIKU_35: "claude-3-5-haiku-latest",
    AnthropicModelName.SONNET_35: "claude-3-5-sonnet-latest",
    GoogleModelName.GEMINI_15_FLASH: "gemini-1.5-flash",
    GoogleModelName.GEMINI_15_PRO: "gemini-1.5-pro",
    GoogleModelName.GEMINI_20_FLASH_LITE: "gemini-2.0-flash-lite",
    GoogleModelName.GEMINI_20_FLASH: "gemini-2.0-flash",
    GoogleModelName.GEMINI_25_FLASH_LITE: "gemini-2.5-flash-lite",
    GoogleModelName.GEMINI_25_FLASH: "gemini-2.5-flash",
    GoogleModelName.GEMINI_25_PRO: "gemini-2.5-pro",
    GroqModelName.LLAMA_31_8B: "llama-3.1-8b-instant",
    GroqModelName.LLAMA_33_70B: "llama-3.3-70b-versatile",
    GroqModelName.LLAMA_GUARD_3_8B: "llama-guard-3-8b",
    AWSModelName.BEDROCK_HAIKU: "anthropic.claude-3-5-haiku-20241022-v1:0",
    AWSModelName.BEDROCK_SONNET: "anthropic.claude-3-5-sonnet-20240620-v1:0",
    OllamaModelName.OLLAMA_GENERIC: "ollama",
    FakeModelName.FAKE: "fake",
}