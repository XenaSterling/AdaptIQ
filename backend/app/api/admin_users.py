"""
Módulo: admin_users.py
Descripción: Define los endpoints de administración de usuarios,
             incluyendo la consulta, creación, actualización y eliminación
             de usuarios mediante operaciones protegidas para administradores.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import require_admin
from app.schemas.admin_user import (
    AdminUserCreate,
    AdminUserUpdate,
    AdminUserResponse
)
from app.services.admin_user_service import (
    get_all_users,
    get_user,
    create_user,
    update_user,
    delete_user,
    serialize_user
)


router = APIRouter(
    prefix="/admin/users",
    tags=["admin-users"]
)


@router.get("", response_model=list[AdminUserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin())
):
    """
    Obtiene la lista de usuarios registrados.

    Args:
        db (Session): Sesión de base de datos.
        admin: Administrador autenticado que realiza la solicitud.

    Returns:
        list[AdminUserResponse]: Lista de usuarios registrados.
    """

    users = get_all_users(db)

    return [serialize_user(u) for u in users]


@router.get("/{user_id}", response_model=AdminUserResponse)
def get_single_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin=Depends(require_admin())
):
    """
    Obtiene los datos de un usuario a partir de su identificador.

    Args:
        user_id (str): Identificador del usuario.
        db (Session): Sesión de base de datos.
        admin: Administrador autenticado que realiza la solicitud.

    Returns:
        AdminUserResponse: Datos del usuario solicitado.

    Raises:
        HTTPException: Si el usuario no existe, devuelve el estado 404.
    """

    user = get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return serialize_user(user)


@router.post("", response_model=AdminUserResponse)
def create_new_user(
    data: AdminUserCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin())
):
    """
    Crea un nuevo usuario.

    Args:
        data (AdminUserCreate): Datos necesarios para crear el usuario.
        db (Session): Sesión de base de datos.
        admin: Administrador autenticado que realiza la solicitud.

    Returns:
        AdminUserResponse: Datos del usuario creado.
    """

    user = create_user(db, data)
    return serialize_user(user)


@router.put("/{user_id}", response_model=AdminUserResponse)
def update_existing_user(
    user_id: str,
    data: AdminUserUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin())
):
    """
    Actualiza los datos de un usuario existente.

    Args:
        user_id (str): Identificador del usuario que se actualizará.
        data (AdminUserUpdate): Datos que se desean modificar.
        db (Session): Sesión de base de datos.
        admin: Administrador autenticado que realiza la solicitud.

    Returns:
        AdminUserResponse: Datos del usuario actualizado.

    Raises:
        HTTPException: Si el usuario no existe, devuelve el estado 404.
    """

    user = update_user(db, user_id, data)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return serialize_user(user)


@router.delete("/{user_id}")
def delete_existing_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin=Depends(require_admin())
):
    """
    Elimina un usuario mediante el procedimiento de eliminación lógica.

    Args:
        user_id (str): Identificador del usuario que se eliminará.
        db (Session): Sesión de base de datos.
        admin: Administrador autenticado que realiza la solicitud.

    Returns:
        dict: Indicador del resultado de la operación.

    Raises:
        HTTPException: Si el usuario no existe, devuelve el estado 404.
    """

    ok = delete_user(db, user_id)

    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

    return {"ok": True}