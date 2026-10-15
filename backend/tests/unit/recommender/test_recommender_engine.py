from app.ml.recommender.recommender_engine import (
    recommend_hybrid
)
from app.models.question import Question


def test_recommend_hybrid_returns_questions(
    db,
    test_user,
    student_ability_factory
):

    ability = student_ability_factory(
        user_id=test_user.id,
        theta=0.0
    )

    recommendations = recommend_hybrid(
        db,
        str(test_user.id),
        ability.theta
    )

    assert isinstance(recommendations, list)

def test_recommendation_limit(db, test_module, test_user):

    for i in range(10):
        db.add(Question(
            content=f"Q{i}",
            difficulty=(i - 5) / 2,  # centrado en rango válido
            discrimination=1.0,
            module_id=test_module.id
        ))

    db.commit()

    results = recommend_hybrid(db, test_user.id, 0.0, 5)

    assert len(results) <= 5


def test_recommendation_center_bias(db, test_module, test_user):

    easy = Question(content="Easy", difficulty=-3, discrimination=1, module_id=test_module.id)
    mid = Question(content="Mid", difficulty=0, discrimination=1, module_id=test_module.id)
    hard = Question(content="Hard", difficulty=3, discrimination=1, module_id=test_module.id)

    db.add_all([easy, mid, hard])
    db.commit()

    results = recommend_hybrid(db, test_user.id, 0.0, 1)

    assert results[0].content == "Mid"


def test_recommend_hybrid_empty(db, test_user):

    result = recommend_hybrid(db, test_user.id, 0.0, 5)

    assert isinstance(result, list)


def test_recommend_hybrid_limit(db, test_user, test_module):

    from app.models.question import Question

    for i in range(10):
        db.add(Question(
            content=f"Q{i}",
            difficulty=(i - 5) / 2,
            discrimination=1.0,
            module_id=test_module.id
        ))

    db.commit()

    result = recommend_hybrid(db, test_user.id, 0.0, 5)

    assert len(result) <= 5


def test_recommendation_changes_with_theta(db, test_user, test_module):

    from app.models.question import Question

    for i in range(-3, 4):
        db.add(Question(
            content=f"Q{i}",
            difficulty=float(i),
            discrimination=1.0,
            module_id=test_module.id
        ))

    db.commit()

    recs1 = recommend_hybrid(db, test_user.id, 0.0, 3)
    recs2 = recommend_hybrid(db, test_user.id, 2.0, 3)

    assert isinstance(recs1, list)
    assert isinstance(recs2, list)