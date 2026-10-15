"""
Módulo: feedback.py
Descripción: Define los esquemas de respuesta para la retroalimentación
             de las evaluaciones, incluyendo el rendimiento, los temas
             débiles y los recursos de aprendizaje recomendados.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import List


class WeakTopicResponse(BaseModel):
    """
    Define los datos de un tema en el que el usuario presenta dificultades.

    Atributos:
        id (str): Identificador del tema.
        name (str): Nombre del tema.
        weakness (float): Valor que representa el grado de dificultad
            o debilidad detectado en el tema.
    """

    id: str
    name: str
    weakness: float


class RecommendedResourceResponse(BaseModel):
    """
    Define los datos de un recurso de aprendizaje recomendado.

    Atributos:
        id (str): Identificador del recurso.
        title (str): Título del recurso recomendado.
        type (str): Tipo de recurso de aprendizaje.
        url (str): Dirección de acceso al recurso.
    """

    id: str
    title: str
    type: str
    url: str


class FeedbackResponse(BaseModel):
    """
    Define los datos de retroalimentación generados tras una evaluación.

    Atributos:
        summary (str): Resumen general del rendimiento del usuario.
        performance (str): Descripción del rendimiento obtenido.
        improvement (str): Recomendaciones para mejorar el aprendizaje.
        level (str): Nivel de habilidad o rendimiento alcanzado.
        accuracy (float): Valor de precisión de las respuestas.
        theta (float): Valor de habilidad estimada mediante IRT.
        theta_change (float): Variación de theta durante la evaluación.
        uncertainty (float): Valor de incertidumbre de la estimación.
        weak_topics (List[WeakTopicResponse]): Lista de temas en los que
            se han detectado dificultades.
        recommended_resources (List[RecommendedResourceResponse]):
            Lista de recursos recomendados para reforzar el aprendizaje.
    """

    summary: str
    performance: str
    improvement: str
    level: str
    accuracy: float
    theta: float
    theta_change: float
    uncertainty: float
    weak_topics: List[WeakTopicResponse]
    recommended_resources: List[
        RecommendedResourceResponse
    ]