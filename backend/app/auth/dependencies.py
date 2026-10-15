"""
Módulo: dependencies.py
Descripción: Define las dependencias de autenticación y autorización
             de la aplicación, incluyendo la validación de tokens JWT
             y la comprobación de permisos según el rol del usuario.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import JWTError, jwt

from app.core.settings import settings


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Valida el token JWT y obtiene los datos del usuario autenticado.

    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales
            de autorización que contienen el token JWT.

    Returns:
        dict: Contenido del token con los datos del usuario autenticado.

    Raises:
        HTTPException: Si el token es inválido o no contiene
            el identificador del usuario, devuelve el estado 401.
    """

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def require_role(
    allowed_roles: list[str]
):
    """
    Crea una dependencia que comprueba los roles permitidos.

    Args:
        allowed_roles (list[str]): Lista de roles autorizados
            para acceder al recurso.

    Returns:
        Callable: Dependencia que valida el rol del usuario
            autenticado y devuelve los datos de su token.

    Raises:
        HTTPException: Si el rol del usuario no está permitido,
            devuelve el estado 403.
    """

    def checker(
        payload=Depends(get_current_user)
    ):
        """
        Comprueba si el usuario autenticado tiene un rol permitido.

        Args:
            payload (dict): Datos del usuario obtenidos del token JWT.

        Returns:
            dict: Datos del usuario autenticado si tiene permisos.

        Raises:
            HTTPException: Si el usuario carece de permisos,
                devuelve el estado 403.
        """

        role = payload.get("role")

        if role not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )

        return payload

    return checker


def require_authentication():
    """
    Define una dependencia que permite el acceso a los roles
    de estudiante, docente y administrador.

    Returns:
        Callable: Dependencia que comprueba la autenticación
            y la pertenencia a uno de los roles permitidos.
    """

    return require_role([
        "student",
        "teacher",
        "admin"
    ])


def require_student():
    """
    Define una dependencia de autorización para estudiantes.

    Returns:
        Callable: Dependencia que permite el acceso únicamente
            a usuarios con el rol de estudiante.
    """

    return require_role([
        "student"
    ])


def require_teacher():
    """
    Define una dependencia de autorización para docentes.

    Returns:
        Callable: Dependencia que permite el acceso únicamente
            a usuarios con el rol de docente.
    """

    return require_role([
        "teacher"
    ])


def require_admin():
    """
    Define una dependencia de autorización para administradores.

    Returns:
        Callable: Dependencia que permite el acceso únicamente
            a usuarios con el rol de administrador.
    """

    return require_role([
        "admin"
    ])