"""My-Agent-Too — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agents, health, mcp, templates, wizard
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Agent-as-a-Service platform with MCP integration",
)

# CORS — permissive for local dev; tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(health.router)
app.include_router(agents.router, prefix="/api/v1")
app.include_router(mcp.router, prefix="/api/v1")
app.include_router(wizard.router, prefix="/api/v1")
app.include_router(templates.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }

