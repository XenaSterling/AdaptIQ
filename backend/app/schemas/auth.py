"""
Módulo: auth.py
Descripción: Define los esquemas de entrada y respuesta para
             el registro y el inicio de sesión.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """
    Define los datos necesarios para registrar un usuario.

    Atributos:
        name (str): Nombre del usuario.
        email (EmailStr): Correo electrónico.
        password (str): Contraseña proporcionada.
    """

    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """
    Define las credenciales necesarias para iniciar sesión.

    Atributos:
        email (EmailStr): Correo electrónico.
        password (str): Contraseña proporcionada.
    """

    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    """
    Define los datos devueltos tras el registro.

    Atributos:
        id (str): Identificador del usuario.
        email (EmailStr): Correo electrónico registrado.
    """

    id: str
    email: EmailStr


class TokenResponse(BaseModel):
    """
    Define los datos de la respuesta de autenticación.

    Atributos:
        access_token (str): Token de acceso.
        token_type (str): Tipo de token.
        user_id (str): Identificador del usuario.
        role (str): Rol del usuario.
    """

    access_token: str
    token_type: str
    user_id: str
    role: str