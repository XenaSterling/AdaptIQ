# AdaptiQ

Sistema de evaluación adaptativa y recomendación educativa basado en Item Response Theory (IRT).

## 1. Estructura del proyecto

El proyecto se divide en tres componentes:

- **Backend:** API, autenticación, lógica de evaluación, base de datos y módulos de Machine Learning.
- **Frontend:** interfaz de usuario para alumnos y profesores.
- **Base de datos:** PostgreSQL gestionado mediante Docker Compose.

Documentación específica:
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- Infraestructura: `docker/docker-compose.yml`

## 2. Requisitos previos

- Python 3.13
- Poetry
- Node.js y npm
- Docker y Docker Compose
- Git

## 3. Puesta en marcha

### 3.1. Base de datos

Desde la carpeta `docker`:

```bash
docker-compose up -d
```

Configuración de PostgreSQL definida en `docker-compose.yml`:

| Parámetro | Valor |
|---|---|
| Imagen | `postgres:15` |
| Contenedor | `adaptiq_db` |
| Base de datos | `adaptiq` |
| Usuario | `user` |
| Contraseña | `password` |
| Puerto | `5432` |
| Volumen | `adaptiq_postgres_data` |

Comprobar el estado del contenedor:

```bash
docker ps
```

## 3.2. Backend

Desde la carpeta `backend`:

- Instalar dependencias: `poetry install`
- Arrancar servidor: `poetry run uvicorn app.main:app --reload --port 8000`

**URLs:**
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## 3.3. Verificar el backend

**Conexión con la base de datos**
- Endpoint: `GET /test-db` (si está disponible).
- Respuesta esperada: `{"msg": "DB connected"}`

**Inicio de sesión**
- Endpoint: `POST /auth/login`
- Body: `{"email": "test@test.com", "password": "1234"}`
- Las credenciales deben corresponder a un usuario existente.

**Tests**
- Ejecución: `poetry run pytest -q`
- Con cobertura: `PYTHONPATH=. poetry run pytest --cov=app`

## 3.4. Frontend

Desde la carpeta `frontend`:

- Instalar dependencias: `npm install`
- Arrancar aplicación: `npm run dev`
- URL: http://localhost:5173
- Documentación: `frontend/README.md`

## 4. Verificación de la integración

- [ ] PostgreSQL en ejecución.
- [ ] Swagger accesible.
- [ ] Inicio de sesión funcional.
- [ ] Tests del backend superados.
- [ ] Frontend accesible.
- [ ] Comunicación frontend-backend funcional.
- [ ] Dashboards y evaluaciones funcionales.

## 5. Inicialización y reinicio de la base de datos

### Cargar datos iniciales

Desde `backend`:

`poetry run python -m app.db.seed_database`

### Reiniciar la base de datos

Desde `docker`:

1. Detener contenedores y eliminar volúmenes: `docker-compose down -v`
2. Volver a iniciar los contenedores: `docker-compose up -d`
3. Desde `backend`, volver a cargar los datos: `poetry run python -m app.db.seed_database`

> **Advertencia:** `docker-compose down -v` elimina los volúmenes y puede borrar todos los datos almacenados.

## 6. Solución de problemas

### Detener Uvicorn

- Detener proceso: `pkill -f 'uvicorn app.main:app'`
- Comprobar procesos activos: `ps aux | grep '[u]vicorn'`
- Detener un proceso concreto: `kill <PID>`
- Forzar la terminación si no responde: `kill -9 <PID>`

### Comprobar el puerto 8000

`ss -ltnp | grep ':8000'`

### Problemas de conexión

**Backend / PostgreSQL**

- [ ] Contenedor activo.
- [ ] Credenciales y URL de conexión correctas.
- [ ] Base de datos inicializada.

**Frontend / Backend**

- [ ] Uvicorn activo.
- [ ] URL de la API correcta.
- [ ] Errores de red revisados.
- [ ] Configuración de CORS comprobada.

## 7. Estrategia de ramas de Git

| Rama | Uso |
|---|---|
| `main` | Versión estable |
| `develop` | Integración de cambios |
| `feature/nombre` | Nuevas funcionalidades |
| `fix/nombre` | Correcciones |
| `hotfix/nombre` | Correcciones urgentes |

### Crear una rama de funcionalidad

1. Cambiar a `develop`: `git checkout develop`
2. Actualizar la rama: `git pull`
3. Crear la nueva rama: `git checkout -b feature/nombre-funcionalidad`

## 8. Documentación

- `README.md`: Documentación general y puesta en marcha.
- `backend/README.md`: Configuración, ejecución y pruebas del backend.
- `frontend/README.md`: Instalación y ejecución del frontend.
- `docker/docker-compose.yml`: Configuración de PostgreSQL.
- [Swagger](http://localhost:8000/docs): Documentación interactiva de la API.