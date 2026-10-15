"""
Módulo: settings.py
Descripción: Define la configuración global de la aplicación,
             incluyendo los parámetros generales, la conexión
             con la base de datos y las opciones de autenticación JWT.
             Los valores pueden obtenerse del archivo de entorno .env.
Autor: Raquel Del Castillo Pérez
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Define los parámetros de configuración de la aplicación.

    Atributos:
        APP_NAME (str): Nombre de la aplicación.
        DEBUG (bool): Indica si el modo de depuración está habilitado.
        DATABASE_URL (str): URL de conexión con la base de datos.
        SQL_ECHO (bool): Indica si se muestran las consultas SQL.
        SECRET_KEY (str): Clave secreta utilizada para firmar los tokens.
        JWT_ALGORITHM (str): Algoritmo de firma de los tokens JWT.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tiempo de validez del token
            de acceso expresado en minutos.
        model_config (SettingsConfigDict): Configuración de carga
            de variables de entorno y tratamiento de campos adicionales.
    """

    APP_NAME: str = "AdaptIQ"

    DEBUG: bool = True

    DATABASE_URL: str

    SQL_ECHO: bool = False

    SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()