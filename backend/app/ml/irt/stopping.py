"""
Módulo: stopping.py
Descripción: Determina si la estimación de habilidad del estudiante
             ha alcanzado la estabilidad necesaria para detener
             una evaluación adaptativa.
Autor: Raquel Del Castillo Pérez
"""

from typing import List


def has_converged(
    theta_history: List[float],
    window: int = 3,
    threshold: float = 0.05
) -> bool:
    """
    Comprueba si la estimación de habilidad se mantiene estable
    durante una ventana de observaciones.

    Atributos:
        theta_history (List[float]): Historial de estimaciones de theta.
        window (int): Número de estimaciones recientes que se analizan.
        threshold (float): Variación máxima permitida para considerar
            estable la estimación.

    Returns:
        bool: True si la estimación ha convergido; False en caso contrario.
    """

    if len(theta_history) < window:
        return False

    recent = theta_history[-window:]

    return (max(recent) - min(recent)) < threshold