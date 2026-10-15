"""
Módulo: result.py
Descripción: Define el modelo ORM que almacena los resultados
             de las preguntas respondidas durante una evaluación.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    Float,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Result(Base):
    """
    Representa el resultado de una pregunta en una evaluación.

    Atributos:
        id (UUID): Identificador único del resultado.
        evaluation_id (UUID): Identificador de la evaluación.
        question_id (UUID): Identificador de la pregunta.
        is_correct (bool): Indica si la respuesta es correcta.
        response_time (float | None): Tiempo empleado en responder.
        theta_before (float | None): Habilidad estimada antes de responder.
        theta_after (float | None): Habilidad estimada después de responder.
        question_difficulty (float | None): Dificultad de la pregunta.
        question_discrimination (float | None): Discriminación de la pregunta.
        evaluation (Evaluation): Evaluación asociada.
        question (Question): Pregunta respondida.
        selected_answers (list[ResultAnswer]): Respuestas seleccionadas.
    """

    __tablename__ = "results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    evaluation_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "evaluations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "questions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    is_correct = Column(Boolean, nullable=False)
    response_time = Column(Float, nullable=True)
    theta_before = Column(Float, nullable=True)
    theta_after = Column(Float, nullable=True)
    question_difficulty = Column(Float, nullable=True)
    question_discrimination = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "evaluation_id",
            "question_id",
            name="uq_evaluation_question"
        ),
    )

    evaluation = relationship("Evaluation", back_populates="results")
    question = relationship("Question", back_populates="results")

    selected_answers = relationship(
        "ResultAnswer",
        back_populates="result",
        cascade="all, delete-orphan"
    )