"""
syswiki — SearchEngine

Orquestador de búsqueda. Decide qué fuente(s) consultar según
el modo, el dominio del concepto, y la configuración disponible.
"""

from __future__ import annotations
from typing import Optional
from app.sources.base import SearchSource
from app.models.contracts import (
    SearchRequest, SearchResult, SearchResponse, SearchMode,
    Concept,
)


class SearchEngine:
    """
    Motor de búsqueda que orquesta múltiples fuentes.

    Modos:
      - simple: consulta una fuente específica
      - all: consulta todas las fuentes en paralelo y combina
      - best: elige la fuente más autoritativa para el dominio
      - auto: decide según el query y contexto
    """

    def __init__(self, sources: list[SearchSource]):
        self.sources = {s.name: s for s in sources}

    async def search(
        self,
        req: SearchRequest,
    ) -> SearchResponse:
        """Buscar según el modo especificado."""
        mode_map = {
            SearchMode.simple: self._search_simple,
            SearchMode.all: self._search_all,
            SearchMode.best: self._search_best,
            SearchMode.auto: self._search_auto,
        }
        handler = mode_map.get(req.mode, self._search_auto)
        return await handler(req)

    async def get_concept(
        self,
        qid: str,
        language: str = "en",
        preferred_source: Optional[str] = None,
    ) -> Optional[Concept]:
        """Obtener un concepto desde la fuente más adecuada."""
        if preferred_source and preferred_source in self.sources:
            return await self.sources[preferred_source].get_concept(qid, language)

        # Probar fuentes en orden de peso
        sorted_sources = sorted(
            self.sources.values(), key=lambda s: s.weight, reverse=True
        )
        for source in sorted_sources:
            concept = await source.get_concept(qid, language)
            if concept:
                return concept
        return None

    async def resolve_qid(
        self,
        query: str,
        language: str = "en",
    ) -> Optional[str]:
        """Resolver query a QID usando la mejor fuente disponible."""
        for source in self.sources.values():
            qid = await source.resolve_qid(query, language)
            if qid:
                return qid
        return None

    async def _search_simple(self, req: SearchRequest) -> SearchResponse:
        source = self.sources.get(req.source or "wikipedia")
        if not source:
            return SearchResponse(results=[], source_used="none")
        results = await source.search(req.query, req.language or "en")
        return SearchResponse(results=results, source_used=source.name)

    async def _search_all(self, req: SearchRequest) -> SearchResponse:
        """Buscar en todas las fuentes en paralelo y combinar."""
        import asyncio
        tasks = [
            source.search(req.query, req.language or "en")
            for source in self.sources.values()
        ]
        all_results = await asyncio.gather(*tasks, return_exceptions=True)
        combined = []
        seen_qids = set()
        for results in all_results:
            if isinstance(results, list):
                for r in results:
                    if r.qid not in seen_qids:
                        combined.append(r)
                        seen_qids.add(r.qid)
        return SearchResponse(
            results=combined[:20],
            source_used="all",
        )

    async def _search_best(self, req: SearchRequest) -> SearchResponse:
        """Elegir la fuente más autoritativa para el dominio."""
        if not req.domain:
            return await self._search_auto(req)

        # Encontrar fuente con mayor peso que cubra este dominio
        best_source = max(
            (s for s in self.sources.values() if req.domain in s.domains),
            key=lambda s: s.weight,
            default=None,
        )
        if not best_source:
            return await self._search_auto(req)

        results = await best_source.search(req.query, req.language or "en")
        return SearchResponse(results=results, source_used=best_source.name)

    async def _search_auto(self, req: SearchRequest) -> SearchResponse:
        """Decisión automática: intentar con la fuente principal."""
        return await self._search_simple(req)
