"""
Módulo: learning_resource.py
Descripción: Define el modelo ORM de los recursos educativos
             y sus relaciones con módulos, usuarios y etiquetas.
Autor: Raquel Del Castillo Pérez
"""

import uuid
import enum

from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey,
    Enum as SqlEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ResourceType(str, enum.Enum):
    """
    Define los tipos de recursos educativos disponibles.
    """

    video = "video"
    article = "article"
    pdf = "pdf"
    exercise = "exercise"


class LearningResource(Base):
    """
    Representa un recurso educativo de la aplicación.

    Atributos:
        id (UUID): Identificador único del recurso.
        title (str): Título del recurso.
        description (str | None): Descripción del recurso.
        url (str): URL del recurso.
        type (ResourceType): Tipo de recurso educativo.
        difficulty (float | None): Nivel de dificultad estimado.
        estimated_time (float | None): Tiempo estimado de realización.
        module_id (UUID | None): Identificador del módulo asociado.
        created_by (UUID | None): Identificador del usuario creador.
        module (Module | None): Módulo asociado al recurso.
        creator (User | None): Usuario que creó el recurso.
        tags (list[ResourceTag]): Etiquetas asociadas al recurso.
        resource_usage (list[ResourceUsage]): Registros de uso del recurso.
    """

    __tablename__ = "learning_resources"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    url = Column(String, nullable=False)

    type = Column(
        SqlEnum(
            ResourceType,
            name="resource_type_enum"
        ),
        nullable=False
    )

    difficulty = Column(Float, default=0.0)
    estimated_time = Column(Float, nullable=True)

    module_id = Column(
        UUID(as_uuid=True),
        ForeignKey("modules.id"),
        nullable=True
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    module = relationship("Module", back_populates="learning_resources")
    creator = relationship("User", back_populates="learning_resources")

    tags = relationship(
        "ResourceTag",
        back_populates="resource",
        cascade="all, delete-orphan"
    )

    resource_usage = relationship(
        "ResourceUsage",
        back_populates="resource",
        cascade="all, delete-orphan"
    )