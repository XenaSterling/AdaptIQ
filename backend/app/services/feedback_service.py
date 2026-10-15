"""
Módulo: feedback_service.py
Descripción: Gestiona la generación de retroalimentación de las evaluaciones,
             incluyendo el rendimiento, la evolución del nivel de habilidad,
             los temas débiles y los recursos de aprendizaje recomendados.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.models.evaluation import Evaluation

from app.ml.irt.uncertainty import compute_uncertainty
from app.ml.recommender.tag_based import get_weak_tags
from app.ml.recommender.resource_recommender import recommend_resources


def classify_theta(theta: float):
    """
    Clasifica el nivel de habilidad según el valor de theta.

    Atributos:
        theta (float): Nivel de habilidad estimado.

    Returns:
        str: Categoría de nivel: "basic", "intermediate" o "advanced".
    """

    if theta < -1:
        return "basic"

    if theta < 1:
        return "intermediate"

    return "advanced"


def classify_performance(score: float):
    """
    Clasifica el rendimiento según la puntuación obtenida.

    Atributos:
        score (float): Puntuación obtenida en la evaluación.

    Returns:
        str: Categoría de rendimiento: "excellent", "good",
            "acceptable" o "needs_improvement".
    """

    if score >= 9:
        return "excellent"

    if score >= 7:
        return "good"

    if score >= 5:
        return "acceptable"

    return "needs_improvement"


def generate_feedback(
    db: Session,
    evaluation: Evaluation,
    user_id: str
):
    """
    Genera la retroalimentación asociada a una evaluación.

    Calcula las métricas de rendimiento, la evolución del nivel
    de habilidad, la incertidumbre, los temas que requieren refuerzo
    y los recursos de aprendizaje recomendados.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        evaluation (Evaluation): Evaluación cuyos resultados se analizan.
        user_id (str): Identificador del usuario evaluado.

    Returns:
        dict: Diccionario con el resumen, el rendimiento, la mejora,
            el nivel estimado, la precisión, la evolución de theta,
            la incertidumbre, los temas débiles y los recursos
            de aprendizaje recomendados.
    """

    results = evaluation.results

    total = len(results)

    correct = sum(
        1 for r in results
        if r.is_correct
    )

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    initial_theta = (
        results[0].theta_before
        if results
        else 0.0
    )

    final_theta = (
        evaluation.final_theta
        or evaluation.current_theta
        or initial_theta
    )

    theta_change = (
        final_theta - initial_theta
    )

    level = classify_theta(final_theta)

    performance = classify_performance(
        evaluation.score or 0
    )

    summary = (
        f"Has respondido correctamente "
        f"{correct} de {total} preguntas. "
        f"Tu nivel estimado actual es "
        f"{round(final_theta, 2)}."
    )

    if theta_change > 0.5:

        improvement = (
            "Se observa una mejora significativa "
            "durante la evaluación."
        )

    elif theta_change > 0:

        improvement = (
            "Se observa una ligera mejora "
            "durante la evaluación."
        )

    elif theta_change < -0.5:

        improvement = (
            "El rendimiento ha estado "
            "por debajo de lo esperado."
        )

    else:

        improvement = (
            "El nivel estimado se mantiene estable."
        )

    uncertainty = compute_uncertainty(
        db,
        user_id
    )

    weak_tags = get_weak_tags(
        db,
        user_id
    )

    weak_topics = []

    ordered = sorted(
        weak_tags.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for tag_id, weakness in ordered[:3]:

        tag = (
            db.query(Tag)
            .filter(Tag.id == tag_id)
            .first()
        )

        if not tag:
            continue

        weak_topics.append(
            {
                "id": str(tag.id),
                "name": tag.name,
                "weakness": round(
                    weakness,
                    2
                )
            }
        )

    resources = recommend_resources(
        db,
        user_id,
        final_theta,
        limit=3
    )

    recommended_resources = [
        {
            "id": str(r.id),
            "title": r.title,
            "type": str(r.type),
            "url": r.url
        }
        for r in resources
    ]

    return {
        "summary": summary,
        "performance": performance,
        "improvement": improvement,
        "level": level,
        "accuracy": round(accuracy, 2),
        "theta": round(final_theta, 2),
        "theta_change": round(theta_change, 2),
        "uncertainty": round(uncertainty, 3),
        "weak_topics": weak_topics,
        "recommended_resources": recommended_resources
    }