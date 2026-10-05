"""
syswiki — Wikipedia Source Implementation

Implementación de SearchSource para Wikipedia.
Usa REST API de Wikipedia + Wikidata para obtener conceptos.
"""

from __future__ import annotations
from typing import Optional
from urllib.parse import quote
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
        Buscar en Wikipedia. Usa la Action API (list=search) y resuelve
        el QID de cada resultado en una llamada aparte.
        """
        action_api = WIKIPEDIA_ACTION_API.format(language=language)
        search_url = (
            f"{action_api}?action=query&list=search&srsearch={quote(query)}"
            f"&srlimit={limit}&format=json"
        )
        data = await self._fetch_json(search_url)
        hits = data.get("query", {}).get("search", [])

        results: list[SearchResult] = []
        for hit in hits:
            title = hit["title"]
            qid = await self.resolve_qid(title, language)
            description = self._strip_html(hit.get("snippet", ""))
            results.append(
                SearchResult(
                    qid=qid or "",
                    title=title,
                    description=description,
                    source=self.name,
                    language=language,
                )
            )
        return results

    async def get_concept(
        self,
        qid: str,
        language: str = "en",
    ) -> Optional[Concept]:
        """
        Obtener concepto completo.

        1. Wikidata EntityData: resolver el sitelink del wiki en `language`.
        2. REST API /page/summary/{title}: extract, thumbnail, descripción corta.
        3. Construir Concept con datos básicos (análisis causal vacío,
           lo completa el pipeline de agentes).
        """
        title = await self._title_from_qid(qid, language)
        if not title:
            return None

        summary_url = f"{WIKIPEDIA_API_BASE.format(language=language)}/page/summary/{quote(title)}"
        try:
            summary = await self._fetch_json(summary_url)
        except httpx.HTTPStatusError:
            return None

        thumbnail = summary.get("thumbnail", {}).get("source", "")
        return Concept(
            qid=qid,
            title=summary.get("title", title),
            language=language,
            source=self.name,
            source_url=summary.get("content_urls", {}).get("desktop", {}).get("page", ""),
            thumbnail_url=thumbnail,
            description=summary.get("extract", ""),
        )

    async def resolve_qid(
        self,
        query: str,
        language: str = "en",
    ) -> Optional[str]:
        """
        Resolver query a QID de Wikidata.

        1. Buscar el título exacto de página en Wikipedia (redirects incluidos).
        2. Obtener pageprops → wikibase_item (QID).
        """
        action_api = WIKIPEDIA_ACTION_API.format(language=language)
        url = (
            f"{action_api}?action=query&titles={quote(query)}"
            f"&prop=pageprops&redirects=1&format=json"
        )
        data = await self._fetch_json(url)
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            qid = page.get("pageprops", {}).get("wikibase_item")
            if qid:
                return qid
        return None

    async def _title_from_qid(self, qid: str, language: str) -> Optional[str]:
        """Wikidata EntityData → título del sitelink en `language`."""
        url = WIKIDATA_API.format(qid=qid)
        data = await self._fetch_json(url)
        entity = data.get("entities", {}).get(qid, {})
        sitelink = entity.get("sitelinks", {}).get(f"{language}wiki")
        return sitelink.get("title") if sitelink else None

    @staticmethod
    def _strip_html(text: str) -> str:
        """Wikipedia devuelve snippets con <span class="searchmatch">…</span>."""
        import re
        return re.sub(r"<[^>]+>", "", text)

    async def _fetch_json(self, url: str) -> dict:
        """GET request con timeout a una URL JSON."""
        async with httpx.AsyncClient(timeout=15.0, http2=False) as client:
            resp = await client.get(url, headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def _fetch_text(self, url: str) -> str:
        """GET request con timeout para texto plano."""
        async with httpx.AsyncClient(timeout=15.0, http2=False) as client:
            resp = await client.get(url, headers=self._headers())
            resp.raise_for_status()
            return resp.text

    @staticmethod
    def _headers() -> dict:
        # Wikimedia bloquea con 403 (política de robots) las requests que
        # negocian HTTP/2 sin un User-Agent identificable con contacto.
        # Forzamos HTTP/1.1 (arriba) y declaramos un UA con contacto.
        return {"User-Agent": "SysWiki/0.1 (https://github.com/mvisca/syswiki; contact: martin.visca@gmail.com)"}
