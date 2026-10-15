"""
Módulo: module.py
Descripción: Define los esquemas de creación y respuesta de los módulos,
             incluyendo su título, orden e identificador del curso asociado.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from uuid import UUID


class ModuleBase(BaseModel):
    """
    Define los atributos básicos de un módulo.

    Atributos:
        title (str): Título del módulo.
        order_index (int): Posición del módulo dentro del curso.
    """

    title: str
    order_index: int


class ModuleCreate(ModuleBase):
    """
    Define los datos necesarios para crear un módulo.

    Atributos:
        course_id (UUID): Identificador del curso al que pertenece
            el módulo.
    """

    course_id: UUID


class ModuleCreateSimple(BaseModel):
    """
    Define los datos básicos necesarios para crear un módulo.

    Atributos:
        title (str): Título del módulo.
        course_id (UUID): Identificador del curso al que pertenece
            el módulo.
    """

    title: str
    course_id: UUID


class ModuleResponse(ModuleBase):
    """
    Define los datos de respuesta de un módulo.

    Atributos:
        id (UUID): Identificador único del módulo.
        title (str): Título del módulo.
        order_index (int): Posición del módulo dentro del curso.
    """

    id: UUID

    class Config:
        from_attributes = True


class ModuleSearchResponse(BaseModel):
    """
    Define los datos de respuesta de una búsqueda de módulos.

    Atributos:
        id (UUID): Identificador único del módulo.
        title (str): Título del módulo.
    """

    id: UUID
    title: str

    class Config:
        from_attributes = True