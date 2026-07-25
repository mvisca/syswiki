"""
syswiki — Enciclopedia Sistémica
Backend contracts: modelos Pydantic compartidos entre servicios, APIs y agentes.

MVP: no-op storage, Wikipedia como fuente principal, agentes simulados.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ─── Enums ─────────────────────────────────────────────────────

class EpistemicStatus(str, Enum):
    known = "known"              # ✅ Conocido
    partial = "partial"          # ❓ Parcial
    frontier = "frontier"        # ❌ Frontera del conocimiento
    indeterminate = "indeterminate"  # ⬜ Indeterminado


class CuratedStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"
    edited = "edited"


class RelationType(str, Enum):
    component_of = "component_of"           # es_componente_de
    material_cause_of = "material_cause_of"  # es_causa_material_de
    formal_cause_of = "formal_cause_of"      # es_causa_formal_de
    efficient_cause_of = "efficient_cause_of"  # es_causa_eficiente_de
    final_cause_of = "final_cause_of"        # es_causa_final_de


class ExchangeSubstance(str, Enum):
    matter = "matter"        # Materia
    energy = "energy"        # Energía
    information = "information"  # Información
    mixed = "mixed"          # Mixto


class ExchangeLevel(str, Enum):
    sub = "sub"     # Subnivel (entre subsistemas)
    same = "same"   # Mismo nivel (entre pares)
    supra = "supra" # Supranivel (sistema ↔ entorno)


class SearchMode(str, Enum):
    simple = "simple"    # Una fuente específica
    all = "all"          # Todas las fuentes en paralelo
    best = "best"        # Fuente más autoritativa
    auto = "auto"        # Decide según query y contexto


class AgentStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


# ─── Cause Analysis ────────────────────────────────────────────

class CauseAnalysis(BaseModel):
    """Análisis de una de las 4 causas aristotélicas para un concepto."""
    summary: str = ""
    epistemic_status: EpistemicStatus = EpistemicStatus.indeterminate
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)  # URLs de fuentes
    related_qids: list[str] = Field(default_factory=list)
    agent_prompt: str = ""  # Prompt usado para generar este análisis


class SystemAnalysis(BaseModel):
    """Vista del concepto como sistema total."""
    components: list[str] = Field(default_factory=list)  # QIDs subsistemas
    emergent_properties: list[str] = Field(default_factory=list)
    boundaries: str = ""
    environment_qids: list[str] = Field(default_factory=list)
    relationship_ids: list[str] = Field(default_factory=list)


# ─── Exchange / Relation ───────────────────────────────────────

class ExchangePhase(BaseModel):
    """Fase de un intercambio (handshake → intercambio → cierre)."""
    name: str = ""                    # "handshake" | "exchange" | "closure"
    order: int = 0
    description: str = ""
    substances: list[ExchangeSubstance] = Field(default_factory=list)
    sub_relationship_ids: list[str] = Field(default_factory=list)


class Exchange(BaseModel):
    """Intercambio de materia/energía/información entre sistemas."""
    substance: ExchangeSubstance = ExchangeSubstance.information
    phases: list[ExchangePhase] = Field(default_factory=list)
    level: ExchangeLevel = ExchangeLevel.same


class Relation(BaseModel):
    """Relación entre dos conceptos (arista del grafo)."""
    id: str = ""
    type: RelationType = RelationType.component_of
    source_qid: str = ""
    target_qid: str = ""
    exchange: Optional[Exchange] = None
    curated_status: CuratedStatus = CuratedStatus.pending
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ─── Concept ───────────────────────────────────────────────────

class Concept(BaseModel):
    """Unidad fundamental del sistema. Cualquier concepto analizado."""
    qid: str = ""                      # Wikidata QID
    title: str = ""
    aliases: list[str] = Field(default_factory=list)
    language: str = "en"
    source: str = ""                   # "wikipedia" | "arxiv" | ...
    source_url: str = ""
    thumbnail_url: str = ""
    description: str = ""              # Resumen breve

    # Análisis causal-sistémico
    causes: dict[str, CauseAnalysis] = Field(default_factory=lambda: {
        k: CauseAnalysis() for k in ("material", "formal", "efficient", "final")
    })
    system_view: Optional[SystemAnalysis] = None

    # Metadatos
    curated_status: CuratedStatus = CuratedStatus.pending
    epistemic_notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def has_any_analysis(self) -> bool:
        return any(
            c.summary.strip() != "" or c.epistemic_status != EpistemicStatus.indeterminate
            for c in self.causes.values()
        )


# ─── Pipeline / Agent ──────────────────────────────────────────

class AgentTask(BaseModel):
    """Tarea asignada a un agente dentro del pipeline."""
    agent_id: str  # "explorer" | "material" | "formal" | "efficient" | "final" | "systemic" | "synthesizer"
    status: AgentStatus = AgentStatus.pending
    input_data: str = ""
    output_data: str = ""
    confidence: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class PipelineStatus(BaseModel):
    """Estado del pipeline de generación multi-agente."""
    concept_qid: str
    tasks: list[AgentTask] = Field(default_factory=list)
    overall_status: AgentStatus = AgentStatus.pending
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    @property
    def progress(self) -> float:
        if not self.tasks:
            return 0.0
        done = sum(1 for t in self.tasks if t.status == AgentStatus.completed)
        return done / len(self.tasks)


# ─── Search ────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    mode: SearchMode = SearchMode.auto
    source: Optional[str] = None      # Fuente específica
    language: Optional[str] = None
    domain: Optional[str] = None       # Para ponderar fuentes


class SearchResult(BaseModel):
    """Resultado individual de búsqueda."""
    qid: str
    title: str
    description: str = ""
    thumbnail_url: str = ""
    source: str = ""
    language: str = ""
    score: float = 0.0
    already_analyzed: bool = False      # ¿Ya fue procesado por el sistema?


class SearchResponse(BaseModel):
    results: list[SearchResult] = Field(default_factory=list)
    source_used: str = ""
    total_found: int = 0


# ─── Curation ──────────────────────────────────────────────────

class CurationRequest(BaseModel):
    """Curación de un análisis por parte del usuario."""
    qid: str
    cause_key: Optional[str] = None    # "material" | "formal" | "efficient" | "final" | None (para vista sistémica)
    summary: Optional[str] = None
    epistemic_status: Optional[EpistemicStatus] = None
    curated_status: CuratedStatus = CuratedStatus.confirmed


class LearningPattern(BaseModel):
    """Patrón aprendido por el sistema a partir de curaciones."""
    id: str = ""
    trigger: str = ""                  # Ej: "Wikipedia infobox: invented_by"
    suggested_relation: RelationType = RelationType.efficient_cause_of
    confidence: float = 0.0            # 0-1
    confirmation_count: int = 0
    rejection_count: int = 0
    min_confirmations: int = 3         # Mínimo para consolidarse
    is_active: bool = True


# ─── API response envelopes ────────────────────────────────────

class ConceptResponse(BaseModel):
    """Respuesta completa de un concepto analizado."""
    concept: Concept
    relations: list[Relation] = Field(default_factory=list)
    pipeline: Optional[PipelineStatus] = None


class ErrorResponse(BaseModel):
    detail: str
    error_code: str = "UNKNOWN"
