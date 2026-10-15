"""
Módulo: dashboard.py
Descripción: Define los esquemas de respuesta de los paneles
             de estudiantes, docentes y administradores.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import List, Dict


class ModuleProgressResponse(BaseModel):
    """
    Define los datos de progreso de un módulo.

    Atributos:
        module (str): Nombre o identificador textual del módulo.
        progress (float): Valor del progreso.
        completed (bool): Indica si el módulo está completado.
    """

    module: str
    progress: float
    completed: bool


class StudentDashboardResponse(BaseModel):
    """
    Define los datos de respuesta del panel del estudiante.

    Atributos:
        theta (float): Valor de habilidad estimada.
        accuracy (float): Valor de precisión.
        score (float): Puntuación.
        evaluations_completed (int): Número de evaluaciones completadas.
        completed_modules (int): Número de módulos completados.
        avg_module_progress (float): Valor medio del progreso de módulos.
        module_progress (List[ModuleProgressResponse]): Progreso por módulo.
        weak_topics (Dict[str, Dict[str, float]]): Datos agrupados por tema.
        theta_evolution (List[Dict]): Datos de evolución de theta.
        uncertainty (float): Valor de incertidumbre.
        uncertainty_level (str): Nivel de incertidumbre.
    """

    theta: float
    accuracy: float
    score: float
    evaluations_completed: int
    completed_modules: int
    avg_module_progress: float
    module_progress: List[ModuleProgressResponse]
    weak_topics: Dict[str, Dict[str, float]]
    theta_evolution: List[Dict]
    uncertainty: float
    uncertainty_level: str


class FailedQuestionResponse(BaseModel):
    """
    Define los datos de una pregunta y sus errores.

    Atributos:
        question_id (str): Identificador de la pregunta.
        question_text (str): Texto de la pregunta.
        errors (int): Número de errores.
    """

    question_id: str
    question_text: str
    errors: int


class HighRiskStudentResponse(BaseModel):
    """
    Define los datos de un estudiante y su puntuación de riesgo.

    Atributos:
        id (str): Identificador del estudiante.
        name (str): Nombre del estudiante.
        risk_score (float): Puntuación de riesgo.
    """

    id: str
    name: str
    risk_score: float


class TeacherDashboardResponse(BaseModel):
    """
    Define los datos de respuesta del panel del docente.

    Atributos:
        total_students (int): Número total de estudiantes.
        accuracy (float): Valor de precisión.
        avg_score (float): Puntuación media.
        avg_theta (float): Valor medio de theta.
        most_failed_questions (List[FailedQuestionResponse]): Preguntas
            con sus recuentos de errores.
        cohorts (List[Dict]): Lista de datos de grupos.
        struggling_students (int): Número de estudiantes con dificultades.
        risk_breakdown (Dict[str, int]): Datos de riesgo agrupados.
        high_risk_students (List[HighRiskStudentResponse]): Estudiantes
            con sus puntuaciones de riesgo.
        total_answers (int): Número total de respuestas.
        total_evaluations (int): Número total de evaluaciones.
    """

    total_students: int
    accuracy: float
    avg_score: float
    avg_theta: float
    most_failed_questions: List[FailedQuestionResponse]
    cohorts: List[Dict]
    struggling_students: int
    risk_breakdown: Dict[str, int]
    high_risk_students: List[HighRiskStudentResponse]
    total_answers: int
    total_evaluations: int


class AdminDashboardResponse(BaseModel):
    """
    Define los datos de respuesta del panel de administración.

    Atributos:
        total_users (int): Número total de usuarios.
        total_courses (int): Número total de cursos.
        total_evaluations (int): Número total de evaluaciones.
        avg_score (float): Puntuación media.
        avg_theta (float): Valor medio de theta.
        abandoned (int): Número de evaluaciones abandonadas.
        role_breakdown (Dict[str, int]): Datos agrupados por rol.
        evaluation_breakdown (Dict[str, int]): Datos agrupados por estado
            de evaluación.
    """

    total_users: int
    total_courses: int
    total_evaluations: int
    avg_score: float
    avg_theta: float
    abandoned: int
    role_breakdown: Dict[str, int]
    evaluation_breakdown: Dict[str, int]