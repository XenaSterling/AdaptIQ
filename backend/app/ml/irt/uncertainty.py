"""
Módulo: uncertainty.py
Descripción: Calcula la incertidumbre de la estimación de habilidad
             de un estudiante a partir de la información acumulada
             de las preguntas respondidas.
Autor: Raquel Del Castillo Pérez
"""

from math import sqrt

from app.ml.irt.information import fisher_information
from app.models.result import Result
from app.models.student_ability import StudentAbility


def compute_uncertainty(db, user_id: str):
    """
    Calcula la incertidumbre asociada a la habilidad estimada
    de un estudiante.

    Atributos:
        db: Sesión de conexión con la base de datos.
        user_id (str): Identificador del estudiante.

    Returns:
        float: Incertidumbre estimada a partir de la información
            acumulada de las preguntas respondidas. Devuelve 1.0
            si el estudiante no tiene resultados registrados.
    """

    ability = (
        db.query(StudentAbility)
        .filter_by(user_id=user_id)
        .first()
    )

    theta = ability.theta if ability else 0.0

    results = (
        db.query(Result)
        .join(Result.evaluation)
        .filter(Result.evaluation.has(user_id=user_id))
        .all()
    )

    infos = []

    for r in results:

        q = r.question

        infos.append(
            fisher_information(
                theta=theta,
                difficulty=q.difficulty,
                discrimination=q.discrimination or 1.0
            )
        )

    if not infos:
        return 1.0

    total_information = sum(infos)

    return 1 / (sqrt(total_information) + 1e-6)