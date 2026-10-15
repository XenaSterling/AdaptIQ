"""
Módulo: learning_resource.py
Descripción: Define los esquemas de solicitud y respuesta para la creación,
             actualización y consulta de recursos de aprendizaje, incluyendo
             sus características, dificultad, módulo asociado y etiquetas.
Autor: Raquel Del Castillo Pérez
"""

from typing import Optional, List, Literal
from uuid import UUID

from pydantic import BaseModel, Field


ResourceType = Literal[
    "video",
    "article",
    "pdf",
    "exercise"
]


class LearningResourceCreateRequest(BaseModel):
    """
    Define los datos necesarios para crear un recurso de aprendizaje.

    Atributos:
        title (str): Título del recurso, con una longitud de entre
            3 y 255 caracteres.
        description (Optional[str]): Descripción del contenido del recurso.
        url (str): Dirección de acceso al recurso.
        type (ResourceType): Tipo de recurso, que puede ser vídeo,
            artículo, PDF o ejercicio.
        difficulty (float): Nivel de dificultad del recurso, comprendido
            entre -4.0 y 4.0.
        estimated_time (Optional[float]): Tiempo estimado necesario
            para completar o consultar el recurso.
        module_id (Optional[UUID]): Identificador del módulo asociado,
            si existe.
        tag_ids (List[UUID]): Lista de identificadores de las etiquetas
            asociadas al recurso.
    """

    title: str = Field(
        min_length=3,
        max_length=255
    )

    description: Optional[str] = None
    url: str
    type: ResourceType
    difficulty: float = Field(
        ge=-4.0,
        le=4.0
    )
    estimated_time: Optional[float] = None
    module_id: Optional[UUID] = None
    tag_ids: List[UUID] = []


class LearningResourceUpdateRequest(BaseModel):
    """
    Define los datos que pueden modificarse en un recurso de aprendizaje.

    Atributos:
        title (Optional[str]): Título del recurso.
        description (Optional[str]): Descripción del contenido del recurso.
        url (Optional[str]): Dirección de acceso al recurso.
        type (Optional[ResourceType]): Tipo de recurso.
        difficulty (Optional[float]): Nivel de dificultad del recurso,
            comprendido entre -4.0 y 4.0.
        estimated_time (Optional[float]): Tiempo estimado necesario
            para completar o consultar el recurso.
        module_id (Optional[UUID]): Identificador del módulo asociado.
        tag_ids (Optional[List[UUID]]): Lista de identificadores de las
            etiquetas asociadas al recurso.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    type: Optional[ResourceType] = None
    difficulty: Optional[float] = Field(
        default=None,
        ge=-4.0,
        le=4.0
    )
    estimated_time: Optional[float] = None
    module_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None


class ResourceTagResponse(BaseModel):
    """
    Define los datos de respuesta de una etiqueta asociada a un recurso.

    Atributos:
        id (str): Identificador de la etiqueta.
        name (str): Nombre de la etiqueta.
    """

    id: str
    name: str


class LearningResourceResponse(BaseModel):
    """
    Define los datos de respuesta de un recurso de aprendizaje.

    Atributos:
        id (UUID): Identificador único del recurso.
        title (str): Título del recurso.
        description (Optional[str]): Descripción del contenido del recurso.
        url (str): Dirección de acceso al recurso.
        type (str): Tipo de recurso de aprendizaje.
        difficulty (float): Nivel de dificultad del recurso.
        estimated_time (Optional[float]): Tiempo estimado necesario
            para completar o consultar el recurso.
        module_id (Optional[UUID]): Identificador del módulo asociado.
        tags (List[ResourceTagResponse]): Lista de etiquetas asociadas
            al recurso.
    """

    id: UUID
    title: str
    description: Optional[str]
    url: str
    type: str
    difficulty: float
    estimated_time: Optional[float]
    module_id: Optional[UUID]
    tags: List[ResourceTagResponse]