"""
Módulo: dashboard.py
Descripción: Define los endpoints de consulta de los paneles
             de estudiantes, docentes y administradores, aplicando
             las restricciones de acceso correspondientes a cada rol.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import (
    require_student,
    require_teacher,
    require_admin
)
from app.services.dashboard_service import (
    get_student_dashboard,
    get_teacher_dashboard,
    get_admin_dashboard
)
from app.schemas.dashboard import (
    StudentDashboardResponse,
    TeacherDashboardResponse,
    AdminDashboardResponse
)


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get(
    "/student/{user_id}",
    response_model=StudentDashboardResponse
)
def student_dashboard(
    user_id: str,
    current_user=Depends(require_student()),
    db: Session = Depends(get_db)
):
    """
    Obtiene los datos del panel de un estudiante.

    Args:
        user_id (str): Identificador del estudiante.
        current_user: Datos del usuario autenticado.
        db (Session): Sesión de base de datos.

    Returns:
        StudentDashboardResponse: Datos del panel del estudiante.

    Raises:
        HTTPException: Si el usuario intenta acceder al panel
            de otro estudiante, devuelve el estado 403.
    """

    authenticated_user_id = str(current_user.get("sub"))
    if user_id != authenticated_user_id: 
        raise HTTPException(
            status_code=403,
            detail="Cannot access another student's dashboard"
        )
    return get_student_dashboard(db, user_id)


@router.get(
    "/teacher",
    response_model=TeacherDashboardResponse
)
def teacher_dashboard(
    current_user=Depends(require_teacher()),
    db: Session = Depends(get_db)
):
    """
    Obtiene los datos del panel del docente.

    Args:
        current_user: Datos del docente autenticado.
        db (Session): Sesión de base de datos.

    Returns:
        TeacherDashboardResponse: Datos del panel del docente.
    """

    return get_teacher_dashboard(db)


@router.get(
    "/admin",
    response_model=AdminDashboardResponse
)
def admin_dashboard(
    current_user=Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Obtiene los datos del panel de administración.

    Args:
        current_user: Datos del administrador autenticado.
        db (Session): Sesión de base de datos.

    Returns:
        AdminDashboardResponse: Datos del panel de administración.
    """

    return get_admin_dashboard(db)