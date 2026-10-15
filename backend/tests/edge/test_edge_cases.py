from app.services.adaptive_engine import get_next_question
from tests.utils.factories import create_user, create_course, create_module, create_question


def test_all_questions_used(db):

    user = create_user(db)
    course = create_course(db, user)
    module = create_module(db, course)
    q = create_question(db, module)

    result = get_next_question(
        db,
        theta=0.0,
        used_question_ids=[q.id]
    )

    assert result is None


def test_extreme_theta_returns_question(db):

    user = create_user(db)
    course = create_course(db, user)
    module = create_module(db, course)

    create_question(db, module, difficulty=0.5)

    result = get_next_question(db, theta=3.0, used_question_ids=[])

    assert result is not None


def test_ignores_used_questions(db):

    user = create_user(db)
    course = create_course(db, user)
    module = create_module(db, course)

    q = create_question(db, module)

    result = get_next_question(
        db,
        theta=0.0,
        used_question_ids=[q.id]
    )

    assert result is None