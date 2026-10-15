"""
Módulo: shared.py
Descripción: Define los esquemas compartidos para representar las respuestas
             y las preguntas utilizadas en las respuestas de la API.
Autor: Raquel Del Castillo Pérez
"""

from uuid import UUID
from pydantic import BaseModel
from typing import List


class AnswerPublic(BaseModel):
    """
    Define los datos públicos de una respuesta.

    Atributos:
        id (UUID): Identificador único de la respuesta.
        content (str): Contenido de la respuesta.
    """

    id: UUID
    content: str

    class Config:
        from_attributes = True


class QuestionPublic(BaseModel):
    """
    Define los datos públicos de una pregunta y sus respuestas.

    Atributos:
        id (UUID): Identificador único de la pregunta.
        content (str): Contenido o enunciado de la pregunta.
        type (str): Tipo de pregunta.
        answers (List[AnswerPublic]): Lista de respuestas asociadas
            a la pregunta.
    """

    id: UUID
    content: str
    type: str
    answers: List[AnswerPublic]

    class Config:
        from_attributes = True