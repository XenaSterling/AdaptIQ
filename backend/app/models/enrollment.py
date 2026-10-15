"""
Módulo: enrollment.py
Descripción: Define el modelo ORM que representa las matrículas
             de usuarios en cursos y evita duplicidades.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Enrollment(Base):
    """
    Representa la matrículación de un usuario en un curso.

    Atributos:
        id (UUID): Identificador único de la matrícula.
        user_id (UUID | None): Identificador del usuario.
        course_id (UUID | None): Identificador del curso.
        user (User): Usuario matriculado.
        course (Course): Curso en el que se matricula.
    """

    __tablename__ = "enrollments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "course_id",
            name="uq_user_course_enrollment"
        ),
    )

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")