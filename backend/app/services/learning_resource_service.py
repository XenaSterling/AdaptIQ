"""
Módulo: learning_resource_service.py
Descripción: Gestiona los recursos de aprendizaje, permitiendo
             crearlos, consultarlos, actualizarlos y eliminarlos,
             así como administrar sus etiquetas asociadas.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session, joinedload

from app.models.learning_resource import LearningResource
from app.models.resource_tag import ResourceTag


def serialize_resource(resource: LearningResource):
    """
    Convierte un recurso de aprendizaje en un diccionario.

    Incluye los datos del recurso y las etiquetas asociadas.

    Atributos:
        resource (LearningResource): Recurso que se desea serializar.

    Returns:
        dict: Diccionario con los datos del recurso y sus etiquetas.
    """

    return {
        "id": resource.id,
        "title": resource.title,
        "description": resource.description,
        "url": resource.url,
        "type": resource.type,
        "difficulty": resource.difficulty,
        "estimated_time": resource.estimated_time,
        "module_id": resource.module_id,
        "tags": [
            {
                "id": str(rt.tag.id),
                "name": rt.tag.name
            }
            for rt in resource.tags
        ]
    }


def create_learning_resource(
    db: Session,
    payload,
    teacher_id
):
    """
    Crea un recurso de aprendizaje y asocia sus etiquetas.

    Persiste el recurso y las asociaciones de etiquetas indicadas
    en los datos recibidos.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        payload: Datos del recurso que se desea crear.
        teacher_id: Identificador del docente que crea el recurso.

    Returns:
        dict: Recurso creado con sus datos y etiquetas asociadas.
    """

    resource = LearningResource(
        title=payload.title,
        description=payload.description,
        url=payload.url,
        type=payload.type,
        difficulty=payload.difficulty,
        estimated_time=payload.estimated_time,
        module_id=payload.module_id,
        created_by=teacher_id
    )

    db.add(resource)
    db.flush()

    for tag_id in payload.tag_ids:

        db.add(
            ResourceTag(
                resource_id=resource.id,
                tag_id=tag_id
            )
        )

    db.commit()
    db.refresh(resource)

    return serialize_resource(resource)


def list_learning_resources(db: Session):
    """
    Obtiene todos los recursos de aprendizaje con sus etiquetas.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        list: Lista de recursos serializados con sus etiquetas.
    """

    resources = (
        db.query(LearningResource)
        .options(
            joinedload(LearningResource.tags)
            .joinedload(ResourceTag.tag)
        )
        .all()
    )

    return [
        serialize_resource(r)
        for r in resources
    ]


def update_learning_resource(
    db: Session,
    resource_id: str,
    payload
):
    """
    Actualiza los datos de un recurso de aprendizaje y sus etiquetas.

    Modifica los campos recibidos y sustituye las asociaciones
    de etiquetas cuando se proporciona el atributo tag_ids.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        resource_id (str): Identificador del recurso que se actualizará.
        payload: Datos con los campos que se desean modificar.

    Returns:
        dict | None: Recurso actualizado y serializado, o None
            si no existe el recurso indicado.
    """

    resource = (
        db.query(LearningResource)
        .options(
            joinedload(LearningResource.tags)
            .joinedload(ResourceTag.tag)
        )
        .filter_by(id=resource_id)
        .first()
    )

    if not resource:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():

        if field != "tag_ids":
            setattr(resource, field, value)

    if payload.tag_ids is not None:

        db.query(ResourceTag).filter_by(
            resource_id=resource.id
        ).delete()

        for tag_id in payload.tag_ids:

            db.add(
                ResourceTag(
                    resource_id=resource.id,
                    tag_id=tag_id
                )
            )

    db.commit()
    db.refresh(resource)

    return serialize_resource(resource)


def delete_learning_resource(
    db: Session,
    resource_id: str
):
    """
    Elimina un recurso de aprendizaje de la base de datos.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        resource_id (str): Identificador del recurso que se eliminará.

    Returns:
        bool: True si el recurso existía y se eliminó; False
            si no se encontró.
    """

    resource = (
        db.query(LearningResource)
        .filter_by(id=resource_id)
        .first()
    )

    if not resource:
        return False

    db.delete(resource)

    db.commit()

    return True