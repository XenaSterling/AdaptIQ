"""
Módulo: recommender_engine.py
Descripción: Implementa un sistema híbrido de recomendación de preguntas
             que combina la habilidad estimada, el análisis de contenido,
             la información colaborativa y las etiquetas débiles.
             Incorpora factores de popularidad y diversidad para
             ordenar las recomendaciones finales.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.question import Question
from app.models.result import Result
from app.ml.recommender.tag_based import get_weak_tags
from app.ml.recommender.collaborative import get_collaborative_question_scores
from app.ml.recommender.content_based import get_content_scores
from app.ml.recommender.normalization import normalize
from app.ml.recommender.explain import diversity_penalty


def compute_popularity_penalty(db: Session, question_id: str):
    """
    Calcula un factor de penalización según la popularidad.

    Cuantas más respuestas registradas tenga una pregunta,
    menor será el factor aplicado a su puntuación.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        question_id (str): Identificador de la pregunta.

    Returns:
        float: Factor de penalización por popularidad.
    """

    count = (
        db.query(Result)
        .filter(Result.question_id == question_id)
        .count()
    )

    return 1 / (1 + count)


def recommend_hybrid(db: Session, user_id: str, theta: float, limit: int = 5, module_id=None):
    """
    Genera recomendaciones de preguntas mediante un enfoque híbrido.

    Combina la adecuación a la habilidad estimada, las puntuaciones
    basadas en contenido, la información colaborativa y las etiquetas
    débiles. Posteriormente, normaliza las puntuaciones y aplica
    factores de popularidad y diversidad.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.
        theta (float): Habilidad estimada del estudiante.
        limit (int): Número máximo de preguntas recomendadas.
        module_id: Identificador opcional del módulo que se filtrará.

    Returns:
        list: Preguntas seleccionadas y ordenadas por puntuación final.
    """

    query = db.query(Question)

    if module_id is not None:
        query = query.filter(
            Question.module_id == module_id
        )

    questions = query.all()

    weak_tags = get_weak_tags(db, user_id)
    collaborative = get_collaborative_question_scores(db, user_id)
    content = get_content_scores(db, user_id)

    raw_scores = {}

    for q in questions:

        score = 0.0

        difficulty_gap = abs(q.difficulty - theta)
        irt_score = max(0, 3.0 - difficulty_gap * 3)
        score += irt_score * 0.4

        score += content.get(q.id, 0.0) * 0.3

        score += collaborative.get(q.id, 0.0) * 0.2

        tag_score = 0.0
        for qt in q.tags:
            tag_score += weak_tags.get(str(qt.tag_id), 0.0)

        score += tag_score * 0.1

        raw_scores[q] = score

    if not raw_scores:
        return []

    normalized_map = normalize({q.id: s for q, s in raw_scores.items()})

    ranked = sorted(
        raw_scores.items(),
        key=lambda x: normalized_map.get(x[0].id, 0),
        reverse=True
    )

    selected = []
    final = []

    for q, _ in ranked:

        base_score = normalized_map.get(q.id, 0)

        popularity = compute_popularity_penalty(db, q.id)

        diversity = diversity_penalty(selected, q)

        final_score = base_score * popularity * diversity

        final.append((q, final_score))
        selected.append(q)

        if len(final) >= limit:
            break

    final.sort(key=lambda x: x[1], reverse=True)

    return [q for q, _ in final]