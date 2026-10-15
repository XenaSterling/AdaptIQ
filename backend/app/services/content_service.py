"""
Módulo: content_service.py
Descripción: Gestiona la creación, consulta, actualización y eliminación
             de preguntas, incluidas sus respuestas y etiquetas asociadas.
Autor: Raquel Del Castillo Pérez
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.question import Question
from app.models.answer import Answer
from app.models.tag import Tag
from app.models.question_tag import QuestionTag


def serialize_question(question: Question):
    """
    Convierte una pregunta y sus relaciones en un diccionario.

    Atributos:
        question (Question): Pregunta que se desea serializar.

    Returns:
        dict: Datos de la pregunta, sus respuestas y las etiquetas
            asociadas.
    """

    return {
        "id": str(question.id),
        "content": question.content,
        "type": question.type,
        "difficulty": question.difficulty,
        "discrimination": question.discrimination,
        "bloom_level": question.bloom_level,
        "module_id": (
            str(question.module_id)
            if question.module_id
            else None
        ),
        "answers": [
            {
                "id": str(a.id),
                "question_id": str(a.question_id),
                "content": a.content,
                "is_correct": a.is_correct
            }
            for a in question.answers
        ],
        "tags": [
            qt.tag_id
            for qt in question.tags
        ]
    }


def create_question(
    db: Session,
    payload
):
    """
    Crea una pregunta con sus respuestas y etiquetas asociadas.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        payload: Datos de la pregunta, sus respuestas y las etiquetas
            que se deben asociar.

    Returns:
        dict: Pregunta creada y serializada con sus relaciones.
    """

    question = Question(
        content=payload.content,
        type=payload.type,
        difficulty=payload.difficulty,
        discrimination=payload.discrimination,
        bloom_level=payload.bloom_level,
        module_id = payload.module_id
    )

    db.add(question)
    db.flush()

    for ans in payload.answers:

        answer = Answer(
            question_id=question.id,
            content=ans.content,
            is_correct=ans.is_correct
        )

        db.add(answer)

    for tag_id in payload.tag_ids:

        db.add(
            QuestionTag(
                question_id=question.id,
                tag_id=tag_id
            )
        )

    db.commit()

    question = (
        db.query(Question)
        .options(
            joinedload(Question.answers),
            joinedload(Question.tags)
        )
        .filter_by(id=question.id)
        .first()
    )

    return serialize_question(question)


def list_questions(db: Session):
    """
    Recupera todas las preguntas con sus respuestas y etiquetas.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.

    Returns:
        list: Preguntas recuperadas y serializadas.
    """

    questions = (
        db.query(Question)
        .options(
            joinedload(Question.answers),
            joinedload(Question.tags)
        )
        .all()
    )

    return [
        serialize_question(q)
        for q in questions
    ]


def update_question(
    db: Session,
    question_id: str,
    payload
):
    """
    Actualiza los datos de una pregunta y, si se proporcionan,
    reemplaza sus respuestas y etiquetas asociadas.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        question_id (str): Identificador de la pregunta que se actualizará.
        payload: Campos que se desean modificar, incluidas las respuestas
            y las etiquetas opcionales.

    Returns:
        dict | None: Pregunta actualizada y serializada, o None si
            no existe.
    """

    question = (
        db.query(Question)
        .options(
            joinedload(Question.answers),
            joinedload(Question.tags)
        )
        .filter_by(id=question_id)
        .first()
    )

    if not question:
        return None

    if payload.content is not None:
        question.content = payload.content

    if payload.type is not None:
        question.type = payload.type

    if payload.difficulty is not None:
        question.difficulty = payload.difficulty

    if payload.discrimination is not None:
        question.discrimination = payload.discrimination

    if payload.bloom_level is not None:
        question.bloom_level = payload.bloom_level

    if payload.module_id is not None:
        question.module_id = payload.module_id

    if payload.answers is not None:

        db.query(Answer).filter_by(
            question_id=question.id
        ).delete()

        for ans in payload.answers:

            db.add(
                Answer(
                    question_id=question.id,
                    content=ans.content,
                    is_correct=ans.is_correct
                )
            )

    if payload.tag_ids is not None:

        db.query(QuestionTag).filter_by(
            question_id=question.id
        ).delete()

        for tag_id in payload.tag_ids:

            db.add(
                QuestionTag(
                    question_id=question.id,
                    tag_id=tag_id
                )
            )

    db.commit()

    updated = (
        db.query(Question)
        .options(
            joinedload(Question.answers),
            joinedload(Question.tags)
        )
        .filter_by(id=question.id)
        .first()
    )

    return serialize_question(updated)


def delete_question(
    db: Session,
    question_id: str
):
    """
    Elimina una pregunta de la base de datos.

    Atributos:
        db (Session): Sesión de conexión con la base de datos.
        question_id (str): Identificador de la pregunta que se eliminará.

    Returns:
        bool: True si la pregunta se ha eliminado; False si no existe.
    """

    question = (
        db.query(Question)
        .filter_by(id=question_id)
        .first()
    )

    if not question:
        return False

    db.delete(question)
    db.commit()

    return True