"""MCP server health checking and tool discovery.

Spawns MCP servers via subprocess (stdio transport), performs a handshake,
lists available tools, and reports health status. Uses asyncio subprocesses
so the backend stays non-blocking.
"""

import asyncio
import json
import time
from typing import Dict, List, Optional

from app.models.mcp import (
    MCPHealthResult,
    MCPServerEntry,
    MCPServerStatus,
    MCPToolSchema,
)
from app.services.mcp_registry import get_server, update_server_health


# ---------------------------------------------------------------------------
# Low-level MCP stdio transport helpers
# ---------------------------------------------------------------------------

_JSONRPC_INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "clientInfo": {"name": "my-agent-too-healthcheck", "version": "0.1.0"},
        "capabilities": {},
    },
}

_JSONRPC_LIST_TOOLS = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {},
}


def _jsonrpc_line(payload: dict) -> bytes:
    """Encode a JSON-RPC message for stdio transport (newline-delimited)."""
    return (json.dumps(payload) + "\n").encode()


async def _read_response(stdout: asyncio.StreamReader, timeout: float = 10.0) -> Optional[dict]:
    """Read a single JSON-RPC response line from stdout."""
    try:
        line = await asyncio.wait_for(stdout.readline(), timeout=timeout)
        if not line:
            return None
        return json.loads(line.decode().strip())
    except (asyncio.TimeoutError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def check_server_health(
    server_id: str,
    env_overrides: Optional[Dict[str, str]] = None,
    timeout: float = 15.0,
) -> MCPHealthResult:
    """Spawn an MCP server, perform handshake + list tools, return health result.

    If the server requires env vars that aren't supplied, it will likely fail
    to start — that's captured as UNHEALTHY with an error message.
    """
    import os

    entry = get_server(server_id)
    if not entry:
        return MCPHealthResult(
            server_id=server_id,
            status=MCPServerStatus.UNHEALTHY,
            error=f"Unknown server: {server_id}",
        )

    start = time.monotonic()
    env = {**os.environ}
    if env_overrides:
        env.update(env_overrides)

    try:
        proc = await asyncio.create_subprocess_exec(
            entry.command, *entry.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        # 1. Send initialize
        assert proc.stdin is not None and proc.stdout is not None
        proc.stdin.write(_jsonrpc_line(_JSONRPC_INIT))
        await proc.stdin.drain()

        init_resp = await _read_response(proc.stdout, timeout=timeout)
        if not init_resp or "result" not in init_resp:
            error_msg = f"Initialize failed: {init_resp}"
            _kill(proc)
            elapsed = (time.monotonic() - start) * 1000
            result = MCPHealthResult(
                server_id=server_id,
                status=MCPServerStatus.UNHEALTHY,
                error=error_msg,
                response_time_ms=elapsed,
            )
            update_server_health(server_id, MCPServerStatus.UNHEALTHY)
            return result

        # 2. Send initialized notification (required by spec)
        proc.stdin.write(_jsonrpc_line({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }))
        await proc.stdin.drain()

        # 3. List tools
        proc.stdin.write(_jsonrpc_line(_JSONRPC_LIST_TOOLS))
        await proc.stdin.drain()

        tools_resp = await _read_response(proc.stdout, timeout=timeout)
        tools: List[MCPToolSchema] = []
        if tools_resp and "result" in tools_resp:
            raw_tools = tools_resp["result"].get("tools", [])
            for t in raw_tools:
                tools.append(MCPToolSchema(
                    name=t.get("name", ""),
                    description=t.get("description", ""),
                    input_schema=t.get("inputSchema", {}),
                ))

        _kill(proc)
        elapsed = (time.monotonic() - start) * 1000

        update_server_health(server_id, MCPServerStatus.HEALTHY, tools)

        return MCPHealthResult(
            server_id=server_id,
            status=MCPServerStatus.HEALTHY,
            tools_count=len(tools),
            tools=tools,
            response_time_ms=elapsed,
        )

    except Exception as exc:
        elapsed = (time.monotonic() - start) * 1000
        update_server_health(server_id, MCPServerStatus.UNHEALTHY)
        return MCPHealthResult(
            server_id=server_id,
            status=MCPServerStatus.UNHEALTHY,
            error=str(exc),
            response_time_ms=elapsed,
        )


def _kill(proc: asyncio.subprocess.Process) -> None:
    """Best-effort kill of a subprocess."""
    try:
        proc.kill()
    except ProcessLookupError:
        pass

