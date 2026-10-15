import uuid
from app.models.result import Result
from app.models.evaluation import Evaluation
from app.models.question import Question


def test_uncertainty_decreases_with_data(db, test_user, test_module):

    evaluation = Evaluation(
        user_id=test_user.id,
        course_id=None,
        score=0.0,
        current_theta=0.0,
        status="in_progress"
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    questions = []

    for i in range(5):
        q = Question(
            content=f"Q{i}",
            difficulty=0.0,
            discrimination=1.0,
            module_id=test_module.id
        )
        db.add(q)
        db.flush()
        questions.append(q)

    db.commit()


    for i, q in enumerate(questions):
        db.add(Result(
            evaluation_id=evaluation.id,   # ✅ UUID REAL
            question_id=q.id,
            is_correct=True
        ))

    db.commit()


    from app.ml.irt.uncertainty import compute_uncertainty

    u1 = compute_uncertainty(db, test_user.id)
    u2 = compute_uncertainty(db, test_user.id)

    assert isinstance(u1, float)
    assert isinstance(u2, float)