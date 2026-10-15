"""
Módulo: role.py
Descripción: Define el modelo ORM que representa los roles
             asignables a los usuarios de la aplicación.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Role(Base):
    """
    Representa un rol de usuario.

    Atributos:
        id (int): Identificador único del rol.
        name (str): Nombre único del rol.
        users (list[User]): Usuarios asociados al rol.
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        back_populates="role_rel"
    )