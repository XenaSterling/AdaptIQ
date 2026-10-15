"""
Módulo: recommendations.py
Descripción: Define los endpoints para obtener recomendaciones
             personalizadas de preguntas y recursos de aprendizaje,
             así como los datos del panel de recomendaciones del usuario.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import get_current_user
from app.services.recommendation_service import (
    get_question_recommendations,
    get_resource_recommendations_service,
    get_recommendation_dashboard_service
)
from app.schemas.recommendation import (
    QuestionRecommendationResponse,
    ResourceRecommendationResponse
)


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)


@router.get(
    "/questions/me",
    response_model=QuestionRecommendationResponse
)
def get_recommendations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtiene recomendaciones personalizadas de preguntas para el usuario.

    Args:
        db (Session): Sesión de base de datos.
        current_user: Datos del usuario autenticado.

    Returns:
        QuestionRecommendationResponse: Habilidad estimada, nivel,
            precisión, etiquetas débiles y preguntas recomendadas.
    """

    return get_question_recommendations(
        db,
        current_user["sub"]
    )


@router.get(
    "/resources/me",
    response_model=ResourceRecommendationResponse
)
def get_resource_recommendations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtiene recomendaciones personalizadas de recursos de aprendizaje.

    Args:
        db (Session): Sesión de base de datos.
        current_user: Datos del usuario autenticado.

    Returns:
        ResourceRecommendationResponse: Habilidad estimada y lista
            de recursos recomendados con sus motivos.
    """

    return get_resource_recommendations_service(
        db,
        current_user["sub"]
    )


@router.get("/dashboard/me")
def get_recommendation_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtiene los datos del panel de recomendaciones del usuario.

    Args:
        db (Session): Sesión de base de datos.
        current_user: Datos del usuario autenticado.

    Returns:
        dict: Datos del panel de recomendaciones generados por el servicio.
    """

    return get_recommendation_dashboard_service(
        db,
        current_user["sub"]
    )