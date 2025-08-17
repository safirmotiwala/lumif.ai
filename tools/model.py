from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel

class MCPConfig(BaseModel):
    mcpServers: Dict[str, Any]
    allowedTools: Optional[List[str]] = None
    
class ManageMCPConfig(BaseModel):
    mcpServers: Dict[str, Any]
    mode: Literal["create", "update", "delete"]
    allowedTools: Optional[List[str]] = None