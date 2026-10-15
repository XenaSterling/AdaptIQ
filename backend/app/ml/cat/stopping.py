"""
Módulo: stopping.py
Descripción: Implementa las reglas de parada de las evaluaciones
             adaptativas mediante el seguimiento de la estabilidad
             de la habilidad estimada y del nivel de incertidumbre.
Autor: Raquel Del Castillo Pérez
"""

from typing import Dict, List


def _session_debug(session_state: Dict) -> Dict:
    """
    Obtiene información resumida del estado de una sesión.

    Args:
        session_state (Dict): Estado actual de la sesión de evaluación.

    Returns:
        Dict: Datos de la habilidad estimada, las preguntas utilizadas
            y las respuestas registradas.
    """

    return {
        "theta": session_state.get("theta"),
        "used": len(session_state.get("used", [])),
        "responses": len(session_state.get("responses", [])),
    }


def should_stop_evaluation(
    session_state: Dict,
    settings,
    theta_history: List[float],
    uncertainty: float,
    questions_answered: int
) -> Dict:
    """
    Determina si debe finalizar una evaluación adaptativa.

    Comprueba el número de preguntas respondidas, la incertidumbre
    de la estimación y la estabilidad de la habilidad estimada.

    Args:
        session_state (Dict): Estado actual de la sesión.
        settings: Configuración de los criterios de parada.
        theta_history (List[float]): Historial de estimaciones de theta.
        uncertainty (float): Nivel actual de incertidumbre.
        questions_answered (int): Número de preguntas respondidas.

    Returns:
        Dict: Decisión de parada, motivo y datos de depuración.
    """

    reasons = []

    if questions_answered < settings.min_questions:
        return {
            "stop": False,
            "reason": "min_questions_not_reached",
            "debug": {
                "session_state": _session_debug(session_state)
            }
        }

    if questions_answered >= settings.max_questions:
        return {
            "stop": True,
            "reason": "max_questions_reached",
            "debug": {
                "session_state": _session_debug(session_state)
            }
        }

    if getattr(settings, "use_uncertainty_stop", False):
        if uncertainty <= settings.max_uncertainty:
            reasons.append("low_uncertainty")

    if len(theta_history) >= settings.stability_window + 1:

        recent = theta_history[-settings.stability_window:]
        previous = theta_history[-(settings.stability_window + 1):-1]

        recent_change = max(recent) - min(recent)
        previous_change = max(previous) - min(previous)

        if recent_change < settings.theta_stability_threshold:
            reasons.append("theta_stable")

    if "theta_stable" in reasons and "low_uncertainty" in reasons:
        return {
            "stop": True,
            "reason": "stable_theta_and_low_uncertainty",
            "debug": {
                "theta_history": theta_history,
                "uncertainty": uncertainty,
                "session_state": _session_debug(session_state)
            }
        }

    return {
        "stop": False,
        "reason": "continue",
        "debug": {
            "reasons": reasons,
            "theta_history": theta_history[-5:],
            "uncertainty": uncertainty,
            "session_state": _session_debug(session_state)
        }
    }