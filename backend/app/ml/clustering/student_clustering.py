"""
Módulo: clustering.py
Descripción: Agrupa a los estudiantes según su nivel de habilidad
             estimado mediante el algoritmo de agrupamiento K-Means.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session
from sklearn.cluster import KMeans

from app.models.student_ability import StudentAbility


def cluster_students(db: Session, k: int = 3):
    """
    Agrupa a los estudiantes según sus valores de theta.

    Ajusta el número de grupos a la cantidad de registros disponibles
    y devuelve un grupo único cuando no es posible realizar
    un agrupamiento con varios clústeres.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        k (int): Número máximo de clústeres que se crearán.

    Returns:
        list: Lista de estudiantes con su identificador, clúster
            asignado y valor de theta.
    """

    abilities = db.query(StudentAbility).all()

    if not abilities:
        return []

    X = [[a.theta] for a in abilities]

    k = min(k, len(X))

    if k <= 1:
        return [
            {
                "user_id": str(a.user_id),
                "cluster": 0,
                "theta": a.theta
            }
            for a in abilities
        ]

    model = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = model.fit_predict(X)

    return [
        {
            "user_id": str(abilities[i].user_id),
            "cluster": int(labels[i]),
            "theta": abilities[i].theta
        }
        for i in range(len(abilities))
    ]