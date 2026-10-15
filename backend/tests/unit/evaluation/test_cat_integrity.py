import uuid

from app.services.adaptive_engine import get_next_question


def test_cat_does_not_repeat_questions(db, test_question):

    used = []

    q1 = get_next_question(
        db=db,
        theta=0.0,
        used_question_ids=used
    )

    assert q1 is not None

    used.append(str(q1.id))

    q2 = get_next_question(
        db=db,
        theta=0.0,
        used_question_ids=used
    )

    if q2 is not None:
        assert q2.id != q1.id


def test_cat_returns_none_when_no_questions(db):

    result = get_next_question(
        db=db,
        theta=0.0,
        used_question_ids=[str(uuid.uuid4())]
    )

    assert result is None