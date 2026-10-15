"""
Módulo: evaluation_settings.py
Descripción: Define el modelo ORM que almacena los parámetros
             de configuración de las evaluaciones adaptativas.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class EvaluationSettings(Base):
    """
    Representa la configuración de una evaluación.

    Atributos:
        id (UUID): Identificador único de la configuración.
        evaluation_id (UUID): Identificador de la evaluación asociada.
        min_questions (int | None): Número mínimo de preguntas (por defecto, 10).
        max_questions (int | None): Número máximo de preguntas (por defecto, 50).
        theta_stability_threshold (float | None): Umbral de estabilidad de theta.
        stability_window (int | None): Ventana de estabilidad (por defecto, 2).
        max_uncertainty (float | None): Incertidumbre máxima permitida.
        extra_config (dict | None): Configuración adicional en formato JSON.
        evaluation (Evaluation): Evaluación asociada.
    """

    __tablename__ = "evaluation_settings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    evaluation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("evaluations.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False
    )

    min_questions = Column(Integer, default=10)
    max_questions = Column(Integer, default=50)
    theta_stability_threshold = Column(Float, default=0.05)
    stability_window = Column(Integer, default=2)
    max_uncertainty = Column(Float, default=0.25)

    extra_config = Column(JSONB, nullable=True)

    evaluation = relationship("Evaluation", back_populates="settings")