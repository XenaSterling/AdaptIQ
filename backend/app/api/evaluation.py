"""
Módulo: evaluation.py
Descripción: Define los endpoints para iniciar evaluaciones adaptativas
             y registrar respuestas de los estudiantes, verificando
             que cada usuario opere únicamente sobre sus evaluaciones.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import require_student
from app.schemas.evaluation import (
    StartEvaluationResponse,
    AnswerQuestionRequest,
    AnswerQuestionResponse
)
from app.services.evaluation_service import (
    start_evaluation_service,
    answer_question_service
)


router = APIRouter(
    prefix="/evaluation",
    tags=["evaluation"]
)


@router.get(
    "/start/{user_id}",
    response_model=StartEvaluationResponse
)
def start_evaluation(
    user_id: str,
    course_id: str | None = None,
    current_user=Depends(require_student()),
    db: Session = Depends(get_db)
):
    """
    Inicia una evaluación para un estudiante.

    Args:
        user_id (str): Identificador del estudiante.
        course_id (str | None): Identificador opcional del curso.
        current_user: Datos del estudiante autenticado.
        db (Session): Sesión de base de datos.

    Returns:
        StartEvaluationResponse: Identificadores de la evaluación
            y de la sesión IRT, habilidad estimada y primera pregunta.

    Raises:
        HTTPException: Si el estudiante intenta iniciar una evaluación
            para otro usuario, devuelve el estado 403.
    """

    authenticated_user_id = str(current_user.get("sub"))
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot start an evaluation for another student"
        )
    return start_evaluation_service(
        db,
        user_id,
        course_id
    )


@router.post(
    "/answer/{user_id}",
    response_model=AnswerQuestionResponse
)
def answer_question(
    user_id: str,
    question_id: str,
    payload: AnswerQuestionRequest,
    current_user=Depends(require_student()),
    db: Session = Depends(get_db)
):
    """
    Registra la respuesta de un estudiante a una pregunta.

    Args:
        user_id (str): Identificador del estudiante.
        question_id (str): Identificador de la pregunta respondida.
        payload (AnswerQuestionRequest): Datos de la respuesta enviada.
        current_user: Datos del estudiante autenticado.
        db (Session): Sesión de base de datos.

    Returns:
        AnswerQuestionResponse: Resultado de la respuesta, habilidad
            estimada y datos de la siguiente pregunta o finalización.

    Raises:
        HTTPException: Si el estudiante intenta responder una evaluación
            en nombre de otro usuario, devuelve el estado 403.
    """

    authenticated_user_id = str(current_user.get("sub"))
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot answer an evaluation for another student"
        )
    return answer_question_service(
        db,
        user_id,
        question_id,
        payload
    )