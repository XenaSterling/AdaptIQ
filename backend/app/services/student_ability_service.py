"""
Módulo: student_ability.py
Descripción: Gestiona la consulta y creación de los registros
             de habilidad de los estudiantes, inicializando
             el nivel de habilidad cuando todavía no existe.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.student_ability import StudentAbility


def get_or_create_student_ability(
    db: Session,
    user_id: str
):
    """
    Obtiene el registro de habilidad de un estudiante o lo crea.

    Comprueba que el usuario exista y, si todavía no tiene un registro
    de habilidad, crea uno con el valor inicial de theta igual a 0.0.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del usuario cuya habilidad
            se desea consultar.

    Returns:
        StudentAbility: Registro de habilidad existente o recién creado.

    Raises:
        HTTPException: Si el usuario no existe, devuelve un error 404.
    """

    user = (
        db.query(User)
        .filter_by(id=user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

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

    return ability