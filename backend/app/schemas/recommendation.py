"""
Módulo: recommendation.py
Descripción: Define los esquemas de respuesta de las recomendaciones
             personalizadas de preguntas y recursos de aprendizaje,
             incluyendo los motivos que justifican cada recomendación.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID


class PeerContext(BaseModel):
    """
    Define el contexto de beneficio obtenido por usuarios similares.

    Atributos:
        similar_users_benefited (bool): Indica si usuarios similares
            se han beneficiado del recurso.
        avg_improvement_after_resource (float): Mejora media observada
            después de utilizar el recurso.
    """

    similar_users_benefited: bool
    avg_improvement_after_resource: float


class RecommendationReason(BaseModel):
    """
    Define los motivos y criterios que justifican una recomendación.

    Atributos:
        explanation (str): Explicación de la recomendación.
        reason_type (str): Tipo de motivo de la recomendación.
        confidence (float): Nivel de confianza de la recomendación.
        difficulty_gap (float | None): Diferencia de dificultad entre
            el nivel estimado y el elemento recomendado.
        theta_match (bool | None): Indica si el elemento se ajusta
            al valor de theta del usuario.
        weak_tags (List[str]): Lista de etiquetas relacionadas con
            los temas en los que el usuario presenta dificultades.
        peer_context (PeerContext): Contexto de los resultados obtenidos
            por usuarios similares.
    """

    explanation: str
    reason_type: str
    confidence: float
    difficulty_gap: float | None = None
    theta_match: bool | None = None
    weak_tags: List[str] = []
    peer_context: PeerContext


class QuestionRecommendationItem(BaseModel):
    """
    Define los datos de una pregunta recomendada.

    Atributos:
        id (UUID): Identificador único de la pregunta.
        content (str): Contenido o enunciado de la pregunta.
        difficulty (float): Nivel de dificultad de la pregunta.
        module_id (UUID): Identificador del módulo al que pertenece.
        tags (List[str]): Lista de etiquetas asociadas a la pregunta.
        reason (RecommendationReason): Motivos que justifican
            la recomendación de la pregunta.
    """

    id: UUID
    content: str
    difficulty: float
    module_id: UUID
    tags: List[str]
    reason: RecommendationReason


class QuestionRecommendationResponse(BaseModel):
    """
    Define los datos de respuesta de las recomendaciones de preguntas.

    Atributos:
        theta (float): Valor de habilidad estimada del usuario.
        level (str): Nivel de habilidad o rendimiento del usuario.
        accuracy (float): Precisión de las respuestas del usuario.
        weak_tags (Dict): Datos de las etiquetas asociadas a los temas
            en los que el usuario presenta dificultades.
        recommendations (List[QuestionRecommendationItem]): Lista de
            preguntas recomendadas con sus motivos correspondientes.
    """

    theta: float
    level: str
    accuracy: float
    weak_tags: Dict
    recommendations: List[
        QuestionRecommendationItem
    ]


class ResourceRecommendationItem(BaseModel):
    """
    Define los datos de un recurso de aprendizaje recomendado.

    Atributos:
        id (UUID): Identificador único del recurso.
        title (str): Título del recurso.
        description (str | None): Descripción del recurso.
        type (str): Tipo de recurso de aprendizaje.
        difficulty (float): Nivel de dificultad del recurso.
        estimated_time (int | None): Tiempo estimado para completar
            o consultar el recurso.
        url (str): Dirección de acceso al recurso.
        reason (RecommendationReason): Motivos que justifican
            la recomendación del recurso.
    """

    id: UUID
    title: str
    description: str | None = None
    type: str
    difficulty: float
    estimated_time: int | None = None
    url: str
    reason: RecommendationReason


class ResourceRecommendationResponse(BaseModel):
    """
    Define los datos de respuesta de las recomendaciones de recursos.

    Atributos:
        theta (float): Valor de habilidad estimada del usuario.
        resources (List[ResourceRecommendationItem]): Lista de recursos
            recomendados con sus motivos correspondientes.
    """

    theta: float
    resources: List[
        ResourceRecommendationItem
    ]

