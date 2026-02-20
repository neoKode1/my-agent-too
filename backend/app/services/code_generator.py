"""Code generation engine — renders agent templates into deployable packages.

Uses Jinja2 templates to produce framework-specific Python or TypeScript code,
Docker configs, cloud deployment configs, environment files, and setup
instructions.  Supports Python frameworks (LangGraph, CrewAI, AutoGen,
Semantic Kernel) and TypeScript frameworks (Vercel AI SDK).
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


# Frameworks that produce TypeScript instead of Python
_TS_FRAMEWORKS = {FrameworkChoice.VERCEL_AI}


def _is_typescript(framework: FrameworkChoice) -> bool:
    """Return True if the framework targets TypeScript/Node.js."""
    return framework in _TS_FRAMEWORKS


def _generate_agent_code(
    template: AgentTemplate,
    ctx: Dict[str, Any],
    files: List[GeneratedFile],
) -> None:
    """Generate the main agent source file (Python or TypeScript)."""
    fw = template.framework
    if _is_typescript(fw):
        tmpl_name = f"{fw.value.replace('-', '_')}_agent.ts.j2"
        out_path, lang = "agent.ts", "typescript"
    else:
        tmpl_name = f"{fw.value.replace('-', '_')}_agent.py.j2"
        out_path, lang = "agent.py", "python"
    try:
        code = _render(tmpl_name, ctx)
        files.append(GeneratedFile(path=out_path, content=code, language=lang))
    except Exception as exc:
        logger.warning("No agent template for %s: %s", tmpl_name, exc)


def _generate_deps(
    template: AgentTemplate,
    ctx: Dict[str, Any],
    files: List[GeneratedFile],
) -> None:
    """Generate dependency manifest (requirements.txt or package.json + tsconfig)."""
    if _is_typescript(template.framework):
        files.append(GeneratedFile(
            path="package.json",
            content=_render("package_json.j2", ctx),
            language="json",
        ))
        files.append(GeneratedFile(
            path="tsconfig.json",
            content=_render("tsconfig_json.j2", ctx),
            language="json",
        ))
    else:
        files.append(GeneratedFile(
            path="requirements.txt",
            content=_render("requirements.txt.j2", ctx),
            language="text",
        ))


def _generate_docker(
    template: AgentTemplate,
    ctx: Dict[str, Any],
    files: List[GeneratedFile],
) -> None:
    """Generate Dockerfile + docker-compose.yml (Python or Node variant)."""
    if _is_typescript(template.framework):
        dockerfile_tmpl = "Dockerfile_node.j2"
    else:
        dockerfile_tmpl = "Dockerfile.j2"
    files.append(GeneratedFile(
        path="Dockerfile",
        content=_render(dockerfile_tmpl, ctx),
        language="dockerfile",
    ))
    files.append(GeneratedFile(
        path="docker-compose.yml",
        content=_render("docker_compose.yml.j2", ctx),
        language="yaml",
    ))


def _generate_deploy_configs(
    deployment: DeploymentTarget,
    ctx: Dict[str, Any],
    files: List[GeneratedFile],
) -> None:
    """Generate cloud deployment configs when deployment != LOCAL."""
    if deployment in (DeploymentTarget.CLOUD, DeploymentTarget.EXPORT):
        try:
            files.append(GeneratedFile(
                path="railway.toml",
                content=_render("railway_toml.j2", ctx),
                language="toml",
            ))
        except Exception as exc:
            logger.warning("Could not render railway.toml: %s", exc)
        try:
            files.append(GeneratedFile(
                path="render.yaml",
                content=_render("render_yaml.j2", ctx),
                language="yaml",
            ))
        except Exception as exc:
            logger.warning("Could not render render.yaml: %s", exc)
        try:
            files.append(GeneratedFile(
                path="vercel.json",
                content=_render("vercel_json.j2", ctx),
                language="json",
            ))
        except Exception as exc:
            logger.warning("Could not render vercel.json: %s", exc)


def generate_package(req: GenerateRequest) -> GeneratedPackage:
    """Generate a full agent package from a template + configuration.

    Returns a GeneratedPackage with all files ready to download or deploy.
    Generates Python packages for LangGraph/CrewAI/AutoGen/Semantic Kernel,
    and TypeScript packages for Vercel AI SDK.  Cloud deployments include
    Railway, Render, and Vercel configs.
    """
    template = get_template(req.template_id)
    if not template:
        raise ValueError(f"Template '{req.template_id}' not found")

    ctx = _build_context(template, req)
    files: List[GeneratedFile] = []
    is_ts = _is_typescript(template.framework)

    # 1. Main agent code — framework-specific (Python or TypeScript)
    _generate_agent_code(template, ctx, files)

    # 2. Dependencies (requirements.txt or package.json + tsconfig.json)
    _generate_deps(template, ctx, files)

    # 3. Dockerfile + docker-compose.yml
    _generate_docker(template, ctx, files)

    # 4. .env.example
    files.append(GeneratedFile(
        path=".env.example",
        content=_render("env_example.j2", ctx),
        language="text",
    ))

    # 5. MCP config
    files.append(GeneratedFile(
        path="mcp-config.json",
        content=_render("mcp_config.json.j2", ctx),
        language="json",
    ))

    # 6. Cloud deployment configs (Railway, Render, Vercel) — when not LOCAL
    _generate_deploy_configs(req.deployment, ctx, files)

    # 7. README
    files.append(GeneratedFile(
        path="README.md",
        content=_render("readme.md.j2", ctx),
        language="markdown",
    ))

    # Build setup instructions — language-aware
    if is_ts:
        setup = [
            "cp .env.example .env",
            "Fill in the required environment variables in .env",
            "npm install",
            "npx tsx agent.ts",
        ]
    else:
        setup = [
            "cp .env.example .env",
            "Fill in the required environment variables in .env",
            "pip install -r requirements.txt",
            "python agent.py",
        ]
    if req.deployment == DeploymentTarget.LOCAL:
        setup = ["docker compose up --build"] + setup

    lang_label = "TypeScript (Vercel AI SDK)" if is_ts else template.framework.value
    return GeneratedPackage(
        project_name=req.project_name,
        template_id=req.template_id,
        framework=template.framework,
        deployment=req.deployment,
        files=files,
        summary=f"Generated {template.name} using {lang_label} with {len(ctx['mcp_servers'])} MCP integration(s).",
        setup_instructions=setup,
        env_vars=ctx["env_vars"],
    )

