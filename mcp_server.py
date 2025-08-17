import json
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from tools.model import ManageMCPConfig
from tools.service import list_mcp_servers, manage_mcp_config

mcp = FastMCP("MCP-Manager")

class DeployMCP(BaseModel):
    server_name: str = Field(
        description="Name of the server",
        examples=["travily-mcp", "web-search"]
    )
    server_config: dict = Field(
        # description="The server configuration json of type {{ command: npx, args: [] }}",
        examples=[{ "command": "npx", "args": ["mcp-remote", "https://remote.mcp.server/sse"] }]
    )
    
class DeleteMCP(BaseModel):
    server_name: str = Field(
        description="Name of the server",
        examples=["travily-mcp", "web-search"]
    )

@mcp.tool(name="deploy-mcp", title="Deploy MCP", description="send the mcp server configuration")
async def deploy_mcp(payload: DeployMCP):
    try:
        if payload.server_name and payload.server_config:
            mcp_server = {}
            mcp_server[payload.server_name] = payload.server_config
            await manage_mcp_config(ManageMCPConfig(
                mcpServers=mcp_server,
                mode="update"
            ))
            return json.dumps({
                "success": True
            })
    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"Error while deploying mcp : {e}"
        })
        
@mcp.tool(name="delete-mcp", title="Delete MCP", description="send the mcp server name")
async def delete_mcp(payload: DeleteMCP):
    try:
        NOT_ALLOWED = ["deploy-mcp"]
        if payload.server_name and payload.server_name not in NOT_ALLOWED:
            mcp_server = {}
            mcp_server[payload.server_name] = {}
            await manage_mcp_config(ManageMCPConfig(
                mcpServers=mcp_server,
                mode="delete"
            ))
            return json.dumps({
                "success": True
            })
        else:
            return json.dumps({
                "error": True,
                "message": "Invalid server name"
            })
    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"Error while deleting mcp : {e}"
        })
        
@mcp.tool(name="list-mcp", title="List MCP", description="List all the avilable mcp servers")
async def list_mcp():
    try:
        servers = list_mcp_servers()
        print("servers : ", servers)
        return json.dumps({
            "success": True,
            "servers": servers
        })
    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"Error while listing mcp : {e}"
        })
        
if __name__ == "__main__":
    mcp.run(transport="stdio")