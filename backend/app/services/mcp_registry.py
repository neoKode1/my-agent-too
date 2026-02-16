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


# ---- Official Reference Servers ----

_reg(MCPServerEntry(
    id="fetch",
    name="Fetch",
    description="Fetch web pages and convert HTML to markdown for LLM-friendly consumption.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-fetch"],
    required_env=[],
    npm_package="@modelcontextprotocol/server-fetch",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/fetch",
    icon="🌐",
    tags=["web", "http", "scraping", "markdown"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="git",
    name="Git",
    description="Local git repository operations — log, diff, status, commit, branch management.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-git"],
    required_env=[],
    optional_env=["GIT_REPO_PATH"],
    npm_package="@modelcontextprotocol/server-git",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/git",
    icon="🔀",
    tags=["git", "version-control", "source-code"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="memory",
    name="Memory (Knowledge Graph)",
    description="Persistent memory via a local knowledge graph — store and retrieve entities and relations.",
    category=MCPCategory.AI_ML,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-memory"],
    required_env=[],
    npm_package="@modelcontextprotocol/server-memory",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/memory",
    icon="🧠",
    tags=["memory", "knowledge-graph", "persistence", "entities"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="sequential-thinking",
    name="Sequential Thinking",
    description="Dynamic, reflective problem-solving through sequential thought chains with revision support.",
    category=MCPCategory.AI_ML,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
    required_env=[],
    npm_package="@modelcontextprotocol/server-sequential-thinking",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking",
    icon="🔗",
    tags=["reasoning", "thinking", "chain-of-thought", "planning"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="time",
    name="Time",
    description="Get current time and perform timezone conversions across IANA timezones.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-time"],
    required_env=[],
    npm_package="@modelcontextprotocol/server-time",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/time",
    icon="🕐",
    tags=["time", "timezone", "datetime", "clock"],
    is_official=True,
))

# ---- Data / Database (additional) ----

_reg(MCPServerEntry(
    id="mysql",
    name="MySQL",
    description="Query MySQL databases — read schemas, run SQL, explore tables and views.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@benborla29/mcp-server-mysql"],
    required_env=["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"],
    npm_package="@benborla29/mcp-server-mysql",
    documentation_url="https://github.com/benborla/mcp-server-mysql",
    icon="🐬",
    tags=["sql", "database", "relational", "mysql"],
))

_reg(MCPServerEntry(
    id="redis",
    name="Redis",
    description="Interact with Redis — get/set keys, manage data structures, pub/sub.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-redis"],
    required_env=["REDIS_URL"],
    npm_package="@modelcontextprotocol/server-redis",
    icon="🔴",
    tags=["cache", "key-value", "database", "redis"],
))

_reg(MCPServerEntry(
    id="supabase",
    name="Supabase",
    description="Manage Supabase projects — query databases, manage auth, storage, and edge functions.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "supabase-mcp-server"],
    required_env=["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"],
    npm_package="supabase-mcp-server",
    documentation_url="https://github.com/supabase/mcp-server-supabase",
    icon="⚡",
    tags=["database", "auth", "storage", "backend-as-a-service"],
))

_reg(MCPServerEntry(
    id="snowflake",
    name="Snowflake",
    description="Query Snowflake data warehouse — run SQL, explore schemas, manage warehouses.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@snowflake/mcp-server"],
    required_env=["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD"],
    optional_env=["SNOWFLAKE_WAREHOUSE", "SNOWFLAKE_DATABASE", "SNOWFLAKE_SCHEMA"],
    npm_package="@snowflake/mcp-server",
    icon="❄️",
    tags=["data-warehouse", "sql", "analytics", "cloud"],
))

_reg(MCPServerEntry(
    id="pinecone",
    name="Pinecone",
    description="Manage Pinecone vector database — upsert, query, and delete vector embeddings.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@pinecone-database/mcp-server"],
    required_env=["PINECONE_API_KEY"],
    optional_env=["PINECONE_INDEX_NAME"],
    npm_package="@pinecone-database/mcp-server",
    icon="🌲",
    tags=["vector-database", "embeddings", "rag", "similarity-search"],
))

_reg(MCPServerEntry(
    id="neo4j",
    name="Neo4j",
    description="Query Neo4j graph database — run Cypher queries, explore nodes and relationships.",
    category=MCPCategory.DATA,
    command="npx",
    args=["-y", "@neo4j/mcp-server"],
    required_env=["NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"],
    npm_package="@neo4j/mcp-server",
    icon="🔵",
    tags=["graph-database", "cypher", "knowledge-graph", "relationships"],
))

# ---- Intelligence ----

_reg(MCPServerEntry(
    id="breach",
    name="Breach Intelligence",
    description=(
        "AI-first open intelligence platform tracking 377+ research facilities, "
        "93 equipment systems, 264 supplier relationships, 61 researchers, and "
        "62 research papers across 11 scientific domains. Includes ClawBot agentic "
        "AI engine, correlation analysis, knowledge graph, satellite tracking, and "
        "NEST agent network integration. 27 tools covering database queries, "
        "web intelligence, analysis, knowledge creation, and inter-agent messaging."
    ),
    category=MCPCategory.INTELLIGENCE,
    command="http",  # HTTP/SSE transport, not stdio
    args=[],
    endpoint_url="https://breach-mcp.nexartis.workers.dev",
    required_env=[],
    optional_env=["BREACH_API_KEY"],
    npm_package=None,
    documentation_url="https://github.com/neoKode1/Breach",
    icon="🔓",
    tags=[
        "intelligence", "research", "facilities", "defense",
        "analysis", "knowledge-graph", "agentic-ai", "satellite",
        "open-source", "palantir-alternative",
    ],
    is_official=False,
))


# ---- Communication (additional) ----

_reg(MCPServerEntry(
    id="twilio",
    name="Twilio",
    description="Send SMS/MMS, make calls, manage phone numbers via Twilio APIs.",
    category=MCPCategory.COMMUNICATION,
    command="npx",
    args=["-y", "@twilio/mcp-server"],
    required_env=["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"],
    optional_env=["TWILIO_PHONE_NUMBER"],
    npm_package="@twilio/mcp-server",
    icon="📱",
    tags=["sms", "voice", "phone", "messaging"],
))

_reg(MCPServerEntry(
    id="telegram",
    name="Telegram",
    description="Send messages, manage bots, and interact with Telegram chats and channels.",
    category=MCPCategory.COMMUNICATION,
    command="npx",
    args=["-y", "telegram-mcp-server"],
    required_env=["TELEGRAM_BOT_TOKEN"],
    npm_package="telegram-mcp-server",
    icon="✈️",
    tags=["chat", "bot", "messaging", "telegram"],
))

_reg(MCPServerEntry(
    id="twitter",
    name="Twitter / X",
    description="Post tweets, search timelines, manage follows and lists on Twitter/X.",
    category=MCPCategory.COMMUNICATION,
    command="npx",
    args=["-y", "twitter-mcp-server"],
    required_env=["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET"],
    npm_package="twitter-mcp-server",
    icon="🐦",
    tags=["social-media", "tweets", "x", "timeline"],
))

# ---- Dev Tools (additional) ----

_reg(MCPServerEntry(
    id="gitlab",
    name="GitLab",
    description="Manage GitLab repos, merge requests, issues, CI pipelines, and wikis.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@gitlab/mcp-server"],
    required_env=["GITLAB_TOKEN"],
    optional_env=["GITLAB_URL"],
    npm_package="@gitlab/mcp-server",
    icon="🦊",
    tags=["git", "code", "ci-cd", "merge-requests"],
))

_reg(MCPServerEntry(
    id="sentry",
    name="Sentry",
    description="Query error reports, manage issues, view performance data in Sentry.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@sentry/mcp-server"],
    required_env=["SENTRY_AUTH_TOKEN"],
    optional_env=["SENTRY_ORG", "SENTRY_PROJECT"],
    npm_package="@sentry/mcp-server",
    icon="🐛",
    tags=["errors", "monitoring", "debugging", "performance"],
))

_reg(MCPServerEntry(
    id="docker",
    name="Docker",
    description="Manage Docker containers, images, volumes, and networks.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@docker/mcp-server"],
    required_env=[],
    optional_env=["DOCKER_HOST"],
    npm_package="@docker/mcp-server",
    icon="🐳",
    tags=["containers", "docker", "devops", "infrastructure"],
))

_reg(MCPServerEntry(
    id="kubernetes",
    name="Kubernetes",
    description="Manage Kubernetes clusters — list pods, deployments, services, view logs.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "kubernetes-mcp-server"],
    required_env=[],
    optional_env=["KUBECONFIG"],
    npm_package="kubernetes-mcp-server",
    icon="☸️",
    tags=["k8s", "containers", "orchestration", "devops"],
))

_reg(MCPServerEntry(
    id="puppeteer",
    name="Puppeteer",
    description="Browser automation — navigate pages, take screenshots, extract content, fill forms.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@modelcontextprotocol/server-puppeteer"],
    required_env=[],
    npm_package="@modelcontextprotocol/server-puppeteer",
    documentation_url="https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer",
    icon="🎭",
    tags=["browser", "automation", "scraping", "testing"],
    is_official=True,
))

_reg(MCPServerEntry(
    id="playwright",
    name="Playwright",
    description="Cross-browser automation — test, scrape, and interact with web pages via Playwright.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@playwright/mcp-server"],
    required_env=[],
    npm_package="@playwright/mcp-server",
    icon="🎪",
    tags=["browser", "automation", "testing", "cross-browser"],
))

_reg(MCPServerEntry(
    id="cloudflare",
    name="Cloudflare",
    description="Manage Cloudflare Workers, KV, R2, D1, DNS, and zones.",
    category=MCPCategory.DEV_TOOLS,
    command="npx",
    args=["-y", "@cloudflare/mcp-server-cloudflare"],
    required_env=["CLOUDFLARE_API_TOKEN"],
    optional_env=["CLOUDFLARE_ACCOUNT_ID"],
    npm_package="@cloudflare/mcp-server-cloudflare",
    icon="🔶",
    tags=["cdn", "workers", "edge", "dns", "serverless"],
))

# ---- Productivity (additional) ----

_reg(MCPServerEntry(
    id="google-calendar",
    name="Google Calendar",
    description="Create, list, update, and search calendar events in Google Calendar.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "google-calendar-mcp-server"],
    required_env=["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
    npm_package="google-calendar-mcp-server",
    icon="📅",
    tags=["calendar", "events", "scheduling", "google"],
))

_reg(MCPServerEntry(
    id="trello",
    name="Trello",
    description="Manage Trello boards, lists, and cards — create, move, archive, and search.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "trello-mcp-server"],
    required_env=["TRELLO_API_KEY", "TRELLO_TOKEN"],
    npm_package="trello-mcp-server",
    icon="📊",
    tags=["kanban", "boards", "project-management", "cards"],
))

_reg(MCPServerEntry(
    id="todoist",
    name="Todoist",
    description="Manage tasks, projects, labels, and filters in Todoist.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "todoist-mcp-server"],
    required_env=["TODOIST_API_TOKEN"],
    npm_package="todoist-mcp-server",
    icon="✅",
    tags=["tasks", "todo", "productivity", "gtd"],
))

_reg(MCPServerEntry(
    id="confluence",
    name="Confluence",
    description="Search, read, and create pages in Atlassian Confluence wikis.",
    category=MCPCategory.PRODUCTIVITY,
    command="npx",
    args=["-y", "@atlassian/confluence-mcp-server"],
    required_env=["CONFLUENCE_URL", "CONFLUENCE_EMAIL", "CONFLUENCE_API_TOKEN"],
    npm_package="@atlassian/confluence-mcp-server",
    icon="📘",
    tags=["wiki", "docs", "knowledge-base", "atlassian"],
))

# ---- Search (additional) ----

_reg(MCPServerEntry(
    id="tavily",
    name="Tavily",
    description="AI-optimised web search — returns clean, structured results ideal for LLM consumption.",
    category=MCPCategory.SEARCH,
    command="npx",
    args=["-y", "tavily-mcp-server"],
    required_env=["TAVILY_API_KEY"],
    npm_package="tavily-mcp-server",
    icon="🔎",
    tags=["search", "ai-search", "web", "research"],
))

_reg(MCPServerEntry(
    id="exa",
    name="Exa",
    description="Neural search engine — find semantically similar content across the web.",
    category=MCPCategory.SEARCH,
    command="npx",
    args=["-y", "exa-mcp-server"],
    required_env=["EXA_API_KEY"],
    npm_package="exa-mcp-server",
    documentation_url="https://docs.exa.ai",
    icon="🧬",
    tags=["search", "neural", "semantic", "embeddings"],
))

# ---- Finance / Commerce ----

_reg(MCPServerEntry(
    id="stripe",
    name="Stripe",
    description="Manage payments, customers, subscriptions, invoices, and products in Stripe.",
    category=MCPCategory.FINANCE,
    command="npx",
    args=["-y", "@stripe/mcp-server"],
    required_env=["STRIPE_SECRET_KEY"],
    npm_package="@stripe/mcp-server",
    icon="💳",
    tags=["payments", "billing", "subscriptions", "commerce"],
))

_reg(MCPServerEntry(
    id="shopify",
    name="Shopify",
    description="Manage Shopify store — products, orders, customers, inventory, and analytics.",
    category=MCPCategory.FINANCE,
    command="npx",
    args=["-y", "@shopify/mcp-server"],
    required_env=["SHOPIFY_STORE_URL", "SHOPIFY_ACCESS_TOKEN"],
    npm_package="@shopify/mcp-server",
    icon="🛒",
    tags=["ecommerce", "store", "products", "orders"],
))

# ---- AI / ML (additional) ----

_reg(MCPServerEntry(
    id="replicate",
    name="Replicate",
    description="Run and manage ML models on Replicate — image gen, LLMs, audio, video.",
    category=MCPCategory.AI_ML,
    command="npx",
    args=["-y", "replicate-mcp-server"],
    required_env=["REPLICATE_API_TOKEN"],
    npm_package="replicate-mcp-server",
    icon="🔄",
    tags=["ml", "inference", "models", "image-generation"],
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

