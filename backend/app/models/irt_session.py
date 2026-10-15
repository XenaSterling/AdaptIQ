"""
Módulo: irt_session.py
Descripción: Define el modelo ORM que registra las sesiones IRT
             y la evolución de la habilidad estimada del usuario.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class IRTSession(Base):
    """
    Representa una sesión de estimación de habilidad mediante IRT.

    Atributos:
        id (UUID): Identificador único de la sesión.
        user_id (UUID): Identificador del usuario.
        course_id (UUID | None): Identificador del curso asociado.
        theta_start (float | None): Habilidad estimada al inicio.
        theta_end (float | None): Habilidad estimada al finalizar.
        started_at (datetime): Fecha y hora de inicio.
        finished_at (datetime | None): Fecha y hora de finalización.
        user (User): Usuario asociado a la sesión.
        course (Course | None): Curso asociado a la sesión.
    """

    __tablename__ = "irt_sessions"

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

    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id"),
        nullable=True
    )

    theta_start = Column(Float, default=0.0)
    theta_end = Column(Float, nullable=True)

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    finished_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="irt_sessions")
    course = relationship("Course", back_populates="irt_sessions")