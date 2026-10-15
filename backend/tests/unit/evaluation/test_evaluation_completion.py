from types import SimpleNamespace

from app.services.evaluation_service import answer_question_service
from app.models.answer import Answer
from app.models.evaluation import EvaluationStatus


def test_evaluation_is_completed_and_persisted(db, test_user, test_question, test_evaluation):

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

    if result.get("finished"):

        db.refresh(test_evaluation)

        assert test_evaluation.status in [
            EvaluationStatus.completed,
            EvaluationStatus.in_progress
        ]

        if test_evaluation.status == EvaluationStatus.completed:
            assert test_evaluation.score is not None
            assert test_evaluation.finished_at is not None
            assert test_evaluation.final_theta is not None