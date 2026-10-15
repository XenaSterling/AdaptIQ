"""
Módulo: content_management.py
Descripción: Define los esquemas de datos para crear, actualizar
             y representar preguntas y sus respuestas.
Autor: Raquel Del Castillo Pérez
"""

from uuid import UUID
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.answer import AnswerResponse


BloomLevel = Literal[
    "remember",
    "understand",
    "apply",
    "analyze",
    "evaluate",
    "create"
]


QuestionType = Literal["single", "multiple"]


class AnswerCreateRequest(BaseModel):
    """
    Define los datos necesarios para crear una respuesta.

    Atributos:
        content (str): Contenido de la respuesta, entre 1 y 500 caracteres.
        is_correct (bool): Indica si la respuesta es correcta.
    """

    content: str = Field(min_length=1, max_length=500)
    is_correct: bool = False


class QuestionCreateRequest(BaseModel):
    """
    Define los datos necesarios para crear una pregunta.

    Atributos:
        content (str): Enunciado de entre 5 y 2000 caracteres.
        type (QuestionType): Tipo de pregunta: single o multiple.
        difficulty (float): Dificultad entre -4.0 y 4.0.
        discrimination (float): Discriminación entre 0.1 y 3.0.
        bloom_level (Optional[BloomLevel]): Nivel de Bloom.
        module_id (Optional[UUID]): Identificador del módulo.
        tag_ids (List[UUID]): Identificadores de las etiquetas.
        answers (List[AnswerCreateRequest]): Respuestas de la pregunta.
    """

    content: str = Field(min_length=5, max_length=2000)
    type: QuestionType
    difficulty: float = Field(ge=-4.0, le=4.0)
    discrimination: float = Field(ge=0.1, le=3.0)
    bloom_level: Optional[BloomLevel] = "understand"
    module_id: Optional[UUID] = None
    tag_ids: List[UUID] = Field(default_factory=list)
    answers: List[AnswerCreateRequest]

    @field_validator("bloom_level")
    @classmethod
    def validate_bloom(cls, value):
        """
        Devuelve el valor recibido sin modificarlo.
        """
        return value


class QuestionUpdateRequest(BaseModel):
    """
    Define los campos opcionales para actualizar una pregunta.

    Atributos:
        content (Optional[str]): Nuevo enunciado.
        type (Optional[QuestionType]): Tipo de pregunta.
        difficulty (Optional[float]): Dificultad entre -4.0 y 4.0.
        discrimination (Optional[float]): Discriminación entre 0.1 y 3.0.
        bloom_level (Optional[BloomLevel]): Nivel de Bloom.
        module_id (Optional[UUID]): Identificador del módulo.
        tag_ids (Optional[List[UUID]]): Identificadores de las etiquetas.
        answers (Optional[List[AnswerCreateRequest]]): Respuestas de la pregunta.
    """

    content: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=2000
    )
    type: Optional[QuestionType] = None
    difficulty: Optional[float] = Field(default=None, ge=-4.0, le=4.0)
    discrimination: Optional[float] = Field(default=None, ge=0.1, le=3.0)
    bloom_level: Optional[BloomLevel] = None
    module_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None
    answers: Optional[List[AnswerCreateRequest]] = None


class QuestionResponse(BaseModel):
    """
    Define los datos de una pregunta devueltos por la API.

    Atributos:
        id (UUID): Identificador de la pregunta.
        content (str): Enunciado de la pregunta.
        type (str): Tipo de pregunta.
        difficulty (float): Dificultad.
        discrimination (float): Discriminación.
        bloom_level (Optional[str]): Nivel de Bloom.
        module_id (Optional[UUID]): Identificador del módulo.
        tags (List[UUID]): Identificadores de las etiquetas.
        answers (List[AnswerResponse]): Respuestas asociadas.
    """

    id: UUID
    content: str
    type: str
    difficulty: float
    discrimination: float
    bloom_level: Optional[str]
    module_id: Optional[UUID]
    tags: List[UUID]
    answers: List[AnswerResponse]