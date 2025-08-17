from fastapi import APIRouter
from tools.service import manage_mcp_config

router = APIRouter(
    prefix="/tools",
    tags=["MCP"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

router.post("/mcp/", responses={403: {"description": "Operation forbidden"}})(manage_mcp_config)