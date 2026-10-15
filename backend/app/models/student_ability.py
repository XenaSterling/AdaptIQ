"""
Módulo: student_ability.py
Descripción: Define el modelo ORM que almacena la estimación
             de habilidad de cada estudiante.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy import Column, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class StudentAbility(Base):
    """
    Representa la habilidad estimada de un estudiante.

    Atributos:
        user_id (UUID): Identificador del usuario.
        theta (float | None): Estimación de habilidad del estudiante.
        updated_at (datetime | None): Fecha de la última actualización.
        user (User): Usuario asociado a la estimación.
    """

    __tablename__ = "student_abilities"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True
    )

    theta = Column(Float, default=0.0)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="ability")