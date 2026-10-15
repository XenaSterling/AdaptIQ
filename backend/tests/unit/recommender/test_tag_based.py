from app.ml.recommender.tag_based import get_weak_tags


def test_get_weak_tags(db, test_user, test_question, test_evaluation):

    from app.models.result import Result

    result = Result(
        evaluation_id=test_evaluation.id,
        question_id=test_question.id,
        is_correct=False
    )

    db.add(result)

    db.commit()

    weak_tags = get_weak_tags(
        db,
        str(test_user.id)
    )

    assert isinstance(weak_tags, dict)


def test_get_weak_tags_basic(db, test_user, test_question):

    from app.models.evaluation import Evaluation
    from app.models.result import Result

    eval = Evaluation(user_id=test_user.id, score=0)
    db.add(eval)
    db.commit()
    db.refresh(eval)

    result = Result(
        evaluation_id=eval.id,
        question_id=test_question.id,
        is_correct=False,
        response_time=10
    )

    db.add(result)
    db.commit()

    weak = get_weak_tags(db, test_user.id)

    assert isinstance(weak, dict)


def test_get_weak_tags_empty(db, test_user):

    weak = get_weak_tags(db, test_user.id)

    assert weak == {}