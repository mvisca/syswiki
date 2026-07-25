"""
syswiki — No-op Storage (MVP)

Implementación que no persiste nada. Declara la interfaz completa
pero todas las operaciones son no-op. Lista para reemplazar por
SQLiteStorage cuando se necesite persistencia real.
"""

from __future__ import annotations
from typing import Optional
from app.storage.base import Storage
from app.models.contracts import (
    Concept, Relation, PipelineStatus, LearningPattern,
    CurationRequest,
)


class NoopStorage(Storage):
    """
    Almacenamiento nulo para MVP.
    Todas las operaciones son válidas pero no persisten.
    Sirve para probar el pipeline y la API sin base de datos.
    """

    def __init__(self):
        self._concepts: dict[str, Concept] = {}

    async def get_concept(self, qid: str) -> Optional[Concept]:
        return self._concepts.get(qid)

    async def save_concept(self, concept: Concept) -> None:
        self._concepts[concept.qid] = concept

    async def get_relations(
        self, qid: str, relation_type: Optional[str] = None
    ) -> list[Relation]:
        return []

    async def save_relation(self, relation: Relation) -> None:
        pass

    async def save_relations(self, relations: list[Relation]) -> None:
        pass

    async def save_pipeline_status(self, status: PipelineStatus) -> None:
        pass

    async def get_pipeline_status(self, qid: str) -> Optional[PipelineStatus]:
        return None

    async def save_curation(self, request: CurationRequest) -> None:
        # En MVP, registrar en memoria o log
        pass

    async def get_learning_patterns(self) -> list[LearningPattern]:
        return []

    async def save_learning_pattern(self, pattern: LearningPattern) -> None:
        pass

    async def search_concepts(
        self, query: str, limit: int = 10
    ) -> list[Concept]:
        # Búsqueda en memoria sobre lo que tenemos
        results = []
        for c in self._concepts.values():
            if query.lower() in c.title.lower() or any(
                query.lower() in a.lower() for a in c.aliases
            ):
                results.append(c)
                if len(results) >= limit:
                    break
        return results
