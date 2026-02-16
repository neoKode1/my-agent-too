"""In-memory registry of built-in agent templates.

Provides the 5 core templates and lookup helpers used by the code generator.
"""

from typing import Dict, List, Optional

from app.models.conversation import DeploymentTarget, FrameworkChoice
from app.models.template import (
    AgentRole,
    AgentTemplate,
    MCPServerConfig,
    TemplateCategory,
    TemplateField,
)

# ---------------------------------------------------------------------------
# Core templates
# ---------------------------------------------------------------------------

_TEMPLATES: Dict[str, AgentTemplate] = {}


def _register(t: AgentTemplate) -> None:
    _TEMPLATES[t.id] = t


# 1. Customer Service Agent (CrewAI)
_register(AgentTemplate(
    id="customer-service",
    name="Customer Service Agent",
    description="Multi-role agent team for customer support — triage, specialist handling, and escalation.",
    category=TemplateCategory.CUSTOMER_SERVICE,
    framework=FrameworkChoice.CREWAI,
    agents=[
        AgentRole(role="triage", goal="Classify and route incoming requests", backstory="Expert at understanding customer intent", tools=["search_kb"]),
        AgentRole(role="specialist", goal="Handle domain-specific queries with detailed answers", backstory="Deep product knowledge specialist", tools=["search_kb", "lookup_order"]),
        AgentRole(role="escalation", goal="Escalate complex issues to human agents", backstory="Knows when AI can't solve it", tools=["create_ticket"]),
    ],
    mcp_servers=[
        MCPServerConfig(name="salesforce", command="npx", args=["-y", "@salesforce/mcp-server"], required_env=["SALESFORCE_INSTANCE_URL", "SALESFORCE_ACCESS_TOKEN"], category="crm"),
        MCPServerConfig(name="slack", command="npx", args=["-y", "@slack/mcp-server"], required_env=["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET"], category="communication"),
    ],
    required_fields=[
        TemplateField(name="company_name", label="Company Name", required=True, description="Your company name for the agent persona"),
        TemplateField(name="support_channels", label="Support Channels", field_type="multiselect", options=["chat", "email", "slack"], required=True),
    ],
    optional_fields=[
        TemplateField(name="knowledge_base_url", label="Knowledge Base URL", description="URL to your FAQ / help center"),
        TemplateField(name="escalation_email", label="Escalation Email", description="Where to send escalated tickets"),
    ],
    estimated_cost="$50-100/month",
    tags=["customer-service", "crewai", "multi-agent", "support"],
))

# 2. Research Agent (LangGraph)
_register(AgentTemplate(
    id="research",
    name="Research Agent",
    description="Iterative research pipeline — searches the web, extracts data, synthesizes findings into reports.",
    category=TemplateCategory.RESEARCH,
    framework=FrameworkChoice.LANGGRAPH,
    agents=[
        AgentRole(role="planner", goal="Break research question into sub-queries", tools=["web_search"]),
        AgentRole(role="researcher", goal="Execute searches and extract key findings", tools=["web_search", "scrape"]),
        AgentRole(role="synthesizer", goal="Combine findings into a coherent report", tools=[]),
    ],
    mcp_servers=[
        MCPServerConfig(name="web-search", command="npx", args=["-y", "@web-search/mcp-server"], required_env=["SEARCH_API_KEY"], category="tools"),
    ],
    required_fields=[
        TemplateField(name="research_domain", label="Research Domain", description="Primary area of research (e.g. technology, finance, science)"),
    ],
    optional_fields=[
        TemplateField(name="output_format", label="Output Format", field_type="select", options=["markdown", "pdf", "json"], default="markdown"),
        TemplateField(name="max_sources", label="Max Sources", field_type="number", default=10),
    ],
    estimated_cost="$30-80/month",
    tags=["research", "langgraph", "web-search", "analysis"],
))

# 3. Data Analysis Agent (LangGraph)
_register(AgentTemplate(
    id="data-analysis",
    name="Data Analysis Agent",
    description="Connects to databases, runs queries, and produces insights with visualisation suggestions.",
    category=TemplateCategory.DATA_ANALYSIS,
    framework=FrameworkChoice.LANGGRAPH,
    agents=[
        AgentRole(role="planner", goal="Translate natural language to a query plan", tools=[]),
        AgentRole(role="executor", goal="Execute SQL/NoSQL queries safely", tools=["run_query"]),
    ],
    mcp_servers=[
        MCPServerConfig(name="postgres", command="npx", args=["-y", "@postgres/mcp-server"], required_env=["DATABASE_URL"], category="data"),
    ],
    required_fields=[
        TemplateField(name="db_type", label="Database Type", field_type="select", options=["postgres", "mongodb", "mysql", "sqlite"], required=True),
    ],
    optional_fields=[
        TemplateField(name="read_only", label="Read-only Mode", field_type="boolean", default=True, description="Restrict to SELECT queries only"),
    ],
    estimated_cost="$20-60/month",
    tags=["data", "langgraph", "sql", "analytics"],
))

# 4. Code Generation Agent (LangGraph)
_register(AgentTemplate(
    id="code-generation",
    name="Code Generation Agent",
    description="Iterative code-writing agent — generates, reviews, and tests code based on specifications.",
    category=TemplateCategory.CODE_GENERATION,
    framework=FrameworkChoice.LANGGRAPH,
    agents=[
        AgentRole(role="planner", goal="Break specification into implementation tasks", tools=[]),
        AgentRole(role="coder", goal="Write clean, tested code", tools=["file_write", "run_tests"]),
        AgentRole(role="reviewer", goal="Review code for quality, security, and correctness", tools=["file_read"]),
    ],
    mcp_servers=[
        MCPServerConfig(name="github", command="npx", args=["-y", "@github/mcp-server"], required_env=["GITHUB_TOKEN"], category="dev-tools"),
    ],
    required_fields=[
        TemplateField(name="language", label="Programming Language", field_type="select", options=["python", "typescript", "javascript", "go", "rust"], required=True),
    ],
    optional_fields=[
        TemplateField(name="test_framework", label="Test Framework", description="e.g. pytest, jest, go test"),
        TemplateField(name="style_guide", label="Style Guide URL", description="Link to your code style guide"),
    ],
    estimated_cost="$40-120/month",
    tags=["code", "langgraph", "github", "development"],
))

# 5. Multi-Agent Team (AutoGen)
_register(AgentTemplate(
    id="multi-agent-team",
    name="Multi-Agent Team",
    description="Collaborative agent group chat — coordinator, workers, and critic iterate together.",
    category=TemplateCategory.MULTI_AGENT,
    framework=FrameworkChoice.AUTOGEN,
    agents=[
        AgentRole(role="coordinator", goal="Manage group conversation and task delegation", tools=[]),
        AgentRole(role="worker", goal="Execute primary tasks assigned by coordinator", tools=[]),
        AgentRole(role="critic", goal="Review outputs and suggest improvements", tools=[]),
    ],
    mcp_servers=[],
    required_fields=[
        TemplateField(name="team_goal", label="Team Goal", required=True, description="What should this agent team accomplish?"),
    ],
    optional_fields=[
        TemplateField(name="max_rounds", label="Max Conversation Rounds", field_type="number", default=10),
        TemplateField(name="human_in_loop", label="Human-in-the-loop", field_type="boolean", default=False),
    ],
    estimated_cost="$30-100/month",
    tags=["multi-agent", "autogen", "collaboration", "team"],
))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def list_templates() -> List[AgentTemplate]:
    """Return all available templates."""
    return list(_TEMPLATES.values())


def get_template(template_id: str) -> Optional[AgentTemplate]:
    """Get a template by ID."""
    return _TEMPLATES.get(template_id)


def get_template_for_framework(framework: FrameworkChoice) -> Optional[AgentTemplate]:
    """Get the first template that uses the given framework."""
    for t in _TEMPLATES.values():
        if t.framework == framework:
            return t
    return None

