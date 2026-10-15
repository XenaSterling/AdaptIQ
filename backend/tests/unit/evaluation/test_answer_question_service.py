from types import SimpleNamespace

from app.services.evaluation_service import answer_question_service
from app.models.answer import Answer


def test_answer_question_correct(db, test_user, test_question, test_evaluation):

    a1 = Answer(
        question_id=test_question.id,
        content="A",
        is_correct=True
    )
    a2 = Answer(
        question_id=test_question.id,
        content="B",
        is_correct=False
    )

    db.add_all([a1, a2])
    db.commit()
    db.refresh(a1)
    db.refresh(a2)

    payload = SimpleNamespace(
        selected_answer_ids=[a1.id],
        response_time=1.0
    )

    result = answer_question_service(
        db=db,
        user_id=str(test_user.id),
        question_id=str(test_question.id),
        payload=payload
    )

    assert result["correct"] is True
    assert "theta" in result
    assert result["finished"] in (True, False)


def test_answer_question_incorrect(db, test_user, test_question, test_evaluation):

    a1 = Answer(
        question_id=test_question.id,
        content="A",
        is_correct=False
    )
    a2 = Answer(
        question_id=test_question.id,
        content="B",
        is_correct=True
    )

    db.add_all([a1, a2])
    db.commit()

    payload = SimpleNamespace(
        selected_answer_ids=[a1.id],
        response_time=1.0
    )

    result = answer_question_service(
        db=db,
        user_id=str(test_user.id),
        question_id=str(test_question.id),
        payload=payload
    )

    assert result["correct"] is False
    assert "theta" in result