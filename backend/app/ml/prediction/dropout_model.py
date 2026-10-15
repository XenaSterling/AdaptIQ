"""
Módulo: dropout_model.py
Descripción: Construye las características de los estudiantes,
             genera etiquetas de riesgo y entrena un modelo
             de clasificación para predecir el riesgo de abandono
             o bajo rendimiento académico.
Autor: Raquel Del Castillo Pérez
"""

import os
import sys

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.student_ability import StudentAbility
from app.models.evaluation import Evaluation, EvaluationStatus
from app.models.result import Result
from app.models.module_progress import ModuleProgress
from app.models.resource_usage import ResourceUsage


if getattr(sys, "frozen", False):
    MODEL_PATH = os.path.join(
        sys._MEIPASS,
        "app",
        "ml",
        "prediction",
        "dropout_model.pkl"
    )
else:
    MODEL_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dropout_model.pkl"
    )


def build_features_for_user(db: Session, user_id: str):
    """
    Construye las características de un estudiante para el modelo.

    Recopila información sobre habilidad, evaluaciones, respuestas,
    progreso académico y utilización de recursos de aprendizaje.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.

    Returns:
        np.ndarray: Vector numérico con las características
            utilizadas por el modelo de predicción.
    """

    ability = (
        db.query(StudentAbility)
        .filter_by(user_id=user_id)
        .first()
    )

    evaluations = (
        db.query(Evaluation)
        .filter_by(user_id=user_id)
        .all()
    )

    results = (
        db.query(Result)
        .join(Result.evaluation)
        .filter(Evaluation.user_id == user_id)
        .all()
    )

    module_progress = (
        db.query(ModuleProgress)
        .filter_by(user_id=user_id)
        .all()
    )

    resource_usage = (
        db.query(ResourceUsage)
        .filter_by(user_id=user_id)
        .all()
    )

    theta = ability.theta if ability else 0.0

    total_evals = len(evaluations)
    completed_evals = len([
        e for e in evaluations if e.status == EvaluationStatus.completed
    ])

    scores = [e.score for e in evaluations if e.score is not None]
    avg_score = np.mean(scores) if scores else 0.0

    total_answers = len(results)
    correct = sum(1 for r in results if r.is_correct)
    accuracy = correct / total_answers if total_answers > 0 else 0.0

    theta_values = [
        r.theta_after
        for r in results
        if r.theta_after is not None
    ]

    theta_trend = (
        theta_values[-1] - theta_values[0]
        if len(theta_values) >= 2
        else 0.0
    )

    failed_difficulties = [
        r.question_difficulty
        for r in results
        if (
            not r.is_correct
            and r.question_difficulty is not None
        )
    ]

    avg_failed_difficulty = (
        float(np.mean(failed_difficulties))
        if failed_difficulties
        else 0.0
    )

    engagement = completed_evals / total_evals if total_evals > 0 else 0.0

    avg_module_progress = (
        float(np.mean([
            mp.progress_percentage
            for mp in module_progress
        ]))
        if module_progress
        else 0.0
    )

    completed_modules = sum(
        1 for mp in module_progress
        if mp.completed
    )

    resources_opened = len(resource_usage)

    resources_completed = sum(
        1 for ru in resource_usage
        if ru.completed
    )

    avg_resource_time = (
        float(np.mean([
            ru.time_spent or 0
            for ru in resource_usage
        ]))
        if resource_usage
        else 0.0
    )

    return np.array([
        theta,
        accuracy,
        avg_score,
        engagement,
        theta_trend,
        avg_failed_difficulty,
        total_answers,
        avg_module_progress,
        completed_modules,
        resources_opened,
        resources_completed,
        avg_resource_time
    ])


def build_label(db: Session, user_id: str):
    """
    Genera la etiqueta de riesgo de un estudiante mediante heurísticas.

    Considera de riesgo a los estudiantes sin evaluaciones registradas
    o cuyo rendimiento medio o habilidad estimada están por debajo
    de los umbrales establecidos.

    Importante saber que un alumno sin actividad se considerara como 
    de riesgo alto.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        user_id (str): Identificador del estudiante.

    Returns:
        int: Valor 1 si existe riesgo y 0 en caso contrario.
    """

    ability = (
        db.query(StudentAbility)
        .filter_by(user_id=user_id)
        .first()
    )

    evaluations = (
        db.query(Evaluation)
        .filter_by(user_id=user_id)
        .all()
    )

    if not evaluations:
        return 1

    scores = [e.score for e in evaluations if e.score is not None]
    avg_score = np.mean(scores) if scores else 0

    theta = ability.theta if ability else 0

    if avg_score < 4 or theta < -1.5:
        return 1
    return 0


def train_model(db: Session):
    """
    Entrena y guarda el modelo de predicción de riesgo académico.

    Obtiene los estudiantes, construye sus características y etiquetas,
    divide los datos en conjuntos de entrenamiento y prueba y ajusta
    un clasificador Random Forest.

    Args:
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        RandomForestClassifier: Modelo entrenado.

    Raises:
        Exception: Si no existen suficientes registros para entrenar.
    """

    users = (
        db.query(User)
        .filter_by(role=3)
        .all()
    )

    X = []
    y = []

    for u in users:
        try:
            x = build_features_for_user(db, u.id)
            label = build_label(db, u.id)

            X.append(x)
            y.append(label)

        except Exception as e:
            print(f"Dropout prediction error for {u.id}: {e}")

    X = np.array(X)
    y = np.array(y)

    if len(X) < 5:
        raise Exception("Not enough data to train dropout model")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model


class DropoutModel:
    """
    Gestiona la carga y utilización del modelo de predicción de riesgo.

    Atributos:
        model: Modelo de clasificación cargado desde disco,
            o None si todavía no existe un modelo guardado.
    """

    def __init__(self):
        """
        Inicializa el modelo cargándolo desde su archivo si existe.
        """

        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            self.model = None

    def predict(self, db: Session, user_id: str):
        """
        Predice el nivel de riesgo de un estudiante.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            user_id (str): Identificador del estudiante.

        Returns:
            dict: Identificador del estudiante, puntuación de riesgo
                y categoría asignada.

        Raises:
            Exception: Si el modelo todavía no ha sido entrenado.
        """

        if not self.model:
            raise Exception("Model not trained. Run train_model(db) first.")

        x = build_features_for_user(db, user_id).reshape(1, -1)

        proba = self.model.predict_proba(x)[0][1]

        if proba < 0.33:
            category = "low"
        elif proba < 0.66:
            category = "medium"
        else:
            category = "high"

        return {
            "user_id": user_id,
            "risk_score": float(proba),
            "risk_category": category
        }

    def predict_all_students(self, db: Session):
        """
        Predice el nivel de riesgo de todos los estudiantes registrados.

        Omite los estudiantes cuya predicción produce una excepción.

        Args:
            db (Session): Sesión activa de SQLAlchemy.

        Returns:
            list: Lista de predicciones individuales de riesgo.
        """

        users = (
            db.query(User)
            .filter_by(role=3)
            .all()
        )

        results = []

        for u in users:
            try:
                results.append(self.predict(db, u.id))
            except Exception as e:
                print(f"Dropout prediction error for {u.id}: {e}")

        return results