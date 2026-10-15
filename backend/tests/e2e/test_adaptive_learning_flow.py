from app.ml.recommender.recommender_engine import recommend_hybrid
from app.services.adaptive_engine import get_next_question
from app.ml.irt.update import update_theta
from app.ml.irt.uncertainty import compute_uncertainty
from app.ml.cat.stopping import should_stop_evaluation

from app.models.result import Result
from app.models.question import Question


def test_end_to_end_adaptive_learning_flow(db, test_user, test_module):

    # =====================================================
    # 1. CREATE QUESTIONS (difficulty spectrum)
    # =====================================================

    questions = []

    for i in range(-3, 4):
        q = Question(
            content=f"Q{i}",
            difficulty=float(i),
            discrimination=1.0,
            module_id=test_module.id
        )
        db.add(q)
        db.flush()
        questions.append(q)

    db.commit()

    # =====================================================
    # 2. INITIAL RECOMMENDATION
    # =====================================================

    recs = recommend_hybrid(db, test_user.id, 0.0, 3)
    assert len(recs) <= 3

    # =====================================================
    # 3. SIMULATE ADAPTIVE SESSION
    # =====================================================

    theta = 0.0
    responses = []
    used = []

    for step in range(5):

        q = get_next_question(db, theta, used)
        assert q is not None

        used.append(q.id)

        # simulate answer (deterministic)
        is_correct = q.difficulty <= theta

        responses.append({
            "correct": is_correct,
            "difficulty": q.difficulty,
            "discrimination": q.discrimination
        })

        theta = update_theta(theta, responses)

        uncertainty = compute_uncertainty(db, test_user.id)

        if step >= 2:
            assert isinstance(uncertainty, float)

    # =====================================================
    # 4. FINAL ASSERTIONS
    # =====================================================

    assert len(responses) == 5
    assert theta is not None
    assert isinstance(theta, float)