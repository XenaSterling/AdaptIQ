from app.ml.prediction.dropout_model import (
    build_features_for_user
)

from app.models.student_ability import StudentAbility
from app.models.evaluation import (
    Evaluation,
    EvaluationStatus
)

from app.models.result import Result

from tests.utils.factories import create_user


def test_good_student_has_better_features_than_bad_student(
    db,
    test_question
):

    good = create_user(db)
    bad = create_user(db)

    db.add(
        StudentAbility(
            user_id=good.id,
            theta=2.0
        )
    )

    db.add(
        StudentAbility(
            user_id=bad.id,
            theta=-2.0
        )
    )

    db.commit()

    good_eval = Evaluation(
        user_id=good.id,
        status=EvaluationStatus.completed,
        score=9
    )

    bad_eval = Evaluation(
        user_id=bad.id,
        status=EvaluationStatus.completed,
        score=2
    )

    db.add_all([
        good_eval,
        bad_eval
    ])

    db.commit()

    db.refresh(good_eval)
    db.refresh(bad_eval)

    for _ in range(5):

        eval_good = Evaluation(
            user_id=good.id,
            status=EvaluationStatus.completed,
            score=9
        )

        eval_bad = Evaluation(
            user_id=bad.id,
            status=EvaluationStatus.completed,
            score=2
        )

        db.add_all([
            eval_good,
            eval_bad
        ])

        db.flush()

        db.add(
            Result(
                evaluation_id=eval_good.id,
                question_id=test_question.id,
                is_correct=True,
                theta_before=1.8,
                theta_after=2.0,
                question_difficulty=0.0,
                question_discrimination=1.0
            )
        )

        db.add(
            Result(
                evaluation_id=eval_bad.id,
                question_id=test_question.id,
                is_correct=False,
                theta_before=-1.8,
                theta_after=-2.0,
                question_difficulty=0.0,
                question_discrimination=1.0
            )
        )

    db.commit()

    good_features = build_features_for_user(
        db,
        good.id
    )

    bad_features = build_features_for_user(
        db,
        bad.id
    )

    assert good_features[0] > bad_features[0]
    assert good_features[1] > bad_features[1]
    assert good_features[2] > bad_features[2]