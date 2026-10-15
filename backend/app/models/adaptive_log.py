"""
Módulo: adaptive_log.py
Descripción: Define el modelo ORM que registra las interacciones
             y métricas del sistema de evaluación adaptativa.
Autor: Raquel Del Castillo Pérez
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class AdaptiveLog(Base):
    """ 
    Representa un registro de actividad de una evaluación adaptativa.

    Atributos:
        id (UUID): Identificador único del registro.
        user_id (UUID): Identificador del usuario.
        evaluation_id (UUID): Identificador de la evaluación.
        question_id (UUID): Identificador de la pregunta.
        theta_before (float | None): Habilidad estimada antes de responder.
        theta_after (float | None): Habilidad estimada después de responder.
        correct (bool): Indica si la respuesta es correcta.
        fisher_information (float | None): Información de Fisher.
        difficulty_gap (float | None): Diferencia de dificultad.
        exploration_bonus (float | None): Bonificación de exploración.
        final_score (float | None): Puntuación final calculada.
        timestamp (datetime | None): Fecha y hora del registro. 
    """
    
    __tablename__ = "adaptive_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    evaluation_id = Column(UUID(as_uuid=True), nullable=False)
    question_id = Column(UUID(as_uuid=True), nullable=False)

    theta_before = Column(Float)
    theta_after = Column(Float)

    correct = Column(Boolean, nullable=False)

    fisher_information = Column(Float)
    difficulty_gap = Column(Float)
    exploration_bonus = Column(Float)
    final_score = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)