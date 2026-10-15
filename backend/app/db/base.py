"""
Módulo: base.py
Descripción: Define la clase base declarativa de SQLAlchemy que utilizan
             los modelos para registrar sus tablas y metadatos.
Autor: Raquel Del Castillo Pérez
"""

from sqlalchemy.orm import declarative_base


Base = declarative_base()