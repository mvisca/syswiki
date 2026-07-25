"""
syswiki — SearchSource (abstract interface)

Fuente de búsqueda y obtención de conceptos. Abstracción para
Wikipedia, arXiv, PubMed, etc.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from app.models.contracts import (
    SearchResult, SearchMode, Concept,
)


class SearchSource(ABC):
    """Fuente de datos abstracta. Implementar por cada proveedor."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Identificador único de la fuente (ej: 'wikipedia', 'arxiv')."""
        ...

    @property
    @abstractmethod
    def weight(self) -> float:
        """Confiabilidad 0.0 - 1.0."""
        ...

    @property
    @abstractmethod
    def domains(self) -> list[str]:
        """Temas donde esta fuente es autoritativa (ej: ['science', 'general'])."""
        ...

    @abstractmethod
    async def search(
        self,
        query: str,
        language: str = "en",
        limit: int = 10,
    ) -> list[SearchResult]:
        """Buscar conceptos por texto libre."""
        ...

    @abstractmethod
    async def get_concept(
        self,
        qid: str,
        language: str = "en",
    ) -> Optional[Concept]:
        """Obtener un concepto por su QID (Wikidata) o ID nativo."""
        ...

    @abstractmethod
    async def resolve_qid(
        self,
        query: str,
        language: str = "en",
    ) -> Optional[str]:
        """Resolver un texto a su QID canónico (Wikidata)."""
        ...

    def supports_language(self, language: str) -> bool:
        """Verificar si esta fuente soporta un idioma."""
        return True
