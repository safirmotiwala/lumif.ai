from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BUILD : str = "0.0.1"
    DEVELOPMENT: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    TITLE: str = "Lumif AI Backend"
    DESCRIPTION: str = "Lumif AI Backend powered by FASTAPI, PostgreSQL, MCP and Langgraph."
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    DEFAULT_AGENT_NAME: str = "lumif-ai"
    DEFAULT_MODEL: str = "gemini-2.5-flash"
    DEFAULT_TEMPERATURE: float = 0.5
    GRAPH_RECURSION_LIMIT: int = 40
    MCP_CONFIG_FILE: str = "./mcp.json"
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = "AIzaSyCeLhb-CAo1ONT6n6SdZ0OQczfr2UV-wWg"
    
settings = Settings()