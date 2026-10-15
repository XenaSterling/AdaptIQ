from app.ml.recommender.content_based import (
    build_user_profile,
    score_by_content
)


def test_build_user_profile(
    db,
    test_user
):

    profile = build_user_profile(
        db,
        str(test_user.id)
    )

    assert isinstance(profile, dict)



def test_build_user_profile_empty(db, test_user):

    profile = build_user_profile(db, test_user.id)

    assert isinstance(profile, dict)


def test_score_by_content_basic(test_question):

    profile = {"tag1": 1.0, "tag2": -0.5}

    score = score_by_content(test_question, profile)

    assert isinstance(score, float)