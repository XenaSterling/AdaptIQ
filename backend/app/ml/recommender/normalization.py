"""
Módulo: normalization.py
Descripción: Proporciona funciones de normalización de puntuaciones
             para facilitar la comparación de resultados generados
             por los algoritmos de recomendación.
Autor: Raquel Del Castillo Pérez
"""

def normalize(scores: dict):
    """
    Normaliza las puntuaciones mediante el método min-max.

    Transforma los valores al intervalo comprendido entre 0 y 1.
    Si todas las puntuaciones son iguales, asigna el valor 0
    a cada elemento.

    Args:
        scores (dict): Diccionario de elementos y sus puntuaciones.

    Returns:
        dict: Diccionario con las puntuaciones normalizadas.
    """

    if not scores:
        return scores

    values = list(scores.values())

    min_v = min(values)
    max_v = max(values)

    if max_v == min_v:
        return {k: 0.0 for k in scores}

    return {
        k: (v - min_v) / (max_v - min_v)
        for k, v in scores.items()
    }