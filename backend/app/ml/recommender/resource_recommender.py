"""
Módulo: resource_recommender.py
Descripción: Implementa un sistema de recomendación de recursos
             de aprendizaje que combina la adecuación de dificultad,
             las etiquetas débiles del estudiante, su estilo
             de aprendizaje y la novedad de los recursos.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session

from app.models.learning_resource import LearningResource
from app.models.learning_profile import LearningProfile
from app.models.learning_profile import LearningStyle
from app.models.resource_usage import ResourceUsage

from app.ml.recommender.tag_based import get_weak_tags


def learning_style_bonus(resource, profile):
    """
    Calcula una bonificación por compatibilidad con el estilo.

    Asigna una puntuación según la correspondencia entre el estilo
    de aprendizaje del estudiante y el tipo de recurso.

    Args:
        resource: Recurso de aprendizaje que se evalúa.
        profile: Perfil de aprendizaje del estudiante.

    Returns:
        float: Bonificación de compatibilidad del estilo.
    """

    if not profile:
        return 0.0

    style = profile.learning_style

    if not style:
        return 0.0

    res_type = get_resource_type_value(resource)

    if style == LearningStyle.visual and res_type == "video":
        return 1.0
    if style == LearningStyle.reading and res_type in ["article", "pdf"]:
        return 1.0
    if style == LearningStyle.kinesthetic and res_type == "exercise":
        return 1.0
    if style == LearningStyle.auditory and res_type == "video":
        return 0.8

    return 0.2


def get_resource_type_value(resource):
    """
    Obtiene el valor textual del tipo de recurso.

    Si el tipo está representado mediante una enumeración,
    devuelve su atributo value.

    Args:
        resource: Recurso cuyo tipo se desea consultar.

    Returns:
        str: Tipo de recurso en formato textual.
    """

    return (
        resource.type.value
        if hasattr(resource.type, "value")
        else resource.type
    )


def difficulty_fit(resource, theta):
    """
    Calcula la adecuación entre la dificultad y la habilidad estimada.

    Reduce la puntuación conforme aumenta la distancia entre
    la dificultad del recurso y el valor de theta del estudiante.

    Args:
        resource: Recurso de aprendizaje que se evalúa.
        theta (float): Habilidad estimada del estudiante.

    Returns:
        float: Factor de adecuación de dificultad.
    """

    gap = abs(resource.difficulty - theta)
    return max(0.0, 1.0 - (gap / 4.0))


def tag_score(resource, weak_tags):
    """
    Calcula la puntuación de un recurso según las etiquetas débiles.

    Suma las puntuaciones de debilidad correspondientes a las etiquetas
    asociadas al recurso.

    Args:
        resource: Recurso de aprendizaje que se evalúa.
        weak_tags (dict): Puntuaciones de debilidad por etiqueta.

    Returns:
        float: Puntuación de correspondencia con las dificultades.
    """

    score = 0.0

    for rt in resource.tags:
        score += weak_tags.get(str(rt.tag_id), 0.0)

    return score


def recommend_resources(db: Session, user_id: str, theta: float, limit: int = 5):
    """
    Recomienda recursos de aprendizaje adaptados al estudiante.

    Combina la adecuación de dificultad, las etiquetas débiles,
    la compatibilidad con el estilo de aprendizaje y la novedad
    de los recursos según el historial de utilización.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.
        theta (float): Habilidad estimada del estudiante.
        limit (int): Número máximo de recursos que se devolverán.

    Returns:
        list: Recursos ordenados por puntuación de recomendación.
    """

    resources = db.query(LearningResource).all()

    profile = db.query(LearningProfile).filter_by(user_id=user_id).first()

    weak_tags = get_weak_tags(db, user_id)

    scores = []

    for r in resources:

        score = 0.0

        score += difficulty_fit(r, theta) * 0.4

        score += tag_score(r, weak_tags) * 0.3

        score += learning_style_bonus(r, profile) * 0.2

        past_attempts = (
            db.query(ResourceUsage)
            .filter_by(
                user_id=user_id,
                resource_id=r.id
            )
            .count()
        )
        novelty = 1 / (1 + 0.5 * past_attempts)
        score += novelty * 0.1

        scores.append((r, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return [r for r, _ in scores[:limit]]