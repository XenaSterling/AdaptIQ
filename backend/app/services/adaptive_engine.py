"""
Módulo: adaptive_engine.py
Descripción: Selecciona la siguiente pregunta de una evaluación adaptativa
             según la habilidad estimada del estudiante y la información
             proporcionada por cada pregunta.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session, joinedload
from app.models.question import Question
from app.ml.irt.information import fisher_information


def get_next_question(
    db: Session,
    theta: float,
    used_question_ids: list,
    module_id=None
):
    """
    Selecciona la pregunta más adecuada para continuar una evaluación
    adaptativa mediante la información de Fisher y criterios de proximidad.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        theta (float): Nivel de habilidad estimado del estudiante.
        used_question_ids (list): Identificadores de las preguntas
            utilizadas durante la evaluación.
        module_id: Identificador del módulo al que deben pertenecer
            las preguntas, si se especifica.

    Returns:
        Question | None: Pregunta seleccionada con sus respuestas
            asociadas y metadatos de selección, o None si no hay
            preguntas disponibles.
    """

    query = db.query(Question).options(joinedload(Question.answers))

    if module_id is not None:
        query = query.filter(Question.module_id == module_id)


    if used_question_ids is not None and len(used_question_ids) > 0:
        query = query.filter(~Question.id.in_(used_question_ids))

    questions = query.all()

    if not questions:
        return None

    best_question = None
    best_score = float("-inf")

    for q in questions:

        info = fisher_information(
            theta=theta,
            difficulty=q.difficulty,
            discrimination=q.discrimination or 1.0
        )

        difficulty_gap = abs(q.difficulty - theta)
        proximity_bonus = max(0, 1 - difficulty_gap)

        exploration_bonus = 0.05

        score = info + 0.3 * proximity_bonus + exploration_bonus

        if score > best_score:
            best_score = score
            best_question = q

    if best_question:
        best_question.cat_metadata = {
            "score": best_score
        }

    print("USED:", used_question_ids)
    print("ALL:", [q.id for q in questions])

    return best_question