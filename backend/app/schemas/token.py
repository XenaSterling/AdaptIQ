"""
Módulo: token.py
Descripción: Define el esquema de los datos contenidos en la información
             de identificación del usuario asociada a un token.
Autor: Raquel Del Castillo Pérez
"""

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """
    Define los datos de identificación incluidos en el token.

    Atributos:
        sub (str): Identificador del sujeto al que pertenece el token.
    """
    sub: str