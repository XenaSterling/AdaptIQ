"""
Módulo: tag_service.py
Descripción: Gestiona las etiquetas, permitiendo consultarlas,
             buscarlas por nombre y crear nuevas etiquetas
             sin duplicar las existentes.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session

from app.models.tag import Tag


def list_tags(db: Session):
    """
    Obtiene todas las etiquetas ordenadas por nombre.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        list[Tag]: Lista de etiquetas ordenadas alfabéticamente.
    """

    return (
        db.query(Tag)
        .order_by(Tag.name)
        .all()
    )


def search_tags(db: Session, q: str):
    """
    Busca etiquetas cuyo nombre contenga el texto indicado.

    La búsqueda no distingue entre mayúsculas y minúsculas
    y devuelve un máximo de diez resultados.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        q (str): Texto que se desea buscar en el nombre de la etiqueta.

    Returns:
        list[Tag]: Lista de etiquetas coincidentes, ordenadas
            por nombre y limitada a diez resultados.
    """

    return (
        db.query(Tag)
        .filter(Tag.name.ilike(f"%{q}%"))
        .order_by(Tag.name)
        .limit(10)
        .all()
    )


def create_tag(db: Session, name: str):
    """
    Obtiene una etiqueta existente o crea una nueva.

    Si ya existe una etiqueta con el mismo nombre, sin distinguir
    entre mayúsculas y minúsculas, devuelve el registro existente.
    En caso contrario, crea y persiste una nueva etiqueta.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        name (str): Nombre de la etiqueta que se desea crear.

    Returns:
        Tag: Etiqueta existente o recién creada.
    """

    existing = (
        db.query(Tag)
        .filter(Tag.name.ilike(name))
        .first()
    )

    if existing:
        return existing

    tag = Tag(name=name)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag