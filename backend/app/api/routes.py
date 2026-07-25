"""
syswiki — API Routes

Contratos HTTP del backend. Cada endpoint define request/response.
"""

from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.contracts import (
    ConceptResponse, SearchRequest, SearchResponse,
    CurationRequest, LearningPattern, PipelineStatus,
    Concept, Relation,
)

router = APIRouter(prefix="/api/v1", tags=["syswiki"])


# ─────────────────────────────────────────────────────────────
# 1. BÚSQUEDA
# ─────────────────────────────────────────────────────────────

@router.post("/search", response_model=SearchResponse)
async def search_concepts(
    req: SearchRequest,
) -> SearchResponse:
    """
    Buscar conceptos que coincidan con el texto de consulta.

    Delegado a SearchEngine que orquesta las fuentes según el modo.
    Resultados incluyen QID, título, descripción y si ya fueron analizados.
    """
    ...  # ver implementation.py


@router.get("/search", response_model=SearchResponse)
async def search_concepts_get(
    q: str = Query(..., min_length=1, description="Texto de búsqueda"),
    mode: str = Query("auto", description="simple | all | best | auto"),
    language: str = Query("es", description="Idioma preferido"),
) -> SearchResponse:
    """Versión GET de búsqueda (para autocomplete rápido)."""
    ...


# ─────────────────────────────────────────────────────────────
# 2. CONCEPTOS
# ─────────────────────────────────────────────────────────────

@router.get("/concepts/{qid}", response_model=ConceptResponse)
async def get_concept(
    qid: str,
    language: str = Query("es", description="Idioma preferido"),
) -> ConceptResponse:
    """
    Obtener un concepto con su análisis completo.

    Si el concepto no existe en caché, dispara el pipeline multi-agente
    (síncrono para MVP, asíncrono después).

    Retorna:
      - concept: ficha completa con 4 causas + vista sistémica
      - relations: relaciones con otros conceptos
      - pipeline: estado del pipeline (útil si está procesando)
    """
    ...


@router.get("/concepts/{qid}/relations", response_model=list[Relation])
async def get_concept_relations(
    qid: str,
    type: Optional[str] = Query(None, description="Filtrar por tipo de relación"),
) -> list[Relation]:
    """Obtener todas las relaciones de un concepto."""
    ...


@router.get("/concepts/{qid}/pipeline", response_model=Optional[PipelineStatus])
async def get_pipeline_status(
    qid: str,
) -> Optional[PipelineStatus]:
    """
    Consultar el estado del pipeline de análisis para un concepto.
    Útil para polling desde el frontend mientras se procesa.
    """
    ...


# ─────────────────────────────────────────────────────────────
# 3. CURACIÓN
# ─────────────────────────────────────────────────────────────

@router.post("/curate", response_model=ConceptResponse)
async def curate_concept(
    req: CurationRequest,
) -> ConceptResponse:
    """
    Registrar una curación del usuario sobre un análisis.

    El usuario puede:
      - Confirmar un análisis existente
      - Rechazar y pedir regeneración
      - Editar el texto de una causa
      - Cambiar el estado epistémico de una causa

    El sistema registra la curación y actualiza sus patrones de aprendizaje.
    """
    ...


# ─────────────────────────────────────────────────────────────
# 4. APRENDIZAJE (para curadores)
# ─────────────────────────────────────────────────────────────

@router.get("/learning/patterns", response_model=list[LearningPattern])
async def get_learning_patterns() -> list[LearningPattern]:
    """
    Obtener todos los patrones de aprendizaje del sistema.
    El curador puede ver qué relaciones aprendió el sistema.
    """
    ...


@router.post("/learning/patterns/{pattern_id}/revert")
async def revert_learning_pattern(
    pattern_id: str,
) -> dict:
    """
    Revertir un patrón aprendido. Útil cuando el sistema
    aprendió una correlación incorrecta.
    """
    ...


# ─────────────────────────────────────────────────────────────
# 5. EXPLORACIÓN (grafo)
# ─────────────────────────────────────────────────────────────

@router.get("/explore/{qid}/neighborhood", response_model=ConceptResponse)
async def get_concept_neighborhood(
    qid: str,
    depth: int = Query(1, ge=1, le=3, description="Profundidad del vecindario"),
) -> ConceptResponse:
    """
    Obtener el vecindario de un concepto: él mismo + sus relaciones
    directas (depth=1) o expandiendo relaciones de relaciones (depth=2+).
    Para construir el grafo de navegación.
    """
    ...


@router.get("/explore/root", response_model=list[Concept])
async def get_root_concepts(
    domain: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
) -> list[Concept]:
    """
    Conceptos raíz para la exploración inicial del grafo.
    Agrupados por dominio si se especifica.
    """
    ...


# ─────────────────────────────────────────────────────────────
# 6. HEALTH / STATUS
# ─────────────────────────────────────────────────────────────

@router.get("/health")
async def health_check() -> dict:
    """Health check del backend."""
    return {"status": "ok", "version": "0.1.0"}
