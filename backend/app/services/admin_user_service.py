"""
Módulo: admin_user_service.py
Descripción: Gestiona las operaciones de consulta, creación, actualización
             y desactivación de usuarios desde el área de administración.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.auth.security import hash_password


def _get_role_id(db: Session, role_name: str):
    """
    Obtiene el identificador de un rol a partir de su nombre.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        role_name (str): Nombre del rol que se desea consultar.

    Returns:
        Identificador del rol encontrado.

    Raises:
        ValueError: Si el rol no existe en la base de datos.
    """

    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist")
    return role.id


def serialize_user(user):
    """
    Convierte un usuario en un diccionario con sus datos públicos.

    Atributos:
        user: Objeto de usuario que se desea serializar.

    Returns:
        dict: Identificador, nombre, correo electrónico, rol y estado
            de actividad del usuario.
    """

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role_rel.name,
        "is_active": user.is_active,
    }


def get_all_users(db: Session):
    """
    Recupera todos los usuarios registrados.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        Lista de usuarios registrados.
    """

    return db.query(User).all()


def get_user(db: Session, user_id: str):
    """
    Busca un usuario por su identificador.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del usuario que se desea consultar.

    Returns:
        Usuario encontrado o None si no existe.
    """

    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, data):
    """
    Crea un usuario con los datos proporcionados y la contraseña cifrada.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        data: Datos del usuario, incluidos nombre, correo electrónico,
            contraseña, rol y estado de actividad.

    Returns:
        Usuario creado y actualizado con los datos de la base de datos.
    """

    role_id = _get_role_id(db, data.role)

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=role_id,
        is_active=data.is_active
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: str, data):
    """
    Actualiza los datos de un usuario existente.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del usuario que se desea actualizar.
        data: Datos opcionales que se aplicarán al usuario.

    Returns:
        Usuario actualizado o None si no existe.
    """

    user = get_user(db, user_id)

    if not user:
        return None

    if data.name is not None:
        user.name = data.name

    if data.email is not None:
        user.email = data.email

    if data.role is not None:
        user.role = _get_role_id(db, data.role)

    if data.is_active is not None:
        user.is_active = data.is_active

    if data.password:
        user.password_hash = hash_password(data.password)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: str):
    """
    Desactiva un usuario sin eliminarlo físicamente de la base de datos.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        user_id (str): Identificador del usuario que se desea desactivar.

    Returns:
        bool: True si el usuario se ha desactivado; False si no existe.
    """

    user = get_user(db, user_id)

    if not user:
        return False

    user.is_active = False

    db.commit()

    return True