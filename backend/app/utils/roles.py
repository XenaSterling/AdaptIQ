"""
Módulo: roles.py
Descripción: Proporciona funciones auxiliares para obtener y crear
             roles de usuario predeterminados en la base de datos.
Autor: Raquel Del Castillo Pérez
"""

from app.models.role import Role


def get_or_create_default_role(db, name="student"):
    """
    Obtiene un rol existente o crea uno nuevo si no existe.

    Args:
        db: Sesión de conexión con la base de datos.
        name (str): Nombre del rol que se desea obtener o crear.
            Por defecto, se utiliza el rol "student".

    Returns:
        Role: Objeto del rol existente o del rol recién creado.
    """

    role = db.query(Role).filter(Role.name == name).first()

    if role:
        return role

    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)

    return role