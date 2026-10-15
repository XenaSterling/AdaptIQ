from app.ml.irt.uncertainty import compute_uncertainty

from app.models.result import Result
from app.models.student_ability import StudentAbility
from app.models.evaluation import Evaluation

from tests.utils.factories import (
    create_user,
    create_course,
    create_module,
    create_question
)


def test_uncertainty_decreases_when_more_answers_exist(db):

    teacher = create_user(db, "teacher")

    course = create_course(db, teacher)
    module = create_module(db, course)

    student = create_user(db)

    db.add(
        StudentAbility(
            user_id=student.id,
            theta=0.0
        )
    )

    evaluation = Evaluation(
        user_id=student.id,
        status="completed",
        current_theta=0.0
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    uncertainty_before = compute_uncertainty(
        db,
        student.id
    )

    questions = [
        create_question(
            db,
            module,
            difficulty=float(i) / 10.0
        )
        for i in range(10)
    ]

    for q in questions:

        db.add(
            Result(
                evaluation_id=evaluation.id,
                question_id=q.id,
                is_correct=True,
                theta_before=0.0,
                theta_after=0.1,
                question_difficulty=q.difficulty,
                question_discrimination=1.0
            )
        )

    db.commit()

    uncertainty_after = compute_uncertainty(
        db,
        student.id
    )

    assert uncertainty_after < uncertainty_before