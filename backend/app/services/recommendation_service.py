"""
Módulo: recommendation_service.py
Descripción: Gestiona las recomendaciones personalizadas de preguntas
             y recursos de aprendizaje, utilizando el nivel de habilidad
             del usuario, sus temas débiles y algoritmos de recomendación.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student_ability import StudentAbility

from app.ml.recommender.recommender_engine import recommend_hybrid
from app.ml.recommender.resource_recommender import recommend_resources
from app.ml.recommender.tag_based import get_weak_tags
from app.ml.recommender.explain import explain_resource

from app.services.feedback_service import classify_theta
from app.models.evaluation import Evaluation


def get_user_theta(
    db: Session,
    user_id
):
    """
    Obtiene el nivel de habilidad del usuario.

    Si el usuario todavía no tiene un registro de habilidad, crea uno
    con el valor inicial de theta igual a 0.0 y lo persiste en la
    base de datos.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id: Identificador del usuario cuya habilidad se consulta.

    Returns:
        float: Valor de theta del usuario, existente o recién creado.
    """

    ability = (
        db.query(StudentAbility)
        .filter_by(user_id=user_id)
        .first()
    )

    if not ability:
        ability = StudentAbility(
            user_id=user_id,
            theta=0.0
        )
        db.add(ability)
        db.commit()
        db.refresh(ability)

    return ability.theta


def build_reason(
    explanation,
    reason_type,
    confidence,
    weak_tags=None,
    difficulty_gap=None,
    theta_match=None
):
    """
    Construye la justificación de una recomendación.

    Incluye la explicación, el tipo de recomendación, la confianza
    estimada, la diferencia de dificultad y los temas débiles asociados.

    Atributos:
        explanation: Explicación de la recomendación.
        reason_type: Tipo de recomendación generada.
        confidence: Nivel de confianza de la recomendación.
        weak_tags: Lista de etiquetas relacionadas con temas débiles.
        difficulty_gap: Diferencia entre la dificultad y el nivel
            de habilidad del usuario.
        theta_match: Indica si la dificultad se ajusta al nivel
            de habilidad del usuario.

    Returns:
        dict: Diccionario con la justificación y los indicadores
            asociados a la recomendación.
    """

    return {
        "explanation": explanation,
        "reason_type": reason_type,
        "confidence": round(confidence, 2),
        "difficulty_gap": difficulty_gap,
        "theta_match": theta_match,
        "weak_tags": weak_tags or [],
        "peer_context": {
            "similar_users_benefited": True,
            "avg_improvement_after_resource": 0.23
        }
    }


def get_question_recommendations(
    db: Session,
    user_id
):
    """
    Genera recomendaciones personalizadas de preguntas.

    Obtiene el nivel de habilidad y el rendimiento del usuario,
    identifica sus temas débiles y genera recomendaciones mediante
    el sistema híbrido, incluyendo la justificación de cada pregunta.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id: Identificador del usuario para el que se generan
            las recomendaciones.

    Returns:
        dict: Diccionario con el nivel de habilidad, la categoría
            correspondiente, la precisión, las etiquetas débiles
            y las preguntas recomendadas con sus justificaciones.
    """

    theta = get_user_theta(db, user_id)

    evaluations = (
        db.query(Evaluation)
        .filter_by(user_id=user_id)
        .all()
    )

    scores = [e.score for e in evaluations if e.score is not None]
    accuracy = round(
        sum(scores) / len(scores),
        2
    ) if scores else 0

    level = classify_theta(theta)

    questions = recommend_hybrid(
        db,
        user_id,
        theta
    )

    weak_tags = get_weak_tags(
        db,
        user_id
    )
    
    diff_cache = {
        q.id: (q.difficulty - theta)
        for q in questions
    }

    return {
        "theta": theta,
        "level": level,
        "accuracy": accuracy,
        "weak_tags": weak_tags,
        "recommendations": [
            {
                "id": q.id,
                "content": q.content,
                "difficulty": q.difficulty,
                "module_id": q.module_id,
                "tags": [
                    qt.tag.name
                    for qt in q.tags
                    if qt.tag
                ],
                "reason": build_reason(
                    explanation=(
                        "adaptive_learning"
                        if abs(q.difficulty - theta) < 0.5
                        else "difficulty_progression"
                    ),
                    reason_type=(
                        "adaptive_learning"
                        if abs(q.difficulty - theta) < 0.5
                        else "difficulty_progression"
                    ),
                    confidence=max(0.5, 1 - abs(diff_cache[q.id])),
                    difficulty_gap=round(abs(q.difficulty - theta), 2),
                    theta_match=abs(q.difficulty - theta) < 0.5,
                    weak_tags=[
                        qt.tag.name
                        for qt in q.tags
                        if qt.tag and str(qt.tag_id) in weak_tags
                    ]
                )
            }
            for q in questions
        ]
    }


def get_resource_recommendations_service(
    db: Session,
    user_id
):
    """
    Genera recomendaciones personalizadas de recursos de aprendizaje.

    Obtiene el nivel de habilidad del usuario, calcula su rendimiento
    e identifica sus temas débiles para recomendar recursos adecuados
    con una explicación de su relevancia.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id: Identificador del usuario para el que se generan
            las recomendaciones.

    Returns:
        dict: Diccionario con el nivel de habilidad, la categoría,
            la precisión y los recursos recomendados con sus
            respectivas justificaciones.
    """

    theta = get_user_theta(db, user_id)
    level = classify_theta(theta)

    evaluations = (
        db.query(Evaluation)
        .filter_by(user_id=user_id)
        .all()
    )

    scores = [e.score for e in evaluations if e.score is not None]
    accuracy = round(sum(scores) / len(scores), 2) if scores else 0

    resources = recommend_resources(
        db,
        user_id,
        theta
    )

    weak_tags = get_weak_tags(
        db,
        user_id
    )

    return {
        "theta": theta,
        "level": level,
        "accuracy": accuracy,
        "resources": [
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "type": r.type,
                "difficulty": r.difficulty,
                "estimated_time": r.estimated_time,
                "url": r.url,
                "reason": build_reason(
                    explanation=explain_resource(r, weak_tags),
                    reason_type="weakness_based",
                    confidence=max(0.5, 1 - abs(r.difficulty - theta)),
                    difficulty_gap=round(abs(r.difficulty - theta), 2),
                    theta_match=abs(r.difficulty - theta) < 0.5
                )
            }
            for r in resources
        ]
    }


def get_recommendation_dashboard_service(
    db: Session,
    user_id
):
    """
    Genera un resumen de las recomendaciones para el usuario.

    Combina las recomendaciones de preguntas y recursos de aprendizaje,
    incluyendo las etiquetas asociadas a los temas débiles del usuario.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id: Identificador del usuario para el que se genera
            el resumen de recomendaciones.

    Returns:
        dict: Diccionario con el nivel de habilidad, los temas débiles,
            las preguntas recomendadas y los recursos de aprendizaje
            con sus respectivas justificaciones.
    """

    theta = get_user_theta(db, user_id)

    questions = recommend_hybrid(
        db,
        user_id,
        theta
    )

    resources = recommend_resources(
        db,
        user_id,
        theta
    )

    weak_tags = get_weak_tags(
        db,
        user_id
    )

    return {
        "theta": theta,
        "weak_tags": weak_tags,
        "questions": [
            {
                "id": q.id,
                "content": q.content,
                "difficulty": q.difficulty,
                "module_id": q.module_id,
                "tags": [
                    qt.tag.name
                    for qt in q.tags
                    if qt.tag
                ],
                "reason": {
                    "theta_match": abs(q.difficulty - theta) < 0.5,
                    "weak_tags": [
                        qt.tag.name
                        for qt in q.tags
                        if qt.tag and str(qt.tag_id) in weak_tags
                    ]
                }
            }
            for q in questions
        ],
        "resources": [
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "type": r.type,
                "difficulty": r.difficulty,
                "estimated_time": r.estimated_time,
                "url": r.url,
                "reason": explain_resource(r, weak_tags)
            }
            for r in resources
        ]
    }