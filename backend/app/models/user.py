"""
Módulo: user.py
Descripción: Define el modelo ORM de los usuarios y sus relaciones
             con evaluaciones, cursos, recursos y perfiles de aprendizaje.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    """
    Representa un usuario de la aplicación.

    Atributos:
        id (UUID): Identificador único del usuario.
        name (str): Nombre del usuario.
        email (str): Correo electrónico único.
        password_hash (str): Hash de la contraseña.
        role (int): Identificador del rol asignado.
        learning_style (str | None): Estilo de aprendizaje del usuario.
        is_active (bool | None): Indica si la cuenta está activa.
        role_rel (Role): Rol asociado al usuario.
        evaluations (list[Evaluation]): Evaluaciones realizadas.
        enrollments (list[Enrollment]): Matrículas del usuario.
        irt_sessions (list[IRTSession]): Sesiones IRT del usuario.
        ability (StudentAbility | None): Habilidad estimada.
        recommendations (list[Recommendation]): Recomendaciones recibidas.
        module_progress (list[ModuleProgress]): Progreso en los módulos.
        learning_profile (LearningProfile | None): Perfil de aprendizaje.
        learning_resources (list[LearningResource]): Recursos creados.
        resource_usage (list[ResourceUsage]): Registros de uso de recursos.
    """

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(ForeignKey("roles.id"), nullable=False)
    learning_style = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    role_rel = relationship("Role", back_populates="users")

    evaluations = relationship(
        "Evaluation",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    irt_sessions = relationship(
        "IRTSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    ability = relationship(
        "StudentAbility",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    module_progress = relationship(
        "ModuleProgress",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    learning_profile = relationship(
        "LearningProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    learning_resources = relationship(
        "LearningResource",
        back_populates="creator",
        cascade="all, delete-orphan"
    )

    resource_usage = relationship(
        "ResourceUsage",
        back_populates="user",
        cascade="all, delete-orphan"
    )