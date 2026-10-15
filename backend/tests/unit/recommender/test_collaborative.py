from app.ml.recommender.collaborative import (
    get_similar_users,
    get_collaborative_question_scores
)


def test_get_similar_users(
    db,
    student_ability_factory,
    test_user
):

    student_ability_factory(
        theta=0.5
    )

    student_ability_factory(
        theta=0.6
    )

    similar = get_similar_users(
        db,
        str(test_user.id)
    )

    assert isinstance(similar, list)


def test_get_collaborative_empty(db, test_user):

    scores = get_collaborative_question_scores(db, test_user.id)

    assert isinstance(scores, dict)


def test_get_collaborative_returns_scores(db, test_user, test_question):

    scores = get_collaborative_question_scores(db, test_user.id)

    assert isinstance(scores, dict)