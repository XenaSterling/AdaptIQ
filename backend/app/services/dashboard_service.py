"""
Módulo: dashboard_service.py
Descripción: Proporciona los datos estadísticos y analíticos necesarios
             para construir los paneles de control de estudiantes,
             profesores y administradores.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.result import Result
from app.models.question import Question
from app.models.student_ability import StudentAbility
from app.models.user import User
from app.models.role import Role
from app.models.course import Course
from app.models.evaluation import Evaluation, EvaluationStatus
from app.models.module_progress import ModuleProgress
from app.models.resource_usage import ResourceUsage

from app.ml.irt.update import update_theta
from app.ml.irt.uncertainty import compute_uncertainty
from app.ml.clustering.student_clustering import cluster_students
from app.ml.prediction.dropout_model import DropoutModel


def get_theta_evolution(db: Session, user_id: str):
    """
    Calcula la evolución de la habilidad estimada de un estudiante
    a partir de sus respuestas registradas en las evaluaciones.

    Para cada respuesta, vuelve a estimar theta utilizando el conjunto
    acumulado de respuestas hasta ese momento.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del estudiante.

    Returns:
        list[dict]: Lista ordenada de estimaciones que contiene
            el número de respuesta procesada y el valor de theta
            correspondiente.
    """

    results = (
        db.query(Result)
        .join(Result.evaluation)
        .filter(Result.evaluation.has(user_id=user_id))
        .order_by(Result.id)
        .all()
    )

    theta = 0.0
    evolution = []

    for i in range(1, len(results) + 1):

        subset = results[:i]

        responses = [
            {
                "correct": r.is_correct,
                "difficulty": r.question.difficulty,
                "discrimination": r.question.discrimination or 1.0
            }
            for r in subset
        ]

        theta = update_theta(theta, responses)

        evolution.append({
            "step": i,
            "theta": theta
        })

    return evolution


def get_student_dashboard(db: Session, user_id: str):
    """
    Genera el conjunto de indicadores del panel de control de un
    estudiante, incluyendo rendimiento, progreso, uso de recursos,
    temas con dificultades y evolución de su habilidad.

    También calcula el nivel de incertidumbre de la estimación
    de habilidad para facilitar el seguimiento del aprendizaje.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del estudiante.

    Returns:
        dict: Diccionario con la habilidad estimada, precisión,
            puntuación media, evaluaciones completadas, progreso
            por módulos, utilización de recursos, temas débiles,
            evolución de theta e incertidumbre de la estimación.
    """

    ability = db.query(StudentAbility).filter_by(user_id=user_id).first()

    results = (
        db.query(Result)
        .join(Result.evaluation)
        .filter(Result.evaluation.has(user_id=user_id))
        .all()
    )

    total = len(results)
    correct = sum(1 for r in results if r.is_correct)

    accuracy = correct / total if total > 0 else 0

    module_progress = (
        db.query(ModuleProgress)
        .filter_by(user_id=user_id)
        .all()
    )

    module_progress_data = [
        {
            "module": mp.module.title,
            "progress": round(mp.progress_percentage, 1),
            "completed": mp.completed
        }
        for mp in module_progress
    ]

    completed_modules = sum(
        1 for mp in module_progress
        if mp.completed
    )

    avg_module_progress = round(
        sum(mp.progress_percentage for mp in module_progress)
        / len(module_progress),
        2
    ) if module_progress else 0

    resource_usage = (
        db.query(ResourceUsage)
        .filter_by(user_id=user_id)
        .all()
    )

    resources_opened = len(resource_usage)

    resources_completed = sum(
        1 for ru in resource_usage
        if ru.completed
    )

    avg_resource_time = round(
        sum(
            ru.time_spent or 0
            for ru in resource_usage
        ) / len(resource_usage),
        2
    ) if resource_usage else 0

    tag_errors = defaultdict(int)
    tag_total = defaultdict(int)

    for r in results:

        question = r.question

        for qt in question.tags:

            tag_name = qt.tag.name

            tag_total[tag_name] += 1

            if not r.is_correct:
                tag_errors[tag_name] += 1

    weak_topics = {
        tag: {
            "error_rate": tag_errors[tag] / tag_total[tag]
        }
        for tag in tag_total
    }

    evaluations = (
        db.query(Evaluation)
        .filter_by(user_id=user_id)
        .all()
    )

    scores = [e.score for e in evaluations if e.score is not None]
    avg_score =  round(
        sum(scores) / len(scores),
        2
    ) if scores else 0

    evaluations_completed = (
        db.query(Evaluation)
        .filter_by(
            user_id=user_id,
            status="completed"
        )
        .count()
    )

    uncertainty = compute_uncertainty(
        db,
        user_id
    )

    if uncertainty < 0.20:
        uncertainty_level = "low"
    elif uncertainty < 0.50:
        uncertainty_level = "medium"
    else:
        uncertainty_level = "high"

    return {
        "theta": ability.theta if ability else 0.0,
        "accuracy": accuracy,
        "score": avg_score,
        "evaluations_completed": evaluations_completed,
        "completed_modules": completed_modules,
        "avg_module_progress": avg_module_progress,
        "module_progress": module_progress_data,
        "resources_opened": resources_opened,
        "resources_completed": resources_completed,
        "avg_resource_time": avg_resource_time,
        "weak_topics": weak_topics,
        "theta_evolution": get_theta_evolution(db, user_id),
        "uncertainty": uncertainty,
        "uncertainty_level": uncertainty_level
    }


def get_teacher_dashboard(db: Session):
    """
    Genera los indicadores globales del panel de control del profesor.

    Analiza el rendimiento de las respuestas y evaluaciones, identifica
    estudiantes con riesgo de abandono, detecta las preguntas con mayor
    número de errores y obtiene los grupos de estudiantes mediante
    técnicas de clustering.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        dict: Diccionario con estadísticas generales, rendimiento
            académico, distribución del riesgo de abandono, estudiantes
            de alto riesgo, preguntas con más errores y cohortes.
    """

    results = db.query(Result).all()

    total_answers = len(results)
    total_evaluations = db.query(Evaluation).count()

    correct = sum(1 for r in results if r.is_correct)
    accuracy = correct / total_answers if total_answers > 0 else 0

    total_students = db.query(User).filter_by(role=3).count()

    dropout_model = DropoutModel()

    risk_scores = dropout_model.predict_all_students(db)

    struggling_students = sum(
        1 for r in risk_scores if r["risk_category"] != "low"
    )

    high_risk_students = []

    for r in risk_scores:

        if r["risk_category"] != "high":
            continue

        student = (
            db.query(User)
            .filter_by(id=r["user_id"])
            .first()
        )

        if student:
            high_risk_students.append({
                "id": str(student.id),
                "name": student.name,
                "risk_score": round(r["risk_score"], 2)
            })

    risk_breakdown = {
        "low": 0,
        "medium": 0,
        "high": 0
    }

    for r in risk_scores:
        cat = r["risk_category"]
        risk_breakdown[cat] += 1

    completed_scores = [
        e.score
        for e in db.query(Evaluation)
        .filter(Evaluation.status == EvaluationStatus.completed)
        .all() if e.score is not None
    ]
    avg_score = round(sum(completed_scores) / len(completed_scores), 2) if completed_scores else 0

    theta_values = [s.theta for s in db.query(StudentAbility).all()]
    avg_theta = round(sum(theta_values) / len(theta_values), 2) if theta_values else 0

    question_errors = defaultdict(int)

    for r in results:
        if not r.is_correct:
            question_errors[r.question_id] += 1

    most_failed = []

    for question_id, errors in sorted(
        question_errors.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]:

        question = db.query(Question).filter_by(
            id=question_id
        ).first()

        most_failed.append({
            "question_id": str(question_id),
            "question_text": question.content if question else "Unknown question",
            "errors": errors
        })

    cohorts = cluster_students(db)

    return {
        "total_students": total_students,
        "accuracy": accuracy,
        "avg_score": avg_score,
        "avg_theta": avg_theta,
        "most_failed_questions": most_failed,
        "cohorts": cohorts,
        "struggling_students": struggling_students,
        "risk_breakdown": risk_breakdown,
        "high_risk_students": high_risk_students,
        "total_answers": total_answers,
        "total_evaluations": total_evaluations
    }


def get_admin_dashboard(db: Session):
    """
    Genera las estadísticas generales del sistema para el panel
    de administración.

    Incluye el número de usuarios, cursos y evaluaciones, las
    puntuaciones y habilidades medias, las evaluaciones abandonadas
    y la distribución de usuarios y evaluaciones por categoría.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        dict: Diccionario con los indicadores globales del sistema,
            el desglose de usuarios por rol y la distribución
            de evaluaciones según su estado.
    """

    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_evaluations = db.query(Evaluation).count()

    completed_scores = [
        e.score
        for e in db.query(Evaluation)
        .filter(Evaluation.status == EvaluationStatus.completed)
        .all() if e.score is not None
    ]
    avg_score = round(sum(completed_scores) / len(completed_scores), 2) if completed_scores else 0

    theta_values = [s.theta for s in db.query(StudentAbility).all()]
    avg_theta = round(sum(theta_values) / len(theta_values), 2) if theta_values else 0

    abandoned = db.query(Evaluation).filter(Evaluation.status == EvaluationStatus.abandoned).count()

    roles = db.query(Role).all()

    role_breakdown = {
        role.name: db.query(User).filter_by(role=role.id).count()
        for role in roles
    }

    evaluation_breakdown = {
        "completed": db.query(Evaluation)
            .filter(Evaluation.status == EvaluationStatus.completed)
            .count(),

        "abandoned": db.query(Evaluation)
            .filter(Evaluation.status == EvaluationStatus.abandoned)
            .count(),

        "in_progress": db.query(Evaluation)
            .filter(Evaluation.status == EvaluationStatus.in_progress)
            .count()
    }

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_evaluations": total_evaluations,
        "avg_score": avg_score,
        "avg_theta": avg_theta,
        "abandoned": abandoned,
        "role_breakdown": role_breakdown,
        "evaluation_breakdown": evaluation_breakdown
    }