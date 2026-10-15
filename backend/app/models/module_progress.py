"""
Módulo: module_progress.py
Descripción: Define el modelo ORM que registra el progreso
             de los usuarios en los módulos formativos.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    Float,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ModuleProgress(Base):
    """
    Representa el progreso de un usuario en un módulo.

    Atributos:
        id (UUID): Identificador único del registro.
        user_id (UUID): Identificador del usuario.
        module_id (UUID): Identificador del módulo.
        completed (bool | None): Indica si el módulo está completado.
        progress_percentage (float | None): Porcentaje de progreso.
        updated_at (datetime | None): Fecha y hora de actualización.
        user (User): Usuario asociado al progreso.
        module (Module): Módulo asociado al progreso.
    """

    __tablename__ = "module_progress"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    module_id = Column(
        UUID(as_uuid=True),
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False
    )

    completed = Column(Boolean, default=False)
    progress_percentage = Column(Float, default=0.0)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "module_id",
            name="uq_user_module_progress"
        ),
    )

    user = relationship("User", back_populates="module_progress")
    module = relationship("Module", back_populates="progress")