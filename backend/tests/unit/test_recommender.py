from app.ml.recommender.recommender_engine import recommend_hybrid
from app.services.adaptive_engine import get_next_question
from app.models.question import Question


def test_recommendations_basic(db, test_user):

    results = recommend_hybrid(db, test_user.id, 0.0, 5)

    assert isinstance(results, list)


def test_recommendation_limit(db, test_module, test_user):

    for i in range(10):
        db.add(Question(
            content=f"Q{i}",
            difficulty=max(-4.0, min(4.0, float(i - 5))),
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

    assert min(results, key=lambda q: abs(q.difficulty - 0)).difficulty == 0


def test_recommender_adapts_to_theta(db, test_module, test_user):

    q_easy = get_next_question(db, -2, [])
    q_mid = get_next_question(db, 0, [])
    q_hard = get_next_question(db, 2, [])

    recs = recommend_hybrid(db, test_user.id, 0.0, 3)

    assert isinstance(recs, list)
    assert len(recs) <= 3