"""
Módulo: teacher_service.py
Descripción: Proporciona información general sobre la actividad
             académica y analiza el rendimiento de los estudiantes
             para identificar posibles situaciones de riesgo.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.result import Result
from app.models.evaluation import Evaluation
from app.models.user import User


def get_teacher_overview(db: Session):
    """
    Obtiene un resumen general de la actividad académica.

    Calcula el número de estudiantes, evaluaciones y respuestas,
    la precisión global y la cantidad de estudiantes con un
    porcentaje de respuestas correctas inferior al 50 %.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        dict: Diccionario con el número total de estudiantes,
            evaluaciones y respuestas, la precisión global
            y la cantidad de estudiantes con dificultades.
    """

    results = db.query(Result).all()
    evaluations = db.query(Evaluation).all()
    users = db.query(User).all()

    total_answers = len(results)
    total_evaluations = len(evaluations)
    total_students = len(users)

    correct = sum(1 for r in results if r.is_correct)

    accuracy = correct / total_answers if total_answers else 0

    student_scores = defaultdict(lambda: {"correct": 0, "total": 0})

    for r in results:
        uid = r.evaluation.user_id
        student_scores[uid]["total"] += 1
        if r.is_correct:
            student_scores[uid]["correct"] += 1

    struggling_students = sum(
        1 for s in student_scores.values()
        if s["total"] > 0 and (s["correct"] / s["total"]) < 0.5
    )

    return {
        "total_students": total_students,
        "total_evaluations": total_evaluations,
        "total_answers": total_answers,
        "accuracy": accuracy,
        "struggling_students": struggling_students
    }


def get_student_risk_analysis(db: Session):
    """
    Analiza el rendimiento de los estudiantes para identificar
    posibles situaciones de riesgo académico.

    Clasifica a cada estudiante según su porcentaje de respuestas
    correctas: riesgo bajo, medio o alto.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        list[dict]: Lista de estudiantes con respuestas registradas,
            incluyendo su identificador, precisión, nivel de riesgo
            y número total de respuestas.
    """

    results = db.query(Result).all()

    student_map = defaultdict(lambda: {"correct": 0, "total": 0})

    for r in results:
        uid = r.evaluation.user_id
        student_map[uid]["total"] += 1
        if r.is_correct:
            student_map[uid]["correct"] += 1

    output = []

    for user_id, stats in student_map.items():

        if stats["total"] == 0:
            continue

        accuracy = stats["correct"] / stats["total"]

        risk_level = "low"
        if accuracy < 0.4:
            risk_level = "high"
        elif accuracy < 0.7:
            risk_level = "medium"

        output.append({
            "user_id": user_id,
            "accuracy": accuracy,
            "risk_level": risk_level,
            "total_answers": stats["total"]
        })

    return output