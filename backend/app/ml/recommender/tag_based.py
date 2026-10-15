"""
Módulo: tag_based.py
Descripción: Analiza el rendimiento del estudiante por etiquetas
             y permite recuperar preguntas relacionadas con aquellas
             en las que presenta mayores dificultades.
Autor: Raquel Del Castillo Pérez
"""

from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.result import Result
from app.models.question import Question


def get_weak_tags(db: Session, user_id: str, min_attempts: int = 2):
    """
    Calcula las puntuaciones de debilidad de las etiquetas.

    Agrupa las respuestas por etiqueta, calcula la precisión
    y obtiene una puntuación de debilidad como complemento
    de dicha precisión. Solo considera etiquetas con el número
    mínimo de respuestas establecido.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.
        min_attempts (int): Número mínimo de respuestas por etiqueta.

    Returns:
        dict: Puntuaciones de debilidad asociadas a cada etiqueta.
    """

    results = (
        db.query(Result)
        .join(Result.evaluation)
        .filter(Result.evaluation.has(user_id=user_id))
        .all()
    )

    tag_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    for r in results:

        question = r.question
        if not question:
            continue

        for qt in question.tags:
            tag_id = str(qt.tag_id)

            tag_stats[tag_id]["total"] += 1

            if r.is_correct:
                tag_stats[tag_id]["correct"] += 1

    weak_tags = {}

    for tag_id, stats in tag_stats.items():

        if stats["total"] < min_attempts:
            continue

        accuracy = stats["correct"] / stats["total"]

        weak_score = 1.0 - accuracy

        weak_tags[tag_id] = weak_score

    return weak_tags


def recommend_questions_by_tags(db: Session, weak_tags: dict, limit: int = 5):
    """
    Recupera preguntas relacionadas con las etiquetas débiles.

    Selecciona las etiquetas con mayor puntuación de debilidad
    y busca preguntas asociadas a ellas.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        weak_tags (dict): Puntuaciones de debilidad por etiqueta.
        limit (int): Número máximo de preguntas que se recuperarán.

    Returns:
        list: Preguntas relacionadas con las etiquetas seleccionadas.
    """

    from app.models.question_tag import QuestionTag

    tag_ids = sorted(weak_tags, key=weak_tags.get, reverse=True)[:3]

    if not tag_ids:
        return []

    questions = (
        db.query(Question)
        .join(QuestionTag)
        .filter(QuestionTag.tag_id.in_(tag_ids))
        .limit(limit)
        .all()
    )

    return questions