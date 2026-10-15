from app.services.adaptive_engine import get_next_question


def test_no_questions_returns_none(db):

    result = get_next_question(db, 0.0, [])

    assert result is None


def test_all_questions_used(db, test_question):

    result = get_next_question(db, 0.0, [test_question.id])

    assert result is None


def test_extreme_theta_still_works(db, test_module):

    from tests.utils.factories import create_question

    create_question(db, test_module, difficulty=3.95)

    result = get_next_question(db, 999, [])

    assert result is not None