"""
syswiki — Base Agent (abstract interface)

Todos los agentes del pipeline heredan de esta clase.
Cada agente analiza un concepto desde una perspectiva específica.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from app.models.contracts import (
    Concept, CauseAnalysis, SystemAnalysis,
    AgentTask, PipelineStatus,
)


class BaseAgent(ABC):
    """Agente base. Cada subclase implementa analyze()."""

    AGENT_ID: str = ""  # Sobreescribir en subclases

    @abstractmethod
    async def analyze(
        self,
        concept: Concept,
        article_text: str,
        task: AgentTask,
    ) -> AgentTask:
        """
        Analizar un concepto desde la perspectiva del agente.
        Recibe el concepto parcial y el texto crudo del artículo.
        Devuelve el task actualizado con output y confidence.
        """
        ...

    @classmethod
    def create_initial_task(cls, input_data: str = "") -> AgentTask:
        return AgentTask(
            agent_id=cls.AGENT_ID,
            status="pending",
            input_data=input_data,
        )


class Pipeline:
    """
    Orquestador del pipeline multi-agente.

    Flujo:
      1. Explorador (fetch article from source)
      2. 4 agentes de causa en paralelo (material, formal, efficient, final)
      3. Agente sistémico
      4. Sintetizador (combina todo en una ficha coherente)
    """

    AGENT_ORDER = [
        "explorer",
        "material", "formal", "efficient", "final",  # paralelo
        "systemic",
        "synthesizer",
    ]

    def __init__(
        self,
        material_agent: BaseAgent,
        formal_agent: BaseAgent,
        efficient_agent: BaseAgent,
        final_agent: BaseAgent,
        explorer_agent: BaseAgent,
        systemic_agent: BaseAgent,
        synthesizer_agent: BaseAgent,
    ):
        self.agents = {
            "explorer": explorer_agent,
            "material": material_agent,
            "formal": formal_agent,
            "efficient": efficient_agent,
            "final": final_agent,
            "systemic": systemic_agent,
            "synthesizer": synthesizer_agent,
        }

    async def run(
        self,
        concept: Concept,
        article_text: str,
    ) -> PipelineStatus:
        """
        Ejecutar pipeline completo para un concepto.
        Retorna el estado final con todos los análisis.
        """
        ...

    async def get_status(self, qid: str) -> Optional[PipelineStatus]:
        """Obtener estado del pipeline en ejecución."""
        ...

    def _validate_agent_order(self) -> None:
        missing = [aid for aid in self.AGENT_ORDER if aid not in self.agents]
        if missing:
            raise ValueError(f"Missing agents: {missing}")
