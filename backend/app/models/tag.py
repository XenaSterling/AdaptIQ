"""
Módulo: tag.py
Descripción: Define el modelo ORM de las etiquetas utilizadas
             para clasificar preguntas y recursos educativos.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tag(Base):
    """
    Representa una etiqueta clasificatoria.

    Atributos:
        id (UUID): Identificador único de la etiqueta.
        name (str): Nombre único de la etiqueta.
        questions (list[QuestionTag]): Asociaciones con preguntas.
        resources (list[ResourceTag]): Asociaciones con recursos educativos.
    """

    __tablename__ = "tags"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, unique=True, nullable=False)

    questions = relationship("QuestionTag", back_populates="tag")
    resources = relationship(
        "ResourceTag",
        back_populates="tag",
        cascade="all, delete-orphan"
    )