"""
Módulo: common.py
Descripción: Define los esquemas comunes para mensajes,
             errores y respuestas paginadas.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel
from typing import Any


class MessageResponse(BaseModel):
    """
    Define una respuesta que contiene un mensaje.

    Atributos:
        message (str): Texto del mensaje.
    """

    message: str


class ErrorResponse(BaseModel):
    """
    Define una respuesta que contiene información de error.

    Atributos:
        detail (str): Descripción del error.
    """

    detail: str


class PaginatedResponse(BaseModel):
    """
    Define una respuesta con el total de elementos y una lista de datos.

    Atributos:
        total (int): Número total de elementos.
        items (list[Any]): Lista de elementos de la respuesta.
    """

    total: int
    items: list[Any]