"""
Módulo: resource_tag.py
Descripción: Define el modelo ORM que relaciona recursos educativos
             con etiquetas mediante una tabla intermedia.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ResourceTag(Base):
    """
    Representa la asociación entre un recurso educativo y una etiqueta.

    Atributos:
        resource_id (UUID): Identificador del recurso.
        tag_id (UUID): Identificador de la etiqueta.
        resource (LearningResource): Recurso asociado.
        tag (Tag): Etiqueta asociada.
    """

    __tablename__ = "resource_tags"

    resource_id = Column(
        UUID(as_uuid=True),
        ForeignKey("learning_resources.id"),
        primary_key=True
    )

    tag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        primary_key=True
    )

    resource = relationship("LearningResource", back_populates="tags")
    tag = relationship("Tag", back_populates="resources")