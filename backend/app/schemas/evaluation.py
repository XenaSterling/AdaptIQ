"""
Módulo: evaluation.py
Descripción: Define los esquemas de solicitud y respuesta para iniciar
             evaluaciones, presentar preguntas y registrar respuestas
             durante el proceso de evaluación adaptativa.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from app.schemas.shared import AnswerPublic
from app.schemas.feedback import FeedbackResponse


class QuestionResponse(BaseModel):
    """
    Define los datos de respuesta de una pregunta.

    Atributos:
        id (UUID): Identificador único de la pregunta.
        content (str): Contenido o enunciado de la pregunta.
        type (str): Tipo de pregunta.
        answers (List[AnswerPublic]): Lista de respuestas disponibles
            para la pregunta.
    """

    id: UUID
    content: str
    type: str
    answers: List[AnswerPublic]


class StartEvaluationResponse(BaseModel):
    """
    Define los datos de respuesta al iniciar una evaluación.

    Atributos:
        evaluation_id (UUID): Identificador único de la evaluación.
        irt_session_id (UUID): Identificador de la sesión del modelo IRT.
        theta (float): Valor inicial de la habilidad estimada.
        question (QuestionResponse): Primera pregunta de la evaluación.
    """

    evaluation_id: UUID
    irt_session_id: UUID
    theta: float
    question: QuestionResponse


class AnswerQuestionRequest(BaseModel):
    """
    Define los datos necesarios para responder una pregunta.

    Atributos:
        selected_answer_ids (List[UUID]): Identificadores de las
            respuestas seleccionadas por el usuario.
        response_time (Optional[float]): Tiempo empleado en responder
            la pregunta, si está disponible.
    """

    selected_answer_ids: List[UUID]
    response_time: Optional[float] = None


class AnswerQuestionResponse(BaseModel):
    """
    Define los datos de respuesta tras registrar una respuesta
    durante una evaluación.

    Atributos:
        question (Optional[QuestionResponse]): Siguiente pregunta de
            la evaluación, si corresponde.
        theta (float): Valor actualizado de la habilidad estimada.
        correct (Optional[bool]): Indica si la respuesta fue correcta.
        finished (Optional[bool]): Indica si la evaluación ha finalizado.
        final_theta (Optional[float]): Valor final de la habilidad
            estimada al terminar la evaluación.
        score (Optional[float]): Puntuación obtenida en la evaluación.
        feedback (Optional[FeedbackResponse]): Retroalimentación
            generada a partir del rendimiento del usuario.
    """

    question: Optional[QuestionResponse]
    theta: float
    correct: Optional[bool]
    finished: Optional[bool]
    final_theta: Optional[float]
    score: Optional[float] = None
    feedback: Optional[FeedbackResponse] = None
