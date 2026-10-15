"""
Módulo: teacher.py
Descripción: Define los endpoints del área docente para consultar
             estadísticas y riesgos de estudiantes, gestionar parámetros
             de evaluación y administrar preguntas, recursos, etiquetas
             y módulos de aprendizaje.
Autor: Raquel Del Castillo Pérez
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import (
    require_teacher,
    get_current_user
)
from app.services.teacher_service import (
    get_teacher_overview,
    get_student_risk_analysis
)
from app.services.evaluation_settings_service import (
    get_evaluation_settings,
    update_evaluation_settings
)
from app.services.content_service import (
    create_question,
    update_question,
    delete_question,
    list_questions
)
from app.services.learning_resource_service import (
    create_learning_resource,
    list_learning_resources,
    update_learning_resource,
    delete_learning_resource
)
from app.services.tag_service import (
    list_tags,
    search_tags,
    create_tag
)
from app.services.module_service import (
    list_modules,
    search_modules,
    create_module
)
from app.schemas.teacher import (
    EvaluationSettingsResponse,
    UpdateEvaluationSettingsRequest,
    TeacherOverviewResponse,
    StudentRiskResponse
)
from app.schemas.content_management import (
    QuestionCreateRequest,
    QuestionUpdateRequest,
    QuestionResponse
)
from app.schemas.learning_resource import (
    LearningResourceCreateRequest,
    LearningResourceUpdateRequest,
    LearningResourceResponse
)
from app.schemas.tag import (
    TagCreateRequest,
    TagResponse
)
from app.schemas.module import (
    ModuleSearchResponse,
    ModuleCreateSimple
)


router = APIRouter(
    prefix="/teacher",
    tags=["teacher"],
    dependencies=[Depends(require_teacher())]
)


@router.get(
    "/evaluations/{evaluation_id}/settings",
    response_model=EvaluationSettingsResponse
)
def get_settings(
    evaluation_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene la configuración de una evaluación.

    Args:
        evaluation_id (str): Identificador de la evaluación.
        db (Session): Sesión de base de datos.

    Returns:
        EvaluationSettingsResponse: Parámetros de configuración
            de la evaluación solicitada.
    """

    return get_evaluation_settings(
        db,
        evaluation_id
    )


@router.put(
    "/evaluations/{evaluation_id}/settings",
    response_model=EvaluationSettingsResponse
)
def update_settings(
    evaluation_id: str,
    payload: UpdateEvaluationSettingsRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza la configuración de una evaluación.

    Args:
        evaluation_id (str): Identificador de la evaluación.
        payload (UpdateEvaluationSettingsRequest): Parámetros
            de configuración que se desean actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        EvaluationSettingsResponse: Configuración actualizada.
    """

    return update_evaluation_settings(
        db,
        evaluation_id,
        payload.model_dump()
    )


@router.get(
    "/overview",
    response_model=TeacherOverviewResponse
)
def teacher_overview(
    db: Session = Depends(get_db)
):
    """
    Obtiene un resumen de la actividad docente.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        TeacherOverviewResponse: Estadísticas generales de estudiantes,
            evaluaciones, respuestas, precisión y dificultades.
    """

    return get_teacher_overview(db)


@router.get(
    "/students/risk",
    response_model=list[StudentRiskResponse]
)
def student_risk(
    db: Session = Depends(get_db)
):
    """
    Obtiene el análisis de riesgo de los estudiantes.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[StudentRiskResponse]: Lista de estudiantes con sus métricas
            de precisión y nivel de riesgo.
    """

    return get_student_risk_analysis(db)


@router.post(
    "/questions",
    response_model=QuestionResponse
)
def create_new_question(
    payload: QuestionCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva pregunta.

    Args:
        payload (QuestionCreateRequest): Datos necesarios para crear
            la pregunta.
        db (Session): Sesión de base de datos.

    Returns:
        QuestionResponse: Datos de la pregunta creada.
    """

    return create_question(
        db,
        payload
    )


@router.get(
    "/questions",
    response_model=list[QuestionResponse]
)
def get_questions(
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de preguntas disponibles.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[QuestionResponse]: Lista de preguntas registradas.
    """

    return list_questions(db)


@router.put(
    "/questions/{question_id}",
    response_model=QuestionResponse
)
def update_existing_question(
    question_id: str,
    payload: QuestionUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza una pregunta existente.

    Args:
        question_id (str): Identificador de la pregunta.
        payload (QuestionUpdateRequest): Datos que se desean modificar.
        db (Session): Sesión de base de datos.

    Returns:
        QuestionResponse: Datos de la pregunta actualizada.

    Raises:
        HTTPException: Si la pregunta no existe, devuelve el estado 404.
    """

    question = update_question(
        db,
        question_id,
        payload
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question


@router.delete("/questions/{question_id}")
def delete_existing_question(
    question_id: str,
    db: Session = Depends(get_db)
):
    """
    Elimina una pregunta existente.

    Args:
        question_id (str): Identificador de la pregunta.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Mensaje que confirma la eliminación de la pregunta.

    Raises:
        HTTPException: Si la pregunta no existe, devuelve el estado 404.
    """

    deleted = delete_question(
        db,
        question_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return {
        "message": "Question deleted"
    }


@router.post(
    "/resources",
    response_model=LearningResourceResponse
)
def create_resource(
    payload: LearningResourceCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Crea un recurso de aprendizaje asociado al docente autenticado.

    Args:
        payload (LearningResourceCreateRequest): Datos del recurso.
        db (Session): Sesión de base de datos.
        current_user: Datos del usuario autenticado.

    Returns:
        LearningResourceResponse: Datos del recurso creado.
    """

    teacher_id = current_user["sub"]

    return create_learning_resource(
        db,
        payload,
        teacher_id
    )


@router.get(
    "/resources",
    response_model=list[LearningResourceResponse]
)
def get_resources(
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de recursos de aprendizaje.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[LearningResourceResponse]: Lista de recursos disponibles.
    """

    return list_learning_resources(db)


@router.put(
    "/resources/{resource_id}",
    response_model=LearningResourceResponse
)
def update_resource(
    resource_id: str,
    payload: LearningResourceUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza un recurso de aprendizaje existente.

    Args:
        resource_id (str): Identificador del recurso.
        payload (LearningResourceUpdateRequest): Datos que se desean
            modificar en el recurso.
        db (Session): Sesión de base de datos.

    Returns:
        LearningResourceResponse: Datos del recurso actualizado.

    Raises:
        HTTPException: Si el recurso no existe, devuelve el estado 404.
    """

    resource = update_learning_resource(
        db,
        resource_id,
        payload
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource


@router.delete("/resources/{resource_id}")
def delete_resource(
    resource_id: str,
    db: Session = Depends(get_db)
):
    """
    Elimina un recurso de aprendizaje existente.

    Args:
        resource_id (str): Identificador del recurso.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Mensaje que confirma la eliminación del recurso.

    Raises:
        HTTPException: Si el recurso no existe, devuelve el estado 404.
    """

    deleted = delete_learning_resource(
        db,
        resource_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return {
        "message": "Resource deleted"
    }


@router.get(
    "/tags",
    response_model=list[TagResponse]
)
def get_tags(
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de etiquetas disponibles.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[TagResponse]: Lista de etiquetas registradas.
    """

    return list_tags(db)


@router.get(
    "/tags/search",
    response_model=list[TagResponse]
)
def search_tags_endpoint(
    q: str,
    db: Session = Depends(get_db)
):
    """
    Busca etiquetas según un término de búsqueda.

    Args:
        q (str): Texto utilizado para buscar etiquetas.
        db (Session): Sesión de base de datos.

    Returns:
        list[TagResponse]: Lista de etiquetas que coinciden
            con el término de búsqueda.
    """

    return search_tags(db, q)


@router.post(
    "/tags",
    response_model=TagResponse
)
def create_tag_endpoint(
    payload: TagCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva etiqueta.

    Args:
        payload (TagCreateRequest): Datos necesarios para crear
            la etiqueta.
        db (Session): Sesión de base de datos.

    Returns:
        TagResponse: Datos de la etiqueta creada.
    """

    return create_tag(
        db,
        payload.name
    )


@router.get(
    "/modules",
    response_model=list[ModuleSearchResponse]
)
def get_modules(
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de módulos disponibles.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[ModuleSearchResponse]: Lista de módulos registrados.
    """

    return list_modules(db)


@router.get(
    "/modules/search",
    response_model=list[ModuleSearchResponse]
)
def search_modules_endpoint(
    q: str,
    db: Session = Depends(get_db)
):
    """
    Busca módulos según un término de búsqueda.

    Args:
        q (str): Texto utilizado para buscar módulos.
        db (Session): Sesión de base de datos.

    Returns:
        list[ModuleSearchResponse]: Lista de módulos que coinciden
            con el término de búsqueda.
    """

    return search_modules(db, q)


@router.post(
    "/modules",
    response_model=ModuleSearchResponse
)
def create_module_endpoint(
    payload: ModuleCreateSimple,
    db: Session = Depends(get_db)
):
    """
    Crea un módulo asociado a un curso.

    Args:
        payload (ModuleCreateSimple): Título e identificador del curso.
        db (Session): Sesión de base de datos.

    Returns:
        ModuleSearchResponse: Identificador y título del módulo creado.
    """

    return create_module(
        db,
        payload.title,
        payload.course_id
    )