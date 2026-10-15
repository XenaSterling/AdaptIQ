"""
Módulo: service.py
Descripción: Gestiona las operaciones de autenticación de usuarios,
             incluyendo el registro de nuevas cuentas, la comprobación
             de correos electrónicos existentes y la validación
             de credenciales durante el inicio de sesión.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import HTTPException

from app.models.user import User
from app.models.role import Role
from app.auth.security import (
    hash_password,
    verify_password
)
from app.utils.roles import get_or_create_default_role


def register_user(
    db,
    name,
    email,
    password,
    role_id = 1
):
    """
    Registra un nuevo usuario y le asigna el rol de estudiante.

    Args:
        db: Sesión de conexión con la base de datos.
        name: Nombre del usuario.
        email: Correo electrónico del usuario.
        password: Contraseña del usuario en texto plano.
        role_id: Identificador de rol opcional. El registro asigna
            el rol de estudiante independientemente de este parámetro.

    Returns:
        User: Objeto del usuario registrado.

    Raises:
        HTTPException: Si el correo electrónico ya está registrado,
            devuelve el estado 400.
        Exception: Si no existe el rol de estudiante en la base
            de datos, indica un problema de inicialización.
    """

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(password)

    default_role = db.query(Role).filter_by(name="student").first()

    if not default_role:
        raise Exception("Role 'student' must exist (seed issue)")

    user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role_rel = default_role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db,
    email,
    password
):
    """
    Comprueba las credenciales de un usuario.

    Args:
        db: Sesión de conexión con la base de datos.
        email: Correo electrónico del usuario.
        password: Contraseña proporcionada durante el inicio de sesión.

    Returns:
        User | None: Usuario autenticado si las credenciales son
            correctas, o None si el usuario no existe o la contraseña
            no coincide.
    """

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user