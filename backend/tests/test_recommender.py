"""Tests for the rule-based recommendation engine."""

from app.models.conversation import (
    DeploymentTarget,
    ExtractedRequirements,
    FrameworkChoice,
    Recommendation,
)
from app.services.recommender import (
    build_recommendation,
    pick_deployment,
    pick_framework,
    resolve_integrations,
)


# ---------- pick_framework ----------

def test_pick_framework_respects_preference():
    reqs = ExtractedRequirements(framework_preference=FrameworkChoice.CREWAI)
    assert pick_framework(reqs) == FrameworkChoice.CREWAI


def test_pick_framework_keyword_crewai():
    reqs = ExtractedRequirements(use_case="customer support triage")
    assert pick_framework(reqs) == FrameworkChoice.CREWAI


def test_pick_framework_keyword_langgraph():
    reqs = ExtractedRequirements(use_case="research pipeline")
    assert pick_framework(reqs) == FrameworkChoice.LANGGRAPH


def test_pick_framework_keyword_rig():
    reqs = ExtractedRequirements(use_case="rust agent")
    assert pick_framework(reqs) == FrameworkChoice.RIG


def test_pick_framework_keyword_adk_go():
    reqs = ExtractedRequirements(use_case="golang microservice")
    assert pick_framework(reqs) == FrameworkChoice.ADK_GO


def test_pick_framework_default():
    reqs = ExtractedRequirements(use_case="something generic")
    assert pick_framework(reqs) == FrameworkChoice.LANGGRAPH


# ---------- pick_deployment ----------

def test_pick_deployment_respects_preference():
    reqs = ExtractedRequirements(deployment_preference=DeploymentTarget.LOCAL)
    assert pick_deployment(reqs) == DeploymentTarget.LOCAL


def test_pick_deployment_high_scale():
    reqs = ExtractedRequirements(scale="high")
    assert pick_deployment(reqs) == DeploymentTarget.CLOUD


def test_pick_deployment_default():
    reqs = ExtractedRequirements()
    assert pick_deployment(reqs) == DeploymentTarget.CLOUD


# ---------- resolve_integrations ----------

def test_resolve_known_integration():
    result = resolve_integrations(["slack"])
    assert len(result) == 1
    assert "name" in result[0]
    assert "command" in result[0]


def test_resolve_unknown_integration():
    result = resolve_integrations(["nonexistent_thing_xyz"])
    assert result == []


def test_resolve_deduplicates():
    result = resolve_integrations(["slack", "slack"])
    assert len(result) == 1


def test_resolve_multiple():
    result = resolve_integrations(["slack", "github", "postgres"])
    names = {r["name"] for r in result}
    assert len(names) == 3


# ---------- build_recommendation ----------

def test_build_recommendation_returns_recommendation():
    reqs = ExtractedRequirements(
        use_case="customer support",
        integrations=["slack"],
    )
    rec = build_recommendation(reqs)
    assert isinstance(rec, Recommendation)
    assert rec.framework == FrameworkChoice.CREWAI
    assert rec.deployment == DeploymentTarget.CLOUD
    assert len(rec.summary) > 0


def test_build_recommendation_with_framework_pref():
    reqs = ExtractedRequirements(
        use_case="anything",
        framework_preference=FrameworkChoice.VERCEL_AI,
    )
    rec = build_recommendation(reqs)
    assert rec.framework == FrameworkChoice.VERCEL_AI

