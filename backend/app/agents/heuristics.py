"""
syswiki — Agentes heurísticos (sin LLM)

Implementación inicial de los 7 agentes del pipeline usando pattern
matching léxico sobre el texto del artículo. Confidence siempre baja
(0.2-0.3) y epistemic_status=partial para dejar explícito que esto no
es análisis real, sino una primera aproximación reemplazable por
agentes con inferencia LLM sin cambiar la interfaz (BaseAgent.analyze).
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from app.agents.base import BaseAgent
from app.models.contracts import (
    Concept, CauseAnalysis, AgentTask, AgentStatus, EpistemicStatus,
)


def _find_sentence(text: str, keywords: list[str]) -> Optional[str]:
    """Primera oración que contenga alguno de los keywords (case-insensitive)."""
    for sentence in text.split(". "):
        lowered = sentence.lower()
        if any(kw in lowered for kw in keywords):
            return sentence.strip().rstrip(".") + "."
    return None


def _run_cause_heuristic(
    task: AgentTask,
    article_text: str,
    keywords: list[str],
    agent_prompt: str,
) -> AgentTask:
    """Lógica compartida por los 4 agentes causales: buscar oración clave."""
    task.status = AgentStatus.running
    task.started_at = datetime.now(timezone.utc)

    sentence = _find_sentence(article_text, keywords)
    if sentence:
        task.output_data = sentence
        task.confidence = 0.3
    else:
        task.output_data = ""
        task.confidence = 0.0

    task.status = AgentStatus.completed
    task.completed_at = datetime.now(timezone.utc)
    return task


class ExplorerAgent(BaseAgent):
    """Provee el texto crudo del artículo a los demás agentes (sin análisis)."""

    AGENT_ID = "explorer"

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        task.status = AgentStatus.running
        task.started_at = datetime.now(timezone.utc)
        task.output_data = article_text
        task.confidence = 1.0  # dato crudo, no inferencia
        task.status = AgentStatus.completed
        task.completed_at = datetime.now(timezone.utc)
        return task


class MaterialAgent(BaseAgent):
    """Causa material: ¿de qué está hecho / compuesto el concepto?"""

    AGENT_ID = "material"
    KEYWORDS = [
        "compuest", "formad", "se compone de",
        "made of", "composed of", "consists of",
    ]

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        return _run_cause_heuristic(
            task, article_text, self.KEYWORDS,
            agent_prompt="heurística: regex sobre keywords de composición material",
        )


class FormalAgent(BaseAgent):
    """Causa formal: ¿qué es / a qué categoría o forma pertenece?"""

    AGENT_ID = "formal"
    KEYWORDS = [
        "es un tipo de", "es una clase de", "tipo de", "categoría de",
        "is a type of", "is a kind of", "is a class of",
    ]

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        return _run_cause_heuristic(
            task, article_text, self.KEYWORDS,
            agent_prompt="heurística: regex sobre keywords de categoría/tipo",
        )


class EfficientAgent(BaseAgent):
    """Causa eficiente: ¿quién o qué lo originó / produjo?"""

    AGENT_ID = "efficient"
    KEYWORDS = [
        "descubiert", "inventad", "cread", "desarrollad",
        "discovered by", "invented by", "created by", "developed by",
    ]

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        return _run_cause_heuristic(
            task, article_text, self.KEYWORDS,
            agent_prompt="heurística: regex sobre keywords de origen/autoría",
        )


class FinalAgent(BaseAgent):
    """Causa final: ¿para qué existe / cuál es su propósito?"""

    AGENT_ID = "final"
    KEYWORDS = [
        "se utiliza para", "sirve para", "tiene como propósito", "utilizad",
        "used for", "purpose of", "used to",
    ]

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        return _run_cause_heuristic(
            task, article_text, self.KEYWORDS,
            agent_prompt="heurística: regex sobre keywords de propósito/uso",
        )


class SystemicAgent(BaseAgent):
    """
    Vista sistémica: heurística mínima, solo toma la primera oración del
    artículo como aproximación a los "límites" (boundaries) del sistema.
    Sin inferencia real, components/emergent_properties quedan vacíos.
    """

    AGENT_ID = "systemic"

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        task.status = AgentStatus.running
        task.started_at = datetime.now(timezone.utc)

        first_sentence = article_text.split(". ")[0].strip() if article_text else ""
        task.output_data = first_sentence
        task.confidence = 0.2 if first_sentence else 0.0

        task.status = AgentStatus.completed
        task.completed_at = datetime.now(timezone.utc)
        return task


class SynthesizerAgent(BaseAgent):
    """
    Combina el resultado de los agentes previos. En esta etapa heurística
    no fusiona contenido (eso lo hace Pipeline.run() al armar el Concept),
    solo valida que las tareas previas hayan terminado y resume su
    confidence promedio como propia.
    """

    AGENT_ID = "synthesizer"

    async def analyze(
        self, concept: Concept, article_text: str, task: AgentTask,
    ) -> AgentTask:
        task.status = AgentStatus.running
        task.started_at = datetime.now(timezone.utc)
        task.output_data = "synthesis"
        task.confidence = 0.0
        task.status = AgentStatus.completed
        task.completed_at = datetime.now(timezone.utc)
        return task
