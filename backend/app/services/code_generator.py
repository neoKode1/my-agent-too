"""Code generation engine — renders agent templates into deployable packages.

Uses Jinja2 templates to produce framework-specific Python code, Docker configs,
environment files, and setup instructions.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.models.conversation import DeploymentTarget, FrameworkChoice
from app.models.template import (
    AgentRole,
    AgentTemplate,
    GeneratedFile,
    GeneratedPackage,
    GenerateRequest,
    MCPServerConfig,
)
from app.services.template_registry import get_template

logger = logging.getLogger(__name__)

# Jinja2 environment — looks for *.j2 files in app/templates/
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_jinja_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape([]),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def _render(template_name: str, ctx: Dict[str, Any]) -> str:
    """Render a Jinja2 template with the given context."""
    tmpl = _jinja_env.get_template(template_name)
    return tmpl.render(**ctx)


def _build_context(
    template: AgentTemplate,
    req: GenerateRequest,
) -> Dict[str, Any]:
    """Build the Jinja2 rendering context from template + request."""
    agents = req.agents if req.agents else template.agents
    mcp_servers = req.mcp_servers if req.mcp_servers else template.mcp_servers
    return {
        "project_name": req.project_name,
        "framework": template.framework.value,
        "deployment": req.deployment.value,
        "category": template.category.value,
        "template_name": template.name,
        "template_description": template.description,
        "agents": [a.model_dump() for a in agents],
        "mcp_servers": [s.model_dump() for s in mcp_servers],
        "config": req.config,
        "env_vars": _collect_env_vars(mcp_servers),
    }


def _collect_env_vars(servers: List[MCPServerConfig]) -> List[str]:
    """Collect all required env vars across MCP servers."""
    env_vars = ["ANTHROPIC_API_KEY"]
    seen = set(env_vars)
    for s in servers:
        for var in s.required_env:
            if var not in seen:
                env_vars.append(var)
                seen.add(var)
    return env_vars


def generate_package(req: GenerateRequest) -> GeneratedPackage:
    """Generate a full agent package from a template + configuration.

    Returns a GeneratedPackage with all files ready to download or deploy.
    """
    template = get_template(req.template_id)
    if not template:
        raise ValueError(f"Template '{req.template_id}' not found")

    ctx = _build_context(template, req)
    files: List[GeneratedFile] = []

    # 1. Main agent code — framework-specific
    framework_template = f"{template.framework.value}_agent.py.j2"
    try:
        agent_code = _render(framework_template, ctx)
        files.append(GeneratedFile(path="agent.py", content=agent_code, language="python"))
    except Exception as exc:
        logger.warning("No template for %s: %s", framework_template, exc)

    # 2. Requirements file
    files.append(GeneratedFile(
        path="requirements.txt",
        content=_render("requirements.txt.j2", ctx),
        language="text",
    ))

    # 3. Dockerfile
    files.append(GeneratedFile(
        path="Dockerfile",
        content=_render("Dockerfile.j2", ctx),
        language="dockerfile",
    ))

    # 4. docker-compose.yml
    files.append(GeneratedFile(
        path="docker-compose.yml",
        content=_render("docker_compose.yml.j2", ctx),
        language="yaml",
    ))

    # 5. .env.example
    files.append(GeneratedFile(
        path=".env.example",
        content=_render("env_example.j2", ctx),
        language="text",
    ))

    # 6. MCP config
    files.append(GeneratedFile(
        path="mcp-config.json",
        content=_render("mcp_config.json.j2", ctx),
        language="json",
    ))

    # 7. README
    files.append(GeneratedFile(
        path="README.md",
        content=_render("readme.md.j2", ctx),
        language="markdown",
    ))

    # Build setup instructions
    setup = [
        "cp .env.example .env",
        "Fill in the required environment variables in .env",
        "pip install -r requirements.txt",
        "python agent.py",
    ]
    if req.deployment == DeploymentTarget.LOCAL:
        setup = ["docker compose up --build"] + setup

    return GeneratedPackage(
        project_name=req.project_name,
        template_id=req.template_id,
        framework=template.framework,
        deployment=req.deployment,
        files=files,
        summary=f"Generated {template.name} using {template.framework.value} with {len(ctx['mcp_servers'])} MCP integration(s).",
        setup_instructions=setup,
        env_vars=ctx["env_vars"],
    )

