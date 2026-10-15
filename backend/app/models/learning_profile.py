"""
Módulo: learning_profile.py
Descripción: Define el modelo ORM que almacena las preferencias
             de aprendizaje de cada usuario.
Autor: Raquel Del Castillo Pérez
"""

import uuid
import enum

from sqlalchemy import Column, Enum as SqlEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class LearningStyle(str, enum.Enum):
    """
    Define los estilos de aprendizaje disponibles.
    """

    visual = "visual"
    auditory = "auditory"
    reading = "reading"
    kinesthetic = "kinesthetic"


class LearningProfile(Base):
    """
    Representa el perfil de aprendizaje de un usuario.

    Atributos:
        user_id (UUID): Identificador del usuario y clave primaria.
        learning_style (LearningStyle): Estilo de aprendizaje preferido.
        preferred_difficulty_growth (LearningStyle | None): Preferencia
            de progresión de dificultad.
        user (User): Usuario asociado al perfil.
    """

    __tablename__ = "learning_profiles"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True
    )

    learning_style = Column(
        SqlEnum(
            LearningStyle,
            name="learning_style_enum"
        ),
        nullable=False,
        default=LearningStyle.visual
    )

    preferred_difficulty_growth = Column(
        SqlEnum(
            LearningStyle,
            name="difficulty_growth_enum"
        ),
        nullable=True
    )

    user = relationship("User", back_populates="learning_profile")