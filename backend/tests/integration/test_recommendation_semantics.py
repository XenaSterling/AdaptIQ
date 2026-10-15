from app.ml.recommender.recommender_engine import recommend_hybrid
from app.ml.recommender.resource_recommender import recommend_resources

from app.models.student_ability import StudentAbility
from app.models.learning_resource import (
    LearningResource,
    ResourceType
)

from tests.utils.factories import (
    create_user,
    create_course,
    create_module,
    create_question
)


def test_recommendations_follow_theta(db):

    teacher = create_user(db, "teacher")

    course = create_course(db, teacher)
    module = create_module(db, course)

    create_question(db, module, difficulty=-2)
    create_question(db, module, difficulty=-1)
    create_question(db, module, difficulty=0)
    create_question(db, module, difficulty=1)
    create_question(db, module, difficulty=2)

    strong = create_user(db)
    weak = create_user(db)

    db.add(
        StudentAbility(
            user_id=strong.id,
            theta=2.0
        )
    )

    db.add(
        StudentAbility(
            user_id=weak.id,
            theta=-2.0
        )
    )

    db.commit()

    strong_rec = recommend_hybrid(
        db,
        strong.id,
        theta=2.0,
        limit=3
    )

    weak_rec = recommend_hybrid(
        db,
        weak.id,
        theta=-2.0,
        limit=3
    )

    strong_avg = (
        sum(q.difficulty for q in strong_rec)
        / len(strong_rec)
    )

    weak_avg = (
        sum(q.difficulty for q in weak_rec)
        / len(weak_rec)
    )

    assert strong_avg > weak_avg


def test_resources_follow_theta(db):

    strong = create_user(db)
    weak = create_user(db)

    db.add(
        StudentAbility(
            user_id=strong.id,
            theta=2.0
        )
    )

    db.add(
        StudentAbility(
            user_id=weak.id,
            theta=-2.0
        )
    )

    db.commit()

    resources = [
        LearningResource(
            title="Easy",
            description="easy",
            url="http://easy",
            type=ResourceType.article,
            difficulty=-2
        ),
        LearningResource(
            title="Medium",
            description="medium",
            url="http://medium",
            type=ResourceType.article,
            difficulty=0
        ),
        LearningResource(
            title="Hard",
            description="hard",
            url="http://hard",
            type=ResourceType.article,
            difficulty=2
        )
    ]

    db.add_all(resources)
    db.commit()

    strong_rec = recommend_resources(
        db,
        strong.id,
        theta=2.0,
        limit=1
    )

    weak_rec = recommend_resources(
        db,
        weak.id,
        theta=-2.0,
        limit=1
    )

    strong_avg = (
        sum(r.difficulty for r in strong_rec)
        / len(strong_rec)
    )

    weak_avg = (
        sum(r.difficulty for r in weak_rec)
        / len(weak_rec)
    )

    assert strong_avg > weak_avg
    assert strong_rec[0].difficulty == 2
    assert weak_rec[0].difficulty == -2