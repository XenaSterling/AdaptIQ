"""
Módulo: collaborative.py
Descripción: Implementa la recomendación colaborativa de preguntas
             a partir de la similitud entre estudiantes y sus
             resultados en evaluaciones anteriores.
Autor: Raquel Del Castillo Pérez
"""

from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.result import Result
from app.models.student_ability import StudentAbility


def get_similar_users(db: Session, user_id: str, limit: int = 5):
    """
    Busca estudiantes con una habilidad estimada similar.

    Calcula la similitud a partir de la distancia absoluta entre
    los valores de theta y devuelve los usuarios más similares.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante objetivo.
        limit (int): Número máximo de usuarios que se devolverán.

    Returns:
        list: Lista de tuplas con el identificador de cada usuario
            similar y su puntuación de similitud.
    """

    target = db.query(StudentAbility).filter_by(user_id=user_id).first()

    if not target:
        return []

    users = db.query(StudentAbility).all()

    similarities = []

    for u in users:

        if u.user_id == user_id:
            continue

        distance = abs(u.theta - target.theta)
        similarity = 1 / (1 + distance)

        similarities.append((u.user_id, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:limit]


def get_collaborative_question_scores(db: Session, user_id: str):
    """
    Calcula puntuaciones colaborativas para las preguntas.

    Asigna mayor puntuación a las preguntas falladas por estudiantes
    con una habilidad estimada similar a la del usuario objetivo.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante objetivo.

    Returns:
        defaultdict: Puntuación acumulada de cada pregunta según
            la similitud de los estudiantes que la han fallado.
    """

    similar_users = get_similar_users(db, user_id)

    scores = defaultdict(float)

    for other_user_id, weight in similar_users:

        results = (
            db.query(Result)
            .join(Result.evaluation)
            .filter(Result.evaluation.has(user_id=other_user_id))
            .all()
        )

        for r in results:

            if not r.is_correct:
                scores[r.question_id] += weight

    return scores