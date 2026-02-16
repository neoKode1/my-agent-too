"""MCP server management endpoints.

Provides:
  - Server registry browsing & search
  - Individual server detail + tool listing
  - Health checks (live spawn + handshake)
  - Per-project credential management
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.models.mcp import (
    MCPCategory,
    MCPHealthResult,
    MCPServerEntry,
    MCPServerListResponse,
    CredentialSetRequest,
)
from app.services.mcp_registry import (
    get_categories,
    get_server,
    list_servers,
    server_count,
)
from app.services.mcp_health import check_server_health
from app.services.credential_store import (
    delete_credentials,
    get_credential_summary,
    get_decrypted_env,
    set_credentials,
)

router = APIRouter(prefix="/mcp", tags=["mcp"])


# ---------------------------------------------------------------------------
# Server registry
# ---------------------------------------------------------------------------

@router.get("/servers", response_model=MCPServerListResponse)
async def get_servers(
    category: Optional[MCPCategory] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search name/description/tags"),
    official_only: bool = Query(False, description="Official MCP servers only"),
):
    """List all registered MCP servers with optional filters."""
    servers = list_servers(category=category, search=search, official_only=official_only)
    return MCPServerListResponse(
        servers=servers,
        total=len(servers),
        categories=get_categories(),
    )


@router.get("/servers/{server_id}", response_model=MCPServerEntry)
async def get_server_detail(server_id: str):
    """Get full details for a single MCP server."""
    entry = get_server(server_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"MCP server '{server_id}' not found")
    return entry


@router.get("/servers/{server_id}/tools")
async def get_server_tools(server_id: str):
    """Return cached tools for a server (from last health check)."""
    entry = get_server(server_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"MCP server '{server_id}' not found")
    return {
        "server_id": server_id,
        "tools": [t.model_dump() for t in entry.tools],
        "tools_count": len(entry.tools),
        "status": entry.status.value,
        "last_health_check": entry.last_health_check,
    }


@router.get("/categories")
async def get_mcp_categories():
    """List available MCP server categories."""
    return {"categories": get_categories(), "total_servers": server_count()}


# ---------------------------------------------------------------------------
# Health checks
# ---------------------------------------------------------------------------

@router.post("/servers/{server_id}/healthcheck", response_model=MCPHealthResult)
async def run_health_check(
    server_id: str,
    project_id: Optional[str] = Query(None, description="Project ID to use stored creds"),
):
    """Spawn the MCP server, perform handshake, list tools, report health.

    If project_id is provided, stored credentials for that project will be
    injected as environment variables.
    """
    entry = get_server(server_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"MCP server '{server_id}' not found")

    env_overrides: Optional[Dict[str, str]] = None
    if project_id:
        env_overrides = get_decrypted_env(project_id, server_id)

    result = await check_server_health(server_id, env_overrides=env_overrides)
    return result


# ---------------------------------------------------------------------------
# Credential management
# ---------------------------------------------------------------------------

@router.post("/credentials")
async def store_credentials(body: CredentialSetRequest):
    """Store encrypted credentials for a project + MCP server."""
    proj = set_credentials(body.project_id, body.server_id, body.credentials)
    return {
        "project_id": proj.project_id,
        "server_id": body.server_id,
        "keys_stored": list(body.credentials.keys()),
        "updated_at": proj.updated_at,
    }


@router.get("/credentials/{project_id}")
async def get_project_credentials(project_id: str):
    """List which credential keys are stored (no values returned)."""
    summary = get_credential_summary(project_id)
    return {"project_id": project_id, "servers": summary}


@router.delete("/credentials/{project_id}/{server_id}")
async def remove_credentials(project_id: str, server_id: str):
    """Remove stored credentials for a specific server in a project."""
    ok = delete_credentials(project_id, server_id)
    if not ok:
        raise HTTPException(status_code=404, detail="No credentials found")
    return {"deleted": True}

