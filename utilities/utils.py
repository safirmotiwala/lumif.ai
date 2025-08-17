import inspect
import re
from typing import Any
from .logger import get_logger
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.messages import (
    ChatMessage as LangchainChatMessage,
)
from chat.model import ChatMessage
from fastapi import status

logger = get_logger(__name__)

def remove_empty_values_from_object(data):
    cleaned_data = {k: v for k, v in data.items() if v is not None}
    return cleaned_data

def replace_nonalphanumeric(input_string, replacement='_'):
    # Replace all non-alphanumeric characters with replacement string or an underscore
    try:
        return re.sub(r'\W+', replacement, input_string)
    except Exception as err:
        logger.error(f"Error while replacing non-alphanumeric characters {err}")
        return input_string

def agent_name_formatter(agent_name: str, agent_id: str) -> str:
    """
    Format the agent name to ensure it is unique and does not exceed a certain length.
    """
    try:
        agent_name_max_length = 50
        agent_id_max_length = 4
        formatted_name = f"{replace_nonalphanumeric(agent_name, '_')}_{str(agent_id)[-agent_id_max_length:]}"
        return formatted_name[:agent_name_max_length]
    except Exception as err:
        logger.error(f"Error while formatting agent name: {err}")
        return agent_name
    
def convert_message_content_to_string(content: str | list[str | dict]) -> str:
    try:
        if isinstance(content, str):
            return content

        text: list[str] = []
        for content_item in content:
            if isinstance(content_item, str):
                text.append(content_item)
                continue
            if content_item["type"] == "text":
                text.append(content_item["text"])
    except Exception as err:
        logger.error(f"Error while converting message content to string: {err}")

    return "".join(text)

def langchain_to_chat_message(message: BaseMessage) -> ChatMessage:
    """Create a ChatMessage from a LangChain message."""
    try:
        match message:
            case HumanMessage():
                human_message = ChatMessage(
                    type="human",
                    content=convert_message_content_to_string(message.content),
                )
                return human_message
            case AIMessage():
                ai_message = ChatMessage(
                    type="ai",
                    content=convert_message_content_to_string(message.content),
                )
                if message.tool_calls:
                    ai_message.tool_calls = message.tool_calls
                if message.response_metadata:
                    ai_message.response_metadata = message.response_metadata
                if message.usage_metadata:
                    ai_message.usage_metadata = message.usage_metadata
                return ai_message
            case SystemMessage():
                ai_message = ChatMessage(
                    type="ai",
                    content=convert_message_content_to_string(message.content),
                )
                return ai_message
            case ToolMessage():
                tool_message = ChatMessage(
                    type="tool",
                    content=convert_message_content_to_string(message.content),
                    tool_call_id=message.tool_call_id,
                )
                return tool_message
            case LangchainChatMessage():
                if message.role == "custom":
                    custom_message = ChatMessage(
                        type="custom",
                        content="",
                        custom_data=message.content[0],
                    )
                    return custom_message
                else:
                    raise ValueError(f"Unsupported chat message role: {message.role}")
            case _:
                raise ValueError(f"Unsupported message type: {message.__class__.__name__}")
    except Exception as err:
        logger.error(f"Error while creating ChatMessage from LangChain message: {err}")
        return None
    
def remove_tool_calls(content: str | list[str | dict]) -> str | list[str | dict]:
    """Remove tool calls from content."""
    if isinstance(content, str):
        return content

    # Currently only Anthropic models stream tool calls, using content item type tool_use.
    return [
        content_item
        for content_item in content
        if isinstance(content_item, str) or content_item["type"] != "tool_use"
    ]
    
def mcp_tools_info_extractor(mcp_tools: list = []):
    """
    Extracts MCP tool information from a list of MCP tools.
    """
    try:
        if not mcp_tools:
            return []

        tools_info = []
        for tool in mcp_tools:
            tools_info.append({
                "name": tool.name,
                "description": tool.description,
                "args_schema": tool.args_schema
            })
        return tools_info
    except Exception as err:
        logger.error(f"Error while extracting MCP tools info: {err}")
        return []
    
def _create_ai_message(parts: dict) -> AIMessage:
    sig = inspect.signature(AIMessage)
    valid_keys = set(sig.parameters)
    filtered = {k: v for k, v in parts.items() if k in valid_keys}
    return AIMessage(**filtered)
    
def sse_response_example() -> dict[int, Any]:
    return {
        status.HTTP_200_OK: {
            "description": "Server Sent Event Response",
            "content": {
                "text/event-stream": {
                    "example": "data: {'type': 'token', 'content': 'Hello'}\n\ndata: {'type': 'token', 'content': ' World'}\n\ndata: [DONE]\n\n",
                    "schema": {"type": "string"},
                }
            },
        }
    }