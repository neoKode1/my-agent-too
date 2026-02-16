"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration – reads from env vars / .env file."""

    # My-Agent-Too
    app_name: str = "My-Agent-Too"
    app_version: str = "0.1.0"
    debug: bool = False

    # NANDA Index
    nanda_url: str = "http://localhost:6900"

    # LLM
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-20250514"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

