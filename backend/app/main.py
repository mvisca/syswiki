"""
syswiki — Enciclopedia Sistémica
FastAPI Application entry point.
"""

from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    settings = Settings()
    app.state.settings = settings

    # Inicializar dependencias
    from app.services.search_engine import SearchEngine
    from app.sources.wikipedia import WikipediaSource
    from app.storage.noop import NoopStorage

    app.state.search_engine = SearchEngine(sources=[WikipediaSource()])
    app.state.storage = NoopStorage()

    yield  # La app corre aquí

    # Cleanup if needed
    pass


app = FastAPI(
    title="SysWiki — Enciclopedia Sistémica",
    description="""
    API de la Enciclopedia Sistémica.
    Combina Teoría General de Sistemas con Causas Aristotélicas.
    """,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# CORS: permitir frontend local en desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "app": "SysWiki - Enciclopedia Sistémica",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
