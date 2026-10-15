"""
Módulo: question.py
Descripción: Define el modelo ORM de las preguntas, sus parámetros
             de dificultad y discriminación, y sus relaciones.
Autor: Raquel Del Castillo Pérez
"""

import uuid
import enum

from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    Enum as SqlEnum,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class QuestionType(str, enum.Enum):
    """
    Define las modalidades de respuesta de una pregunta.
    """

    single = "single"
    multiple = "multiple"


class Question(Base):
    """
    Representa una pregunta de un módulo formativo.

    Atributos:
        id (UUID): Identificador único de la pregunta.
        module_id (UUID | None): Identificador del módulo asociado.
        content (str): Enunciado de la pregunta.
        type (QuestionType): Modalidad de respuesta.
        difficulty (float | None): Parámetro de dificultad (por defecto, 0.0).
        discrimination (float | None): Parámetro de discriminación
            (por defecto, 1.0).
        bloom_level (str | None): Nivel de la taxonomía de Bloom.
        module (Module | None): Módulo asociado.
        answers (list[Answer]): Respuestas disponibles.
        results (list[Result]): Resultados asociados a la pregunta.
        tags (list[QuestionTag]): Etiquetas asociadas.
        recommendations (list[Recommendation]): Recomendaciones asociadas.
    """

    __tablename__ = "questions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    module_id = Column(
        UUID(as_uuid=True),
        ForeignKey("modules.id"),
        nullable=True
    )

    content = Column(String, nullable=False)

    type = Column(
        SqlEnum(QuestionType, name="question_type_enum"),
        nullable=False,
        default=QuestionType.single,
        server_default=QuestionType.single.value
    )

    difficulty = Column(Float, default=0.0)
    discrimination = Column(Float, default=1.0)
    bloom_level = Column(String, nullable=True)

    module = relationship("Module", back_populates="questions")
    
    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    results = relationship("Result", back_populates="question")

    tags = relationship(
        "QuestionTag",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "difficulty >= -4.0 AND difficulty <= 4.0"
        ),
        CheckConstraint(
            "discrimination >= 0.1 AND discrimination <= 3.0"
        ),
    )