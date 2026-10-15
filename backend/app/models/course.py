"""
Módulo: course.py
Descripción: Define el modelo ORM de los cursos y sus relaciones
             con docentes, módulos, matrículas y evaluaciones.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Course(Base):
    """
    Representa un curso de la aplicación.

    Atributos:
        id (UUID): Identificador único del curso.
        title (str): Título del curso.
        description (str | None): Descripción del curso.
        teacher_id (UUID | None): Identificador del docente responsable.
        teacher (User): Docente asociado al curso.
        modules (list[Module]): Módulos del curso.
        enrollments (list[Enrollment]): Matrículas del curso.
        irt_sessions (list[IRTSession]): Sesiones IRT del curso.
        evaluations (list[Evaluation]): Evaluaciones del curso.
    """

    __tablename__ = "courses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    teacher_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    teacher = relationship("User")
    modules = relationship("Module", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    irt_sessions = relationship("IRTSession", back_populates="course")
    evaluations = relationship("Evaluation", back_populates="course")