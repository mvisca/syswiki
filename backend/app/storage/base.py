"""
syswiki — Storage (abstract interface)

Repositorio de persistencia. Abstracción para no-op (MVP),
SQLite (post-MVP) o PostgreSQL (futuro).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from app.models.contracts import (
    Concept, Relation, PipelineStatus, LearningPattern,
    CurationRequest, CuratedStatus,
)


class Storage(ABC):
    """Repositorio abstracto de persistencia."""

    @abstractmethod
    async def get_concept(self, qid: str) -> Optional[Concept]:
        """Obtener concepto por QID."""
        ...

    @abstractmethod
    async def save_concept(self, concept: Concept) -> None:
        """Guardar o actualizar concepto."""
        ...

    @abstractmethod
    async def get_relations(
        self, qid: str, relation_type: Optional[str] = None
    ) -> list[Relation]:
        """Obtener relaciones de un concepto."""
        ...

    @abstractmethod
    async def save_relation(self, relation: Relation) -> None:
        """Guardar o actualizar relación."""
        ...

    @abstractmethod
    async def save_relations(self, relations: list[Relation]) -> None:
        """Guardar varias relaciones (batch)."""
        ...

    @abstractmethod
    async def save_pipeline_status(self, status: PipelineStatus) -> None:
        """Guardar estado del pipeline para un concepto."""
        ...

    @abstractmethod
    async def get_pipeline_status(self, qid: str) -> Optional[PipelineStatus]:
        """Obtener estado del pipeline."""
        ...

    @abstractmethod
    async def save_curation(self, request: CurationRequest) -> None:
        """Registrar curación del usuario."""
        ...

    @abstractmethod
    async def get_learning_patterns(self) -> list[LearningPattern]:
        """Obtener patrones de aprendizaje."""
        ...

    @abstractmethod
    async def save_learning_pattern(self, pattern: LearningPattern) -> None:
        """Guardar o actualizar patrón."""
        ...

    @abstractmethod
    async def search_concepts(
        self, query: str, limit: int = 10
    ) -> list[Concept]:
        """Buscar conceptos en el almacén local (por título/alias)."""
        ...
