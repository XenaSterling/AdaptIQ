"""
Módulo: evaluation.py
Descripción: Define los modelos ORM de las evaluaciones y sus estados,
             incluyendo resultados, configuración y estimaciones de habilidad.
Autor: Raquel Del Castillo Pérez
"""

import uuid
import enum

from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Float,
    DateTime,
    Enum as SqlEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class EvaluationStatus(str, enum.Enum):
    """
    Define los estados posibles de una evaluación.
    """

    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class Evaluation(Base):
    """
    Representa una evaluación realizada por un usuario.

    Atributos:
        id (UUID): Identificador único de la evaluación.
        user_id (UUID): Identificador del usuario que realiza la evaluación.
        course_id (UUID | None): Identificador del curso asociado.
        module_id (UUID | None): Identificador del módulo asociado.
        status (EvaluationStatus): Estado actual de la evaluación.
        current_theta (float | None): Estimación actual de habilidad.
        final_theta (float | None): Estimación final de habilidad.
        score (float | None): Puntuación obtenida.
        started_at (datetime | None): Fecha y hora de inicio.
        finished_at (datetime | None): Fecha y hora de finalización.
        user (User): Usuario que realiza la evaluación.
        course (Course): Curso asociado a la evaluación.
        results (list[Result]): Resultados de la evaluación.
        settings (EvaluationSettings | None): Configuración de la evaluación.
        module (Module): Módulo asociado a la evaluación.
    """

    __tablename__ = "evaluations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id", 
            ondelete="CASCADE"
        ),
        nullable=False
    )

    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "courses.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    module_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "modules.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    status = Column(
        SqlEnum(
            EvaluationStatus,
            name="evaluation_status_enum"
        ),
        nullable=False,
        default=EvaluationStatus.in_progress,
        server_default=EvaluationStatus.in_progress.value
    )

    current_theta = Column(Float, default=0.0)
    final_theta = Column(Float, nullable=True)
    score = Column(Float, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="evaluations")
    course = relationship("Course", back_populates="evaluations")

    results = relationship(
        "Result",
        back_populates="evaluation",
        cascade="all, delete-orphan"
    )

    settings = relationship(
        "EvaluationSettings",
        back_populates="evaluation",
        uselist=False,
        cascade="all, delete-orphan"
    )

    module = relationship("Module", back_populates="evaluations")