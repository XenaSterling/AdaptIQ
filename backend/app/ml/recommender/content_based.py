"""
Módulo: content_based.py
Descripción: Implementa la recomendación basada en contenido mediante
             el análisis de las etiquetas de las preguntas que
             el estudiante ha respondido correcta o incorrectamente.
Autor: Raquel Del Castillo Pérez
"""

from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.question import Question


def build_user_profile(db: Session, user_id: str):
    """
    Construye un perfil del estudiante a partir de sus respuestas.

    Incrementa la puntuación de las etiquetas asociadas a respuestas
    incorrectas y reduce la puntuación de las asociadas a respuestas
    correctas.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.

    Returns:
        defaultdict: Puntuación acumulada de cada etiqueta del perfil.
    """

    from app.models.result import Result

    results = (
        db.query(Result)
        .join(Result.evaluation)
        .filter(Result.evaluation.has(user_id=user_id))
        .all()
    )

    profile = defaultdict(float)

    for r in results:

        question = r.question

        if not question:
            continue

        weight = 1.0 if not r.is_correct else -0.5

        for qt in question.tags:
            profile[qt.tag_id] += weight

    return profile


def score_by_content(question, user_profile):
    """
    Calcula la puntuación de una pregunta según el perfil del usuario.

    Suma las puntuaciones de las etiquetas asociadas a la pregunta.

    Args:
        question: Pregunta que se desea evaluar.
        user_profile: Puntuaciones de las etiquetas del estudiante.

    Returns:
        float: Puntuación de afinidad entre la pregunta y el perfil.
    """

    score = 0.0

    for qt in question.tags:

        score += user_profile.get(qt.tag_id, 0.0)

    return score


def get_content_scores(db: Session, user_id: str):
    """
    Calcula la puntuación basada en contenido de cada pregunta.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.

    Returns:
        dict: Puntuaciones asociadas a los identificadores
            de las preguntas disponibles.
    """

    from app.models.question import Question

    profile = build_user_profile(db, user_id)

    questions = db.query(Question).all()

    scores = {}

    for q in questions:
        scores[q.id] = score_by_content(q, profile)

    return scores