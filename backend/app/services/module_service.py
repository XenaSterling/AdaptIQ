"""
Módulo: module_service.py
Descripción: Gestiona las operaciones de consulta, búsqueda
             y creación de módulos formativos asociados a cursos.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session

from app.models.module import Module


def list_modules(db: Session):
    """
    Obtiene todos los módulos ordenados por título.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        list[Module]: Lista de módulos ordenados alfabéticamente.
    """

    return (
        db.query(Module)
        .order_by(Module.title)
        .all()
    )


def search_modules(
    db: Session,
    q: str
):
    """
    Busca módulos por coincidencia en el título.

    La búsqueda no distingue entre mayúsculas y minúsculas
    y devuelve un máximo de diez resultados.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        q (str): Texto que se desea buscar en el título del módulo.

    Returns:
        list[Module]: Lista de módulos coincidentes, ordenados
            por título y limitada a diez resultados.
    """

    return (
        db.query(Module)
        .filter(Module.title.ilike(f"%{q}%"))
        .order_by(Module.title)
        .limit(10)
        .all()
    )


def create_module(
    db: Session,
    title: str,
    course_id
):
    """
    Obtiene un módulo existente o crea uno nuevo para un curso.

    Si ya existe un módulo con el mismo título y curso, devuelve
    el registro existente. En caso contrario, crea y persiste uno nuevo.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        title (str): Título del módulo.
        course_id: Identificador del curso al que pertenece el módulo.

    Returns:
        Module: Módulo existente o recién creado.
    """

    existing = (
        db.query(Module)
        .filter(
            Module.title.ilike(title),
            Module.course_id == course_id
        )
        .first()
    )

    if existing:
        return existing

    module = Module(
        title=title,
        course_id=course_id
    )

    db.add(module)
    db.commit()
    db.refresh(module)

    return module