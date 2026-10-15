from types import SimpleNamespace

from app.ml.recommender.resource_recommender import (
    difficulty_fit,
    learning_style_bonus,
    tag_score,
    recommend_resources
)

from app.models.learning_profile import LearningProfile
from app.models.learning_resource import LearningResource


def test_difficulty_fit_exact_match():

    resource = SimpleNamespace(
        difficulty=0.0
    )

    score = difficulty_fit(
        resource,
        0.0
    )

    assert score == 1.0


def test_difficulty_fit_far():

    resource = SimpleNamespace(
        difficulty=4.0
    )

    score = difficulty_fit(
        resource,
        0.0
    )

    assert score == 0.0


def test_learning_style_bonus_visual():

    profile = SimpleNamespace(
        learning_style="visual"
    )

    resource = SimpleNamespace(
        type="video"
    )

    score = learning_style_bonus(
        resource,
        profile
    )

    assert score > 0


def test_learning_style_bonus_visual(db, test_user):

    profile = LearningProfile(
        user_id=test_user.id,
        learning_style="visual"
    )

    resource = LearningResource(
        title="Video",
        description="",
        type="video",
        difficulty=0.0,
        url="x"
    )

    assert learning_style_bonus(resource, profile) == 1.0


def test_learning_style_bonus_reading(db, test_user):

    profile = LearningProfile(
        user_id=test_user.id,
        learning_style="reading"
    )

    resource = LearningResource(
        title="Article",
        description="",
        type="article",
        difficulty=0.0,
        url="x"
    )

    assert learning_style_bonus(resource, profile) == 1.0


def test_difficulty_fit_centered():

    class R:
        difficulty = 0.0

    assert difficulty_fit(R(), 0.0) == 1.0


def test_tag_score_empty():

    class R:
        tags = []

    assert tag_score(R(), {}) == 0.0


def test_recommend_resources_limit(db, test_user, test_module):

    from app.models.learning_resource import LearningResource

    for i in range(10):
        db.add(LearningResource(
            title=f"R{i}",
            description="desc",
            type="video",
            difficulty=float(i),
            url=f"url{i}"
        ))

    db.commit()

    result = recommend_resources(db, test_user.id, 0.0, limit=5)

    assert len(result) <= 5