"""
Módulo: course.py
Descripción: Define los esquemas de datos para crear y representar cursos.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class CourseBase(BaseModel):
    """
    Define los campos comunes de un curso.

    Atributos:
        title (str): Título del curso.
        description (Optional[str]): Descripción del curso.
    """

    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    """
    Define los datos necesarios para crear un curso.

    Atributos:
        teacher_id (Optional[UUID]): Identificador del docente.
    """

    teacher_id: Optional[UUID] = None


class CourseResponse(CourseBase):
    """
    Define los datos de un curso devueltos por la API.

    Atributos:
        id (UUID): Identificador del curso.
    """

    id: UUID

    class Config:
        from_attributes = True