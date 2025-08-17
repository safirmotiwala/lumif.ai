from typing import AsyncGenerator
from uuid import uuid4

from fastapi.responses import StreamingResponse
from agents.model import BuildAgent, BuildInputMessage, BuildRunnableConfig, ExecuteAgentInput, LLMConfig
from agents.service import build_agent, build_input_message, build_runnable_config, execute_agent
from chat.model import ChatInput, ChatResponse
from config import settings
from tools.service import load_tools_from_mcp_json
from utilities.logger import get_logger
from utilities.utils import langchain_to_chat_message

logger = get_logger(__name__)

async def chat_service(payload: ChatInput) -> ChatResponse:
    try:
        logger.info(f"Received chat payload: {payload}")
        
        thread_id = payload.thread_id or str(uuid4())
        run_id = uuid4()
        
        tools = await load_tools_from_mcp_json()
        
        agent = await build_agent(BuildAgent(
            name=settings.DEFAULT_AGENT_NAME,
            prompt=payload.prompt,
            tools=tools,
            llm_config=LLMConfig(
                model=payload.model,
                temperature=payload.temperature
            )
        ))
        
        config = build_runnable_config(BuildRunnableConfig(
            thread_id=thread_id,
            run_id=run_id,
            model=payload.model
        ))
        
        input = build_input_message(BuildInputMessage(
            query=payload.query
        ))
        
        output = await execute_agent(ExecuteAgentInput(
            agent=agent,
            input=input,
            config=config,
            mode="ainvoke"
        ))

        output = langchain_to_chat_message(output["messages"][-1])
        
        logger.info(f'Output : {output}')

        return ChatResponse(
            thread_id=thread_id,
            run_id=str(run_id),
            query=payload.query,
            reply=output.content,
        )
        
    except Exception as e:
        logger.error(f"Error in chat service: {e}")
        raise e
    
async def stream_chat_service(payload: ChatInput) -> ChatResponse:
    try:
        logger.info(f"Received chat payload: {payload}")
        
        thread_id = payload.thread_id or str(uuid4())
        run_id = uuid4()
        
        tools = await load_tools_from_mcp_json()
        
        agent = await build_agent(BuildAgent(
            name=settings.DEFAULT_AGENT_NAME,
            prompt=payload.prompt,
            tools=tools,
            llm_config=LLMConfig(
                model=payload.model,
                temperature=payload.temperature,
                streaming=payload.stream
            )
        ))
        
        config = build_runnable_config(BuildRunnableConfig(
            thread_id=thread_id,
            run_id=run_id,
            model=payload.model
        ))
        
        input = build_input_message(BuildInputMessage(
            query=payload.query
        ))
        
        async def stream_generator() -> AsyncGenerator[str, None]:
            # Await the astream() call to get the async iterator
            async for chunk in agent.astream(input=input, config=config):
                # Check for a specific key in the chunk
                # In a real LangGraph setup, you might check for "messages" or "output"
                # and extract the relevant text
                if "__end__" in chunk and "generator" in chunk["__end__"]:
                    # The generator node is the one producing the text, so we yield its output.
                    # The `chunk["__end__"]["generator"]` will be the text yielded from the node.
                    yield chunk["__end__"]["generator"]

        # Return a StreamingResponse with the async generator
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
        
        # output = await execute_agent(ExecuteAgentInput(
        #     agent=agent,
        #     input=input,
        #     config=config,
        #     mode="ainvoke"
        # ))

        # output = langchain_to_chat_message(output["messages"][-1])
        
        # logger.info(f'Output : {output}')

        # return ChatResponse(
        #     thread_id=thread_id,
        #     run_id=str(run_id),
        #     query=payload.query,
        #     reply=output.content,
        # )
        
    except Exception as e:
        logger.error(f"Error in chat service: {e}")
        raise e
    
# async def stream_chat_service(payload: ChatInput):
#     try:
#         logger.info(f"Received chat payload: {payload}")
        
#         thread_id = payload.thread_id or str(uuid4())
#         run_id = uuid4()
        
#         tools = await load_tools_from_mcp_json()
        
#         agent = await build_agent(BuildAgent(
#             name=settings.DEFAULT_AGENT_NAME,
#             prompt=payload.prompt,
#             tools=tools,
#             llm_config=LLMConfig(
#                 model=payload.model,
#                 temperature=payload.temperature,
#                 streaming=payload.stream
#             )
#         ))
        
#         config = build_runnable_config(BuildRunnableConfig(
#             thread_id=thread_id,
#             run_id=run_id,
#             model=payload.model
#         ))
        
#         input = build_input_message(BuildInputMessage(
#             query=payload.query
#         ))
        
#         # Process streamed events from the graph and yield messages over the SSE stream.
#         async for stream_event in agent.astream(
#             input=input, config=config, stream_mode=["updates", "messages", "custom"], subgraphs=True
#         ):
#             if not isinstance(stream_event, tuple):
#                 continue
#             # Handle different stream event structures based on subgraphs
#             if len(stream_event) == 3:
#                 # With subgraphs=True: (node_path, stream_mode, event)
#                 _, stream_mode, event = stream_event
#             else:
#                 # Without subgraphs: (stream_mode, event)
#                 stream_mode, event = stream_event
#             new_messages = []
#             if stream_mode == "updates":
#                 for node, updates in event.items():
#                     # A simple approach to handle agent interrupts.
#                     # In a more sophisticated implementation, we could add
#                     # some structured ChatMessage type to return the interrupt value.
#                     if node == "__interrupt__":
#                         interrupt: Interrupt
#                         for interrupt in updates:
#                             new_messages.append(AIMessage(content=interrupt.value))
#                         continue
#                     updates = updates or {}
#                     update_messages = updates.get("messages", [])
#                     # special cases for using langgraph-supervisor library
#                     if node == "supervisor":
#                         # Get only the last ToolMessage since is it added by the
#                         # langgraph lib and not actual AI output so it won't be an
#                         # independent event
#                         if isinstance(update_messages[-1], ToolMessage):
#                             update_messages = [update_messages[-1]]
#                         else:
#                             update_messages = []

#                     if node in ("research_expert", "math_expert"):
#                         update_messages = []
#                     new_messages.extend(update_messages)

#             if stream_mode == "custom":
#                 new_messages = [event]

#             # LangGraph streaming may emit tuples: (field_name, field_value)
#             # e.g. ('content', <str>), ('tool_calls', [ToolCall,...]), ('additional_kwargs', {...}), etc.
#             # We accumulate only supported fields into `parts` and skip unsupported metadata.
#             # More info at: https://langchain-ai.github.io/langgraph/cloud/how-tos/stream_messages/
#             processed_messages = []
#             current_message: dict[str, Any] = {}
#             for message in new_messages:
#                 if isinstance(message, tuple):
#                     key, value = message
#                     # Store parts in temporary dict
#                     current_message[key] = value
#                 else:
#                     # Add complete message if we have one in progress
#                     if current_message:
#                         processed_messages.append(_create_ai_message(current_message))
#                         current_message = {}
#                     processed_messages.append(message)

#             # Add any remaining message parts
#             if current_message:
#                 processed_messages.append(_create_ai_message(current_message))

#             for message in processed_messages:
#                 try:
#                     chat_message = langchain_to_chat_message(message)
#                     chat_message.run_id = str(run_id)
#                 except Exception as e:
#                     logger.error(f"Error parsing message: {e}")
#                     yield f"data: {json.dumps({'type': 'error', 'content': 'Unexpected error'})}\n\n"
#                     continue
#                 # LangGraph re-sends the input message, which feels weird, so drop it
#                 if chat_message.type == "human" and chat_message.content == payload.query:
#                     continue
#                 yield f"data: {json.dumps({'type': 'message', 'content': chat_message.model_dump()})}\n\n"

#             if stream_mode == "messages":
#                 if not payload.stream:
#                     continue
#                 msg, metadata = event
#                 if "skip_stream" in metadata.get("tags", []):
#                     continue
#                 # For some reason, astream("messages") causes non-LLM nodes to send extra messages.
#                 # Drop them.
#                 if not isinstance(msg, AIMessageChunk):
#                     continue
#                 content = remove_tool_calls(msg.content)
#                 if content:
#                     # Empty content in the context of OpenAI usually means
#                     # that the model is asking for a tool to be invoked.
#                     # So we only print non-empty content.
#                     yield f"data: {json.dumps({'type': 'token', 'content': convert_message_content_to_string(content)})}\n\n"
        
#     except Exception as e:
#         logger.error(f"Error in chat service: {e}")
#         raise e