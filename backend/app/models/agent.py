"""Pydantic models for agent data flowing through My-Agent-Too."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Request models ----------

class AgentCreateRequest(BaseModel):
    """Payload sent by the frontend to create / register an agent."""

    agent_id: str = Field(..., description="Unique agent identifier")
    name: str = Field(..., description="Human-friendly agent name")
    agent_url: str = Field(..., description="URL where the agent code / repo lives")
    api_url: str = Field(..., description="Runtime API endpoint for the agent")
    capabilities: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    framework: Optional[str] = Field(None, description="Agent framework: langgraph, crewai, autogen, semantic-kernel")
    mcp_servers: List[str] = Field(default_factory=list, description="MCP servers this agent uses")
    deployment_type: Optional[str] = Field(None, description="local | cloud | export")


class AgentStatusUpdate(BaseModel):
    """Partial update for an agent's runtime status."""

    alive: Optional[bool] = None
    assigned_to: Optional[str] = None
    capabilities: Optional[List[str]] = None
    tags: Optional[List[str]] = None


# ---------- Response models ----------

class AgentResponse(BaseModel):
    """Agent data as returned by NANDA Index."""

    agent_id: str
    agent_url: Optional[str] = None
    api_url: Optional[str] = None
    alive: bool = False
    assigned_to: Optional[str] = None
    last_update: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class RegistrationResult(BaseModel):
    """Result after registering an agent."""

    status: str
    message: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    nanda_connected: bool

