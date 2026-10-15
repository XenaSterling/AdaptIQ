"""
Módulo: evaluation_settings.py
Descripción: Define los parámetros de configuración de las evaluaciones,
             incluyendo los límites de preguntas y los criterios de
             estabilidad e incertidumbre.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class EvaluationSettings(BaseModel):
    """
    Define los parámetros de configuración de una evaluación.

    Atributos:
        min_questions (int): Número mínimo de preguntas de la evaluación.
        max_questions (int): Número máximo de preguntas de la evaluación.
        theta_stability_threshold (float): Umbral de variación de theta
            para determinar la estabilidad de la habilidad estimada.
        stability_window (int): Número de mediciones utilizadas para
            evaluar la estabilidad de theta.
        use_uncertainty_stop (bool): Indica si se utiliza la incertidumbre
            como criterio para finalizar la evaluación.
        max_uncertainty (float): Valor máximo de incertidumbre permitido
            para aplicar el criterio de finalización.
        extra_config (Optional[Dict[str, Any]]): Configuración adicional
            con parámetros personalizados.
    """

    min_questions: int = 10
    max_questions: int = 50
    theta_stability_threshold: float = 0.05
    stability_window: int = 2
    use_uncertainty_stop: bool = True
    max_uncertainty: float = 0.25

    extra_config: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True