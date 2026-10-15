"""
Módulo: auth.py
Descripción: Define los endpoints de autenticación de usuarios,
             incluyendo el registro de nuevas cuentas y el inicio
             de sesión mediante credenciales.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.service import register_user, authenticate_user
from app.auth.security import create_access_token
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RegisterResponse,
    TokenResponse
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/register",
    response_model = RegisterResponse
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Registra un nuevo usuario en la aplicación.

    Args:
        payload (RegisterRequest): Datos necesarios para registrar
            al usuario, incluyendo nombre, correo y contraseña.
        db (Session): Sesión de base de datos.

    Returns:
        RegisterResponse: Identificador y correo del usuario registrado.
    """

    user = register_user(
        db,
        payload.name,
        payload.email,
        payload.password
    )

    return RegisterResponse(
        id = str(user.id),
        email = user.email
    )


@router.post(
    "/login",
    response_model = TokenResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Autentica a un usuario y genera un token de acceso.

    Args:
        payload (LoginRequest): Credenciales del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        TokenResponse: Token de acceso, tipo de token, identificador
            del usuario y rol asignado.

    Raises:
        HTTPException: Si las credenciales no son válidas,
            devuelve el estado 401.
    """

    user = authenticate_user(
        db,
        payload.email,
        payload.password
    )

    if not user:
        raise HTTPException(
            status_code = 401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role_rel.name,
        "email": user.email
    })

    return TokenResponse(
        access_token = token,
        token_type = "bearer",
        user_id = str(user.id),
        role = user.role_rel.name
    )