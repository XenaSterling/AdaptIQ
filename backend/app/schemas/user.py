"""
Módulo: user.py
Descripción: Define los esquemas base y de respuesta para representar
             los datos de los usuarios de la aplicación.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    """
    Define los atributos básicos de un usuario.

    Atributos:
        name (str): Nombre del usuario.
        email (EmailStr): Dirección de correo electrónico del usuario.
    """

    name: str
    email: EmailStr


class UserResponse(UserBase):
    """
    Define los datos de respuesta de un usuario.

    Atributos:
        id (UUID): Identificador único del usuario.
        name (str): Nombre del usuario.
        email (EmailStr): Dirección de correo electrónico del usuario.
        role (Optional[str]): Rol asignado al usuario, si está disponible.
    """

    id: UUID
    role: Optional[str] = None

    class Config:
        from_attributes = True