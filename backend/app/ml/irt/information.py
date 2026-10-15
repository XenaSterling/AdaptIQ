"""
Módulo: information.py
Descripción: Calcula la información de Fisher de una pregunta según
             el modelo de teoría de respuesta al ítem (IRT).
Autor: Raquel Del Castillo Pérez
"""

from app.ml.irt.model import probability_correct


def fisher_information(theta: float, difficulty: float, discrimination: float = 1.0) -> float:
    """
    Calcula la información de Fisher de una pregunta.

    Atributos:
        theta (float): Nivel de habilidad estimado del estudiante.
        difficulty (float): Nivel de dificultad de la pregunta.
        discrimination (float): Capacidad de la pregunta para distinguir
            entre estudiantes con diferentes niveles de habilidad.

    Returns:
        float: Información proporcionada por la pregunta.
    """

    p = probability_correct(theta, difficulty, discrimination)

    return (discrimination ** 2) * p * (1 - p)