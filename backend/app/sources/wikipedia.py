"""
syswiki — Wikipedia Source Implementation

Implementación de SearchSource para Wikipedia.
Usa REST API de Wikipedia + Wikidata para obtener conceptos.
"""

from __future__ import annotations
from typing import Optional
import httpx
from app.sources.base import SearchSource
from app.models.contracts import SearchResult, Concept


WIKIPEDIA_API_BASE = "https://{language}.wikipedia.org/api/rest_v1"
WIKIPEDIA_ACTION_API = "https://{language}.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"


class WikipediaSource(SearchSource):

    @property
    def name(self) -> str:
        return "wikipedia"

    @property
    def weight(self) -> float:
        return 0.8  # Alta confiabilidad para información general

    @property
    def domains(self) -> list[str]:
        return ["general", "science", "history", "culture", "technology"]

    async def search(
        self,
        query: str,
        language: str = "en",
        limit: int = 10,
    ) -> list[SearchResult]:
        """
        Buscar en Wikipedia. Usa la Action API (opensearch + query).
        """
        # 1. Búsqueda via Action API
        # 2. Por cada resultado, obtener QID de Wikidata
        # 3. Retornar SearchResult con QID, título, descripción
        ...
        return []

    async def get_concept(
        self,
        qid: str,
        language: str = "en",
    ) -> Optional[Concept]:
        """
        Obtener concepto completo.

        1. Resolver QID → título del artículo en `language`
        2. Fetch REST API /page/summary/{title}
        3. Fetch Action API: extract, categories, links
        4. Construir Concept con datos básicos (análisis causal vacío)
        """
        ...

    async def resolve_qid(
        self,
        query: str,
        language: str = "en",
    ) -> Optional[str]:
        """
        Resolver query a QID de Wikidata.

        1. Buscar artículo en Wikipedia
        2. Obtener pageprops → wikibase_item (QID)
        """
        ...

    async def _fetch_json(self, url: str) -> dict:
        """GET request con timeout a una URL JSON."""
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers={"User-Agent": "SysWiki/0.1"})
            resp.raise_for_status()
            return resp.json()

    async def _fetch_text(self, url: str) -> str:
        """GET request con timeout para texto plano."""
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers={"User-Agent": "SysWiki/0.1"})
            resp.raise_for_status()
            return resp.text
