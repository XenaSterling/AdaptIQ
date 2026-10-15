"""
Módulo: module.py
Descripción: Define el modelo ORM de los módulos formativos
             y sus relaciones con cursos y contenidos educativos.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Module(Base):
    """
    Representa un módulo perteneciente a un curso.

    Atributos:
        id (UUID): Identificador único del módulo.
        title (str): Título del módulo.
        order_index (int | None): Posición del módulo en el curso.
        course_id (UUID): Identificador del curso al que pertenece.
        course (Course): Curso asociado al módulo.
        questions (list[Question]): Preguntas del módulo.
        learning_resources (list[LearningResource]): Recursos educativos.
        progress (list[ModuleProgress]): Registros de progreso.
        evaluations (list[Evaluation]): Evaluaciones asociadas al módulo.
    """

    __tablename__ = "modules"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(String, nullable=False)
    order_index = Column(Integer, default=0)

    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id"),
        nullable=False
    )

    course = relationship("Course", back_populates="modules")

    questions = relationship(
        "Question",
        back_populates="module",
        cascade="all, delete-orphan"
    )

    learning_resources = relationship(
        "LearningResource",
        back_populates="module",
        cascade="all, delete-orphan"
    )

    progress = relationship(
        "ModuleProgress",
        back_populates="module",
        cascade="all, delete-orphan"
    )

    evaluations = relationship("Evaluation", back_populates="module")