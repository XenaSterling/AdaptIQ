"""
Módulo: admin_user.py
Descripción: Define los esquemas de validación y respuesta para
             la gestión administrativa de usuarios.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class AdminUserBase(BaseModel):
    """
    Define los campos comunes de un usuario.

    Atributos:
        name (str): Nombre del usuario.
        email (EmailStr): Correo electrónico del usuario.
        role (str): Rol del usuario (student, teacher o admin).
        is_active (bool): Estado de actividad de la cuenta.
    """

    name: str
    email: EmailStr
    role: str
    is_active: bool = True


class AdminUserCreate(AdminUserBase):
    """
    Define los datos necesarios para crear un usuario.

    Atributos:
        password (str): Contraseña del usuario.
    """

    password: str


class AdminUserUpdate(BaseModel):
    """
    Define los campos opcionales para actualizar un usuario.

    Atributos:
        name (Optional[str]): Nombre del usuario.
        email (Optional[EmailStr]): Correo electrónico.
        role (Optional[str]): Rol del usuario.
        is_active (Optional[bool]): Estado de actividad de la cuenta.
        password (Optional[str]): Nueva contraseña.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class AdminUserResponse(BaseModel):
    """
    Define los datos de usuario devueltos por la API.

    Atributos:
        id (str): Identificador del usuario.
        name (str): Nombre del usuario.
        email (str): Correo electrónico.
        role (str): Rol asignado.
        is_active (bool): Estado de la cuenta.
    """

    id: str
    name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True