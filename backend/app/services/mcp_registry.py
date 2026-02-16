"""Comprehensive MCP server registry.

Centralised catalogue of all supported MCP servers with full metadata,
category filtering, search, and health-status tracking.
"""

from typing import Dict, List, Optional

from app.models.mcp import MCPCategory, MCPServerEntry, MCPServerStatus


# ---------------------------------------------------------------------------
# Registry data  (source of truth for all supported MCP servers)
# ---------------------------------------------------------------------------

_SERVERS: Dict[str, MCPServerEntry] = {}


def _reg(entry: MCPServerEntry) -> None:
    _SERVERS[entry.id] = entry


# ---- Data Sources ----

_reg(MCPServerEntry(
    id="postgres",
    name="PostgreSQL",
    description="Query PostgreSQL databases — read schemas, run SQL, explore tables.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-postgres"],
    required_env=["DATABASE_URL"],
    npm_package="@modelcontextprotocol/server-postgres",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/postgres",
    icon="🐘",
    tags=["sql", "database", "relational"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="mongodb",
    name="MongoDB",
    description="Interact with MongoDB — list collections, query documents, aggregate.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-mongodb"],
    required_env=["MONGODB_URI"],
    npm_package="@modelcontextprotocol/server-mongodb",
    icon="🍃",
    tags=["nosql", "database", "documents"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="sqlite",
    name="SQLite",
    description="Read and query local SQLite databases.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-sqlite"],
    required_env=["SQLITE_PATH"],
    npm_package="@modelcontextprotocol/server-sqlite",
    icon="📦",
    tags=["sql", "database", "local", "embedded"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="google-drive",
    name="Google Drive",
    description="Search, list, and read files from Google Drive.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-gdrive"],
    required_env=["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
    npm_package="@modelcontextprotocol/server-gdrive",
    icon="📁",
    tags=["files", "cloud", "google"],
    is_official=True,
))

# ---- Communication ----

_reg(MCPServerEntry(
    id="slack",
    name="Slack",
    description="Send messages, list channels, search conversations in Slack workspaces.",
    category=MCPCategory.COMMUNICATION,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-slack"],
    required_env=["SLACK_BOT_TOKEN"],
    optional_env=["SLACK_SIGNING_SECRET"],
    npm_package="@modelcontextprotocol/server-slack",
    icon="💬",
    tags=["chat", "messaging", "team"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="email",
    name="Email (SMTP/IMAP)",
    description="Send and read emails via SMTP and IMAP protocols.",
    category=MCPCategory.COMMUNICATION,
    command="npx",
    args=["-y", "@email/mcp-server"],
    required_env=["SMTP_HOST", "SMTP_USER", "SMTP_PASS", "IMAP_HOST"],
    npm_package="@email/mcp-server",
    icon="📧",
    tags=["email", "smtp", "imap"],
))

_reg(MCPServerEntry(
    id="discord",
    name="Discord",
    description="Interact with Discord — send messages, manage channels, list guilds.",
    category=MCPCategory.COMMUNICATION,
    command="npx",
    args=["-y", "@discord/mcp-server"],
    required_env=["DISCORD_BOT_TOKEN"],
    npm_package="@discord/mcp-server",
    icon="🎮",
    tags=["chat", "gaming", "community"],
))

# ---- Dev Tools ----

_reg(MCPServerEntry(
    id="github",
    name="GitHub",
    description="Manage repos, issues, PRs, search code, and more on GitHub.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    required_env=["GITHUB_TOKEN"],
    npm_package="@modelcontextprotocol/server-github",
    icon="🐙",
    tags=["git", "code", "issues", "ci"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="filesystem",
    name="Filesystem",
    description="Read, write, and search files on the local filesystem (sandboxed).",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem"],
    required_env=["ALLOWED_DIRECTORIES"],
    npm_package="@modelcontextprotocol/server-filesystem",
    icon="📂",
    tags=["files", "local", "io"],
    is_official=True,
))

# ---- Productivity ----

_reg(MCPServerEntry(
    id="notion",
    name="Notion",
    description="Search pages, read content, create and update pages in Notion.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-notion"],
    required_env=["NOTION_API_KEY"],
    npm_package="@modelcontextprotocol/server-notion",
    icon="📝",
    tags=["wiki", "notes", "docs"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="linear",
    name="Linear",
    description="Manage issues, projects, and teams in Linear.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "@linear/mcp-server"],
    required_env=["LINEAR_API_KEY"],
    npm_package="@linear/mcp-server",
    icon="🔷",
    tags=["issues", "project-management", "agile"],
))

_reg(MCPServerEntry(
    id="jira",
    name="Jira",
    description="Create/search issues, manage sprints and boards in Jira.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "@atlassian/jira-mcp-server"],
    required_env=["JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN"],
    npm_package="@atlassian/jira-mcp-server",
    icon="📋",
    tags=["issues", "project-management", "atlassian"],
))

# ---- Search ----

_reg(MCPServerEntry(
    id="web-search",
    name="Web Search",
    description="Search the web using Brave Search API.",
    category=MCPCategory.SEARCH,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-brave-search"],
    required_env=["BRAVE_API_KEY"],
    npm_package="@modelcontextprotocol/server-brave-search",
    icon="🔍",
    tags=["search", "web", "brave"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="arxiv",
    name="Arxiv",
    description="Search and retrieve academic papers from Arxiv.",
    category=MCPCategory.SEARCH,
    command="npx",
    args=["-y", "@arxiv/mcp-server"],
    required_env=[],
    npm_package="@arxiv/mcp-server",
    icon="📄",
    tags=["research", "papers", "academic"],
))

# ---- AI / ML ----

_reg(MCPServerEntry(
    id="huggingface",
    name="Hugging Face",
    description="Browse models, datasets, and run inference on Hugging Face Hub.",
    category=MCPCategory.AI_ML,
    command="npx",
    args=["-y", "@huggingface/mcp-server"],
    required_env=["HF_TOKEN"],
    npm_package="@huggingface/mcp-server",
    icon="🤗",
    tags=["models", "inference", "datasets"],
))

# ---- CRM ----

_reg(MCPServerEntry(
    id="salesforce",
    name="Salesforce",
    description="Query, create, and update Salesforce objects — leads, contacts, opportunities.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@salesforce/mcp-server"],
    required_env=["SALESFORCE_INSTANCE_URL", "SALESFORCE_ACCESS_TOKEN"],
    npm_package="@salesforce/mcp-server",
    icon="☁️",
    tags=["crm", "sales", "enterprise"],
))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def list_servers(
    category: Optional[MCPCategory] = None,
    search: Optional[str] = None,
    official_only: bool = False,
) -> List[MCPServerEntry]:
    """Return servers, optionally filtered by category/search/official."""
    results = list(_SERVERS.values())
    if category:
        results = [s for s in results if s.category == category]
    if official_only:
        results = [s for s in results if s.is_official]
    if search:
        q = search.lower()
        results = [
            s for s in results
            if q in s.name.lower()
            or q in s.description.lower()
            or any(q in t for t in s.tags)
        ]
    return results


def get_server(server_id: str) -> Optional[MCPServerEntry]:
    """Get a single server by ID."""
    return _SERVERS.get(server_id)


def get_categories() -> List[str]:
    """Return distinct categories with at least one server."""
    cats = sorted({s.category.value for s in _SERVERS.values()})
    return cats


def update_server_health(
    server_id: str,
    status: MCPServerStatus,
    tools: list | None = None,
) -> None:
    """Update cached health status of a server."""
    srv = _SERVERS.get(server_id)
    if srv:
        srv.status = status
        if tools is not None:
            srv.tools = tools
        from datetime import datetime
        srv.last_health_check = datetime.utcnow()


def server_count() -> int:
    return len(_SERVERS)

