"""
Módulo: model.py
Descripción: Implementa el modelo de teoría de respuesta al ítem (IRT)
             de dos parámetros para calcular la probabilidad de responder
             correctamente a una pregunta.
Autor: Raquel Del Castillo Pérez
"""

import math


def probability_correct(theta: float, difficulty: float, discrimination: float = 1.0) -> float:
    """
    Módulo: model.py
    Descripción: Implementa el modelo de teoría de respuesta al ítem (IRT)
                de dos parámetros para calcular la probabilidad de responder
                correctamente a una pregunta.
    Autor: Raquel Del Castillo Pérez
    """

    x = discrimination * (theta - difficulty)

    if x < -20:
        return 0.0
    if x > 20:
        return 1.0

    return 1 / (1 + math.exp(-x))