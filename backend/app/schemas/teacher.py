"""
Módulo: teacher.py
Descripción: Define los esquemas de respuesta y solicitud para la
             configuración de evaluaciones, el resumen de actividad
             docente y el análisis de riesgo de los estudiantes.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import Optional, List


class EvaluationSettingsResponse(BaseModel):
    """
    Define los datos de respuesta de la configuración de una evaluación.

    Atributos:
        evaluation_id (str): Identificador de la evaluación.
        min_questions (int): Número mínimo de preguntas de la evaluación.
        max_questions (int): Número máximo de preguntas de la evaluación.
        theta_stability_threshold (float): Umbral de variación de theta
            utilizado para determinar la estabilidad de la habilidad.
        stability_window (int): Número de mediciones consideradas
            para evaluar la estabilidad de theta.
        max_uncertainty (float): Valor máximo de incertidumbre permitido
            en la evaluación.
    """

    evaluation_id: str
    min_questions: int
    max_questions: int
    theta_stability_threshold: float
    stability_window: int
    max_uncertainty: float


class UpdateEvaluationSettingsRequest(BaseModel):
    """
    Define los datos que pueden modificarse en la configuración
    de una evaluación.

    Atributos:
        min_questions (Optional[int]): Número mínimo de preguntas.
        max_questions (Optional[int]): Número máximo de preguntas.
        theta_stability_threshold (Optional[float]): Umbral de variación
            de theta para determinar la estabilidad de la habilidad.
        stability_window (Optional[int]): Número de mediciones utilizadas
            para evaluar la estabilidad de theta.
        max_uncertainty (Optional[float]): Valor máximo de incertidumbre
            permitido en la evaluación.
    """

    min_questions: Optional[int] = None
    max_questions: Optional[int] = None
    theta_stability_threshold: Optional[float] = None
    stability_window: Optional[int] = None
    max_uncertainty: Optional[float] = None


class TeacherOverviewResponse(BaseModel):
    """
    Define los datos de resumen de la actividad docente.

    Atributos:
        total_students (int): Número total de estudiantes.
        total_evaluations (int): Número total de evaluaciones realizadas.
        total_answers (int): Número total de respuestas registradas.
        accuracy (float): Valor de precisión de las respuestas.
        struggling_students (int): Número de estudiantes que presentan
            dificultades de aprendizaje.
    """

    total_students: int
    total_evaluations: int
    total_answers: int
    accuracy: float
    struggling_students: int


class StudentRiskResponse(BaseModel):
    """
    Define los datos de análisis de riesgo de un estudiante.

    Atributos:
        user_id (str): Identificador del usuario.
        accuracy (float): Valor de precisión de las respuestas
            del estudiante.
        risk_level (str): Nivel de riesgo asignado al estudiante.
        total_answers (int): Número total de respuestas registradas
            del estudiante.
    """

    user_id: str
    accuracy: float
    risk_level: str
    total_answers: int