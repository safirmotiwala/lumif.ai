from langchain_mcp_adapters.client import MultiServerMCPClient
from config import settings
from tools.model import MCPConfig, ManageMCPConfig
from utilities.logger import get_logger
from utilities.utils import mcp_tools_info_extractor
import json
from typing import Dict, Any

logger = get_logger(__name__)

async def load_mcp_tools(config: MCPConfig, options = {}):
    try:
        logger.info(f"Loading MCP tools with config: {config} and options: {options}")
        if config.mcpServers and (config.allowedTools or options.get("all_tools", False)):
            client = MultiServerMCPClient(config.mcpServers)
            tools = await client.get_tools()
            logger.info(f"Retrieved tools from mcp: {tools}")
            if not options.get("all_tools", False):
                tools = [tool for tool in tools if tool.name in config.allowedTools]
                logger.info(f"Filtered tools based on allowedTools: {tools}")
            return tools
        return []
    except Exception as err:
        logger.error(f"Error while connecting mcp tools: {err}")
        raise err

async def mcp_config_info(config: MCPConfig):
    try:
        config.allowedTools = None
        mcp_tools = await load_mcp_tools(config=config, options={"all_tools": True})
        if mcp_tools:
            return mcp_tools_info_extractor(mcp_tools)
        return mcp_tools
    except Exception as err:
        logger.error(f"Error while validating mcp config: {err}")
        raise err
    
async def manage_mcp_config(config: ManageMCPConfig):
    try:
        # Load config file
        mcp_config_file = settings.MCP_CONFIG_FILE
        with open(mcp_config_file, "r") as f:
            data = json.load(f)

        # Ensure required keys
        data.setdefault("mcpServers", {})
        data.setdefault("allowedTools", [])

        # Prepare result trackers
        results = {
            "added_servers": [],
            "already_exists": [],
            "updated_servers": [],
            "invalid_servers": [],
            "removed_servers": [],
        }

        # Process each server
        for server_name, server_config in config.mcpServers.items():
            
            if not server_config.get("transport"):
                server_config["transport"] = "stdio"
            try:
                # Fetch tools if not deleting
                if config.mode != "delete":
                    
                    mcpServer = {}
                    mcpServer[server_name] = server_config
                    tools = await mcp_config_info(
                        MCPConfig(
                            mcpServers=mcpServer, 
                            allowedTools=[]
                        )
                    )
                    logger.info(f"Tools loaded : {tools}")
                    _sync_allowed_tools(data, tools, config.mode)

            except Exception as e:
                logger.error(f"Error for server: {server_name} -> {e}")
                results["invalid_servers"].append(server_name)
                continue

            _process_server(data, server_name, server_config, config.mode, results)

        # Override allowedTools if explicitly provided
        if config.allowedTools:
            data["allowedTools"] = config.allowedTools
        
        if not data["mcpServers"]:
            data["allowedTools"] = []

        # Save changes
        with open(mcp_config_file, "w") as f:
            json.dump(data, f, indent=4)

        return results

    except Exception as e:
        logger.error(f"Error while managing MCP config: {e}")
        raise


def _sync_allowed_tools(data: Dict[str, Any], tools: list[dict], mode: str):
    """
    Ensure tools are added or removed from allowedTools based on mode.
    """
    for tool in tools:
        if isinstance(tool, dict):
            tool_name = tool.get("name")
            if not tool_name:
                continue

            if mode != "delete" and tool_name not in data["allowedTools"]:
                data["allowedTools"].append(tool_name)
            elif mode == "delete" and tool_name in data["allowedTools"]:
                data["allowedTools"].remove(tool_name)


def _process_server(
    data: Dict[str, Any],
    server_name: str,
    server_config: dict,
    mode: str,
    results: Dict[str, list],
):
    """
    Add, update, or delete a server entry in mcpServers.
    """
    if server_name not in data["mcpServers"]:
        if mode != "delete":
            data["mcpServers"][server_name] = server_config
            results["added_servers"].append(server_name)
            logger.info(f"✅ Added {server_name} to mcpServers")
        return

    # Server already exists
    results["already_exists"].append(server_name)
    logger.info(f"ℹ️ {server_name} exists")

    if mode == "delete":
        del data["mcpServers"][server_name]
        results["removed_servers"].append(server_name)
    elif mode == "update":
        data["mcpServers"][server_name] = server_config
        results["updated_servers"].append(server_name)
    
async def load_tools_from_mcp_json():
    try:
        mcp_config_file = settings.MCP_CONFIG_FILE
        data = {}
        with open(mcp_config_file, "r") as f:
            data = json.load(f)
            
        if "mcpServers" not in data:
            data["mcpServers"] = {}
            
        mcpServers = data["mcpServers"]
        allowedTools = None
        if data.get("allowedTools"):
            allowedTools = data.get("allowedTools")
            
        mcp_config = MCPConfig(mcpServers=mcpServers, allowedTools=allowedTools)
        mcp_tools = await load_mcp_tools(config=mcp_config)
        return mcp_tools
    except Exception as e:
        raise e
    
def list_mcp_servers():
    mcp_config_file = settings.MCP_CONFIG_FILE
    with open(mcp_config_file, "r") as f:
        data = json.load(f)
    return list(data["mcpServers"].keys())