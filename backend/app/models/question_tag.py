"""
Módulo: question_tag.py
Descripción: Define el modelo ORM que relaciona preguntas
             con etiquetas mediante una tabla intermedia.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class QuestionTag(Base):
    """
    Representa la asociación entre una pregunta y una etiqueta.

    Atributos:
        question_id (UUID): Identificador de la pregunta.
        tag_id (UUID): Identificador de la etiqueta.
        question (Question): Pregunta asociada.
        tag (Tag): Etiqueta asociada.
    """

    __tablename__ = "question_tags"

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("questions.id"),
        primary_key=True
    )

    tag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        primary_key=True
    )

    question = relationship("Question", back_populates="tags")
    tag = relationship("Tag", back_populates="questions")