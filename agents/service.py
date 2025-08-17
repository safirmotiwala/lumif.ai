from langgraph.prebuilt import create_react_agent
from agents.model import BuildAgent, BuildInputMessage, BuildRunnableConfig, ExecuteAgentInput
from config import settings
from utilities.logger import get_logger
from utilities.model import get_model
from utilities.utils import agent_name_formatter
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

logger = get_logger(__name__)
checkpointer = InMemorySaver()

async def build_agent(payload: BuildAgent) -> CompiledStateGraph:
    try:
        model = get_model(payload.llm_config)
        agent = create_react_agent(
            model,
            tools=payload.tools,
            prompt=payload.prompt,
            name=agent_name_formatter(payload.name, "reAct"),
            checkpointer=checkpointer
        )
        
        return agent
    except Exception as e:
        logger.error(f"Error building agent: {e}")
        raise e
    
def build_runnable_config(payload: BuildRunnableConfig) -> RunnableConfig:
    try:
        configurable = {
            "thread_id": payload.thread_id,
            "model": payload.model
        }
        
        return RunnableConfig(
            configurable=configurable,
            run_id=payload.run_id,
            recursion_limit=settings.GRAPH_RECURSION_LIMIT
        )
    except Exception as e:
        logger.error(f"Error building runnable config: {e}")
        raise e
    
def build_input_message(payload: BuildInputMessage) -> dict:
    content = [
        {"type": "text", "text": payload.query},
    ]
    
    return {
        "messages": [HumanMessage(content=content, additional_kwargs={})]
    }
    
async def execute_agent(payload: ExecuteAgentInput) -> list[AIMessage]:
    try:
        agent = payload.agent
        input = payload.input
        config = payload.config
        if payload.mode == "invoke":
            response = agent.invoke(input=input, config=config)
        elif payload.mode == "ainvoke":
            response = await agent.ainvoke(input=input, config=config)
            
        return response
    except Exception as e:
        logger.error(f"Error executing agent : {e}")
        raise e