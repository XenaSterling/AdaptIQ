"""
Módulo: answer.py
Descripción: Define el modelo ORM que representa las respuestas
             asociadas a las preguntas.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Answer(Base):
    """
    Representa una respuesta asociada a una pregunta.

    Atributos:
        id (UUID): Identificador único de la respuesta.
        question_id (UUID): Identificador de la pregunta asociada.
        content (str): Contenido de la respuesta.
        is_correct (bool): Indica si la respuesta es correcta.
        question (Question): Pregunta a la que pertenece la respuesta.
    """

    __tablename__ = "answers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    content = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="answers")