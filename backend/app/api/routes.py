"""
syswiki — API Routes

Contratos HTTP del backend. Cada endpoint define request/response.
"""

from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Request
from app.models.contracts import (
    ConceptResponse, SearchRequest, SearchResponse,
    CurationRequest, LearningPattern, PipelineStatus,
    Concept, Relation, CuratedStatus,
)

router = APIRouter(prefix="/api/v1", tags=["syswiki"])


# ─────────────────────────────────────────────────────────────
# 1. BÚSQUEDA
# ─────────────────────────────────────────────────────────────

@router.post("/search", response_model=SearchResponse)
async def search_concepts(
    req: SearchRequest,
    request: Request,
) -> SearchResponse:
    """
    Buscar conceptos que coincidan con el texto de consulta.

    Delegado a SearchEngine que orquesta las fuentes según el modo.
    Resultados incluyen QID, título, descripción y si ya fueron analizados.
    """
    return await request.app.state.search_engine.search(req)


@router.get("/search", response_model=SearchResponse)
async def search_concepts_get(
    request: Request,
    q: str = Query(..., min_length=1, description="Texto de búsqueda"),
    mode: str = Query("auto", description="simple | all | best | auto"),
    language: str = Query("es", description="Idioma preferido"),
) -> SearchResponse:
    """Versión GET de búsqueda (para autocomplete rápido)."""
    req = SearchRequest(query=q, mode=mode, language=language)
    return await request.app.state.search_engine.search(req)


# ─────────────────────────────────────────────────────────────
# 2. CONCEPTOS
# ─────────────────────────────────────────────────────────────

@router.get("/concepts/{qid}", response_model=ConceptResponse)
async def get_concept(
    qid: str,
    request: Request,
    language: str = Query("es", description="Idioma preferido"),
) -> ConceptResponse:
    """
    Obtener un concepto con su análisis completo.

    Si el concepto no existe en caché (storage), se busca en las fuentes
    y se guarda. El análisis causal queda vacío hasta que exista el
    Pipeline multi-agente (ver app/agents/base.py) — por ahora se
    devuelve con epistemic_status=indeterminate en las 4 causas.

    Retorna:
      - concept: ficha completa con 4 causas + vista sistémica
      - relations: relaciones con otros conceptos
      - pipeline: estado del pipeline (None hasta que el Pipeline exista)
    """
    storage = request.app.state.storage
    search_engine = request.app.state.search_engine

    concept = await storage.get_concept(qid)
    if concept is None:
        concept = await search_engine.get_concept(qid, language=language)
        if concept is None:
            raise HTTPException(status_code=404, detail=f"Concepto {qid} no encontrado")
        await storage.save_concept(concept)

    relations = await storage.get_relations(qid)
    pipeline = await storage.get_pipeline_status(qid)
    return ConceptResponse(concept=concept, relations=relations, pipeline=pipeline)


@router.get("/concepts/{qid}/relations", response_model=list[Relation])
async def get_concept_relations(
    qid: str,
    request: Request,
    type: Optional[str] = Query(None, description="Filtrar por tipo de relación"),
) -> list[Relation]:
    """Obtener todas las relaciones de un concepto."""
    return await request.app.state.storage.get_relations(qid, relation_type=type)


@router.get("/concepts/{qid}/pipeline", response_model=Optional[PipelineStatus])
async def get_pipeline_status(
    qid: str,
    request: Request,
) -> Optional[PipelineStatus]:
    """
    Consultar el estado del pipeline de análisis para un concepto.
    Útil para polling desde el frontend mientras se procesa.
    """
    return await request.app.state.storage.get_pipeline_status(qid)


# ─────────────────────────────────────────────────────────────
# 3. CURACIÓN
# ─────────────────────────────────────────────────────────────

@router.post("/curate", response_model=ConceptResponse)
async def curate_concept(
    req: CurationRequest,
    request: Request,
) -> ConceptResponse:
    """
    Registrar una curación del usuario sobre un análisis.

    El usuario puede:
      - Confirmar un análisis existente
      - Rechazar (curated_status=rejected) — la regeneración real requiere
        el Pipeline multi-agente, todavía no implementado (TODO).
      - Editar el texto de una causa (summary)
      - Cambiar el estado epistémico de una causa

    Si cause_key es None, la curación aplica a la vista sistémica
    (system_view) en vez de a una causa puntual.
    """
    storage = request.app.state.storage
    concept = await storage.get_concept(req.qid)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concepto {req.qid} no encontrado")

    if req.cause_key is not None:
        if req.cause_key not in concept.causes:
            raise HTTPException(status_code=400, detail=f"Causa inválida: {req.cause_key}")
        cause = concept.causes[req.cause_key]
        if req.summary is not None:
            cause.summary = req.summary
        if req.epistemic_status is not None:
            cause.epistemic_status = req.epistemic_status

    # CauseAnalysis no tiene curated_status propio (solo Concept y Relation
    # lo tienen), así que el estado de curación siempre se registra a nivel
    # de Concept, sea la curación sobre una causa puntual o sobre system_view.
    concept.curated_status = req.curated_status

    # TODO(pipeline): cuando curated_status == rejected, disparar
    # regeneración del análisis vía Pipeline. Sin Pipeline implementado
    # todavía, solo queda registrado el rechazo.

    await storage.save_curation(req)
    await storage.save_concept(concept)

    relations = await storage.get_relations(req.qid)
    pipeline = await storage.get_pipeline_status(req.qid)
    return ConceptResponse(concept=concept, relations=relations, pipeline=pipeline)


# ─────────────────────────────────────────────────────────────
# 4. APRENDIZAJE (para curadores)
# ─────────────────────────────────────────────────────────────

@router.get("/learning/patterns", response_model=list[LearningPattern])
async def get_learning_patterns(request: Request) -> list[LearningPattern]:
    """
    Obtener todos los patrones de aprendizaje del sistema.
    El curador puede ver qué relaciones aprendió el sistema.
    """
    return await request.app.state.storage.get_learning_patterns()


@router.post("/learning/patterns/{pattern_id}/revert")
async def revert_learning_pattern(
    pattern_id: str,
    request: Request,
) -> dict:
    """
    Revertir un patrón aprendido. Útil cuando el sistema
    aprendió una correlación incorrecta.
    """
    storage = request.app.state.storage
    patterns = await storage.get_learning_patterns()
    pattern = next((p for p in patterns if p.id == pattern_id), None)
    if pattern is None:
        raise HTTPException(status_code=404, detail=f"Patrón {pattern_id} no encontrado")

    pattern.is_active = False
    await storage.save_learning_pattern(pattern)
    return {"reverted": pattern_id}


# ─────────────────────────────────────────────────────────────
# 5. EXPLORACIÓN (grafo)
# ─────────────────────────────────────────────────────────────

@router.get("/explore/{qid}/neighborhood", response_model=ConceptResponse)
async def get_concept_neighborhood(
    qid: str,
    request: Request,
    depth: int = Query(1, ge=1, le=3, description="Profundidad del vecindario"),
) -> ConceptResponse:
    """
    Obtener el vecindario de un concepto: él mismo + sus relaciones
    directas (depth=1) o expandiendo relaciones de relaciones (depth=2+).

    NOTA: con NoopStorage no hay relaciones persistidas, así que esto
    devuelve el concepto solo (relations=[]) hasta que exista un storage
    con datos reales. depth > 1 no tiene efecto todavía.
    """
    storage = request.app.state.storage
    concept = await storage.get_concept(qid)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concepto {qid} no encontrado")

    relations = await storage.get_relations(qid)
    pipeline = await storage.get_pipeline_status(qid)
    return ConceptResponse(concept=concept, relations=relations, pipeline=pipeline)


@router.get("/explore/root", response_model=list[Concept])
async def get_root_concepts(
    request: Request,
    domain: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
) -> list[Concept]:
    """
    Conceptos raíz para la exploración inicial del grafo.

    NOTA: con NoopStorage esto solo devuelve lo que se haya buscado/guardado
    en esta misma sesión de proceso (no persiste entre reinicios).
    """
    return await request.app.state.storage.search_concepts(domain or "", limit=limit)


# ─────────────────────────────────────────────────────────────
# 6. HEALTH / STATUS
# ─────────────────────────────────────────────────────────────

@router.get("/health")
async def health_check() -> dict:
    """Health check del backend."""
    return {"status": "ok", "version": "0.1.0"}
