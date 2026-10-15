"""
Módulo: evaluation_service.py
Descripción: Gestiona el ciclo de vida de las evaluaciones adaptativas,
             incluyendo su inicio, la selección y corrección de preguntas,
             la actualización de la habilidad del estudiante y la
             finalización de la evaluación.
Autor: Raquel Del Castillo Pérez
"""

from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session, joinedload

from app.models.question import Question
from app.models.result import Result
from app.models.evaluation import Evaluation, EvaluationStatus
from app.models.irt_session import IRTSession

from app.services.student_ability_service import (
    get_or_create_student_ability
)
from app.services.adaptive_engine import get_next_question
from app.services.evaluation_settings_service import (
    get_evaluation_settings
)
from app.services.feedback_service import generate_feedback

from app.ml.irt.update import update_theta
from app.ml.irt.uncertainty import compute_uncertainty
from app.ml.cat.stopping import should_stop_evaluation


def serialize_question(question: Question):
    """
    Convierte un objeto Question en un diccionario serializable
    que contiene la información necesaria para presentar la pregunta
    al estudiante.

    Se incluyen el identificador, el enunciado, el tipo de pregunta
    y las respuestas disponibles, sin exponer si son correctas.

    Atributos:
        question (Question): Objeto de pregunta que se desea serializar.

    Returns:
        dict: Representación de la pregunta con sus respuestas
            disponibles, preparada para su envío a la API.
    """

    return {
        "id": question.id,
        "content": question.content,
        "type": question.type,
        "answers": [
            {
                "id": a.id,
                "content": a.content
            }
            for a in question.answers
        ]
    }


def compute_score(responses: list[dict]) -> float:
    """
    Calcula la puntuación final de una evaluación a partir de las
    respuestas registradas y de los parámetros de dificultad
    y discriminación de las preguntas.

    Cada respuesta recibe un peso calculado a partir de dichos
    parámetros. La puntuación resultante se normaliza a una escala
    de 0 a 10.

    Atributos:
        responses (list[dict]): Lista de respuestas que contiene
            los campos correct, difficulty y discrimination.

    Returns:
        float: Puntuación final redondeada a dos decimales.
            Devuelve 0.0 si no hay respuestas o si el peso total
            es cero.
    """

    if not responses:
        return 0.0

    weighted_sum = 0.0
    weight_total = 0.0

    for r in responses:
        weight = abs(r.get("difficulty", 1.0)) * r.get("discrimination", 1.0)

        weight_total += weight

        if r["correct"]:
            weighted_sum += weight

    if weight_total == 0:
        return 0.0

    score = (weighted_sum / weight_total) * 10

    return round(max(0.0, min(10.0, score)), 2)


def get_active_evaluation(
    db: Session,
    user_id: str
):
    """
    Busca la evaluación que el estudiante tiene actualmente
    en curso.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del estudiante.

    Returns:
        Evaluation | None: Evaluación cuyo estado es in_progress,
            o None si el estudiante no tiene ninguna evaluación activa.
    """

    return (
        db.query(Evaluation)
        .filter(
            Evaluation.user_id == user_id,
            Evaluation.status == EvaluationStatus.in_progress
        )
        .first()
    )


def build_session_state(
    db: Session,
    evaluation: Evaluation
):
    """
    Reconstruye el estado de una evaluación a partir de los resultados
    persistidos y de la sesión IRT que permanece abierta.

    Recupera las preguntas utilizadas, las respuestas registradas,
    el historial de habilidad estimada y los identificadores de
    evaluación y sesión.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        evaluation (Evaluation): Evaluación cuyo estado se reconstruye.

    Returns:
        dict: Estado de la sesión con los campos theta, used,
            responses, theta_history, evaluation_id e irt_session_id.
    """

    results = (
        db.query(Result)
        .join(Result.question)
        .filter(Result.evaluation_id == evaluation.id)
        .all()
    )

    used_questions = [
        str(r.question_id)
        for r in results
    ]

    responses = [
        {
            "correct": r.is_correct,
            "difficulty": r.question_difficulty,
            "discrimination": r.question_discrimination or 1.0
        }
        for r in results
    ]

    theta_history = []

    if results:
        theta_history.append(results[0].theta_before)

        for r in results:
            theta_history.append(r.theta_after)

    else:
        theta_history.append(evaluation.current_theta)

    irt_session = (
        db.query(IRTSession)
        .filter(
            IRTSession.user_id == evaluation.user_id,
            IRTSession.finished_at.is_(None)
        )
        .order_by(IRTSession.started_at.desc())
        .first()
    )

    return {
        "theta": evaluation.current_theta,
        "used": used_questions,
        "responses": responses,
        "theta_history": theta_history,
        "evaluation_id": evaluation.id,
        "irt_session_id": irt_session.id if irt_session else None
    }


def start_evaluation_service(
    db: Session,
    user_id: str,
    course_id: str | None = None,
    module_id: str | None = None,
):
    """
    Inicia una evaluación adaptativa o recupera una evaluación
    que el estudiante ya tiene en curso.

    Si existe una evaluación activa, reconstruye su estado y selecciona
    la siguiente pregunta disponible. En caso contrario, crea una nueva
    evaluación y una sesión IRT, y selecciona la primera pregunta
    teniendo en cuenta la habilidad inicial del estudiante.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del estudiante.
        course_id (str | None): Identificador opcional del curso.
        module_id (str | None): Identificador opcional del módulo
            al que se limita la evaluación.

    Returns:
        dict: Información de la evaluación y de la primera pregunta
            que debe presentarse, incluyendo los identificadores
            de evaluación y sesión IRT y el valor actual de theta.

    Raises:
        HTTPException: Error 400 si una evaluación activa no dispone
            de preguntas restantes.
        HTTPException: Error 404 si no hay preguntas disponibles
            para iniciar una nueva evaluación.
    """

    existing = get_active_evaluation(
        db,
        user_id
    )

    if existing:

        session_state = build_session_state(
            db,
            existing
        )

        next_question = get_next_question(
            db=db,
            theta=session_state["theta"],
            used_question_ids=session_state["used"]
        )

        if not next_question:
            raise HTTPException(
                status_code=400,
                detail="Evaluation has no remaining questions"
            )

        return {
            "evaluation_id": existing.id,
            "irt_session_id": session_state["irt_session_id"],
            "theta": session_state["theta"],
            "question": serialize_question(next_question)
        }

    ability = get_or_create_student_ability(
        db,
        user_id
    )

    evaluation = Evaluation(
        user_id=user_id,
        course_id=course_id,
        module_id=module_id,
        score=0.0,
        current_theta=ability.theta,
        status=EvaluationStatus.in_progress,
        started_at=datetime.utcnow()
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    irt_session = IRTSession(
        user_id=user_id,
        course_id=course_id,
        theta_start=ability.theta
    )

    db.add(irt_session)
    db.commit()
    db.refresh(irt_session)

    question = get_next_question(
        db=db,
        theta=ability.theta,
        used_question_ids=[],
        module_id=evaluation.module_id
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="No questions available"
        )

    return {
        "evaluation_id": evaluation.id,
        "irt_session_id": irt_session.id,
        "theta": ability.theta,
        "question": serialize_question(question)
    }


def answer_question_service(
    db: Session,
    user_id: str,
    question_id: str,
    payload
):
    """
    Procesa la respuesta de un estudiante a una pregunta de una
    evaluación adaptativa.

    Comprueba la sesión activa y que la pregunta no se haya respondido
    previamente, determina si la respuesta es correcta, actualiza
    la habilidad estimada y registra el resultado. A continuación,
    evalúa los criterios de parada para decidir si finaliza la
    evaluación o selecciona una nueva pregunta.

    Cuando la evaluación termina, calcula la puntuación final,
    actualiza el estado de la sesión IRT y genera el feedback
    correspondiente.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del estudiante.
        question_id (str): Identificador de la pregunta respondida.
        payload: Datos de la respuesta enviada, incluidos los
            identificadores de las respuestas seleccionadas y,
            si está disponible, el tiempo de respuesta.

    Returns:
        dict: Resultado del procesamiento, con la siguiente pregunta
            si la evaluación continúa o con la puntuación final,
            la habilidad estimada y el feedback si termina.

    Raises:
        HTTPException: Error 400 si no hay una evaluación activa
            o si la pregunta ya ha sido respondida.
        HTTPException: Error 404 si no se encuentra la pregunta.
    """

    evaluation = get_active_evaluation(
        db,
        user_id
    )

    if not evaluation:
        raise HTTPException(
            status_code=400,
            detail="Session not started"
        )

    session = build_session_state(
        db,
        evaluation
    )

    if question_id in session["used"]:
        raise HTTPException(
            status_code=400,
            detail="Question already answered"
        )

    question = (
        db.query(Question)
        .options(joinedload(Question.answers))
        .filter_by(id=question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    correct_answers = {
        str(a.id)
        for a in question.answers
        if a.is_correct
    }

    selected_answers = set(
        str(x)
        for x in payload.selected_answer_ids
    )

    is_correct = selected_answers == correct_answers

    session["responses"].append({
        "correct": is_correct,
        "difficulty": question.difficulty,
        "discrimination": question.discrimination or 1.0
    })

    previous_theta = session["theta"]

    new_theta = update_theta(
        theta=previous_theta,
        responses=session["responses"]
    )

    ability = get_or_create_student_ability(
        db,
        user_id
    )

    ability.theta = new_theta

    evaluation.current_theta = new_theta

    result = Result(
        evaluation_id=evaluation.id,
        question_id=question.id,
        is_correct=is_correct,
        response_time=payload.response_time,
        theta_before=previous_theta,
        theta_after=new_theta,
        question_difficulty=question.difficulty,
        question_discrimination=question.discrimination
    )

    db.add(result)
    db.flush()

    updated_session = build_session_state(
        db,
        evaluation
    )

    uncertainty = compute_uncertainty(
        db,
        user_id
    )

    settings = get_evaluation_settings(
        db,
        str(evaluation.id)
    )

    stop = should_stop_evaluation(
        session_state=updated_session,
        settings=settings,
        theta_history=updated_session["theta_history"],
        uncertainty=uncertainty,
        questions_answered=len(updated_session["used"])
    )

    if stop["stop"]:

        final_score = compute_score(updated_session["responses"])

        evaluation.final_theta = new_theta
        evaluation.score = final_score
        evaluation.status = EvaluationStatus.completed
        evaluation.finished_at = datetime.utcnow()

        irt_session = (
            db.query(IRTSession)
            .filter_by(id=updated_session["irt_session_id"])
            .first()
        )

        if irt_session:
            irt_session.theta_end = new_theta
            irt_session.finished_at = datetime.utcnow()

        db.commit()

        feedback_data = generate_feedback(
            db=db,
            evaluation=evaluation,
            user_id=user_id
        )

        return {
            "question": None,
            "theta": new_theta,
            "correct": is_correct,
            "finished": True,
            "final_theta": new_theta,
            "score": final_score,
            "feedback": feedback_data
        }

    next_question = get_next_question(
        db=db,
        theta=new_theta,
        used_question_ids=updated_session["used"],
        module_id=evaluation.module_id
    )

    if not next_question:

        final_score = compute_score(updated_session["responses"])

        evaluation.final_theta = new_theta
        evaluation.score = final_score
        evaluation.status = EvaluationStatus.completed
        evaluation.finished_at = datetime.utcnow()

        db.commit()

        feedback_data = generate_feedback(
            db=db,
            evaluation=evaluation,
            user_id=user_id
        )

        return {
            "question": None,
            "theta": new_theta,
            "correct": is_correct,
            "finished": True,
            "final_theta": new_theta,
            "score": evaluation.score,
            "feedback": feedback_data
        }

    db.commit()

    return {
        "question": serialize_question(next_question),
        "theta": new_theta,
        "correct": is_correct,
        "finished": False,
        "final_theta": None,
        "score": None
    }