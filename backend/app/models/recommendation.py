"""
Módulo: recommendation.py
Descripción: Define el modelo ORM que almacena las recomendaciones
             de preguntas y el seguimiento de su interacción por el usuario.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from datetime import datetime

from sqlalchemy import Column, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Recommendation(Base):
    """
    Representa una recomendación de pregunta para un usuario.

    Atributos:
        id (UUID): Identificador único de la recomendación.
        user_id (UUID): Identificador del usuario.
        question_id (UUID): Identificador de la pregunta recomendada.
        score (float): Puntuación de la recomendación.
        created_at (datetime): Fecha de creación.
        viewed (bool): Indica si la recomendación ha sido visualizada.
        accepted (bool): Indica si la recomendación ha sido aceptada.
        user (User): Usuario destinatario.
        question (Question): Pregunta recomendada.
    """

    __tablename__ = "recommendations"

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
    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False
    )

    score = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    viewed = Column(Boolean, default=False, nullable=False)
    accepted = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates = "recommendations")
    question = relationship(
        "Question",
        back_populates = "recommendations"
    )