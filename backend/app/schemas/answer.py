"""
Módulo: answer.py
Descripción: Define los esquemas de validación y respuesta
             para las respuestas asociadas a preguntas.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel


class AnswerBase(BaseModel):
    """
    Define los campos comunes de una respuesta.

    Atributos:
        content (str): Contenido de la respuesta.
        is_correct (bool): Indica si la respuesta es correcta.
    """

    content: str
    is_correct: bool = False


class AnswerCreate(AnswerBase):
    """
    Define los datos necesarios para crear una respuesta.

    Atributos:
        question_id (str): Identificador de la pregunta asociada.
    """

    question_id: str


class AnswerResponse(AnswerBase):
    """
    Define los datos de una respuesta devueltos por la API.

    Atributos:
        id (str): Identificador de la respuesta.
        question_id (str): Identificador de la pregunta asociada.
    """

    id: str
    question_id: str

    class Config:
        from_attributes = True