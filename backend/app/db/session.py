"""
Módulo: session.py
Descripción: Configura el motor de conexión con la base de datos
             y la fábrica de sesiones de SQLAlchemy utilizando
             los parámetros definidos en la configuración global.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)