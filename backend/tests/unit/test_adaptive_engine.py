from app.services.adaptive_engine import get_next_question
from app.models.question import Question


def test_get_next_question_returns_best_match(db, test_module, test_question):

    result = get_next_question(
        db,
        theta=0.0,
        used_question_ids=[]
    )

    assert result is not None
    assert hasattr(result, "difficulty")


def test_get_next_question_empty(db):

    result = get_next_question(db, 0.0, [])
    print(db.query(Question).count())

    assert result is None


def test_get_next_question_respects_used(db, test_question):

    result = get_next_question(
        db,
        theta=0.0,
        used_question_ids=[test_question.id]
    )

    assert result is None