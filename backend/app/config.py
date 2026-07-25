"""
syswiki — Configuración
"""

from __future__ import annotations
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración del backend. Valores por defecto para desarrollo."""

    # App
    app_name: str = "SysWiki"
    debug: bool = True

    # Wikipedia
    wikipedia_user_agent: str = "SysWiki/0.1 (https://github.com/mvisca/syswiki)"

    # Pipeline
    pipeline_timeout_seconds: int = 60
    max_agents_parallel: int = 4

    # Storage (no-op para MVP)
    storage_type: str = "noop"  # "noop" | "sqlite"

    # CORS
    allowed_origins: list[str] = ["*"]

    class Config:
        env_prefix = "SYSWIKI_"
