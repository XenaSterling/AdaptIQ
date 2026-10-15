"""
Módulo: result_answer.py
Descripción: Define el modelo ORM que relaciona los resultados
             de las evaluaciones con las respuestas seleccionadas.
Autor: Raquel Del Castillo Pérez
"""

import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ResultAnswer(Base):
    """
    Representa una respuesta seleccionada en un resultado.

    Atributos:
        id (UUID): Identificador único del registro.
        result_id (UUID): Identificador del resultado.
        answer_id (UUID): Identificador de la respuesta seleccionada.
        result (Result): Resultado al que pertenece la selección.
        answer (Answer): Respuesta seleccionada.
    """

    __tablename__ = "result_answers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    result_id = Column(
        UUID(as_uuid=True),
        ForeignKey("results.id", ondelete="CASCADE"),
        nullable=False
    )
    answer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("answers.id"),
        nullable=False
    )

    result = relationship("Result", back_populates="selected_answers")
    answer = relationship("Answer")