"""
Módulo: explain.py
Descripción: Proporciona funciones auxiliares para favorecer
             la diversidad de las preguntas recomendadas y explicar
             la relación entre los recursos y las necesidades
             de aprendizaje del estudiante.
Autor: Raquel Del Castillo Pérez
"""

def diversity_penalty(selected_questions, question):
    """
    Calcula una penalización según la similitud entre preguntas.

    La penalización disminuye cuando la pregunta comparte etiquetas
    con las preguntas que ya han sido seleccionadas.

    Args:
        selected_questions (list): Preguntas seleccionadas previamente.
        question: Pregunta cuya diversidad se desea evaluar.

    Returns:
        float: Factor de diversidad comprendido entre 0 y 1.
    """

    tags_selected = set()

    for q in selected_questions:
        for qt in q.tags:
            tags_selected.add(qt.tag_id)

    question_tags = {qt.tag_id for qt in question.tags}

    overlap = len(tags_selected.intersection(question_tags))

    return 1 / (1 + overlap)


def explain_resource(resource, weak_tags):
    """
    Identifica el motivo principal de recomendación de un recurso.

    Comprueba si el recurso está relacionado con alguna etiqueta
    en la que el estudiante presenta dificultades.

    Args:
        resource: Recurso de aprendizaje que se evalúa.
        weak_tags (dict): Puntuaciones de debilidad por etiqueta.

    Returns:
        str: Motivo de recomendación, que indica un tema débil
            o una coincidencia con la habilidad del estudiante.
    """

    for rt in resource.tags:
        if weak_tags.get(str(rt.tag_id), 0) > 0:
            return "weak_topic"

    return "matches_ability"