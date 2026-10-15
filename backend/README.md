# Backend

- API backend de AdaptIQ, desarrollada con FastAPI y Python. Gestiona la autenticación y autorización de usuarios, las evaluaciones, el seguimiento del aprendizaje y las recomendaciones educativas.
- Utiliza PostgreSQL como base de datos e integra algoritmos de aprendizaje adaptativo, teoría de respuesta al ítem (IRT) y recomendación de recursos.
- Autor: rdelcasti26@alumno.uned.es

## Requisitos previos

- **Python 3.11**
- **Poetry**: Para gestión de dependencias.
- **PostgreSQL 15**: Como sistema gestor de base de datos.
- **Git**: Para obtener el código fuente del proyecto.

## Instalación de dependencias

- Clona el repositorio y accede al directorio del backend:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <DIRECTORIO_DEL_BACKEND>
```

- Instala las dependencias definidas en `pyproject.toml` y bloqueadas en `poetry.lock`:
```bash
poetry install
```

- Este comando instala las dependencias del proyecto y las herramientas de desarrollo declaradas en su configuración.

## Configuración de variables de entorno

El backend utiliza un archivo `.env` para gestionar la configuración de la aplicación, la conexión con PostgreSQL y los parámetros de autenticación JWT.

### Variables de entorno

Crea un archivo `.env` en el directorio raíz del backend, tomando como referencia `.env.example`.

| Variable | Descripción | Valor predeterminado |
|---|---|---|
| `APP_NAME` | Nombre de la aplicación. | `AdaptIQ` |
| `DEBUG` | Activa o desactiva el modo de depuración. | `True` |
| `DATABASE_URL` | URL de conexión con PostgreSQL. | Obligatoria |
| `SQL_ECHO` | Activa o desactiva el registro de consultas SQL. | `False` |
| `SECRET_KEY` | Clave secreta para firmar los tokens JWT. | Obligatoria |
| `JWT_ALGORITHM` | Algoritmo de firma de los tokens JWT. | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token de acceso en minutos. | `60` |

### Ejemplo de configuración

```dotenv
APP_NAME=AdaptIQ
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/adaptiq
SQL_ECHO=False
SECRET_KEY=REEMPLAZAR_POR_UNA_CLAVE_SEGURA
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Adapta `DATABASE_URL` a la configuración de tu entorno y sustituye `SECRET_KEY` por una clave aleatoria segura.

## Inicio del servidor

- Una vez instalada la aplicación, configuradas las variables de entorno y disponible la base de datos, inicia el backend con:
```bash
poetry run python run_backend.py
```
- El servidor se inicia en la dirección http://127.0.0.1:8000.
- La configuración actual utiliza el puerto 8000 y limita la escucha a la dirección local 127.0.0.1.

## Documentación de la API

FastAPI genera automáticamente la documentación interactiva de los endpoints. Con el servidor en ejecución, se puede acceder a:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Comprobación del estado: http://127.0.0.1:8000/
- Comprobación de la conexión a la base de datos: http://127.0.0.1:8000/test-db

El endpoint / devuelve el estado de la API y el nombre de la aplicación. El endpoint /test-db permite comprobar que se puede obtener una sesión de base de datos.

Nota de seguridad: el endpoint /users devuelve los usuarios registrados y está destinado a tareas de depuración.Debería restringirse o eliminarse antes de desplegar la aplicación en un entorno de producción real.

## Configuración de la base de datos

El backend utiliza PostgreSQL y SQLAlchemy para gestionar la conexión y las operaciones sobre la base de datos.

La configuración se obtiene de las variables de entorno definidas en .env. En particular, `DATABASE_URL` determina la dirección de conexión y `SQL_ECHO` permite activar o desactivar el registro de las consultas SQL.

### Inicialización del esquema
Al arrancar la aplicación, app/main.py ejecuta `Base.metadata.create_all(bind=engine)`
Esta operación crea las tablas correspondientes a los modelos registrados que todavía no existan en la base de datos. No elimina ni actualiza automáticamente las tablas existentes para adaptarlas a cambios posteriores en los modelos.

### Carga de datos de demostración
El proyecto incluye app/db/seed_database.py, un script que inicializa la base de datos con datos de ejemplo para probar las funcionalidades de AdaptIQ.

Para ejecutarlo:
```bash
poetry run python -m app.db.seed_database
```

El script crea roles y usuarios de ejemplo, cursos, módulos, preguntas, respuestas, recursos educativos y registros de evaluaciones. También genera datos de progreso y entrena el modelo de predicción de abandono.

Advertencia: el proceso ejecuta operaciones de reinicio sobre las tablas mediante TRUNCATE ... RESTART IDENTITY CASCADE. Esto elimina datos existentes y registros relacionados, ejecútalo únicamente en una base de datos de desarrollo o demostración cuyos datos puedan descartarse.

## Seguridad

- El archivo .env contiene configuración local y posibles secretos, por lo que no puede subirse al repositorio.
- El archivo .env.example se incluiye en Git como plantilla, sin credenciales reales.
- No utilizar los credenciales de ejemplo ni una clave secreta de desarrollo en producción.

## Esquema directorios

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── admin_users.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── evaluation.py
│   │   ├── recommendations.py
│   │   └── teacher.py
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── security.py
│   │   └── service.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── db/
│   │   ├── base.py
│   │   ├── deps.py
│   │   ├── seed_database.py
│   │   ├── seed_demo.py
│   │   ├── seed_test.py
│   │   └── session.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── cat/
│   │   │   └── stopping.py
│   │   ├── clustering/
│   │   │   └── student_clustering.py
│   │   ├── irt/
│   │   │   ├── __init__.py
│   │   │   ├── information.py
│   │   │   ├── model.py
│   │   │   ├── stopping.py
│   │   │   ├── uncertainty.py
│   │   │   └── update.py
│   │   ├── prediction/
│   │   │   ├── dropout_model.pkl
│   │   │   └── dropout_model.py
│   │   └── recommender/
│   │       ├── collaborative.py
│   │       ├── content_based.py
│   │       ├── explain.py
│   │       ├── normalization.py
│   │       ├── recommender_engine.py
│   │       ├── resource_recommender.py
│   │       └── tag_based.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── adaptive_log.py
│   │   ├── answer.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   ├── evaluation.py
│   │   ├── evaluation_settings.py
│   │   ├── irt_session.py
│   │   ├── learning_profile.py
│   │   ├── learning_resource.py
│   │   ├── module.py
│   │   ├── module_progress.py
│   │   ├── question.py
│   │   ├── question_tag.py
│   │   ├── recommendation.py
│   │   ├── resource_tag.py
│   │   ├── resource_usage.py
│   │   ├── result.py
│   │   ├── result_answer.py
│   │   ├── role.py
│   │   ├── student_ability.py
│   │   ├── tag.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── admin_user.py
│   │   ├── answer.py
│   │   ├── auth.py
│   │   ├── common.py
│   │   ├── content_management.py
│   │   ├── course.py
│   │   ├── dashboard.py
│   │   ├── evaluation.py
│   │   ├── evaluation_settings.py
│   │   ├── feedback.py
│   │   ├── learning_resource.py
│   │   ├── module.py
│   │   ├── recommendation.py
│   │   ├── shared.py
│   │   ├── tag.py
│   │   ├── teacher.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services/
│   │   ├── adaptive_engine.py
│   │   ├── admin_user_service.py
│   │   ├── content_service.py
│   │   ├── dashboard_service.py
│   │   ├── evaluation_service.py
│   │   ├── evaluation_settings_service.py
│   │   ├── feedback_service.py
│   │   ├── learning_resource_service.py
│   │   ├── module_service.py
│   │   ├── recommendation_service.py
│   │   ├── student_ability_service.py
│   │   ├── tag_service.py
│   │   └── teacher_service.py
│   └── utils/
│       └── roles.py
├── poetry.lock
├── pyproject.toml
├── run_backend.py
└── tests/
    ├── conftest.py
    ├── e2e/
    ├── edge/
    ├── integration/
    ├── unit/
    └── utils/
```

### Descripción de los directorios principales

- **`app/api/`**: Endpoints de la API para autenticación, evaluaciones, recomendaciones, dashboard y administración.
- **`app/auth/`**: Autenticación, seguridad y dependencias de autorización.
- **`app/core/`**: Configuración general de la aplicación.
- **`app/db/`**: Conexión a la base de datos, dependencias y scripts de inicialización y carga de datos.
- **`app/ml/`**: Algoritmos de aprendizaje adaptativo, teoría de respuesta al ítem (IRT), predicción, agrupamiento y recomendación.
- **`app/models/`**: Modelos de datos de la aplicación.
- **`app/schemas/`**: Esquemas de validación y serialización de datos.
- **`app/services/`**: Lógica de negocio para evaluaciones, recomendaciones, recursos y usuarios.
- **`app/utils/`**: Funciones auxiliares.
- **`tests/`**: Pruebas unitarias, de integración, de extremo a extremo y de casos límite.
- **`run_backend.py`**: Script de ejecución del backend.
- **`pyproject.toml` y `poetry.lock`**: Configuración del proyecto y dependencias gestionadas con Poetry.
- **`AdaptIQBackend.spec`**: Configuración de PyInstaller para generar el ejecutable.

## Ejecución de pruebas

El backend utiliza pytest para ejecutar las pruebas automatizadas. Los tests se encuentran en el directorio tests/ y se organizan por categorías:

- **`tests/unit/`**: Pruebas unitarias de los componentes y algoritmos.
- **`tests/integration/`**: Pruebas de integración entre componentes.
- **`tests/e2e/`**: Pruebas de extremo a extremo de los principales flujos de la aplicación.
- **`tests/edge/`**: Pruebas de casos límite y situaciones excepcionales.
- **`tests/utils/`**: Utilidades compartidas por las pruebas.

El archivo tests/conftest.py define las fixtures comunes, el cliente de pruebas de FastAPI, las sesiones de base de datos y los datos necesarios para ejecutar los tests.

- Ejecutar todas las pruebas
```bash
poetry run pytest
```

### Consideraciones sobre la base de datos de pruebas
Las pruebas utilizan la configuración de conexión definida para la aplicación. Además, la fixture setup_db de tests/conftest.py crea las tablas al inicio de la sesión de pruebas y ejecuta Base.metadata.drop_all(bind=engine) al finalizar.

Por este motivo, es imprescindible configurar DATABASE_URL para apuntar a una base de datos exclusiva de pruebas antes de ejecutar la suite completa. No deben ejecutarse las pruebas contra una base de datos de producción ni contra una base de desarrollo con información que se quiera conservar.



