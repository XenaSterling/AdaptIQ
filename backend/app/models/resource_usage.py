"""
Módulo: resource_usage.py
Descripción: Define el modelo ORM que registra el uso de los recursos
             educativos por parte de los usuarios.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ResourceUsage(Base):
    """
    Representa el uso de un recurso educativo por un usuario.

    Atributos:
        id (UUID): Identificador único del registro.
        user_id (UUID): Identificador del usuario.
        resource_id (UUID): Identificador del recurso.
        opened_at (datetime | None): Fecha y hora de apertura.
        completed (bool | None): Indica si se completó el recurso.
        time_spent (float | None): Tiempo dedicado al recurso.
        user (User): Usuario que utiliza el recurso.
        resource (LearningResource): Recurso utilizado.
    """

    __tablename__ = "resource_usage"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    resource_id = Column(
        UUID(as_uuid=True),
        ForeignKey("learning_resources.id"),
        nullable=False
    )

    opened_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    time_spent = Column(Float, nullable=True)

    user = relationship("User", back_populates="resource_usage")
    resource = relationship(
        "LearningResource",
        back_populates="resource_usage"
    )