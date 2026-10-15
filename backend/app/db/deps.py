"""
Módulo: deps.py
Descripción: Proporciona dependencias para gestionar las sesiones
             de conexión con la base de datos durante las solicitudes
             de la aplicación.
Autor: Raquel Del Castillo Pérez
"""

from app.db.session import SessionLocal


def get_db():
    """
    Obtiene una sesión de base de datos para una solicitud.

    La sesión se cierra automáticamente cuando finaliza su uso,
    incluso si se produce una excepción durante la solicitud.

    Yields:
        Session: Sesión activa de SQLAlchemy.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()