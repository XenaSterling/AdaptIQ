"""
Módulo: tag.py
Descripción: Define los esquemas de solicitud y respuesta para la creación
             y consulta de etiquetas.
Autor: Raquel Del Castillo Pérez
"""

from uuid import UUID
from pydantic import BaseModel


class TagCreateRequest(BaseModel):
    """
    Define los datos necesarios para crear una etiqueta.

    Atributos:
        name (str): Nombre de la etiqueta.
    """

    name: str


class TagResponse(BaseModel):
    """
    Define los datos de respuesta de una etiqueta.

    Atributos:
        id (UUID): Identificador único de la etiqueta.
        name (str): Nombre de la etiqueta.
    """

    id: UUID
    name: str

    class Config:
        from_attributes = True