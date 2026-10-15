"""
Módulo: security.py
Descripción: Proporciona funciones de seguridad para gestionar
             las contraseñas de los usuarios mediante hash y verificación,
             así como para generar tokens de acceso JWT.
Autor: Raquel Del Castillo Pérez
"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.settings import settings


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str):
    """
    Genera el hash de una contraseña mediante el algoritmo configurado.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        str: Hash generado a partir de la contraseña.
    """

    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed: str
):
    """
    Comprueba si una contraseña coincide con su hash almacenado.

    Args:
        password (str): Contraseña en texto plano.
        hashed (str): Hash de la contraseña almacenada.

    Returns:
        bool: True si la contraseña coincide con el hash,
            False en caso contrario.
    """

    return pwd_context.verify(
        password,
        hashed
    )


def create_access_token(data: dict):
    """
    Genera un token JWT con los datos proporcionados y su expiración.

    Args:
        data (dict): Datos que se incluirán en el contenido del token.

    Returns:
        str: Token JWT firmado con la clave secreta configurada.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt