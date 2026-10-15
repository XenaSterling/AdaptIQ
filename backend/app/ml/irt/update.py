"""
Módulo: update.py
Descripción: Actualiza la estimación de habilidad del estudiante mediante
             el modelo IRT de dos parámetros, utilizando estimación
             bayesiana MAP y el método de Newton-Raphson.
Autor: Raquel Del Castillo Pérez
"""

from typing import List

from app.ml.irt.model import probability_correct


def clamp(
    x: float,
    min_val: float = -4.0,
    max_val: float = 4.0
) -> float:
    """
    Limita un valor a un intervalo determinado.

    Atributos:
        x (float): Valor que se desea limitar.
        min_val (float): Límite inferior permitido.
        max_val (float): Límite superior permitido.

    Returns:
        float: Valor comprendido entre los límites establecidos.
    """
    return max(min_val, min(max_val, x))


def update_theta(theta: float, responses: List[dict], max_iter: int = 3) -> float:
    """
    Actualiza la estimación de habilidad a partir de las respuestas
    registradas mediante el modelo IRT 2PL y la estimación bayesiana MAP.

    Atributos:
        theta (float): Estimación inicial de la habilidad del estudiante.
        responses (List[dict]): Respuestas registradas, con los campos
            correct, difficulty y discrimination opcional.
        max_iter (int): Número máximo de iteraciones de actualización.

    Returns:
        float: Nueva estimación de habilidad, limitada al intervalo
            comprendido entre -4.0 y 4.0.
    """

    if not responses:
        return theta

    prior_variance = 1.0
    weight = min(1.0, len(responses) / 5.0)

    for _ in range(min(max_iter, len(responses))):

        gradient = 0.0
        hessian = 0.0

        for r in responses:
            u = 1 if r["correct"] else 0
            b = r["difficulty"]
            a = r.get("discrimination", 1.0)

            p = probability_correct(theta, b, a)

            gradient += a * (u - p)
            hessian -= (a ** 2) * p * (1 - p)

        gradient += -(theta / prior_variance)
        hessian += -(1 / prior_variance)

        gradient *= weight
        hessian *= weight

        if abs(hessian) < 1e-5:
            return theta

        learning_rate = 0.3
        delta = learning_rate * (gradient / hessian)

        max_step = 0.5
        delta = max(-max_step, min(max_step, delta))

        theta = theta - delta

        if abs(delta) < 1e-3:
            break

    return clamp(theta)