"""
Módulo: evaluation_settings_service.py
Descripción: Gestiona la configuración específica de las evaluaciones,
             permitiendo consultar, crear y actualizar los parámetros
             utilizados por el motor de evaluación adaptativa.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session
from app.models.evaluation_settings import EvaluationSettings


def get_evaluation_settings(db: Session, evaluation_id: str):
    """
    Obtiene la configuración asociada a una evaluación.

    Si todavía no existe un registro de configuración, crea uno
    utilizando los valores predeterminados definidos en el modelo
    EvaluationSettings y lo persiste en la base de datos.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        evaluation_id (str): Identificador de la evaluación
            cuya configuración se desea consultar.

    Returns:
        EvaluationSettings: Objeto con los parámetros de configuración
            de la evaluación, existentes o recién creados.
    """

    settings = (
        db.query(EvaluationSettings)
        .filter_by(evaluation_id=evaluation_id)
        .first()
    )

    if not settings:
        settings = EvaluationSettings(
            evaluation_id=evaluation_id
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


def update_evaluation_settings(db: Session, evaluation_id: str, data: dict):
    """
    Actualiza la configuración de una evaluación a partir de un
    diccionario de parámetros.

    Obtiene la configuración existente o crea una nueva si todavía
    no existe. Después, actualiza únicamente los atributos cuyos
    valores recibidos no sean None y persiste los cambios.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        evaluation_id (str): Identificador de la evaluación
            cuya configuración se desea modificar.
        data (dict): Diccionario de atributos y valores que se
            desean actualizar. Los valores None se ignoran.

    Returns:
        EvaluationSettings: Objeto de configuración actualizado
            y sincronizado con la base de datos.
    """

    settings = get_evaluation_settings(db, evaluation_id)

    for key, value in data.items():
        if value is not None:
            setattr(settings, key, value)

    db.commit()
    db.refresh(settings)

    return settings