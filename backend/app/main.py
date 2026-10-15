"""
Módulo: main.py
Descripción: Configura y pone en marcha la aplicación FastAPI,
             registra el middleware CORS, inicializa las tablas
             de la base de datos e incorpora las rutas de la API.
             También proporciona endpoints básicos de estado
             y comprobación de la conexión con la base de datos.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.core.settings import settings
from app.db.base import Base
from app.db.session import engine
from app.db.deps import get_db

from app.api.auth import router as auth_router
from app.api.evaluation import router as evaluation_router
from app.api.recommendations import router as recommendations_router
from app.api.dashboard import router as dashboard_router
from app.api.teacher import router as teacher_router
from app.api.admin_users import router as admin_users_router

from app.models.user import User


app = FastAPI(
    title=settings.APP_NAME
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# DEV / TEST ONLY
# =====================================================

Base.metadata.create_all(bind=engine)

# =====================================================
# ROUTERS
# =====================================================

app.include_router(auth_router)
app.include_router(evaluation_router)
app.include_router(recommendations_router)
app.include_router(dashboard_router)
app.include_router(teacher_router)
app.include_router(admin_users_router)


@app.get("/")
def root():
    """
    Devuelve el estado de la API y el nombre de la aplicación.

    Returns:
        dict: Diccionario con el estado de ejecución de la API
            y el nombre configurado de la aplicación.
    """

    return {
        "status": "API running",
        "app": settings.APP_NAME
    }


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    """
    Comprueba que se puede obtener una sesión de base de datos.

    Args:
        db (Session): Sesión de base de datos proporcionada
            mediante la dependencia get_db.

    Returns:
        dict: Mensaje que indica que la conexión con la base de datos
            está disponible.
    """

    return {
        "msg": "DB connected"
    }


@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de usuarios registrados en la base de datos.
    NO debería estar expuesto nunca en un proyecto productivo,
    pero de cara a hacer debug del producto con el swagger es muy
    útil.

    Args:
        db (Session): Sesión de base de datos proporcionada
            mediante la dependencia get_db.

    Returns:
        List[User]: Lista de usuarios almacenados en la base de datos.
    """

    return db.query(User).all()