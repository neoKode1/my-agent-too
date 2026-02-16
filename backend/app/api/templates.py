"""Template API — browse templates and generate agent packages."""

from typing import List

from fastapi import APIRouter, HTTPException

from app.models.template import (
    AgentTemplate,
    GeneratedPackage,
    GenerateRequest,
)
from app.services.code_generator import generate_package
from app.services.template_registry import get_template, list_templates

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("", response_model=List[AgentTemplate])
async def get_templates():
    """List all available agent templates."""
    return list_templates()


@router.get("/{template_id}", response_model=AgentTemplate)
async def get_template_by_id(template_id: str):
    """Get a specific template by ID."""
    template = get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    return template


@router.post("/{template_id}/generate", response_model=GeneratedPackage)
async def generate_from_template(template_id: str, body: GenerateRequest):
    """Generate a deployable agent package from a template.

    The template_id in the path must match body.template_id.
    Returns the full generated package with all files.
    """
    if body.template_id != template_id:
        body.template_id = template_id  # path takes precedence

    template = get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")

    try:
        package = generate_package(body)
        return package
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Code generation failed: {exc}") from exc

