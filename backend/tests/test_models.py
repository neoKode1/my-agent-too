"""Tests for Pydantic models — conversation, template, mcp."""

from datetime import datetime, timezone

from app.models.conversation import (
    ChatRequest,
    ChatResponse,
    DeploymentTarget,
    ExtractedRequirements,
    FrameworkChoice,
    Message,
    Recommendation,
    Role,
    SessionStatus,
    WizardSession,
)


# ---------- Message ----------

def test_message_defaults():
    msg = Message(role=Role.USER, content="hello")
    assert msg.role == Role.USER
    assert msg.content == "hello"
    assert isinstance(msg.timestamp, datetime)
    assert msg.timestamp.tzinfo is not None  # timezone-aware


def test_message_roles():
    for role in Role:
        msg = Message(role=role, content="x")
        assert msg.role == role


# ---------- ExtractedRequirements ----------

def test_extracted_requirements_defaults():
    reqs = ExtractedRequirements()
    assert reqs.use_case is None
    assert reqs.integrations == []
    assert reqs.capabilities == []
    assert reqs.framework_preference is None
    assert reqs.deployment_preference is None


def test_extracted_requirements_populated():
    reqs = ExtractedRequirements(
        use_case="customer support",
        integrations=["slack", "github"],
        framework_preference=FrameworkChoice.CREWAI,
        deployment_preference=DeploymentTarget.CLOUD,
    )
    assert reqs.use_case == "customer support"
    assert len(reqs.integrations) == 2
    assert reqs.framework_preference == FrameworkChoice.CREWAI


# ---------- Recommendation ----------

def test_recommendation_creation():
    rec = Recommendation(
        framework=FrameworkChoice.LANGGRAPH,
        framework_reason="Best for this use case",
        deployment=DeploymentTarget.LOCAL,
        summary="A simple local agent",
    )
    assert rec.framework == FrameworkChoice.LANGGRAPH
    assert rec.agents == []
    assert rec.mcp_servers == []


# ---------- WizardSession ----------

def test_session_defaults():
    session = WizardSession()
    assert len(session.session_id) == 12
    assert session.status == SessionStatus.GATHERING
    assert session.messages == []
    assert session.recommendation is None
    assert session.created_at.tzinfo is not None


def test_session_unique_ids():
    s1 = WizardSession()
    s2 = WizardSession()
    assert s1.session_id != s2.session_id


# ---------- Enums ----------

def test_framework_choice_values():
    assert FrameworkChoice.LANGGRAPH.value == "langgraph"
    assert FrameworkChoice.RIG.value == "rig"
    assert FrameworkChoice.ADK_GO.value == "adk-go"
    assert len(FrameworkChoice) == 7


def test_session_status_values():
    assert SessionStatus.GATHERING.value == "gathering"
    assert SessionStatus.COMPLETE.value == "complete"
    assert len(SessionStatus) == 5


def test_deployment_target_values():
    assert DeploymentTarget.LOCAL.value == "local"
    assert DeploymentTarget.CLOUD.value == "cloud"
    assert DeploymentTarget.EXPORT.value == "export"


# ---------- API models ----------

def test_chat_request_new_session():
    req = ChatRequest(message="hi")
    assert req.session_id is None
    assert req.message == "hi"


def test_chat_request_existing_session():
    req = ChatRequest(session_id="abc123", message="hi")
    assert req.session_id == "abc123"


def test_chat_response():
    resp = ChatResponse(
        session_id="abc",
        reply="hello",
        status=SessionStatus.GATHERING,
    )
    assert resp.reply == "hello"
    assert resp.recommendation is None

